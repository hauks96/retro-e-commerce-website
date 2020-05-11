$(document).ready(function () {
    if ($('#address-value')!==undefined){
        let address = $('#address-value').val();
        if (address!=="" && address!==null && address!==undefined){
            let address_input = $('#id_address');
            address_input.val(address);
        };

    };
    if ($('#country-value')!==undefined){
        let country = $('#country-value').val();
        if (country!=="" && country!==null && country!==undefined) {
            let country_input = $('#id_country');
            country_input.val(country);
        };

    };
    if ($('#city-value')!==undefined){
        let city = $('#city-value').val();
        if (city!=="" && city!==null && city!==undefined) {
            let city_input = $('#id_city');
            city_input.val(city);
        };

    };
    if ($('#postal-code-value')!==undefined){
        let postalCode = $('#postal-code-value').val();
        if (postalCode!=="" && postalCode!==null && postalCode!==undefined) {
            let postalCode_input = $('#id_postal_code');
            postalCode_input.val(postalCode);
        };

    };
    if ($('#note-value')!==undefined){
        let note = $('#note-value').val();
        if (note!=="" && note!==null && note!==undefined) {
            let note_input = $('#id_note');
            note_input.val(note);
        };

    };
});


