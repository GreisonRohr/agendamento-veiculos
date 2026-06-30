document.addEventListener("DOMContentLoaded", () => {

    const menu = document.getElementById("menu-toggle");

    const sidebar = document.getElementById("sidebar");

    if(menu){

        menu.addEventListener("click", () => {

            sidebar.classList.toggle("show");

        });

    }

});