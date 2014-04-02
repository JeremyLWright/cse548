
var geoResults = {};
var geocoder;
var map;
var wpt1, wpt2, wpt3;
var searchResults = [];
function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(35.256, -111.644);
    var myOptions = {
        zoom: 8,
        center: latlng,
    }

    map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);
    google.maps.event.addListener(map, "rightclick", function(event) {
        var lat = event.latLng.lat();
        var lng = event.latLng.lng();
        // populate yor box/field with lat, lng
        alert("address1=" + lat +"," + lng); 

    });
}

function codeAddress(id) {
    var address = document.getElementById(id).value;
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            map.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
            searchResults[id] = results[0].geometry.location;
        } else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });
}
function setboundary(id,id) {
    //set boundary           
}
function view(id) {
    //pull specific tractor infor from database          
}
function Terminate(id) {
    //delete tractor information from database          
}
function process(id) {
    //upload job to the database          
}
function launch(id) {
    //initiate tractor ro process the job          
}

function drawLine() {
    var points = [searchResults.wpt1, searchResults.wpt2, searchResults.wpt3];
    var polyline = new google.maps.Polyline({
        path: points,
        strokeColor: '#ff0000',
        strokeWeight: 5,
        strokeOpacity: 0.7,
        map: map
    });
}

function clearDiv1() {
    document.getElementById("wpt1").value = "";
}

function clearDiv2() {
    document.getElementById("wpt22").value = "";
}
function clearDiv3() {
    document.getElementById("wpt3").value = "";
}

$(document).ready(function()
        {
            initialize();
            $.ajax({
                url: "/api/v1/tractor/?format=json",
                cache: false
            })
            .done(function(obj) {
                var mSelect = $('#tractor-selector');
                $.each(obj.objects, function(val, text) {
                    console.log(text);
              mSelect.append($('<option></option>').val(text.id).html(text.name));
                });
            console.log(obj)
            });
        });
