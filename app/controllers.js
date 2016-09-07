/* 
 LIRC Web Admin - a web admin for LIRC administration 

 You may use any Web Server Admin project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2016 Emilio Mariscal (emi420 [at] gmail.com)
 
 */

 (function() {

var SETTINGS = {
	host: "http://192.168.10.105:8001"
}

angular.module('app.controllers', [])

    .controller('IndexCtrl', function($scope, $http, $timeout) {

      var statusTextareaElement = document.getElementById("statusTextarea");
      var updateTextareaScroll = function() {
        $timeout(function() {
          statusTextareaElement.scrollTop = statusTextareaElement.scrollHeight;        
        }, 10);
      }

      $scope.getStatus = false;

      $scope.IRRecord = {
        status: "",

        launch: function() {
          $http.get(SETTINGS.host + '/ws/irrecord/').then(function(r) {
            $scope.IRRecord.status = r.data;
            $scope.getStatus = true;
            $scope.IRRecord.getStatus();
          }, function(r) {
            $scope.IRRecord.status = "Error.";
          });                      
        },

        getNamespace: function() {
          $http.get(SETTINGS.host + '/ws/irrecord/get-namespace/').then(function(r) {
            $scope.namespace = r.data.split("\n");
          }, function(r) {
            $scope.IRRecord.status = "Error.";
          });                      
        },

        mode2: function() {
          $http.get(SETTINGS.host + '/ws/irrecord/mode2/').then(function(r) {
            $scope.IRRecord.status = r.data;
            $scope.getStatus = true;
            $scope.IRRecord.getStatus();
          }, function(r) {
            $scope.IRRecord.status = "Error.";
          });                      
        },

        enter: function() {
          $http.get(SETTINGS.host + '/ws/irrecord/enter/').then(function(r) {
            $scope.IRRecord.status = $scope.IRRecord.status + r.data;
          }, function(r) {
            $scope.IRRecord.status = "Error.";
          });                      
        },


        stop: function() {
          $scope.getStatus = false;
          $http.get(SETTINGS.host + '/ws/irrecord/kill/').then(function(r) {
            
          }, function(r) {
            $scope.IRRecord.status = "Error.";
          });                      
        },

        sendNamespace: function() {
          $http.get(SETTINGS.host + '/ws/irrecord/' + $scope.selectedNamespace + '/send/' ).then(function(r) {
            $scope.IRRecord.status = $scope.IRRecord.status + r.data;
          }, function(r) {
            $scope.IRRecord.status = "Error.";
          });                      
        },

        getLastConfig: function() {
          $http.get(SETTINGS.host + '/ws/irrecord/get-last-config/' ).then(function(r) {
            $scope.IRRecord.status = r.data;
          }, function(r) {
            $scope.IRRecord.status = "Error.";
          });                      
        },

        getStatus: function() {
            $http.get(SETTINGS.host + '/ws/irrecord/status/').then(function(r) {
              if (r.data) {
                $scope.IRRecord.status = $scope.IRRecord.status + r.data;
                updateTextareaScroll();                
              }
              if ($scope.getStatus === true) {
                 $timeout($scope.IRRecord.getStatus, 500);
              }
            }, function(r) {
              $scope.IRRecord.status = "Error.";
            });                      
        },

      }



    })

}())
