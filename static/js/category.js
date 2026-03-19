$(".like_button").click(function(e) {
    e.preventDefault();
    e.stopPropagation();

    const $btn = $(this);
    const recipeID = $btn.data("recipe-id")
    const liked = $btn.attr("aria-pressed") === "true";
    const formAction = liked ? "DELETE" : "POST";
    $btn.prop('disabled', true);

    $.ajax({
        url: `api/like/${recipeID}/`,
        type: formAction,
        headers: {
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
        },

        success: function(response) {
            const likeCount = response.like_count
            const liked = response.liked

            $btn.attr("aria-pressed", liked ? "true" : "false");
            liked ? $btn.text("Liked") : $btn.text("Like");
            $btn.closest(".like_section").find(".like_counter").text(likeCount + " Likes");
        },
        error: function (xhr) {
            console.error(xhr.responseText || xhr.statusText);
            alert("Something went wrong.");
        },
        complete: function () {
            $btn.prop('disabled', false);
        }
    })
});
