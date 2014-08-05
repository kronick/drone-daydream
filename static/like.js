function like(photo, el) {
    $.get("/like/" + photo, function(data) {
        like_el = $(el).parent().siblings(".likes")
        like_el.fadeOut(300, function() {
            like_el.text(data);
            like_el.fadeIn(300);
        });
    });
}
