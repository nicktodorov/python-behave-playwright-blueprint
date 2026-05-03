from behave import step
import time
from pages import RegistrationPage

# This file contains the step definitions that map the Gherkin steps from
# the .feature files to executable Python code. The steps delegate the actual
# browser interactions to the appropriate Page Object.

# --- Happy Path Steps ---

@step('I am on login page')
def open_login_page(context):
    """Initial step to load the starting page of the application."""
    page = RegistrationPage(context.page)
    page.load_login_page()

@step('I navigate to the registration page')
def navigate_to_registration(context):
    """Step to trigger the navigation from the login page to the sign-up form."""
    page = RegistrationPage(context.page)
    page.go_to_signup()

@step('I fill in the registration details with a valid email and password')
def enter_registration_details(context):
    """
    Fills the registration form with valid, dynamically generated data.
    Using a timestamp ensures the email is unique for each test run, preventing
    failures due to a pre-existing user account.
    """
    page = RegistrationPage(context.page)
    unique_email = f"automation.tester+{int(time.time())}@example.com"
    page.fill_credentials(unique_email, "SecureP@ssw0rd!")

@step('I accept the terms and conditions')
def accept_terms_and_conditions(context):
    """Checks the 'Terms and Conditions' checkbox."""
    page = RegistrationPage(context.page)
    page.accept_terms()

@step('I click the Register button')
def click_register_button(context):
    """Clicks the final submission button to register the user."""
    page = RegistrationPage(context.page)
    page.submit_form()

@step('the activation code popup should be displayed')
def verify_activation_popup(context):
    """Verifies that the successful registration leads to the activation step."""
    page = RegistrationPage(context.page)
    page.verify_activation_popup()

# --- Negative Case Steps ---

@step('I fill in the registration details with "{email}" and "{password}"')
def enter_specific_credentials(context, email, password):
    """
    Fills the form with specific data from the Scenario Outline's examples table.
    This step handles special placeholder values like [BLANK] and [DYNAMIC]
    to test various edge cases without hardcoding them in the feature file.
    """
    if email == "[BLANK]":
        email = ""
    elif email == "[DYNAMIC]":
        # Generate a unique email for tests that need a valid format but aren't testing uniqueness.
        email = f"automation.tester+{int(time.time())}@example.com"
    
    if password == "[BLANK]":
        password = ""
        
    page = RegistrationPage(context.page)
    page.fill_credentials(email, password)

@step('I set the terms and conditions checkbox to "{terms_state}"')
def set_terms_checkbox(context, terms_state):
    """
    Controls the state of the terms and conditions checkbox based on the scenario.
    If the state is "unchecked", no action is taken, which correctly simulates a user not interacting with it.
    """
    page = RegistrationPage(context.page)
    if terms_state.lower() == "checked":
        page.accept_terms()

@step('the registration should be blocked due to "{error_reason}"')
def verify_registration_blocked(context, error_reason):
    """
    Verifies that the appropriate validation error is displayed on the page.
    This is a critical step for negative testing.
    """
    page = RegistrationPage(context.page)
    # 1. Retrieve all visible error messages from the page.
    actual_errors = page.get_validation_errors()
    
    # 2. Assert that at least one error message was found.
    assert len(actual_errors) > 0, "Expected a validation error message, but none appeared."
    
    # 3. Check if the expected error message is present among the actual errors.
    #    This allows for multiple validation errors to be on the page, as long as ours is one of them.
    match_found = any(error_reason.lower() in error.lower() for error in actual_errors)
    assert match_found, f"Expected to find error '{error_reason}', but found: {actual_errors}"
