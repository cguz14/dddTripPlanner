'use strict';

// Initialize and add the map
let map;

async function initMap() {
  
  // Start map near middle of US
  const position = { lat: 40, lng: -100 };

  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map
  map = new Map(document.getElementById("edit-trip-page-map"), {
    zoom: 4,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

    const stopInfo = new google.maps.InfoWindow();

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

        const stopMarker = new google.maps.Marker({
        position: {
            lat: stop.restaurant_latitude,
            lng: stop.restaurant_longitude,
        },
        title: `Restaurant: ${stop.restaurant_name}`,
        icon: {
            url: 'static/img/attachment-guys-diner-background.jpg',
            scaledSize: new google.maps.Size(50, 50),
        },
        map, // same as saying map: map
        });

        stopMarker.addListener('click', () => {
        stopInfo.close();
        stopInfo.setContent(stopInfoContent);
        stopInfo.open(map, stopMarker);
        });
    }
    })
    .catch(() => {
    alert(`
    We were unable to retrieve Stop data!!!
    `);
    });

}

initMap();