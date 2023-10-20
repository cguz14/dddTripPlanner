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
  // causes issue if there is no value to grab. Need to ensure there are protections for empty trips
  const lati = document.getElementById("lat").innerHTML;
//   used different selector for sake of testing if they did same thing
  const lngi = document.querySelector("#lng").innerHTML;

  
  const position = { lat: parseFloat(lati), lng: parseFloat(lngi) };


  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map
  map = new Map(document.getElementById("edit-trip-page-map"), {
    zoom: 5,
    center: position,
    mapId: "DEMO_MAP_ID",
  });

  // The marker
  const marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    title: "Test Restaurant",
  });
}

initMap();