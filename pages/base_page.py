from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = "/"):
        """Appends the path to the base_url seamlessly."""
        self.page.goto(path)
