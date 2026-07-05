/**
 * Propertism Address Autocomplete Framework
 * Centralized Reusable Component for Google Places Autocomplete
 */

(function() {
    const API_URL = 'https://maps.googleapis.com/maps/api/js';
    let isScriptLoaded = false;
    let isScriptLoading = false;
    const loaderCallbacks = [];

    // Dynamically inject the Google Maps Places library script only when needed
    function loadGooglePlacesAPI(apiKey, callback) {
        if (isScriptLoaded || (window.google && window.google.maps && window.google.maps.places)) {
            isScriptLoaded = true;
            callback();
            return;
        }
        loaderCallbacks.push(callback);
        if (isScriptLoading) return;
        isScriptLoading = true;

        const callbackName = 'googleMapsPlacesLoadedCallback';
        window[callbackName] = () => {
            isScriptLoaded = true;
            isScriptLoading = false;
            while (loaderCallbacks.length > 0) {
                const cb = loaderCallbacks.shift();
                try { cb(); } catch (e) { console.error("Loader callback error:", e); }
            }
            try { delete window[callbackName]; } catch (e) {}
        };

        const script = document.createElement('script');
        script.src = `${API_URL}?key=${apiKey}&libraries=places&callback=${callbackName}`;
        script.async = true;
        script.defer = true;
        script.onerror = () => {
            isScriptLoading = false;
            console.error("Google Places API failed to load. Falling back to manual entry.");
        };
        document.head.appendChild(script);
    }

    // Initialize Autocomplete instance on target input element
    function initAutocompleteOnInput(input) {
        const apiKey = input.getAttribute('data-api-key') || '';
        if (!apiKey) {
            console.warn("Google Maps API Key not specified on autocomplete input.");
            return;
        }

        loadGooglePlacesAPI(apiKey, () => {
            if (!window.google || !window.google.maps || !window.google.maps.places) {
                console.warn("Google Places API library ('places') is not available. Autocomplete disabled. Manual entry fallback active.");
                return;
            }
            const countryString = input.getAttribute('data-countries') || 'in';
            const countries = countryString.split(',').map(c => c.trim().toLowerCase());
            
            const options = {
                fields: ['address_components', 'geometry', 'formatted_address', 'place_id'],
                types: ['address']
            };

            if (countries.length > 0 && countries[0] !== '') {
                options.componentRestrictions = { country: countries };
            }

            const autocomplete = new google.maps.places.Autocomplete(input, options);

            // Locate containing address group
            const group = input.closest('[data-address-group]');
            if (!group) {
                console.warn("data-address-autocomplete input is missing a parent container with data-address-group attribute.");
            }

            autocomplete.addListener('place_changed', function() {
                const place = autocomplete.getPlace();
                if (!place.geometry) {
                    console.warn("No geometry details available for selected address.");
                    return;
                }

                const extracted = extractPlaceData(place);
                if (group) {
                    populateGroupFields(group, extracted);
                }
                
                // Dispatch custom event for programmatic integration (e.g. realBOT, analytics)
                const event = new CustomEvent('address-selected', { detail: extracted, bubbles: true });
                input.dispatchEvent(event);
            });
        });
    }

    // Helper to standardise the API address components
    function extractPlaceData(place) {
        const components = place.address_components || [];
        const data = {
            full_address: place.formatted_address || '',
            formatted_address: place.formatted_address || '',
            place_id: place.place_id || '',
            latitude: place.geometry.location.lat(),
            longitude: place.geometry.location.lng(),
            street_address: '',
            locality: '',
            area: '',
            city: '',
            district: '',
            state: '',
            country: '',
            postal_code: ''
        };

        let streetNumber = '';
        let route = '';

        components.forEach(comp => {
            const types = comp.types || [];
            const value = comp.long_name || '';

            if (types.includes('street_number')) {
                streetNumber = value;
            } else if (types.includes('route')) {
                route = value;
            } else if (types.includes('sublocality_level_1') || types.includes('sublocality')) {
                data.locality = value;
            } else if (types.includes('sublocality_level_2')) {
                data.area = value;
            } else if (types.includes('locality')) {
                data.city = value;
            } else if (types.includes('administrative_area_level_2')) {
                data.district = value;
            } else if (types.includes('administrative_area_level_1')) {
                data.state = value;
            } else if (types.includes('country')) {
                data.country = value;
            } else if (types.includes('postal_code')) {
                data.postal_code = value;
            }
        });

        data.street_address = [streetNumber, route].filter(Boolean).join(' ');

        if (!data.locality && data.area) {
            data.locality = data.area;
        }

        return data;
    }

    // Auto-fill hidden/visible inputs in the same data-address-group wrapper
    function populateGroupFields(group, data) {
        const fields = group.querySelectorAll('[data-address-field]');
        fields.forEach(field => {
            const fieldName = field.getAttribute('data-address-field');
            if (fieldName in data) {
                const val = data[fieldName];
                if (field.tagName === 'INPUT' || field.tagName === 'SELECT' || field.tagName === 'TEXTAREA') {
                    field.value = val;
                    field.dispatchEvent(new Event('change', { bubbles: true }));
                } else {
                    field.textContent = val;
                }
            }
        });
    }

    // Auto scan DOM for inputs
    function initializeAllAutocompletes() {
        const inputs = document.querySelectorAll('[data-address-autocomplete]');
        inputs.forEach(input => {
            if (!input.hasAttribute('data-autocomplete-initialized')) {
                input.setAttribute('data-autocomplete-initialized', 'true');
                initAutocompleteOnInput(input);
            }
        });
    }

    // Expose Framework API globally
    window.AddressAutocompleteFramework = {
        init: initializeAllAutocompletes,
        initInput: initAutocompleteOnInput
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeAllAutocompletes);
    } else {
        initializeAllAutocompletes();
    }
})();
