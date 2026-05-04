from playwright.sync_api import sync_playwright
from pathlib import Path
import argparse
import base64
import csv
import sys
import time

# Pos_0008: Image resizing - Upload valid PNG image and verify preview functionality
DEFAULT_URL = "https://www.pixelssuite.com/resize-image"
DEFAULT_TIMEOUT_MS = 60000
DEFAULT_SLOW_MO_MS = 300

PNG_1X1_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMB/6X9wYQAAAAASUVORK5CYII="
)


def configure_stdout():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    except Exception:
        pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--png", default="sample.png")
    parser.add_argument("--out-dir", default="results")
    parser.add_argument("--csv", default="execution_results.csv")
    parser.add_argument("--headless", action="store_true", default=False)
    parser.add_argument("--timeout-ms", type=int, default=DEFAULT_TIMEOUT_MS)
    parser.add_argument("--slow-mo-ms", type=int, default=DEFAULT_SLOW_MO_MS)
    return parser.parse_args()


def create_default_png_if_missing(file_path: Path):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if not file_path.exists():
        file_path.write_bytes(base64.b64decode(PNG_1X1_BASE64))


def find_file_input(page, timeout_ms: int):
    deadline = time.time() + (timeout_ms / 1000)

    while time.time() < deadline:
        locator = page.locator('input[type="file"]').first
        try:
            if locator.count() > 0:
                return locator
        except Exception:
            pass
        page.wait_for_timeout(300)

    raise RuntimeError("File upload input was not found on the image resizing page.")


def fill_resize_values_if_available(page):
    """Some resize pages show width/height inputs after upload. Fill them if they exist."""
    possible_width_selectors = [
        'input[name*="width" i]',
        'input[placeholder*="width" i]',
        'input[aria-label*="width" i]',
    ]
    possible_height_selectors = [
        'input[name*="height" i]',
        'input[placeholder*="height" i]',
        'input[aria-label*="height" i]',
    ]

    for selector in possible_width_selectors:
        try:
            width = page.locator(selector).first
            if width.count() > 0 and width.is_visible():
                width.fill("300")
                break
        except Exception:
            pass

    for selector in possible_height_selectors:
        try:
            height = page.locator(selector).first
            if height.count() > 0 and height.is_visible():
                height.fill("300")
                break
        except Exception:
            pass


def check_preview_visible(page):
    script = """
    () => {
        const visible = (el) => !!(el && el.getClientRects && el.getClientRects().length);

        const media = Array.from(document.querySelectorAll("img, canvas, svg, video"))
            .filter(el => visible(el))
            .filter(el => {
                const box = el.getBoundingClientRect();
                return box.width > 20 && box.height > 20;
            });

        const previewText = Array.from(document.querySelectorAll("body *"))
            .filter(el => visible(el))
            .some(el => (el.textContent || "").trim().toLowerCase().includes("preview"));

        return media.length > 0 && previewText;
    }
    """
    return page.evaluate(script)


def write_result_to_csv(csv_path: Path, row: dict):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "tc_id",
        "feature",
        "scenario",
        "file_type",
        "file_path",
        "preview_detected",
        "status",
        "screenshot",
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)


def run_test():
    configure_stdout()
    args = parse_args()

    png_path = Path(args.png).resolve()
    out_dir = Path(args.out_dir).resolve()
    csv_path = Path(args.csv).resolve()

    out_dir.mkdir(parents=True, exist_ok=True)
    create_default_png_if_missing(png_path)

    result = {
        "tc_id": "Pos_0008",
        "feature": "Image resizing",
        "scenario": "Upload valid PNG image and verify preview functionality",
        "file_type": "PNG",
        "file_path": str(png_path),
        "preview_detected": False,
        "status": "FAIL",
        "screenshot": "",
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless, slow_mo=args.slow_mo_ms)
        page = browser.new_page()
        page.set_default_timeout(args.timeout_ms)

        try:
            page.goto(args.url, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass

            file_input = find_file_input(page, args.timeout_ms)
            file_input.set_input_files(str(png_path))
            page.wait_for_timeout(1500)

            fill_resize_values_if_available(page)

            deadline = time.time() + (args.timeout_ms / 1000)
            preview_found = False
            while time.time() < deadline:
                if check_preview_visible(page):
                    preview_found = True
                    break
                page.wait_for_timeout(500)

            status = "PASS" if preview_found else "FAIL"
            screenshot_path = out_dir / f"pos_0008_image_resize_preview_{status.lower()}.png"
            page.screenshot(path=str(screenshot_path), full_page=True)

            result.update({
                "preview_detected": preview_found,
                "status": status,
                "screenshot": str(screenshot_path),
            })

            print("========== TEST RESULT ==========")
            print("TC ID           : Pos_0008")
            print("Feature         : Image resizing")
            print(f"PNG file        : {png_path}")
            print(f"Preview detected: {preview_found}")
            print(f"Status          : {status}")
            print(f"Screenshot      : {screenshot_path}")
            print(f"CSV             : {csv_path}")

        except Exception as e:
            error_screenshot = out_dir / "pos_0008_image_resize_preview_error.png"
            try:
                page.screenshot(path=str(error_screenshot), full_page=True)
            except Exception:
                pass
            result.update({
                "preview_detected": False,
                "status": "FAIL",
                "screenshot": str(error_screenshot),
            })
            print("========== TEST RESULT ==========")
            print("TC ID           : Pos_0008")
            print("Feature         : Image resizing")
            print("Preview detected: False")
            print("Status          : FAIL")
            print(f"Screenshot      : {error_screenshot}")
            print(f"CSV             : {csv_path}")
            print(f"Error           : {e}")

        finally:
            browser.close()

    write_result_to_csv(csv_path, result)


if __name__ == "__main__":
    run_test()
