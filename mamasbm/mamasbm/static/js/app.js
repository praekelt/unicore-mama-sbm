/* App Module */

var profilesApp = angular.module('profilesApp', [
  'ngRoute',
  'profilesControllers'
]);

profilesApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/profiles', {
        templateUrl: '/static/html/profiles.html',
        controller: 'ProfilesListCtrl'
      }).
      when('/profiles/:uuid', {
        templateUrl: '/static/html/profile_edit.html',
        controller: 'ProfileEditCtrl'
      }).
      otherwise({
        redirectTo: '/profiles'
      });
  }
]);
