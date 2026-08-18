// JavaScript file used to customise the review form.

document.addEventListener("DOMContentLoaded", function() {

    // Getting all elements via id from HTML.
    const createBtn = document.getElementById("createBtn");
    const createMenu = document.getElementById("createMenu");
    const closeBtn = document.getElementById("closeBtn")
    const stars = document.querySelectorAll(".star");
    const starInput = document.querySelector("#id_stars");    

    // When create review button clicked open the create review menu.
    if (createBtn, createMenu) {
        createBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            createMenu.classList.remove("hidden");
            createMenu.classList.add("flex")
    })};

    // When close button clicked close the create review menu.
    if (closeBtn, createMenu) {
        closeBtn.addEventListener("click", function() {
            createMenu.classList.remove("flex");
            createMenu.classList.add("hidden");
    })};

    // For each star add click event to update the CSS and starInput value for review form.
    if (stars, starInput) {
        stars.forEach(star => {
            star.addEventListener("click", () => {
                const rating = star.dataset.value;
                starInput.value = rating;

                stars.forEach(s => {
                    s.classList.toggle(
                        "text-yellow-400",
                        s.dataset.value <= rating
                    );
                    s.classList.toggle(
                        "text-gray-300",
                        s.dataset.value > rating
                    );
                });
            });
    })};
});