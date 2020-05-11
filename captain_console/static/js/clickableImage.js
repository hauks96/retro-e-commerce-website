$(document).ready(function () {
    $('#altImg img').click(function () {
        $('#mainImage').attr('src',$(this).attr('src').replace('thumb', "main"));
    });
});
