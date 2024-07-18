document.getElementById('editProfilePicBtn').addEventListener('click', function() {
    document.getElementById('avatarModal').style.display = 'block';
    document.body.classList.add('modal-open');
});

document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('avatarModal').style.display = 'none';
    document.body.classList.remove('modal-open');
});

window.onclick = function(event) {
    if (event.target == document.getElementById('avatarModal')) {
        document.getElementById('avatarModal').style.display = 'none';
        document.body.classList.remove('modal-open');
    }
};

function selectAvatar(avatarPath) {
    document.getElementById('avatar').src = avatarPath;
    document.getElementById('avatarModal').style.display = 'none';
    document.body.classList.remove('modal-open');
}

function uploadAvatar() {
    const fileInput = document.getElementById('uploadAvatar');
    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onloadend = function() {
        document.getElementById('avatar').src = reader.result;
        document.getElementById('avatarModal').style.display = 'none';
        document.body.classList.remove('modal-open');
    };

    if (file) {
        reader.readAsDataURL(file);
    } else {
        alert("No file selected!");
    }
}

// Existing JavaScript code
document.getElementById('editProfileBtn').addEventListener('click', editProfile);
document.getElementById('editProfilePicBtn').addEventListener('click', editProfilePic);

function editProfile() {
    let username = prompt("Enter new username:", "Nick");
    if (username !== null && username !== "") {
        document.getElementById('username').innerText = username;
    }
}

function editProfilePic() {
    document.getElementById('avatarModal').style.display = 'block';
}

function manageNotifications() {
    alert("Manage Notifications clicked");
}

function managePersonalData() {
    alert("Manage Personal Data clicked");
}

function manageSocialMedia() {
    alert("Manage Social Media clicked");
}

// Simulate fetching user data from server
window.onload = function() {
    fetchUserData();
};

function fetchUserData() {
    let userData = {
        username: "Nick",
        avatar: "images/avatar.png",
        stats: {
            routesCovered: 20,
            tasksCompleted: 16,
            timeSpent: "30 hours",
            activeQuests: 5,
            questsCompleted: 12
        },
        rating: 4.5
    };

    document.getElementById('username').innerText = userData.username;
    document.getElementById('avatar').src = userData.avatar;
    document.getElementById('routesCovered').innerText = userData.stats.routesCovered;
    document.getElementById('tasksCompleted').innerText = userData.stats.tasksCompleted;
    document.getElementById('timeSpent').innerText = userData.stats.timeSpent;
    document.getElementById('activeQuests').innerText = userData.stats.activeQuests;
    document.getElementById('questsCompleted').innerText = userData.stats.questsCompleted;
    document.getElementById('userRating').innerText = userData.rating;
}

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.getElementById(pageId).classList.add('active');
}

// Ensure the profile page is visible by default
document.getElementById('profilePage').classList.add('active');
