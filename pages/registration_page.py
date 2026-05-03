import re
from pages.base_page import BasePage
from playwright.sync_api import expect

class RegistrationPage(BasePage):
    """
    This class represents the Registration page and contains all the locators and
    actions related to it. This follows the Page Object Model (POM) design pattern.
    """

    # --- Locator Constants ---
    # Locators are defined as "private" class attributes. This provides a single
    # source of truth for all selectors, making the page object easy to maintain.
    _LOGIN_PATH = "/login"
    _JOIN_LINK_TEXT = "Join"
    _EMAIL_INPUT = "input[name='email']"
    _PASSWORD_INPUT = "input[name='password']"
    _TERMS_CONTAINER = "#signupStep1TermsAndConditions [role='checkbox']"
    _TERMS_VISUAL_BOX = "#signupStep1TermsAndConditions .q-checkbox__inner"
    _REGISTER_BTN_ID = "#signupStep1Next"
    _VERIFICATION_FORM_ID = "#verificationCodeForm"
    _VERIFICATION_TITLE_TEXT = "Verification code sent"
    _ALERT_MESSAGE = "div[role='alert']"

    def __init__(self, page):
        """
        The constructor initializes the page object.
        It creates Playwright Locator objects from the string constants, which can be
        reused across different methods without repeatedly querying the DOM.
        """
        super().__init__(page)
        # --- Page Element Locators ---
        self.join_link = page.get_by_role("link", name=self._JOIN_LINK_TEXT, exact=True)
        self.email_input = page.locator(self._EMAIL_INPUT)
        self.password_input = page.locator(self._PASSWORD_INPUT)
        self.terms_container = page.locator(self._TERMS_CONTAINER)
        self.terms_visual_box = page.locator(self._TERMS_VISUAL_BOX)
        self.register_button = page.locator(self._REGISTER_BTN_ID)
        self.verification_form = page.locator(self._VERIFICATION_FORM_ID)
        self.verification_title = page.get_by_text(self._VERIFICATION_TITLE_TEXT, exact=True)
        self.alert_messages = page.locator(self._ALERT_MESSAGE)

    # --- User Actions ---
    # Methods below encapsulate the actions a user can perform on the page.

    def load_login_page(self):
        """Navigates to the initial login page."""
        self.navigate(self._LOGIN_PATH)

    def go_to_signup(self):
        """Clicks the 'Join' link to navigate to the registration form."""
        self.join_link.click()
        # Assert that the URL has changed to the expected registration step.
        expect(self.page).to_have_url(re.compile(r".*/signup/1$"), timeout=30000)
        # Wait until network requests have settled to ensure the page is fully interactive.
        self.page.wait_for_load_state("networkidle")

    def fill_credentials(self, email, password):
        """Fills the email and password fields."""
        self.email_input.fill(email)
        self.password_input.fill(password)

    def accept_terms(self):
        """Checks the terms and conditions checkbox."""
        # Note: We click the visual box as it's the element that reliably receives user clicks.
        self.terms_visual_box.click()
        # Assert that the underlying checkbox state has changed as expected.
        expect(self.terms_container).to_have_attribute("aria-checked", "true", timeout=2000)

    def submit_form(self):
        """Clicks the main registration submission button."""
        self.register_button.click()

    # --- Verification Methods ---
    # Methods that perform assertions or retrieve state from the page.

    def verify_activation_popup(self):
        """Asserts that the verification code popup is visible after submission."""
        expect(self.verification_form).to_be_visible(timeout=10000)
        expect(self.verification_title).to_be_visible()

    def get_validation_errors(self) -> list[str]:
        """
        Waits for and retrieves all visible validation error messages.
        This is used in negative test scenarios to verify correct error handling.
        """
        try:
            # Wait for the first error message to appear, with a short timeout.
            # This handles cases where there's a slight delay due to animations.
            self.alert_messages.first.wait_for(state="visible", timeout=3000)
            return self.alert_messages.all_inner_texts()
        except Exception:
            # If no alerts appear within the timeout, it's not an error;
            # it simply means no validation messages were displayed.
            return []
