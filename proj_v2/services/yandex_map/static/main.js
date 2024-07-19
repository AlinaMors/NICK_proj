

let myMap;
let taskMarkers = [];
let attractionMarkers = [];
let parkMarkers = [];

function init() {
    myMap = new ymaps.Map("map", {
        center: [55.751574, 37.573856],
        zoom: 10,
        controls: ['zoomControl', 'searchControl', 'typeSelector', 'fullscreenControl', 'routeButtonControl']
    });

    console.log("Map initialized");

    myMap.events.add('click', function (e) {
        let coords = e.get('coords');
        fetchParks(coords);
        fetchRecyclingCenters(coords);
    });

    // document.getElementById('centerMapBtn').addEventListener('click', function () {
    //     myMap.setCenter([55.751574, 37.573856], 10);
    // });
    getLocation()

    document.getElementById('searchPlaceBtn').addEventListener('click', function () {
        let searchControl = myMap.controls.get('searchControl');
        searchControl.search(searchControl.getRequestString());
    });

    document.getElementById('filterTasks').addEventListener('change', function () {
        toggleMarkers(taskMarkers, this.checked);
    });

    document.getElementById('filterAttractions').addEventListener('change', function () {
        toggleMarkers(attractionMarkers, this.checked);
    });

    document.getElementById('filterParks').addEventListener('change', function () {
        toggleMarkers(parkMarkers, this.checked);
    });
}


function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(applyPosition, showError);
    } else {
    }
}

function applyPosition(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    myMap.setCenter([latitude, longitude ], 10);
    fetchParks([latitude, longitude]);
    fetchRecyclingCenters([latitude, longitude]);
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            document.getElementById("location").innerHTML = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            document.getElementById("location").innerHTML = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            document.getElementById("location").innerHTML = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            document.getElementById("location").innerHTML = "An unknown error occurred.";
            break;
    }
}


function toggleMarkers(markers, show) {
    markers.forEach(marker => {
        show ? myMap.geoObjects.add(marker) : myMap.geoObjects.remove(marker);
    });
}

function fetchParks(coords) {
    fetch(`/ya_map/api/parks?location=${coords[0]},${coords[1]}`)
        .then(response => response.json())
        .then(data => {
            data.response.GeoObjectCollection.featureMember.forEach(function (place) {
                let point = place.GeoObject.Point.pos.split(' ');
                let coords = [parseFloat(point[1]), parseFloat(point[0])];
                let marker = new ymaps.Placemark(coords, {
                    hintContent: place.GeoObject.name,
                });
                parkMarkers.push(marker);
                myMap.geoObjects.add(marker);
            });
        });
}

function fetchRecyclingCenters(coords) {
    fetch(`/ya_map/api/recycling_centers?location=${coords[0]},${coords[1]}`)
        .then(response => response.json())
        .then(data => {
            data.response.GeoObjectCollection.featureMember.forEach(function (place) {
                let point = place.GeoObject.Point.pos.split(' ');
                let coords = [parseFloat(point[1]), parseFloat(point[0])];
                let marker = new ymaps.Placemark(coords, {
                    hintContent: place.GeoObject.name,
                });
                parkMarkers.push(marker);
                myMap.geoObjects.add(marker);
            });
        });
}

function showTasks() {
    alert('Showing tasks');
}

function showEnvironmental() {
    alert('Showing environmental tasks');
}

function showCare() {
    alert('Showing care tasks');
}

function showParks() {
    alert('Showing parks');
}

ymaps.ready(init);
console.log("Yandex Maps API is ready");
