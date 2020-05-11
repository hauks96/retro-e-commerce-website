$(document).ready(function () {
    if ($('#cardholder-name-value')!==undefined){
        let cardHolder = $('#cardholder-name-value').val();
        let cardHolder_input = $('#id_cardholder_name');
        cardHolder_input.val(cardHolder)

    };
    if ($('#credit-card-num-value')!==undefined){
        let cardNum = $('#credit-card-num-value').val();
        let cardNum_input = $('#id_credit_card_num');
        cardNum_input.val(cardNum)

    };
    if ($('#expiry-year-value')!==undefined){
        let expiryYear = $('#expiry-year-value').val();
        let expiryYear_input = $('#id_expiry_year');
        expiryYear_input.val(expiryYear)

    };
    if ($('#expiry-month-value')!==undefined){
        let expiryMonth = $('#expiry-month-value').val();
        let expiryMonth_input = $('#id_expiry_month');
        expiryMonth_input.val(expiryMonth)

    };
});


