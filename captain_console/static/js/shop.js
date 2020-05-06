//Here we want to implement some functionality for the shop html
//The filtering
// search bar filtering
$(document).ready(function () {
    $("#search").on("keyup", function () {
        let value = $(this).val().toLowerCase();
        $(".card-title").filter(function () {
            $(this).parent().parent().parent().toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });
});
// button filtering

//The ajax request for adding an item to basket (reference to the onclick button)



