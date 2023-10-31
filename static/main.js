
const utilityToAssets = {
Electrical:["Pedestal", "Control Box", "Manhole", "Pole", "Transformer", "Electric Meter", "Flag Line"],
Sanitary: ["Manhole", "Cleanouts","Flag Lines"],
Stormwater: ["Manhole", "Storm Traps/Outfalls","Flag Lines"],
Telecom: ["Pedestal", "Control Box", "Manhole", "Flag Line"],
Water: [ "Fire Hydrant","Valve Cover","Water Meter", "Flag Line"],
Gas: ["Valve Cover", "Gas Meter", "Flag Line"]
};

const itemList = document.querySelector('.navMenu');

const waterAsset = utilityToAssets.Water;

const waterRulePair = {
  1: ["Valve Cover", "Valve Cover"],
  2: ["Valve Cover", "Fire Hydrant"],
  3: ["Fire Hydrant", "Fire Hydrant"],
};
const sanitaryRulePair = {
  1: ["Manhole", "Manhole"],
  2: ["Manhole", "Cleanouts"]
};
const stormWaterRulePair = {
  1: ["Manhole", "Manhole"],
  2: ["Manhole", "Storm Traps/Outfalls"],
  3: ["lake", "Manhole"],
};

//key DATA
let ruleObject = {
  "Water": waterRulePair,
  "Sanitary": sanitaryRulePair,
  "Stormwater": stormWaterRulePair,
}

localStorage.setItem('DATA', JSON.stringify(ruleObject));
let DATA = JSON.parse(localStorage.getItem('DATA'));

function helperFunction(utility){

  const defauleRule = document.getElementById('defaultRule');
  defauleRule.innerHTML = `Default Rule for ${utility}`;
  defauleRule.className = `ruleTable${utility}`;

  let table = document.createElement('table');
  table.className = `table${utility}`;

  let edit = document.createElement('button');
  edit.innerHTML = "Edit";

  let DATA = JSON.parse(localStorage.getItem('DATA'));

  const tableBody = document.createElement('tbody');
  tableBody.className = `tableBody${utility}`;

  tableBody.addEventListener('click', (event) => {
    if (event.target.classList.contains('btn-delete')) {
        // Find the parent row of the clicked button
        const row = event.target.closest('tr');
        if (row) {
            // Remove the row from the table
            tableBody.removeChild(row);
            let delValue = row.querySelector('td').innerHTML;
            delete DATA[utility][delValue];
            localStorage.setItem('DATA', JSON.stringify(DATA));
        }
    }});

  const addItems = document.getElementById('addRule');
  addItems.addEventListener('click', function(){
    let asset1 = document.getElementById('ruleAssets1').value;
    let asset2 = document.getElementById('ruleAssets2').value;
    let ruleRank = document.getElementById('rank').value;
    DATA[utility][ruleRank] = [asset1, asset2];
    localStorage.setItem('DATA', JSON.stringify(DATA));
    helperFunction(utility);
  }
    );

  for ( let key in DATA[utility]){
    let deleteRule = document.createElement('button');
    deleteRule.innerHTML = "Delete";
    deleteRule.classList.add('btn-delete');
    let row = tableBody.insertRow();
    let cell1 = row.insertCell(0);
    let cell2 = row.insertCell(1);
    let cell3 = row.insertCell(2);
    let cell4 = row.insertCell(3);

    cell1.innerHTML = key;
    cell2.innerHTML = DATA[utility][key][0];
    cell3.innerHTML = DATA[utility][key][1];
    // cell4.appendChild(edit);
    cell4.appendChild(deleteRule);
  }
  table.appendChild(tableBody);
  let header = table.createTHead().insertRow();
  let header1 = header.insertCell(0);
  let header2 = header.insertCell(1);
  let header3 = header.insertCell(2);
  let header4 = header.insertCell(3);
  header1.innerHTML = "Rule Rank";
  header2.innerHTML = "Asset 1";
  header3.innerHTML = "Asset 2";
  header4.innerHTML = "Action";
  defauleRule.appendChild(table);
}


function insertDefaultRule(){
  itemList.addEventListener('click', function(event){
    let clickedValue = event.target.innerHTML;
        helperFunction(clickedValue);
})
};
// function insertDefaultRule()
insertDefaultRule();



const utilityCategory = document.getElementById('utility');
const assetsDropdown  = document.getElementById('assets');


//asset class and utility drop down
function populateSubcategory(value){
  if (!value){
    value = utilityCategory.value;
    // console.log(value);
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
const utility = utilityCategory.value;
populateSubcategory(utility);
//asset class and utility drop down


//utilty rule section
const utilityRule = document.querySelectorAll("nav li");
const ruleAssetDrop = document.querySelectorAll('.ruleAssets')

function populateAssetRUle(){
      // console.log(utilityRule)
      document.addEventListener("DOMContentLoaded", function() {

      utilityRule.forEach(function(item) {
        item.addEventListener("click", function(event) {
          // Get the data-value attribute of the clicked item
          const value = event.currentTarget.getAttribute("data-value");
          const subcategory = utilityToAssets[value];

          ruleAssetDrop.forEach(optionA => optionA.innerHTML = "");

          subcategory.forEach(values => {
              const option = document.createElement('option');
              option.textContent = values;
              ruleAssetDrop.forEach(optionS =>optionS.appendChild(option.cloneNode(true)));
          })
        });
      });
    });
}
populateAssetRUle();
//utilty rule section


//google map section
let map;
let markers = [];
let geocoder;
function initMap() {
  const Ames = { lat: 42.0308, lng: -93.6319};
  map = new google.maps.Map(document.getElementById("mapBck"), {
    zoom: 15,
    center: Ames,
    mapTypeId: "terrain",
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

  document
    .getElementById("delete-single-markers")
    .addEventListener("click", removeClick);
  // Adds a marker at the center of the map.
  addMarker(Ames);
  initAutocomplete();
}


 // Create the search box and link it to the UI element.
function initAutocomplete() {
  const input = document.getElementById("search-input");
  const searchBox = new google.maps.places.SearchBox(input);

  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(input);
  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });
  let markersz = [];

  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();
    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markersz.forEach((marker) => {
      marker.setMap(null);
    });
    markersz = [];

    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();

    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }

      const icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25),
      };

      // Create a marker for each place.
      markersz.push(
        new google.maps.Marker({
          map,
          icon,
          title: place.name,
          position: place.geometry.location,
        }),
      );
      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
}


// Adds a marker to the map and push to the array.
function addMarker(position) {
  const marker = new google.maps.Marker({
    position,
    map,
    draggable: true,
    click:false,
    title: utilityCategory.value + ":" + assetsDropdown.value
    // Animation: google.maps.Animation.DROP,
  });
  const infoWindow = new google.maps.InfoWindow({
    content: `'<div><strong>' ${marker.title} '</strong></div>'`
  });

  marker.addListener('click', () => {
    if (marker.click === false){
      infoWindow.open(map, marker);
      marker.click = true;

  } else {
      infoWindow.close();
      marker.click  = false;
  }
  });


  markers.push(marker);
}


// Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}
function removeClick() {
  for (let i = 0; i < markers.length; i++) {
    if (markers[i].click === true){
      markers[i].setMap(null);
      markers.splice(i, 1);
    }
  }
  console.log(markers);
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




