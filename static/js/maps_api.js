'use strict';

let map;

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("edit-trip-page-map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });
}

initMap();