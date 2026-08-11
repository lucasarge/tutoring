// JavaScript file used to provide popups for navigation in navbar.

document.addEventListener("DOMContentLoaded", function() {

    // Getting all elements via id from HTML.
    const profileBtn = document.getElementById("profileBtn");
    const profileMenu = document.getElementById("profileMenu");
    const profileArrow = document.getElementById("profileArrow");
    const logoBtn = document.getElementById("logoBtn");
    const logoMenu = document.getElementById("logoMenu");
    const logoArrow = document.getElementById("logoArrow");

    // If open button is clicked display profileMenu and profileArrow and stopPropagation for error prevention.
    if (profileBtn) { 
        profileBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            profileMenu.classList.toggle("hidden");
            profileArrow.classList.toggle("hidden");
    })};

    // If anywhere else on the page is clicked then hide profileMenu and profileArrow.
    document.addEventListener("click", function () {
        profileMenu.classList.add("hidden");
        profileArrow.classList.add("hidden");
    });

    // if logo button is clicked display logoMenu and logoArrow and stopPropogation for error prevention.
    if (logoBtn) { 
        logoBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            logoMenu.classList.toggle("hidden");
            logoArrow.classList.toggle("hidden");
    })};

    // If anywhere else on the page is clicked then hide logoMenu and logoArrow.
    document.addEventListener("click", function () {
        logoMenu.classList.add("hidden");
        logoArrow.classList.add("hidden");
    });
});