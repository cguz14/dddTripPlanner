'use strict';

// Initialize and add the map
let map;

async function initMap() {

	// Start map near middle of US
	const position = { lat: 40, lng: -100 };

	// Request needed libraries.
	const { Map, InfoWindow } = await google.maps.importLibrary("maps");
	const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

	// The map
	map = new Map(document.getElementById("restaurants-page-map"), {
		zoom: 4,
		center: position,
		mapId: "All_Restaurants_Map",
	});

	const restaurantInfo = new InfoWindow();
	const markers = [];

	fetch('/api/restaurants')
		.then((response) => response.json())
		.then((restaurants) => {
			for (const restaurant of restaurants) {
				// Define the content of the infoWindow
				const encodedAddress = urlEncode(restaurant.restaurant_address);
				const encodedName = urlEncode(restaurant.restaurant_name);

				const restaurantInfoContent = `
				<div class="card">
					<div class="row no gutters">
						<div class="col-9">
							<div class="card-body">
								<h5 class="card-title">
									<span>Restaurant: ${restaurant.restaurant_name}</span>
								</h5>
								<div class="card-text">
									${restaurant.restaurant_description}
									<br>
									${restaurant.restaurant_address}
									<br>
									<a href="https://www.google.com/maps/search/?api=1&query=${encodedAddress}+${encodedName}">Quick Directions?</a>                
								</div>
							</div>
						</div>
						<div class="col-3">
							<img src="${restaurant.restaurant_icon}" class="restaurant-listing-img float-end rounded">
						</div>            
					</div>
				</div>
				`;

				const restaurantMarker = new AdvancedMarkerElement({
					map,
					position: {
						lat: restaurant.restaurant_latitude,
						lng: restaurant.restaurant_longitude,
					},

					title: `Restaurant: ${restaurant.restaurant_name}`,
				});

				restaurantMarker.addListener('click', () => {
					restaurantInfo.close();
					restaurantInfo.setContent(restaurantInfoContent);
					restaurantInfo.open(map, restaurantMarker);
				});

				markers.push(restaurantMarker)

			}

			new markerClusterer.MarkerClusterer({ markers, map });

		})
		.catch(() => {
			alert('We were unable to retrieve Restaurant data!!!');
		});

}

// function buildMarker(restaurant) {

// 	let restaurantImg = document.createElement("img")
// 	restaurantImg.src = `https:${restaurant.restaurant_icon}`;

// 	if (restaurant.restaurant_icon == `static/img/attachment-guys-diner-background.jpg`) {
// 		restaurantImg.src = restaurant.restaurant_icon;
// 	}

// 	const content = document.createElement("div");

// 	content.innerHTML = `
// 		<div>
// 			<img src=${restaurantImg.src} alt="Image for ${restaurant.restaurant_name}" class="all-restaurant-markers">
// 		</div>
// 	`;

// 	return content;

// }

function urlEncode(param) {

	let encoded_char;
	let param_encoded = '';

	for (const char of param) {

		if (char == "#"){
			encoded_char = "%23";            
			param_encoded += encoded_char;
		}
		else if (char == "/"){
			encoded_char = "%2F";            
			param_encoded += encoded_char;
		}
		else if (char == ' '){
			encoded_char = "%20";
			param_encoded += encoded_char;
		}
		else if (char == ","){
			encoded_char = "%2C";
			param_encoded += encoded_char;
		}
		else if (char == "."){
			encoded_char = "%2E";
			param_encoded += encoded_char;
		}
		else if (char == '"'){
			encoded_char = "%22";
			param_encoded += encoded_char;
		}
		else if (char == '&'){
			encoded_char = "and";
			param_encoded += encoded_char;
		}
		else {
			param_encoded += char;
		}
	}

	return param_encoded;
	
}

initMap();