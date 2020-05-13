$(document).ready(function () {
    $('#carousel-next').on('click', function () {
        $('.carousel').carousel('pause');
        let activeSlideElement = document.getElementsByClassName('active')
        let imageElement = jQuery(activeSlideElement).find("img");
        let imageSource = imageElement.attr('src');

        let mainImageElement = $('#main-image');
        mainImageElement.attr('src', imageSource);

    });
    $('#carousel-previous').on('click', function () {
        $('.carousel').carousel('pause');
        let activeSlideElement = document.getElementsByClassName('active')
        let imageElement = jQuery(activeSlideElement).find("img");
        let imageSource = imageElement.attr('src');

        let mainImageElement = $('#main-image');
        mainImageElement.attr('src', imageSource);

    });
});