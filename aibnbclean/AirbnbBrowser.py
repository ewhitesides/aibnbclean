import os
from playwright.sync_api import sync_playwright, Page


class AirbnbBrowser:
    def __init__(self, headless: bool, user_data_dir: str):
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.playwright = None
        self.context = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
            args=[
                "--start-maximized",
                "--disable-session-crashed-bubble",
                "--hide-crash-restore-bubble",
                "--disable-infobars",
                "--disable-notifications",
            ],
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()

    def get_new_page(self) -> Page:
        # Contexts provide isolation without the overhead of a new browser process
        if not self.context:
            raise RuntimeError(
                "browser context not initialized. Use 'with' statement or call __enter__"
            )
        context = self.context
        return context.new_page()

    def is_logged_in(self) -> bool:
        page = self.get_new_page()
        page.goto("https://www.airbnb.com/hosting")
        logged_in = page.url == "https://www.airbnb.com/hosting"
        page.close()  # Cleanup the specific page/context
        return logged_in

    def login(self):
        page = self.get_new_page()
        page.goto("https://www.airbnb.com/login?redirect_url=%2Fhosting")
        print("login to airbnb in the opened browser window")
        page.wait_for_url("https://www.airbnb.com/hosting", timeout=0)
        print("login successful, closing browser")
        page.close()  # Cleanup the specific page/context
