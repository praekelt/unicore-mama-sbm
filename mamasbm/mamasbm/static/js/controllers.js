var profilesControllers = angular.module('profilesControllers', []);

profilesControllers.controller('ProfilesListCtrl', function ($scope, $http) {
    $http.get('/web/api/profiles.json').success(function(data) {
        $scope.profiles = data['profiles'];
    });
});

profilesControllers.controller('ProfileEditCtrl', function ($scope, $http, $routeParams) {
    $http.get('/web/api/profiles.json?uuid=' + $routeParams.uuid).success(function(data) {
        $scope.profile = data;
    });
});
