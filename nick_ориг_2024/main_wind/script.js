document.addEventListener("DOMContentLoaded", function() {
    // Show welcome popup
    const welcomePopup = document.getElementById("welcomePopup");
    if (welcomePopup) {
        welcomePopup.style.display = "flex";
    }

    // Add hover animation for menu buttons
    const buttons = document.querySelectorAll('.btn-3d, .start-walk-btn');
    buttons.forEach(button => {
        button.addEventListener('mouseover', () => {
            button.style.animation = 'none';
            button.offsetHeight; // trigger reflow
            button.style.animation = null;
        });
    });

    // Add additional animations
    addScrollAnimations();
});

function closeWelcomePopup() {
    const welcomePopup = document.getElementById("welcomePopup");
    if (welcomePopup) {
        welcomePopup.style.display = "none";
    }
}

function addScrollAnimations() {
    const items = document.querySelectorAll('.carousel-item, .recommended-section, .news-section');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, {
        threshold: 0.1
    });

    items.forEach(item => {
        observer.observe(item);
    });
}
