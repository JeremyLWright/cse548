
var geoResults = {};
var geocoder;
var map;
var wpt1, wpt2, wpt3;
var searchResults = [];
function on_emergency_stop(e)
{
        var runningJob = {"active": false};
        srunningJob  = JSON.stringify(runningJob);
        $.ajax({
            type: 'PUT',
            url: '/api/v1/runningjob/1/',
            data: srunningJob,
            contentType: "application/json"
        }).done(function(obj, textStatus, request){
            console.log("Done.");
        });
    
}

function on_select_job(e)
{
    var jobId = $('#inputJobName').val();
    //Delete all jobs on the active list.
    $.ajax({
        url: "/api/v1/runningjob/",
        cache: false,
        async: false,
    }).done(function(obj) {
        $.each(obj.objects, function(val, text){
            $.ajax({
                url: text.resource_uri,
                cache: false,
                async: false,
                type: 'DELETE'
            });
        });
    });


    //Move this job to the running table.
    $.ajax({
        url: "/api/v1/job/?id__exact="+jobId+"&format=json",
        cache: false,
        async: false
    }).done(function(obj) {
        var runningJob = {"active": true, "job": "/api/v1/job/"+jobId+"/", "tractor": "/api/v1/tractor/1/"};
        srunningJob  = JSON.stringify(runningJob);

        $.ajax({
            type: 'POST',
            url: '/api/v1/runningjob/',
            data: srunningJob,
            contentType: "application/json"
        }).done(function(obj, textStatus, request){
            console.log("Done.");
        });
    });

    //Select the waypoints for the job (job__exact=1&)
    $.ajax({
        url: "/api/v1/waypoint/?job__exact="+jobId+"&format=json",
        cache: false
    }).done(function(obj) {
        console.log(obj);
        var c = obj.objects[0];
        var center_point = new google.maps.LatLng(c.lat, c.longitude);
        map.setCenter(center_point);
        $.each(obj.objects, function(id, element){
            drop_waypoint(element.lat, element.longitude);
        });


        var lastIdFetched = 0;
        //Setup the periodic call for completed waypoints
        (function worker() {
            $.ajax({
                url: "/api/v1/completedpoint/?active_job__exact=1&limit=0&id__gt="+lastIdFetched+"&format=json&limit=0",
                success: function(data) {
                    $.each(data.objects, function(id, element){
                       drop_marker(element.lat, element.longitude);
                       lastIdFetched = element.id
                    });
                },
                complete: function() {
                    // Schedule the next request when the current one's complete
                    setTimeout(worker, 5000);
                }
            });
        })();

    });

}

function initialize_map()
{
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(33.423687, -111.939271);
    var myOptions = {
        zoom: 14,
        center: latlng,
    };
    map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);
    document.getElementById('map-canvas').style.display="block";
}
function initialize_farm_view(){
    initialize_map();
    $.ajax({
        url: "/api/v1/job/?format=json&limit=0",
        cache: false
    })
    .done(function(obj) {
        var mSelect = $('#inputJobName');
        $.each(obj.objects, function(val, text) {
            console.log(text);
            mSelect.append($('<option></option>').val(text.id).html(text.name));
        });
    });

    $('#inputJobName').click(on_select_job);
    $('#btnStopJob').click(on_emergency_stop);
}

function initialize_create_job() {

    initialize_map();
    google.maps.event.addListener(map, "click", function(event) {
        var lat = event.latLng.lat();
        var lng = event.latLng.lng();


        drop_waypoint(lat, lng);
        var job = $("body").data("currentJob");
        var sortOrder =   $("body").data('waypointSortCount');
        $("body").data('waypointSortCount', sortOrder+1);
        // populate yor box/field with lat, lng
        console.log("Adding waypoint to job: "+job+" with index "+sortOrder);
        var waypoint = {};
        waypoint["lat"] = lat;
        waypoint["longitude"] = lng;
        waypoint["sort_order"] = sortOrder;
        waypoint["job"] = job;

        swaypoint = JSON.stringify(waypoint);
        $.ajax({
            type: 'POST',
            url: '/api/v1/waypoint/',
            data: swaypoint,
            contentType: "application/json"
        }).done(function(obj, textStatus, request){
            console.log("Done.");
        });


    });
    $('#btnSaveJobName').click(saveJobName);

}

function drop_marker(lat, lng)
{
    //    var latlng = new google.maps.LatLng(35.256, -111.644);
    var latlng = new google.maps.LatLng(lat, lng);

    var marker = new google.maps.Marker({
        map: map,
        position: latlng,
         icon: 'https://chart.googleapis.com/chart?chst=d_map_spin&chld=0.25%7C0%7CFF0000%7C000000'
    });

}

function drop_waypoint(lat, lng)
{
    var latlng = new google.maps.LatLng(lat, lng);

    var marker = new google.maps.Marker({
        map: map,
        position: latlng,
        icon: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
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

function fetch_points(id) {
    //http://localhost:8000/api/v1/completedpoint/?id__gte=5&format=json
    $.ajax({
        url: '/api/v1/completedpoint/?id__gte='+id,
    type: 'GET',
    cache:false
    }).done(function(obj){
        $.each(obj.objects, function(val, text) {
                    drop_marker(text["lat"], text["longitude"]);
                });

    });
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

function saveJobName(e) {
    var job = {};
    job["name"] = $('#inputJobName').val();
    job["boundary"] = '/api/v1/workingboundary/1/'; //Arizona boundary
    job["user"] = '/api/v1/user/1/';

    sjob = JSON.stringify(job);
    $.ajax({
        type: 'POST',
        url: '/api/v1/job/',
        data: sjob,
        contentType: "application/json"
    }).done(function(obj, textStatus, request){
        console.log("Done.");
        console.log(request.getResponseHeader('Location').replace(/https?:\/\/[^\/]+/i, ""));
        $("body").data('currentJob', request.getResponseHeader('Location').replace(/https?:\/\/[^\/]+/i, ""));
        $("body").data('waypointSortCount', 0);
    });
}

// sending a csrftoken with every ajax request
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function()
        {
            $.ajaxSetup({
                crossDomain: false, // obviates need for sameOrigin test
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                }
            }
            });
        });
