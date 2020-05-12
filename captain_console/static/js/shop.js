//Here we want to implement some functionality for the shop html
//The filtering
// search bar filtering
$(document).ready(function () {
    $("#search").on("keyup", function () { // When we type in something
        let value = $(this).val().toLowerCase(); // Makes title lowercase
        let products = document.getElementsByClassName("product-name-div")
        for(let i=0; i<products.length; i++){
            if (products[i].textContent.toLowerCase().includes(value)==false){
                products[i].parentElement.parentElement.style.display = 'none';
            }
            else {
                products[i].parentElement.parentElement.style.display = 'block';
            };
        };
    });
});
// button filtering

//The ajax request for adding an item to basket (reference to the onclick button)
$(document).ready(function () {
    $("#search-mobile").on("keyup", function () { // When we type in something
        let value = $(this).val().toLowerCase(); // Makes title lowercase
        let products = document.getElementsByClassName("product-name-div")
        for(let i=0; i<products.length; i++){
            if (products[i].textContent.toLowerCase().includes(value)==false){
                products[i].parentElement.parentElement.style.display = 'none';
            }
            else {
                products[i].parentElement.parentElement.style.display = 'block';
            };
        };
    });
});
// button