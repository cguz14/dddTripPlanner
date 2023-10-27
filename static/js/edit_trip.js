'use strict';

function replaceName(results) {
    document.querySelector('#trip-name-span').innerHTML = results;
    document.querySelector('#trip-map-span').innerHTML = results;
    alert("Trip Name Updated");
}

function newName(evt) {

    evt.preventDefault();
    const newTripName = document.querySelector('#new-trip-name-field').value;

    fetch(`/change-trip-name.json?newTripName=${newTripName}`)
        .then((response) => response.text())
        .then(replaceName);

}

document.querySelector('#change-trip-name-form').addEventListener('submit', newName);

function replaceDescription(results) {
    document.querySelector('#trip-description-span').innerHTML = results;
    alert("Trip Description Updated");
}

function newDescription(evt) {

    evt.preventDefault();
    const newTripDescription = document.querySelector('#new-trip-description-field').value;

    fetch(`/change-trip-description.json?newTripDescription=${newTripDescription}`)
        .then((response) => response.text())
        .then(replaceDescription);

}

document.querySelector('#change-trip-description-form').addEventListener('submit', newDescription);

function getStartPoint(index) {

    document.getElementById("startPointDropdown").classList.toggle("show");
    if (index >= 0) {
        const restaurantAddress = document.querySelector(`#clicked-restaurant-${index}`).value;
        console.log(`made it into start function: ${restaurantAddress}`)

        fetch(`/start-point-select.json?restaurantAddress=${restaurantAddress}`)
        .then((response) => response.text())
        .then(response);
    }
}

function getEndPoint() {

    document.getElementById("endPointDropdown").classList.toggle("show");
    console.log('made it into end function')

}