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
  map = new Map(document.getElementById("restaurants-page-map"), {
    zoom: 4,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

    const restaurantInfo = new google.maps.InfoWindow();

    fetch('/api/restaurants')
    .then((response) => response.json())
    .then((restaurants) => {
    for (const restaurant of restaurants) {
        // Define the content of the infoWindow
        const restaurantInfoContent = `
        <div>
        <ul class="restaurant-info">
            <li><b>Restaurant Name: </b>${restaurant.restaurant_name}</li>
            <li><b>Restaurant Address: </b>${restaurant.restaurant_address}</li>
        </ul>
        </div>
    `;

        let img = `https:${restaurant.restaurant_icon}`;

        if (restaurant.restaurant_icon == `static/img/attachment-guys-diner-background.jpg`) {
            img = restaurant.restaurant_icon;
        }

        const restaurantMarker = new google.maps.Marker({
        position: {
            lat: restaurant.restaurant_latitude,
            lng: restaurant.restaurant_longitude,
        },
        title: `Restaurant: ${restaurant.restaurant_name}`,

        icon: {
            url: img,
            scaledSize: new google.maps.Size(80, 80),
        },
        map, // same as saying map: map
        });

        restaurantMarker.addListener('click', () => {
        restaurantInfo.close();
        restaurantInfo.setContent(restaurantInfoContent);
        restaurantInfo.open(map, restaurantMarker);
        });
    }
    })
    .catch(() => {
    alert(`
    We were unable to retrieve Restaurant data!!!
    `);
    });

}

initMap();