import pytest
from playwright.async_api import async_playwright

@pytest.fixture(scope="function")
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()

@pytest.fixture(scope="function")
async def page(browser):
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await context.close()
