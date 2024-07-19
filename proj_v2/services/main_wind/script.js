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

getLocation();


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




function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(applyPosition, showError);
    } else {
        document.getElementById("location").innerHTML = "Geolocation is not supported by this browser.";
    }
}



function applyPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    fetchLocationByCoords(latitude, longitude);
}

function fetchLocationByCoords(latitude, longitude) {
    fetch(`/ya_map/api/location_by_coords?lat=${latitude}&long=${longitude}`)
        .then(response => response.json())
        .then(data => {
            let curr_location = data.location;
            for (let i = 0; i < 1; i++) {
                fetchTaskByLocation(curr_location);
            }
        })
}

function fetchTaskByLocation(curr_location)
{
    fetch(`/neurones/api/gen_task_by_location?location=${curr_location}`)
    .then(response => response.json())
    .then(data => {
        let div = document.getElementById("task_list_div");
        div.innerHTML = `<p class="text-center">${data.task}<p>`
    })
}

          

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            break;
        case error.POSITION_UNAVAILABLE:
            break;
        case error.TIMEOUT:
            break;
        case error.UNKNOWN_ERROR:
            break;
    }
}