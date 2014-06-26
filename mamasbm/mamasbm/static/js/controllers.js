var profilesControllers = angular.module('profilesControllers', []);

profilesControllers.controller('ProfilesListCtrl', ['$scope', 'Profile', function ($scope, Profile) {
    $scope.profiles = Profile.query();
}]);

profilesControllers.controller('ProfileEditCtrl', ['$scope', '$routeParams', 'Profile', function ($scope, $routeParams, Profile) {
    $scope.profile = Profile.get({uuid: $routeParams.uuid});
}]);
