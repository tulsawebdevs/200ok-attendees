"use strict";

angular.module('_200OK', ['_200OK.controllers']);

angular.module('_200OK.controllers',[])
    .controller('attendees', function($scope,$http) {
        if (!$scope.attendees){
            $scope.run_animation=false;
            $scope.unique_properties={};
            $scope.venue_latlng =[36.158619,-95.99220514297485]
            
            $scope.map=L.mapbox.map('map_content', 'jdungan.map-rb58pj4k').setView($scope.venue_latlng,16);
                            
            $scope.attendee_markers = L.mapbox.markerLayer().addTo($scope.map);
            $scope.attendee_markers.on('layeradd', function(e) {
                 var marker = e.layer,
                     feature = marker.feature,
                     popupContent =  '';

                 for (var p in marker.feature.properties){
                     if (!$scope.unique_properties[p]){
                         $scope.unique_properties[p]={name:p};
                     } 
                     popupContent +='<p>'+p+':'+marker.feature.properties[p]+'</p>'
                 }

                 marker.setIcon(L.mapbox.marker.icon({
                     'marker-size' : 'medium',
                     'marker-color' : '#f44',
                     'marker-symbol' : 'rocket'
                 }));
                 
                 marker.bindPopup(popupContent,{closeButton: false,});
                 
                 
             });

            $scope.attendee_markers.loadURL('./attendees.json');
                      
        }

        $scope.show_venue = function(){
            $scope.map.setView($scope.venue_latlng, 18, {pan: {animate: true}}); 
        };
        $scope.show_all = function(){
            $scope.map.fitBounds($scope.attendee_markers.getBounds(),{padding:[75,75]})
        };
        $scope.slide_show = function($event){
            var markers = [];
            $scope.run_animation = ! $scope.run_animation;
            $($event.target).text ($scope.run_animation && "Stop"||'Start')
            function cycle(markers) {
                var i = 0;
                function run() {
                    if (++i > markers.length - 1) i = 0;
                    var mk_latlng=markers[i].getLatLng();                    
                    $scope.map.setView(mk_latlng, 12, {pan: {animate: true}}); 
                    markers[i].openPopup();
                    if ($scope.run_animation){
                        window.setTimeout(run, 3000);
                    }
                }
                run();
            }
            if ($scope.run_animation){
                $scope.attendee_markers.eachLayer(function(marker) {
                    markers.push(marker); 
                });
                cycle(markers);
            }

        };
        $scope.property_selected = function(){
            if ($scope.filter_property){
                $scope.attendee_markers.setFilter(function(marker){
                    return marker.properties.hasOwnProperty($scope.filter_property.name)
                }); 
            } else {
                $scope.attendee_markers.setFilter(function(marker){return true;});                
            }
        };

    });    



