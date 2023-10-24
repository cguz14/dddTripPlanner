
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
    const markers=[];
    
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

        let img = `https:${stop.restaurant_icon}`;

        if (stop.restaurant_icon == `static/img/attachment-guys-diner-background.jpg`) {
            img = stop.restaurant_icon;
        }

        const stopMarker = new google.maps.Marker({
        position: {
            lat: stop.restaurant_latitude,
            lng: stop.restaurant_longitude,
        },
        title: `Restaurant: ${stop.restaurant_name}`,
        icon: {
            url: img,
            scaledSize: new google.maps.Size(60, 60),
        },
        map, // same as saying map: map
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
    We were unable to retrieve Stop data!!!
    `);
    });

    // console.log(markers) Maybe the Advanced Marker is needed to cluster?
    // const markerCluster = new markerClusterer.MarkerClusterer({ markers, map });
    // console.log(markerCluster)

}

initMap();