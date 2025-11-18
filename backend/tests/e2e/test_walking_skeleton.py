"""
Walking Skeleton E2E Test

Tests the complete order submission flow from form input to confirmation page.
"""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_when_order_submitted_then_saved_to_database_email_sent_paypal_displayed_and_redirected_to_confirmation(
    page: Page,
    base_url: str
):
    """
    Test complete order submission flow.

    When: User fills form and submits order
    Then:
        1. Order is saved to database
        2. Confirmation email is sent
        3. PayPal payment UI is displayed
        4. User is redirected to order confirmation page
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
    page.fill('#customerName', 'Juan dela Cruz')
    page.fill('#email', 'juan.delacruz@gmail.com')
    page.fill('#phone', '+63 917 123 4567')
    page.fill('#address', 'Makati City, Metro Manila, Philippines')

    # Mock Google Places API place_id selection
    page.evaluate("window.selectedPlaceId = 'test_place_id_12345'")

    # Verify selectedPlaceId was set
    place_id = page.evaluate("window.selectedPlaceId")
    print(f"  selectedPlaceId set to: {place_id}")

    # When: User submits order
    page.click('#paymentButton')
    page.wait_for_timeout(5000)  # Increased timeout

    # Print console messages after submit
    print("\n  Console messages after submit:")
    new_messages = console_messages[len([m for m in console_messages if 'Initialization complete' in m]):]
    for msg in new_messages:
        print(f"  {msg}")

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
    print("\n✅ Walking Skeleton E2E Test Passed:")
    print(f"  📦 Order ID: {order_response['order_id']}")
    print(f"  💾 Database: Saved")
    print(f"  📧 Email: {'Sent' if order_response['email_sent'] else 'Failed'}")
    print(f"  💳 PayPal UI: Displayed")
    print(f"  🎉 Confirmation Page: Loaded")
