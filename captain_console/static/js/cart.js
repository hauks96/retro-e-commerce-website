$('.quantity').change(function(){
  let classes = this.className.split(" ");
  let product_id = classes[2];
  let totalPriceElement = document.getElementsByClassName("total-price-"+product_id)[0];
  let unit_price_element = document.getElementsByClassName("is-price-"+product_id)[0];

  let quantity = parseFloat(this.value);
  let unit = parseFloat(unit_price_element.value);

  let total = unit*quantity;
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