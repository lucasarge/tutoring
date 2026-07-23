document.addEventListener("DOMContentLoaded", function() {
    const createBtn = document.getElementById("createBtn");
    const createMenu = document.getElementById("createMenu");
    const closeBtn = document.getElementById("closeBtn")
    const stars = document.querySelectorAll(".star");
    const starInput = document.querySelector("#id_stars");    

    createBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        createMenu.classList.toggle("hidden");
    });

    closeBtn.addEventListener("click", function() {
        createMenu.classList.add("hidden");
    });

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
    });

});