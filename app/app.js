/* 
 LIRC Web Admin - a web admin for LIRC administration 

 You may use any Web Server Admin project under the terms
 of the GNU General Public License (GPL) Version 3.

 (c) 2016 Emilio Mariscal (emi420 [at] gmail.com)
 
 */

 angular.module('Admin', [
        'app.controllers',
        'ngRoute',
    ])
    .config(['$routeProvider',
     function($routeProvider) {
        $routeProvider.
           when('/index', {
              templateUrl: 'templates/index.html',
              controller: 'IndexCtrl'
           }).
           otherwise({
              redirectTo: '/index'
           });
     }])

