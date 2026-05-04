# IT23310414 ITPM Playwright Test Automation Suite

## Overview

This repository contains automated test scripts for UI testing using **Playwright**, a modern browser automation framework. The tests are designed to validate image processing functionalities, including image preview and image resizing operations.

## Project Structure

```
test_automation_ui/
├── README.md                      # This file
├── image_preview_test.py           # Test for image preview functionality
├── image_resize_preview_test.py    # Test for image resize preview functionality
├── execution_results.csv           # Test execution results log
├── results/                        # Directory containing test results and screenshots
└── sample.png                      # Sample image file for testing
```

## Prerequisites

- **Python 3.8+** (recommended: Python 3.9 or higher)
- **pip** (Python package manager)
- **Virtual Environment** (recommended)

## Installation & Setup

### 1. Clone or Navigate to the Repository

```bash
cd test_automation_ui
```

### 2. Create a Virtual Environment

Creating a virtual environment is recommended to isolate project dependencies:

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

Install the required Python packages:

```bash
pip install --upgrade pip
pip install playwright
```

### 5. Install Playwright Browsers

Playwright requires browser binaries. Install them using:

```bash
playwright install
```

## Running the Tests

### Test Files

#### 1. **image_preview_test.py**
Tests the image preview functionality on the PixelsSuite convert-to-PNG tool.

**Run with default settings:**
```bash
python image_preview_test.py
```

**Run with custom parameters:**
```bash
python image_preview_test.py --url "https://www.pixelssuite.com/convert-to-png" --png "sample.png" --out-dir "results"
```

#### 2. **image_resize_preview_test.py**
Tests the image resizing and preview functionality on the PixelsSuite resize-image tool.

**Run with default settings:**
```bash
python image_resize_preview_test.py
```

**Run with custom parameters:**
```bash
python image_resize_preview_test.py --url "https://www.pixelssuite.com/resize-image" --png "sample.png" --out-dir "results"
```

### Command-Line Arguments

Both test scripts support the following optional arguments:

| Argument | Default | Description |
|----------|---------|-------------|
| `--url` | Tool-specific URL | URL of the web application to test |
| `--png` | `sample.png` | Path to the PNG image file for testing |
| `--out-dir` | `results` | Directory where test results will be saved |

## Test Execution Results

After running the tests, execution results are logged in:
- **execution_results.csv** - Contains test run summary and status
- **results/** - Directory containing screenshots and detailed test artifacts

## Troubleshooting

### 1. Virtual Environment Not Activating
Ensure you're in the correct directory and use the appropriate activation command for your OS.

### 2. Playwright Installation Issues
If `playwright install` fails, try:
```bash
pip install --upgrade playwright
playwright install --with-deps
```

### 3. Module Import Errors
Verify that all dependencies are installed:
```bash
pip list
```

### 4. Test Failures Due to Timeouts
The default timeout is 60 seconds. If tests fail due to slow network, the tests handle this internally with appropriate waits.

## Dependencies

The project requires the following Python packages:

- **playwright** - Browser automation framework for testing web applications
- Standard library modules: `pathlib`, `argparse`, `base64`, `time`, `sys`, `csv`

All dependencies are installed via the `pip install playwright` command.

## Notes

- Tests use the **Playwright Sync API** for synchronous browser automation
- Base64-encoded sample images are used for testing
- Test results include execution timestamps and detailed status reports
- The tests interact with the PixelsSuite web application for image processing validation

## Author

**ID:** IT23310414

## License

This project is part of an IT Project Management course assignment (ITPM Y3S2).

---

For more information on Playwright, visit: [Playwright Documentation](https://playwright.dev/python/)
