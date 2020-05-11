//Here we want to implement some functionality for the shop html
//The filtering
// search bar filtering
$(document).ready(function () {
    $("#search").on("keyup", function () { // When we type in something
        let value = $(this).val().toLowerCase(); // Makes title lowercase
        $("#test").filter(function () {
            $(this).parent().parent().parent().toggle($(this).text().toLowerCase().indexOf(value) > -1); //Finds parent/parent/parent div of card-title
        });
    });
});
// button filtering

//The ajax request for adding an item to basket (reference to the onclick button)



