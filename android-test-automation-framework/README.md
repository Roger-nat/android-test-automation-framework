# Android Test Automation Framework

A Python + Appium + Pytest framework for Android application testing, designed as a portfolio project for Graduate Engineer Trainee / Automation Testing roles.

## What this project demonstrates

- Android UI automation with Appium + UiAutomator2
- Page Object Model (POM)
- Functional and regression test suites
- Pytest markers (`smoke`, `regression`, `functional`, `mobile`)
- Data-driven testing with `pytest.mark.parametrize`
- Explicit waits and reusable UI actions
- Automatic screenshots and Logcat capture on test failure
- ADB utilities for device diagnostics and APK management
- HTML + JUnit test reporting
- Environment-driven device and app configuration
- GitHub Actions CI checks
- Optional AI-assisted test failure analysis

## App under test

The default configuration targets Sauce Labs' open-source **My Demo App (React Native)** because it provides realistic mobile flows such as login, catalog, cart and checkout, and exposes stable accessibility IDs for automation.

Official app repository / releases:
- https://github.com/saucelabs/my-demo-app-rn
- https://github.com/saucelabs/my-demo-app-android/releases

The APK is **not committed** to this repository. Download it locally or point `APP_PATH` to another Android APK.

## Architecture

```text
android-test-automation-framework/
├── config/
│   └── settings.py
├── core/
│   └── driver_factory.py
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── catalog_page.py
│   └── cart_page.py
├── tests/
│   ├── data/
│   │   └── users.json
│   ├── smoke/
│   │   └── test_login_smoke.py
│   ├── regression/
│   │   ├── test_login_regression.py
│   │   ├── test_catalog_regression.py
│   │   └── test_cart_regression.py
│   └── unit/
│       └── test_ai_failure_analyzer.py
├── utils/
│   ├── adb.py
│   ├── ai_failure_analyzer.py
│   ├── artifacts.py
│   ├── logger.py
│   └── waits.py
├── scripts/
│   ├── download_demo_app.py
│   └── check_android_env.ps1
├── .github/workflows/
│   ├── framework-check.yml
│   └── android-regression.yml
├── .env.example
├── .gitignore
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Prerequisites on Windows

Install:

1. Python 3.11+
2. Android Studio
3. Android SDK + Platform Tools
4. An Android Virtual Device (AVD)
5. Node.js
6. Appium 2/3
7. UiAutomator2 driver
8. Git

Verify:

```powershell
python --version
adb --version
node --version
git --version
```

Install Appium:

```powershell
npm install -g appium
appium driver install uiautomator2
appium driver list --installed
```

## Python setup

From the project root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create your environment file:

```powershell
Copy-Item .env.example .env
```

## Download the sample APK

The helper script downloads the configured public My Demo App release.

```powershell
python scripts/download_demo_app.py
```

It saves the APK under:

```text
app/Android.MyDemoAppRN.apk
```

You can also use your own APK by changing `APP_PATH` in `.env`.

## Android emulator

Create an emulator in Android Studio Device Manager. Then start it.

Example:

```powershell
emulator -avd Pixel_6_API_33
```

Verify:

```powershell
adb devices
```

You should see an emulator in the `device` state.

## Start Appium

In a separate terminal:

```powershell
appium
```

Default server:

```text
http://127.0.0.1:4723
```

## Configuration

The main runtime values are controlled by `.env`.

```text
APPIUM_SERVER_URL=http://127.0.0.1:4723
PLATFORM_NAME=Android
AUTOMATION_NAME=UiAutomator2
DEVICE_NAME=Pixel_6_API_33
PLATFORM_VERSION=13
APP_PATH=./app/Android.MyDemoAppRN.apk
APP_PACKAGE=com.swaglabsmobileapp

STANDARD_USER_EMAIL=bob@example.com
STANDARD_USER_PASSWORD=10203040
LOCKED_USER_EMAIL=alice@example.com
LOCKED_USER_PASSWORD=10203040

RUN_MOBILE_TESTS=0

LLM_API_URL=
LLM_API_KEY=
LLM_MODEL=
```

`RUN_MOBILE_TESTS=0` lets the non-device unit suite run without an emulator. Set it to `1` when the emulator + Appium server are ready.

## Test suites

### Smoke

```powershell
pytest -m smoke
```

### Regression

```powershell
pytest -m regression
```

### Functional

```powershell
pytest -m functional
```

### All mobile tests

```powershell
$env:RUN_MOBILE_TESTS="1"
pytest -m mobile
```

### All tests

```powershell
$env:RUN_MOBILE_TESTS="1"
pytest
```

## Reporting

The default Pytest configuration generates:

```text
reports/
├── pytest-report.html
└── junit.xml
```

Test artifacts are stored in:

```text
artifacts/
├── screenshots/
├── logcat/
└── failure_analysis/
```

## Automatic failure evidence

When a mobile test fails, the framework attempts to:

1. Capture a screenshot.
2. Capture recent Android Logcat output.
3. Write the Pytest failure details.
4. Run the optional AI failure analyzer when an LLM endpoint is configured.

Example:

```text
artifacts/
├── screenshots/
│   └── test_invalid_password.png
├── logcat/
│   └── test_invalid_password.txt
└── failure_analysis/
    └── test_invalid_password.md
```

## ADB utility commands

The reusable ADB helper supports:

- Connected device listing
- APK installation
- APK uninstall
- Clear app data
- Force-stop
- Start app
- Device information
- Recent Logcat capture

You can also use the helper directly:

```powershell
python -m utils.adb
```

## AI-assisted test failure analyzer

The AI feature is intentionally optional.

It consumes:

- test name
- failure message
- traceback
- recent Logcat output

and asks a configured LLM endpoint for:

- a short failure summary
- likely cause
- next debugging step

Configure:

```text
LLM_API_URL=https://your-provider.example/v1/chat/completions
LLM_API_KEY=your-key
LLM_MODEL=your-model
```

No API key means the core framework still works normally; the analyzer simply records that AI analysis was not configured.

## CI/CD

Two workflows are included.

### `framework-check.yml`

Runs on normal pushes and pull requests and verifies:

- Python compilation
- Ruff linting
- Unit tests
- HTML/JUnit report generation

This workflow does **not** pretend an Android emulator is available.

### `android-regression.yml`

A manual / optional mobile workflow that:

- sets up Python and Android tooling
- creates an Android emulator
- installs Appium + UiAutomator2
- downloads the sample APK
- starts Appium
- runs the mobile regression suite
- uploads reports, screenshots and Logcat artifacts

Mobile CI depends on the GitHub runner's Android emulator environment and can be slower than local execution. Local emulator execution remains the primary development workflow.

## Interview talking points

Be ready to explain:

- Why Page Object Model is used
- Why explicit waits are preferred over arbitrary sleeps
- How Pytest fixtures manage driver lifecycle
- How failure hooks collect screenshots and Logcat
- How environment variables keep device-specific values out of test code
- Difference between smoke, functional and regression suites
- How ADB helps troubleshoot an Android test environment
- How the CI workflow separates framework checks from full mobile execution
- Why AI analysis is optional rather than a hard dependency

## Future improvements

- Device/API-level matrix expansion
- Parallel Android sessions
- Richer HTML dashboards
- Appium Inspector locator snapshots
- Test execution history
- Allure reporting
- More checkout and navigation coverage
