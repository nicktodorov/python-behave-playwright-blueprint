import os
import datetime
import allure
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Define a global directory for storing failure screenshots.
SCREENSHOTS_DIR = os.path.join(os.getcwd(), "screenshots")

def before_all(context):
    """
    This hook runs once before all features and scenarios.
    It's used for global setup, including configuration and browser initialization.
    """
    # Load environment variables from a .env file if it exists.
    load_dotenv()

    # --- Configuration Loading ---
    # The base_url is considered critical and must be set in the .env file.
    # This enforces consistency across all test runs.
    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("CRITICAL: 'BASE_URL' is not defined. Please set it in the .env file.")
    context.base_url = base_url

    # The headless mode is designed for flexibility.
    # It checks for a command-line override first, then falls back to the .env file,
    # and finally defaults to "true" as a safe fallback for CI environments.
    # Example command-line override: `behave -D headless=false`
    headless_from_cmd = context.config.userdata.get("headless")
    if headless_from_cmd:
        headless_str = headless_from_cmd
    else:
        headless_str = os.getenv("HEADLESS", "true")
    headless = headless_str.lower() == "true"

    # --- Global Browser Setup ---
    # Start Playwright and launch the browser once for the entire test suite.
    # This is more efficient than launching a new browser for every scenario.
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=headless)


def before_scenario(context, scenario):
    """
    This hook runs before each scenario.
    It creates a new, isolated browser context and page for each scenario.
    This ensures that tests do not share state (like cookies or local storage).
    """
    context.browser_context = context.browser.new_context(base_url=context.base_url)
    context.page = context.browser_context.new_page()


def after_step(context, step):
    """
    This hook runs after each step.
    If a step fails, it takes a screenshot and attaches it to the Allure report.
    """
    if step.status == "failed":
        if not os.path.exists(SCREENSHOTS_DIR):
            os.makedirs(SCREENSHOTS_DIR)
        
        current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        scenario_name = context.scenario.name.replace(" ", "_")
        screenshot_filename = f"{scenario_name}_{current_time}.png"
        screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_filename)
        
        try:
            # Take a screenshot using Playwright's built-in method.
            context.page.screenshot(
                path=screenshot_path,
                timeout=5000,  # Use a shorter timeout for screenshots.
                animations="disabled",
                caret="hide"
            )
            # Attach the screenshot to the Allure report for easy debugging.
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
        except Exception as e:
            print(f"Error taking or attaching screenshot: {e}")


def after_scenario(context, scenario):
    """
    This hook runs after each scenario.
    It closes the page and browser context to clean up resources and ensure isolation.
    """
    context.page.close()
    context.browser_context.close()


def after_all(context):
    """
    This hook runs once after all features and scenarios have completed.
    It's used for global teardown, such as closing the browser and stopping Playwright.
    """
    context.browser.close()
    context.playwright.stop()
