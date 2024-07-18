

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

    document.getElementById('centerMapBtn').addEventListener('click', function () {
        myMap.setCenter([55.751574, 37.573856], 10);
    });

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

function toggleMarkers(markers, show) {
    markers.forEach(marker => {
        show ? myMap.geoObjects.add(marker) : myMap.geoObjects.remove(marker);
    });
}

function fetchParks(coords) {
    fetch(`/api/parks?location=${coords[0]},${coords[1]}`)
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
    fetch(`/api/recycling_centers?location=${coords[0]},${coords[1]}`)
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
