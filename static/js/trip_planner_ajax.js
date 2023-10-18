'use strict';

function replaceName(results) {
    document.querySelector('#trip-name-span').innerHTML = results;
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

// function replaceUsername(results) {
//     document.querySelector('#username-span').innerHTML = results;
//     alert("Username Updated");
// }

// function newUsername(evt) {

//     console.log("in the event listener")
//     evt.preventDefault();
//     const newUsername = document.querySelector('#new-username-field').value;

//     fetch(`/change-username.json?newUsername=${newUsername}`)
//         .then((response) => response.text())
//         .then(replaceUsername);

// }

// document.querySelector('#change-username-form').addEventListener('submit', newUsername);