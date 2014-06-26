var profilesControllers = angular.module('profilesControllers', []);

profilesControllers.controller('ProfilesListCtrl', ['$scope', 'Profile', function ($scope, Profile) {
    $scope.profiles = Profile.query();
}]);

profilesControllers.controller('ProfileEditCtrl', ['$scope', '$routeParams', 'Profile', function ($scope, $routeParams, Profile) {
    $scope.profile = Profile.get({uuid: $routeParams.uuid});
    $scope.send_days = [
        {id: 0, name: 'Sunday'},
        {id: 1, name: 'Monday'},
        {id: 2, name: 'Tuesday'},
        {id: 3, name: 'Wednesday'},
        {id: 4, name: 'Thursday'},
        {id: 5, name: 'Friday'},
        {id: 6, name: 'Saturday'}
    ];
}]);
