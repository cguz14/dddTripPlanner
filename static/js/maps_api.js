'use strict';

// let map;

// async function initMap() {
//   const { Map } = await google.maps.importLibrary("maps");

//   map = new Map(document.getElementById("edit-trip-page-map"), {
//     center: { lat: -34.397, lng: 150.644 },
//     zoom: 8,
//   });
// }

// initMap();

// Initialize and add the map
let map;

async function initMap() {
  // The location of Uluru
//   const position = { lat: -25.344, lng: 131.031 };
  const lati = document.getElementById("lat").innerHTML;
  const lngi = document.querySelector("#lng").innerHTML;
  const position = { lat: parseFloat(lati), lng: parseFloat(lngi) };
  console.log(position);
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at Uluru
  map = new Map(document.getElementById("edit-trip-page-map"), {
    zoom: 4,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

  // The marker, positioned at Uluru
  const marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    title: "Test Restaurant",
  });
}

initMap();