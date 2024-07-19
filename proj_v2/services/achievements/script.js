const achievements = {
    ecology: [
        {
            title: 'Экологический Дог Вок',
            image: 'park.png',
            progress: 70,
            description: 'Прогулки с собаками в экологически чистых парках.'
        },
        {
            title: 'Забота о Среде',
            image: 'park.png',
            progress: 50,
            description: 'Участие в акциях по защите окружающей среды.'
        },
        {
            title: 'Чистый Город',
            image: 'park.png',
            progress: 90,
            description: 'Организация уборок в городе.'
        }
    ],
    landmarks: [
        {
            title: 'Посетил Эрмитаж',
            image: 'landmark.png',
            progress: 80,
            description: 'Посещение одного из самых известных музеев мира.'
        },
        {
            title: 'Экскурсия по Петербургу',
            image: 'landmark.png',
            progress: 60,
            description: 'Обзорные экскурсии по историческим местам города.'
        },
        {
            title: 'Исторические Здания',
            image: 'landmark.png',
            progress: 40,
            description: 'Изучение архитектуры и истории зданий.'
        }
    ]
};

function loadAchievements(type) {
    const container = document.getElementById('achievementsContainer');
    container.innerHTML = '';

    achievements[type].forEach(achievement => {
        const card = document.createElement('div');
        card.className = 'col-lg-4 col-md-6 col-sm-12';

        card.innerHTML = `
            <div class="card achievement-card h-100 shadow-sm">
                <div class="card-body">
                    <img src="${achievement.image}" alt="${achievement.title}" class="achievement-icon mx-auto d-block my-3">
                    <h5 class="card-title">${achievement.title}</h5>
                    <div class="d-flex justify-content-center">
                        <span class="badge bg-warning text-dark mx-1">★</span>
                        <span class="badge bg-warning text-dark mx-1">★</span>
                        <span class="badge bg-warning text-dark mx-1">★</span>
                    </div>
                </div>
            </div>
        `;

        container.appendChild(card);
    });

    document.getElementById('filterContainer').style.display = 'block';
}

function filterAchievements(criteria) {
    let sortedAchievements = [];
    let type = document.getElementById('ecologyBtn').classList.contains('btn-primary') ? 'ecology' : 'landmarks';

    if (criteria === 'recent') {
        sortedAchievements = achievements[type].sort((a, b) => b.progress - a.progress);
    } else if (criteria === 'difficult') {
        sortedAchievements = achievements[type].sort((a, b) => a.progress - b.progress);
    } else if (criteria === 'oldest') {
        sortedAchievements = achievements[type];
    }

    loadFilteredAchievements(sortedAchievements);
}

function loadFilteredAchievements(achievements) {
    const container = document.getElementById('achievementsContainer');
    container.innerHTML = '';

    achievements.forEach(achievement => {
        const card = document.createElement('div');
        card.className = 'col-lg-4 col-md-6 col-sm-12';

        card.innerHTML = `
            <div class="card achievement-card h-100 shadow-sm">
                <div class="card-body">
                    <img src="${achievement.image}" alt="${achievement.title}" class="achievement-icon mx-auto d-block my-3">
                    <h5 class="card-title">${achievement.title}</h5>
                    <div class="d-flex justify-content-center">
                        <span class="badge bg-warning text-dark mx-1">★</span>
                        <span class="badge bg-warning text-dark mx-1">★</span>
                        <span class="badge bg-warning text-dark mx-1">★</span>
                    </div>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}

document.getElementById('ecologyBtn').addEventListener('click', () => {
    loadAchievements('ecology');
    document.getElementById('filterOptions').style.display = 'none';
});

document.getElementById('landmarksBtn').addEventListener('click', () => {
    loadAchievements('landmarks');
    document.getElementById('filterOptions').style.display = 'none';
});

document.getElementById('filterBtn').addEventListener('click', (event) => {
    const filterOptions = document.getElementById('filterOptions');
    filterOptions.style.display = filterOptions.style.display === 'block' ? 'none' : 'block';
});

document.getElementById('filterRecent').addEventListener('click', () => filterAchievements('recent'));
document.getElementById('filterDifficult').addEventListener('click', () => filterAchievements('difficult'));
document.getElementById('filterOldest').addEventListener('click', () => filterAchievements('oldest'));

// Load default achievements
loadAchievements('ecology');

