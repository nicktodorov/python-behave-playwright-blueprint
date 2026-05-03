# Enterprise Python Automation Blueprint: Behave & Playwright

## Overview
This repository serves as a reference architecture for scalable, BDD-driven automation. The framework is built to be scalable, maintainable, and easy to use, following modern automation best practices.

The included registration flow serves as a functional demonstration of the framework's capabilities in handling complex UI interactions and data-driven scenarios.

## Key Features
*   **Behavior-Driven Development (BDD):** Scenarios are written in business-readable Gherkin syntax (`.feature` files).
*   **Page Object Model (POM):** UI interactions and locators are encapsulated in page-specific classes for maintainability.
*   **Flexible Configuration:** Uses a `.env` file for environment-specific settings and supports command-line overrides for debugging.
*   **Rich Reporting:** Integrated with Allure to generate detailed, interactive test reports.
*   **Automatic Screenshots:** Captures a screenshot automatically whenever a test step fails.

## Tech Stack
*   **Core Framework:** Scalable BDD Implementation: Leverages Python and Behave to bridge the gap between technical implementation and business requirements.
*   **Browser Automation:** Playwright
*   **Configuration:** `python-dotenv`
*   **Reporting:** `allure-behave`

---

## Getting Started

### Prerequisites
*   Python 3.8+
*   `pip` and `venv`
*   [Allure Commandline](https://allurereport.org/docs/gettingstarted-installation/) (for generating reports)

### Installation & Configuration

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd dev-craft-automation-task
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright browsers:**
    (This is a one-time setup for Playwright)
    ```bash
    playwright install
    ```

5.  **Configure your environment:**
    Create a `.env` file in the project root by copying the example file.
    ```bash
    # For Windows
    copy .env.example .env

    # For macOS/Linux
    cp .env.example .env
    ```
    Now, open the `.env` file and add the base URL for the environment you want to test against.
    ```dotenv
    BASE_URL=https://staging.example-app.com
    HEADLESS=true
    ```

---

## Running Tests

### Executing Scenarios
To run all test scenarios defined in the `.feature` files, simply execute:
```bash
behave
```

**Overriding Headless Mode:**
For debugging, you can easily run the tests in a headed (non-headless) mode by passing a command-line flag:
```bash
behave -D headless=false
```

### Generating Allure Reports
The framework is configured to generate Allure results.

1.  **Run `behave` with the Allure formatter:**
    ```bash
    behave -f allure_behave.formatter:AllureFormatter -o allure-results ./features
    ```

2.  **Serve the report:**
    This command will generate the report and open it in your web browser.
    ```bash
    allure serve allure-results
    ```

---

## Project Structure
```text
dev-craft-automation-task/
├── features/
│   ├── environment.py           # Hooks for setup, teardown, and configuration
│   ├── registration.feature     # Gherkin scenarios for registration
│   └── steps/
│       └── registration_steps.py # Step definitions mapping Gherkin to Python
├── pages/
│   ├── base_page.py             # Base class for all page objects
│   └── registration_page.py     # Locators and methods for the Registration page
├── .env                       # (Untracked) Local environment configuration
├── .env.example               # Example environment file
├── allure-results/            # (Untracked) Raw Allure results
├── screenshots/               # (Untracked) Failure screenshots
├── behave.ini                 # Behave configuration file
├── requirements.txt           # Project dependencies
└── README.md                  # This file
```

