# Unified Test Automation Framework

This is a unified test automation framework that supports API, Web, and Mobile app testing using Gauge and Python.

## Features

- **API Testing**: Test REST APIs using the requests library
- **Web Testing**: Selenium-based web testing with Page Object Model
- **Mobile Testing**: Appium-based mobile testing for Android and iOS with Page Object Model

## Project Structure

```
.
├── core/                   # Core framework components
│   ├── api/                # API testing components
│   ├── web/                # Web testing components
│   │   └── pages/          # Web page objects
│   ├── app/                # Mobile app testing components
│   │   └── pages/          # Mobile page objects
│   └── utils/              # Utility modules
├── resources/              # Test resources
│   ├── config/             # Configuration files
│   └── data/               # Test data
├── specs/                  # Gauge specifications
├── step_impl/              # Step implementations
├── logs/                   # Test logs (generated)
└── screenshots/            # Test screenshots (generated)
```

## Example Test Scenarios

The framework includes example test scenarios for:

1. **API Testing**: JSONPlaceholder REST API testing
2. **Web Testing**: The Internet login page testing
3. **Mobile Testing**: SauceLabs Sample App login testing for Android and iOS

## Prerequisites

- Python 3.8 or higher
- Gauge
- Node.js and npm (for Appium)
- Android SDK and tools (for Android testing)
- Xcode and tools (for iOS testing)
- Appium Server

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Tests

Run all tests:
```
gauge run specs/
```

Run API tests:
```
gauge run specs/api_test.spec
```

Run Web tests:
```
gauge run specs/web_test.spec
```

Run Android tests:
```
gauge run specs/app_test.spec --tags android
```

Run iOS tests:
```
gauge run specs/app_test.spec --tags ios
```

## Configuration

Configuration settings are stored in `resources/config/config.ini`. Update these settings based on your environment.

## Extending the Framework

To add new tests:

1. Create new specification files in the `specs` directory
2. Implement the step definitions in the `step_impl` directory
3. Add any new page objects or API clients as needed 