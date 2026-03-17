$(".like_button").click(function(e) {
    e.preventDefault();
    e.stopPropagation();

    const $btn = $(this);
    const recipeID = $btn.data("recipe-id")
    const liked = $btn.attr("aria-pressed") === "true";
    const formAction = liked ? "DELETE" : "POST";
    alert(liked)
    $btn.prop('disabled', true);

    $.ajax({
        // url: `/api/like/${recipeID}`,
        url: 'api/like/1',
        type: formAction,
        headers: {
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
        }
    })
});
