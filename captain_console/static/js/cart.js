$('.quantity').change(function(){
    let classes = this.className.split(" ");
    let product_id = classes[2];
    let totalPriceElement = document.getElementsByClassName("total-price-"+product_id)[0];
    let current_total = parseFloat(totalPriceElement.value);
    let unit_price_element = document.getElementsByClassName("is-price-"+product_id)[0];

    let quantity = parseFloat(this.value);
    let unit = parseFloat(unit_price_element.value);

    let total = unit*quantity;
    let difference = total-current_total;
    let cartTotalElement = document.getElementById('cart-total-summary');
    let current_cart_total = parseFloat(cartTotalElement.value);
    current_cart_total = current_cart_total+difference;
    cartTotalElement.value = current_cart_total;
    totalPriceElement.value = total;

});
// fetches the edit button that was pressed
$('.edit-button').on('click', function () {
    let product_id = this.id.split('-')[1];
    // Getting the corresponding 'edit' form element
    let editElement = document.getElementsByClassName("is-edit-"+product_id)[0];
    // Changing the values
    editElement.value = 'True';
    // Making sure the opposite element 'remove' isn't set to true
    let removeElement = document.getElementsByClassName("is-remove-"+product_id)[0];
    removeElement.value = 'False';
})

// fetches the remove button that was pressed
$('.remove-button').on('click', function () {
    let product_id = this.id.split('-')[1];
    // Getting the corresponding 'remove' form element
    let removeElement = document.getElementsByClassName("is-remove-"+product_id)[0];
    // Changing the values
    removeElement.value = 'True';
    // Making sure the opposite element 'edit' isn't set to true
    let editElement = document.getElementsByClassName("is-edit-"+product_id)[0];
    editElement.value = 'False';
})


$(document).ready(function() {
    let cookies = document.cookie;
    let cookies_list = cookies.split(';');
    for (let i=0; i<cookies_list.length; i++){
        let current_cookie = cookies_list[i].split('=');
        if (current_cookie[0].includes('itm_count')){
            let itemcount = current_cookie[1];
            if (itemcount == 0){
                let ptcb = $('#proceed-to-checkout-button');
                ptcb.attr('class', 'btn btn-secondary disabled');
                ptcb.attr('disabled', true);
            }
            else {
                let ptcb = $('proceed-to-checkout-button');
                ptcb.attr('class', 'btn btn-primary');
                ptcb.attr('disabled', false);
            };
        };
    };
});


