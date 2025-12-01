import pytest
from playwright.async_api import Page, expect
import asyncio
import random
import string

BASE_URL = "http://localhost:8000"

def generate_unique_email():
    """Generate a unique email for testing"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_string}@example.com"

@pytest.mark.asyncio
async def test_register_with_valid_data(page: Page):
    """Test successful registration with valid email and password"""
    await page.goto(f"{BASE_URL}/register-page")
    
    # Fill in the form with unique email
    unique_email = generate_unique_email()
    await page.fill("#email", unique_email)
    await page.fill("#password", "ValidPass123")
    await page.fill("#confirmPassword", "ValidPass123")
    
    # Submit the form
    await page.click("button[type='submit']")
    
    # Wait for success message
    await page.wait_for_selector(".message.success", timeout=5000)
    
    # Verify success message is displayed
    success_message = page.locator(".message.success")
    await expect(success_message).to_be_visible()
    await expect(success_message).to_contain_text("Registration successful")

@pytest.mark.asyncio
async def test_register_with_short_password(page: Page):
    """Test registration fails with password less than 8 characters"""
    await page.goto(f"{BASE_URL}/register-page")
    
    # Fill in the form with short password
    await page.fill("#email", "shortpass@example.com")
    await page.fill("#password", "Short1")
    await page.fill("#confirmPassword", "Short1")
    
    # Submit the form
    await page.click("button[type='submit']")
    
    # Wait a moment for validation
    await asyncio.sleep(0.5)
    
    # Verify error message is displayed
    error_message = page.locator("#passwordError")
    await expect(error_message).to_be_visible()
    await expect(error_message).to_contain_text("at least 8 characters")

@pytest.mark.asyncio
async def test_register_with_invalid_email(page: Page):
    """Test registration fails with invalid email format"""
    await page.goto(f"{BASE_URL}/register-page")
    
    # Remove HTML5 validation to test JavaScript validation
    await page.evaluate("""
        document.querySelector('#email').removeAttribute('type');
        document.querySelector('#email').setAttribute('type', 'text');
    """)
    
    # Fill in the form with invalid email
    await page.fill("#email", "invalidemail")
    await page.fill("#password", "ValidPass123")
    await page.fill("#confirmPassword", "ValidPass123")
    
    # Submit the form
    await page.click("button[type='submit']")
    
    # Wait a moment for validation
    await asyncio.sleep(0.5)
    
    # Verify error message is displayed
    error_message = page.locator("#emailError")
    await expect(error_message).to_be_visible()
    await expect(error_message).to_contain_text("valid email")

@pytest.mark.asyncio
async def test_register_with_mismatched_passwords(page: Page):
    """Test registration fails when passwords don't match"""
    await page.goto(f"{BASE_URL}/register-page")
    
    # Fill in the form with mismatched passwords
    await page.fill("#email", "mismatch@example.com")
    await page.fill("#password", "ValidPass123")
    await page.fill("#confirmPassword", "DifferentPass123")
    
    # Submit the form
    await page.click("button[type='submit']")
    
    # Wait a moment for validation
    await asyncio.sleep(0.5)
    
    # Verify error message is displayed
    error_message = page.locator("#confirmPasswordError")
    await expect(error_message).to_be_visible()
    await expect(error_message).to_contain_text("do not match")

@pytest.mark.asyncio
async def test_login_with_correct_credentials(page: Page):
    """Test successful login with correct credentials"""
    # First register a user with unique email
    unique_email = generate_unique_email()
    await page.goto(f"{BASE_URL}/register-page")
    await page.fill("#email", unique_email)
    await page.fill("#password", "LoginPass123")
    await page.fill("#confirmPassword", "LoginPass123")
    await page.click("button[type='submit']")
    
    # Wait for redirect or success
    await asyncio.sleep(2)
    
    # Now try to login
    await page.goto(f"{BASE_URL}/login-page")
    await page.fill("#email", unique_email)
    await page.fill("#password", "LoginPass123")
    
    # Submit the form
    await page.click("button[type='submit']")
    
    # Wait for success message
    await page.wait_for_selector(".message.success", timeout=5000)
    
    # Verify success message
    success_message = page.locator(".message.success")
    await expect(success_message).to_be_visible()
    await expect(success_message).to_contain_text("Login successful")

@pytest.mark.asyncio
async def test_login_with_wrong_password(page: Page):
    """Test login fails with incorrect password"""
    await page.goto(f"{BASE_URL}/login-page")
    
    # Try to login with wrong password (using an email that should exist from previous tests)
    await page.fill("#email", "test@example.com")
    await page.fill("#password", "WrongPassword123")
    
    # Submit the form
    await page.click("button[type='submit']")
    
    # Wait for error message
    await page.wait_for_selector(".message.error", timeout=5000)
    
    # Verify error message
    error_message = page.locator(".message.error")
    await expect(error_message).to_be_visible()
    await expect(error_message).to_contain_text("Incorrect email or password")

@pytest.mark.asyncio
async def test_login_with_invalid_email_format(page: Page):
    """Test login client-side validation for invalid email"""
    await page.goto(f"{BASE_URL}/login-page")
    
    # Remove HTML5 validation to test JavaScript validation
    await page.evaluate("""
        document.querySelector('#email').removeAttribute('type');
        document.querySelector('#email').setAttribute('type', 'text');
    """)
    
    # Fill invalid email
    await page.fill("#email", "notanemail")
    await page.fill("#password", "SomePassword123")
    
    # Submit the form
    await page.click("button[type='submit']")
    
    # Wait a moment for validation
    await asyncio.sleep(0.5)
    
    # Verify error message
    error_message = page.locator("#emailError")
    await expect(error_message).to_be_visible()
    await expect(error_message).to_contain_text("valid email")
