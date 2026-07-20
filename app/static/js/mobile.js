document.addEventListener("DOMContentLoaded", () => {

    const menu = document.getElementById("menu-toggle");

    const sidebar = document.getElementById("sidebar");

    const overlay = document.getElementById("sidebar-overlay");

    if(menu){

        menu.addEventListener("click", () => {

            sidebar.classList.toggle("show");

            if (sidebar.classList.contains("show")) {
                overlay.style.display = "block";
            } else {
                overlay.style.display = "none";
            }

        });

    }

    // Fechar sidebar ao clicar no overlay
    if (overlay) {
        overlay.addEventListener("click", () => {
            sidebar.classList.remove("show");
            overlay.style.display = "none";
        });
    }

    // Fechar sidebar ao clicar em um link (mobile)
    const sidebarLinks = sidebar.querySelectorAll("a");
    sidebarLinks.forEach(link => {
        link.addEventListener("click", () => {
            if (window.innerWidth < 992) {
                sidebar.classList.remove("show");
                if (overlay) overlay.style.display = "none";
            }
        });
    });

});
