// Configuration
const CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:8000/api'
        : '/api'
};

// Global state
let selectedPlaceId = null;
let autocomplete = null;
let orderData = null;

// Expose to window for E2E testing
Object.defineProperty(window, 'selectedPlaceId', {
    get: () => selectedPlaceId,
    set: (value) => { selectedPlaceId = value; }
});

/**
 * Initialize Google Places Autocomplete
 */
function initGooglePlaces() {
    const addressInput = document.getElementById('address');

    if (!addressInput || !window.google) {
        console.error('Google Places API not loaded or address input not found');
        return;
    }

    // Initialize autocomplete
    // TODO: Migrate to PlaceAutocompleteElement before March 2025
    // https://developers.google.com/maps/documentation/javascript/places-migration-overview
    // Current API (google.maps.places.Autocomplete) will continue to work but is deprecated for new customers
    autocomplete = new google.maps.places.Autocomplete(addressInput, {
        types: ['address'],
        fields: ['formatted_address', 'place_id', 'name']
    });

    // Listen for place selection
    autocomplete.addListener('place_changed', function() {
        const place = autocomplete.getPlace();

        if (!place.place_id) {
            console.warn('No place selected');
            selectedPlaceId = null;
            return;
        }

        selectedPlaceId = place.place_id;
        console.log('Selected place:', place.formatted_address, 'ID:', selectedPlaceId);
    });
}

/**
 * Initialize PayPal SDK
 */
function initPayPalSDK() {
    if (!window.paypal) {
        console.error('PayPal SDK not loaded');
        return false;
    }

    console.log('PayPal SDK initialized successfully');
    return true;
}

/**
 * Show PayPal payment button
 */
function showPayPalButton() {
    const container = document.getElementById('paypal-button-container');
    const form = document.getElementById('orderForm');

    if (!container || !window.paypal) {
        showError('PayPal SDK를 로드할 수 없습니다.');
        return;
    }

    // Hide form, show PayPal container
    form.style.display = 'none';
    container.style.display = 'block';
    container.innerHTML = ''; // Clear previous buttons

    // Render PayPal button
    paypal.Buttons({
        style: {
            layout: 'vertical',
            color: 'blue',
            shape: 'rect',
            label: 'paypal'
        },
        createOrder: function(data, actions) {
            // This is just for demo - in production, create order via backend
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: '10.00' // Demo amount
                    }
                }]
            });
        },
        onApprove: function(data, actions) {
            console.log('PayPal payment approved:', data);

            // For walking skeleton, we just redirect to confirmation
            // In production, you would capture the payment here
            redirectToConfirmation();
        },
        onCancel: function(data) {
            console.log('PayPal payment cancelled:', data);
            form.style.display = 'block';
            container.style.display = 'none';
        },
        onError: function(err) {
            console.error('PayPal error:', err);
            showError('결제 중 오류가 발생했습니다. 다시 시도해주세요.');
            form.style.display = 'block';
            container.style.display = 'none';
        }
    }).render('#paypal-button-container');
}

/**
 * Submit order to backend
 */
async function submitOrder(formData) {
    showLoading(true);
    hideError();

    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/orders/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customer_name: formData.get('customerName'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                address: formData.get('address'),
                place_id: selectedPlaceId
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Order created:', result);

        // Store order data globally for confirmation
        orderData = result;
        window.lastOrderResponse = result; // For E2E testing

        return result;

    } catch (error) {
        console.error('Failed to create order:', error);
        throw error;
    } finally {
        showLoading(false);
    }
}

/**
 * Redirect to order confirmation page
 */
function redirectToConfirmation() {
    if (!orderData) {
        showError('주문 정보를 찾을 수 없습니다.');
        return;
    }

    const params = new URLSearchParams({
        order_id: orderData.order_id,
        email_sent: orderData.email_sent
    });

    window.location.href = `/order-confirmation.html?${params.toString()}`;
}

/**
 * Handle form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    // Validate address has Google Place selected
    if (!selectedPlaceId) {
        showError('주소 자동완성에서 주소를 선택해주세요.');
        return;
    }

    try {
        // Submit order to backend
        const result = await submitOrder(formData);

        if (result && result.order_id) {
            // Show PayPal button
            showPayPalButton();
        } else {
            throw new Error('Invalid response from server');
        }

    } catch (error) {
        console.error('Order submission error:', error);
        window.lastError = error.message || error.toString();  // For E2E testing
        showError('주문 처리 중 오류가 발생했습니다. 다시 시도해주세요.');
    }
}

/**
 * Show/hide loading indicator
 */
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = show ? 'block' : 'none';
    }
}

/**
 * Show error message
 */
function showError(message) {
    const errorEl = document.getElementById('errorMessage');
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    }
}

/**
 * Hide error message
 */
function hideError() {
    const errorEl = document.getElementById('errorMessage');
    if (errorEl) {
        errorEl.style.display = 'none';
    }
}

/**
 * Initialize application
 */
async function init() {
    console.log('Initializing K-Beauty Landing Page...');

    // Wait for configuration and SDKs to load
    try {
        await window.configPromise;
        console.log('✓ Config and SDKs ready');
    } catch (error) {
        console.error('Failed to load config/SDKs:', error);
        showError('설정을 불러올 수 없습니다. 페이지를 새로고침해주세요.');
        return;
    }

    // Initialize Google Places (SDK already loaded)
    initGooglePlaces();

    // Initialize PayPal (SDK already loaded)
    initPayPalSDK();

    // Attach form submit handler
    const form = document.getElementById('orderForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }

    console.log('✓ Initialization complete');
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Expose redirectToConfirmation to window for E2E testing
window.redirectToConfirmation = redirectToConfirmation;
