document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.querySelector('#menu-icon');
    const sidebar = document.querySelector('#sidebar');
    const mainContent = document.querySelector('.main-content');
    const menuLinks = document.querySelectorAll('.menu a');
    const horizontalMenuLinks = document.querySelectorAll('.horizontal-menu a');

    if (menuIcon && sidebar && mainContent) {
        const toggleSidebar = () => {
            sidebar.classList.toggle('open');
            mainContent.classList.toggle('shifted');
        };

        menuIcon.addEventListener('click', toggleSidebar);

        mainContent.addEventListener('click', () => {
            if (sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
                mainContent.classList.remove('shifted');
            }
        });

        menuLinks.forEach(link => {
            link.addEventListener('click', () => {
                menuLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });

        horizontalMenuLinks.forEach(link => {
            link.addEventListener('click', () => {
                horizontalMenuLinks.forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });
    } else {
        console.error("Не удалось найти необходимые элементы для меню");
    }
});
