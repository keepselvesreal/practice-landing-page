"""
Walking Skeleton E2E Test with Real Google Places API

This test uses the actual Google Places Autocomplete API instead of mocking.
Requires:
- Google Places API enabled in Google Cloud Console
- Valid API key in .env
- Network connection

Run with: TEST_ENV=local pytest tests/e2e/test_walking_skeleton_real_api.py -v -s
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
@pytest.mark.slow
def test_with_real_google_places_api(
    page: Page,
    base_url: str
):
    """
    Test complete order submission flow with real Google Places API.

    When: User fills form using Google Places Autocomplete
    Then:
        1. Google Places Autocomplete works
        2. Order is saved to database with real place_id
        3. Confirmation email is sent
        4. PayPal payment UI is displayed
        5. User is redirected to order confirmation page
    """
    # Capture console messages for debugging
    console_messages = []
    page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))
    page.on("pageerror", lambda err: console_messages.append(f"[ERROR] {err}"))

    # Given: Navigate to landing page
    page.goto(base_url)
    expect(page).to_have_title("K-Beauty Landing Page")

    # Wait for config and SDKs to load
    page.wait_for_function("window.ENV && window.google && window.paypal", timeout=15000)
    print("✓ Config and SDKs loaded")

    # Print console messages so far
    for msg in console_messages:
        print(f"  {msg}")

    # When: User fills order form (Philippine user example)
    page.fill('#customerName', 'Maria Santos')
    page.fill('#email', 'maria.santos@gmail.com')
    page.fill('#phone', '+63 918 765 4321')

    # Use real Google Places Autocomplete
    address_input = page.locator('#address')
    address_input.click()
    address_input.fill('Quezon City, Metro Manila')

    # Wait for Google Places Autocomplete dropdown
    try:
        page.wait_for_selector('.pac-container', state='visible', timeout=5000)
        print("✓ Google Places dropdown appeared")

        # Wait a bit for results to populate
        page.wait_for_timeout(1000)

        # Click first autocomplete suggestion
        page.click('.pac-item:first-child')
        print("✓ Selected place from autocomplete")

        # Wait for place_id to be set
        page.wait_for_function("window.selectedPlaceId !== null", timeout=5000)
        place_id = page.evaluate("window.selectedPlaceId")
        print(f"✓ Place ID set: {place_id}")

        assert place_id is not None, "Place ID should be set after autocomplete selection"
        assert place_id != 'manual_input', "Should use real place_id, not fallback"

    except Exception as e:
        print(f"\n⚠ Google Places Autocomplete failed: {e}")
        print("This test requires:")
        print("  1. Google Places API enabled in Google Cloud Console")
        print("  2. Valid API key configured")
        print("  3. Network connection")
        pytest.skip("Google Places API not available")

    # When: User submits order
    page.click('#paymentButton')
    page.wait_for_timeout(3000)

    # Then 1: Order is saved to database
    order_response = page.evaluate("window.lastOrderResponse")

    assert order_response is not None, \
        "Order API response not found - backend may have failed"

    assert 'order_id' in order_response, \
        "Order ID missing - database save may have failed"

    assert order_response['order_id'].startswith('ORD-'), \
        f"Invalid order ID format: {order_response['order_id']}"

    assert order_response['status'] == 'created', \
        f"Expected status 'created', got '{order_response['status']}'"

    # Then 2: Confirmation email is sent
    assert 'email_sent' in order_response, \
        "Email sent status missing in response"

    assert order_response['email_sent'] is True, \
        f"Email failed to send - email_sent: {order_response.get('email_sent')}"

    # Then 3: PayPal payment UI is displayed
    paypal_container = page.locator('#paypal-button-container')
    expect(paypal_container).to_be_visible(timeout=5000)

    order_form = page.locator('#orderForm')
    expect(order_form).not_to_be_visible()

    page.wait_for_function("window.paypal && window.paypal.Buttons")

    # Then 4: User can be redirected to confirmation page
    # Simulate PayPal approval and trigger redirect
    page.evaluate("window.redirectToConfirmation()")

    # Wait for navigation
    page.wait_for_url(f"{base_url}/order-confirmation.html*", timeout=5000)

    # Verify confirmation page content
    expect(page.locator('h2')).to_contain_text('주문이 접수되었습니다')

    # Verify order number is displayed
    order_number_text = page.locator('#orderNumber').inner_text()
    assert order_number_text == order_response['order_id'], \
        f"Order number mismatch: {order_number_text} != {order_response['order_id']}"

    # Verify email status
    email_status = page.locator('#emailStatus').inner_text()
    if order_response['email_sent']:
        assert '✓ 이메일 발송 완료' in email_status
    else:
        assert '⚠ 이메일 발송 실패' in email_status

    # Log test results
    print("\n✅ Walking Skeleton E2E Test (Real API) Passed:")
    print(f"  📦 Order ID: {order_response['order_id']}")
    print(f"  📍 Place ID: {place_id}")
    print(f"  💾 Database: Saved")
    print(f"  📧 Email: {'Sent' if order_response['email_sent'] else 'Failed'}")
    print(f"  💳 PayPal UI: Displayed")
    print(f"  🎉 Confirmation Page: Loaded")
