$(document).ready(function() { // this waits until the document is fully loaded
        var allRows = $("tr");
        $("input#productSearch").on("keydown keyup", function() {
          allRows.hide();
          $("tr:contains('" + $(this).val() + "')").show();
        });
        });