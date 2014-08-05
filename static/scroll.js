loading_scroll = false;
$(window).scroll(function() {
    if (!loading_scroll && $(window).scrollTop() > $(document).height() - $(window).height() - 800) {
        loading_scroll = true;
        $.get("/scroll/" + (page + 1), function(response) {
            console.log(response);
            $("#post-container").append(response);
            page += 1;
        }).always(function() { loading_scroll = false; })
    }
});
