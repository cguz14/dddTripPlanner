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

// These functions likely to be eliminated after removal of start points selection
// function getStartPoint(index) {

//     document.getElementById("startPointDropdown").classList.toggle("show");
//     if (index >= 0) {
//         const restaurantId = document.querySelector(`#clicked-restaurant-${index}`).value;
//         console.log(`made it into start function: ${restaurantId}`)

//         fetch(`/start-point-select.json?restaurantId=${restaurantId}`)
//         .then((response) => response.text())
//         .then(setStartPoint);
//     }
// }

// function setStartPoint(startAddress) {

//     console.log(startAddress);
//     document.querySelector('#startpoint-choice').innerHTML = "<b>Startpoint:</b>" + startAddress;

// }

function getEndPoint(index) {

    document.getElementById("endPointDropdown").classList.toggle("show");
    if (index >= 0) {
        const restaurantId = document.querySelector(`#clicked-restaurant-${index}`).value;
        // const restaurantId = restaurantAddressLong.trimStart();
        console.log(`made it into end function: ${restaurantId}`)

        fetch(`/end-point-select.json?restaurantId=${restaurantId}`)
        .then((response) => response.text())
        .then(setEndPoint);
    }

}

function setEndPoint(endAddress) {

    console.log(endAddress);
    document.querySelector('#endpoint-choice').innerHTML = "<b>Endpoint:</b>" + endAddress;

}

function insertUserAddress(newUserAddress) {
    document.querySelector('#startpoint-choice').innerHTML = "<b>Startpoint:</b>" + newUserAddress;
    if (newUserAddress === "INVALID_REQUEST") {alert("Address not valid, please try again.")}
    else {alert("User Address accepted")};
}

function newUserAddress(evt) {

    evt.preventDefault();
    const newUserAddress = document.querySelector('#enter-address-field').value;

    fetch(`/new-user-address.json?newUserAddress=${newUserAddress}`)
        .then((response) => response.text())
        .then(insertUserAddress)
        .catch(() => { alert("Entered address was not found, please try again.")});

}

document.querySelector('#enter-address-form').addEventListener('submit', newUserAddress);

// pulls stops in correct order from directions information
function directionsConfirmation(param_address) {
    if (param_address == 'Please first submit "Get Directions"') {
        alert('Please first submit "Get Directions"');
    }
    else if (param_address == 'Please login') {
        alert('Please login');
    }
    else {
        window.open(`https://www.google.com/maps/dir/?api=1&${param_address}`)
        alert("Enjoy the trip to Flavortown!");
    }
}

function getOrderedDirections(evt) {

    evt.preventDefault();
    const orderedStops = document.querySelectorAll('.url-maps-directions');

    let i = 1;
    let params = "";
    while (i < orderedStops.length-1) {
        params += urlEncodeParam(orderedStops[i].innerText) + "QQQQQ";
        i ++;
    }
    params += urlEncodeParam(orderedStops[i].innerText) // Add last stop without the QQQQQ

    fetch(`/route-to-maps.json?orderedStops=${params}`)
        .then((response) => response.text())
        .then(directionsConfirmation)
        .catch(() => { alert("Ordered Directions grab error.")});

}

function urlEncodeParam(param) {

    let encodedParam = ""

    for (let char=0; char < param.length; char ++) {

        if (param[char] == "#") {
            encodedParam += "%23"            
        }
        else if (param[char] == "/") {
            encodedParam += "%2F"
        }
        else if (param[char] == ' ') {
            encodedParam += "%20"
        }
        else if (param[char] == ",") {
            encodedParam += "%2C"
        }
        else if (param[char] == ".") {
            encodedParam += "%2E"
        }
        else if (param[char] == '"') {
            encodedParam += "%22"
        }
        else {
            encodedParam += param[char]
        }
    }

    return encodedParam;
}

document.querySelector('#maps-url').addEventListener('click', getOrderedDirections);
