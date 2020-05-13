$(document).ready(function() {
    let cookies = document.cookie;
    let cookies_list = cookies.split(';');
    for (let i=0; i<cookies_list.length; i++){
        let current_cookie = cookies_list[i].split('=');
        if (current_cookie[0].includes('itm_count')){
            let itemcount = current_cookie[1];
            let itemCountElement = document.getElementById('button-item-count');
            itemCountElement.innerHTML = itemcount;
        };
    };
});
