
function validate(){
    const weight1 = parseFloat(document.getElementById("weight_1").value);
    const weight2 = parseFloat(document.getElementById("weight_2").value);
    const sum = weight1  + weight2;
    if (Math.abs(sum - 1) < 0.0001) {
    return true;
    } else {
    alert("The values must add up to 1.");
    return false
    }};

const utilityToAssets = {
Electrical:["Pedestal", "Control Box", "Manhole", "Pole", "Transformer", "Electric Meter", "Flag Line"],
Sanitary: ["Manhole", "Cleanouts","Flag Lines"],
Stormwater: ["Manhole", "Storm Traps/Outfalls","Flag Lines"],
Telecom: ["Pedestal", "Control Box", "Manhole", "Flag Line"],
Water: ["Manhole", "Fire Hydrant","Valve Cover","Water Meter", "Flag Line"],
Gas: ["Valve Cover", "Gas Meter", "Flag Line"]
};

const utilityCategory = document.getElementById('utility');
const assetsDropdown  = document.getElementById('assets');

function populateSubcategory(value){
  if (!value){
    value = utilityCategory.value;
    console.log(value);
  }
      const subcategory = utilityToAssets[value];

      assetsDropdown.innerHTML = "";
      subcategory.forEach(values => {
          const option = document.createElement('option');
          option.textContent = values;
          assetsDropdown.appendChild(option);
      })
      };

utilityCategory.addEventListener('change',() =>
{
populateSubcategory();
});
  // assetsDropdown.addEventListener('change',() =>
  // {
  // let selectedAsset = assetsDropdown.value;
  // });

const utility = utilityCategory.value;
populateSubcategory(utility);


let map;
let markers = [];
let geocoder;


function initMap() {
  const haightAshbury = { lat: 42.0308, lng: -93.6319};

  map = new google.maps.Map(document.getElementById("mapBck"), {
    zoom: 15,
    center: haightAshbury,
    mapTypeId: "terrain",
  });


  geocoder = new google.maps.Geocoder();
  document.getElementById('search-button').addEventListener('click', function() {
    searchLocation();
    });

  // This event listener will call addMarker() when the map is clicked.
  map.addListener("click", (event) => {
    addMarker(event.latLng);
  });
  // add event listeners for the buttons
  document
    .getElementById("show-markers")
    .addEventListener("click", showMarkers);
  document
    .getElementById("hide-markers")
    .addEventListener("click", hideMarkers);
  document
    .getElementById("delete-markers")
    .addEventListener("click", deleteMarkers);
  // Adds a marker at the center of the map.
  addMarker(haightAshbury);
}

// Adds a marker to the map and push to the array.
function addMarker(position) {
  const marker = new google.maps.Marker({
    position,
    map,
    draggable: true,
    title: utilityCategory.value + ":" + assetsDropdown.value,
    Animation: google.maps.Animation.DROP,
  });
  const infoWindow = new google.maps.InfoWindow({
    content: `'<div><strong>' + ${marker.title} + '</strong></div>'`
  });

  marker.addListener('click', () => {
      infoWindow.open(map, marker);
  });

  markers.push(marker);
}


function searchLocation() {
  const searchInput = document.getElementById('search-input').value;
  geocoder.geocode({ 'address': searchInput }, function(results, status) {
      if (status === 'OK' && results[0].geometry) {
          const location = results[0].geometry.location;
          map.setCenter(location);
          new google.maps.Marker({
              map: map,
              position: location
          });
      } else {
          alert('Location not found');
      }
  });
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function hideMarkers() {
  setMapOnAll(null);
}

// Shows any markers currently in the array.
function showMarkers() {
  setMapOnAll(map);


}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  hideMarkers();
  markers = [];
}


window.initMap = initMap;
// dragMap();
console.log(markers)


// async function dragMap() {
//   // Request needed libraries.
//   const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
//   markers.forEach(markerInfo => {
//     const marker = new AdvancedMarkerElement({
//         position: markerInfo.position,
//         map: map,
//         gmpDraggable: true,
//         title: markerInfo.name
//         // You can add more customization options here, like custom icons or info windows
//     })
//     const infoWindow = new google.maps.InfoWindow();

//     marker.addListener("dragend", (event) => {
//     const position = marker.position;
//     infoWindow.setContent(
//       `Pin dropped at: ${position.lat()}, ${position.lng()}`,
//     );
//     infoWindow.open(marker.map, marker);
//   });
//   });

// }


