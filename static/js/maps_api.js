
'use strict';

// Initialize and add the map
let map;

async function initMap() {
  
    // Start map near middle of US
    const position = { lat: 40, lng: -100 };

    // Request needed libraries.
    //@ts-ignore

    const { Map, InfoWindow } = await google.maps.importLibrary("maps");
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    const { DirectionsService, DirectionsRenderer } = await google.maps.importLibrary("routes")

    const directionsService = new DirectionsService();
    const directionsRenderer = new DirectionsRenderer();

    // The map
    map = new Map(document.getElementById("edit-trip-page-map"), {
        zoom: 4,
        center: position,
        mapId: "DEMO_MAP_ID",
    });

    directionsRenderer.setMap(map);

    const stopInfo = new InfoWindow();
    const markers = [];
    
    fetch('/api/stops')
    .then((response) => response.json())
    .then((stops) => {
    for (const stop of stops) {
        // Define the content of the infoWindow
        const stopInfoContent = `
        <div>
        <ul class="stop-info">
            <li><b>Restaurant Name: </b>${stop.restaurant_name}</li>
            <li><b>Restaurant Address: </b>${stop.restaurant_address}</li>
        </ul>
        </div>
        `;

        const stopMarker = new AdvancedMarkerElement({
        map,
        position: {
            lat: stop.restaurant_latitude,
            lng: stop.restaurant_longitude,
        },
        content: buildMarker(stop),
        title: `Restaurant: ${stop.restaurant_name}`,
        });

        markers.push(stopMarker)
        stopMarker.addListener('click', () => {
        stopInfo.close();
        stopInfo.setContent(stopInfoContent);
        stopInfo.open(map, stopMarker);
        });
    }
    })
    .catch(() => {
    alert(`
    Error while retrieving/displaying Stop map data.
    `);
    });

    document.querySelector('#get-directions').addEventListener("click", () => {
        calculateAndDisplayTrip(directionsService, directionsRenderer);
        alert('Calculating Directions...');
    });

    // console.log(markers) Maybe the Advanced Marker is needed to cluster?
    // const markerCluster = new markerClusterer.MarkerClusterer({ markers, map });
    // May not work with custom markers?

}

function buildMarker(stop) {
    
    let restaurantImg = document.createElement("img")
    restaurantImg.src = `https:${stop.restaurant_icon}`;

    if (stop.restaurant_icon == `static/img/attachment-guys-diner-background.jpg`) {
        restaurantImg.src = stop.restaurant_icon;
    }

    const content = document.createElement("div");

    content.innerHTML = `
    <div>
        <img src=${restaurantImg.src} alt="Image for ${stop.restaurant_name}" class="restaurant-markers">
    </div>
    `;
  
    return content;

}

async function calculateAndDisplayTrip(directionsService, directionsRenderer) {

    const directionsWaypoints = [];
    let originWaypoint;
    let destinationWaypoint;
    let i = 0;

    // Get some time to ask about this and async functions to understand better why this
    //      didn't work at first as a regular fetch. Standard fetch had delay in data
    //      being available but async and await allowed variables to come available
    let response = await fetch('/api/direction-stops');
    let stops = await response.json();

    if (stops.length == 0) {
        alert('Please select a startpoint and endpoint.');
        return
    };

    for (const stop of stops) {
        if (i == 0) {
            originWaypoint = `${stop.restaurant_address}`;
            console.log('in this if')
            console.log(originWaypoint)
        }
        else if (i == stops.length-1) {
            destinationWaypoint = `${stop.restaurant_address}`;
        }
        else {
            directionsWaypoints.push({
                location: `${stop.restaurant_address}`,
                stopover: true,
            });
        };
        
        i ++;
    };

    console.log(originWaypoint);
    console.log(directionsWaypoints);
    console.log(destinationWaypoint);

    directionsService
        .route({
            origin: `${originWaypoint}`,
            destination: `${destinationWaypoint}`,
            waypoints: directionsWaypoints,
            optimizeWaypoints: true,
            travelMode: google.maps.TravelMode.DRIVING,
        })
        .then ((response) => {
            directionsRenderer.setDirections(response);

            const route = response.routes[0];
            const directionsPanel = document.querySelector('#directions-panel');

            directionsPanel.innerHTML = "";

            // Display directions for each route
            for (let i = 0; i < route.legs.length; i ++) {

                const routeSegment = i + 1;

                directionsPanel.innerHTML += "<b>Route Segment: " + routeSegment + "</b><br>";
                directionsPanel.innerHTML += `<span id="stop${i}" class="url-maps-directions">` + route.legs[i].start_address + "</span> to ";
                directionsPanel.innerHTML += route.legs[i].end_address + "<br>";
                directionsPanel.innerHTML += route.legs[i].distance.text + "<br><br>";

            }
        })
        .catch(() => alert("Directions request failed, you trying to drive overseas or something wild?!"));

}

initMap();