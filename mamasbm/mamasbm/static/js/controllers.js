var profilesControllers = angular.module('profilesControllers', []);

profilesControllers.controller('ProfilesListCtrl', ['$scope', 'Profile', '$location', '$window', function ($scope, Profile, $location, $window) {
    $scope.profiles = Profile.query();
    $scope.remove = function(profile){
        profile.$delete()
               .then(function(profile){
                    $scope.profiles = Profile.query();
               });
    };
}]);

profilesControllers.controller(
    'ProfileEditCtrl',
    ['$scope', '$routeParams', 'Profile', '$location', '$http', '$route',
    function ($scope, $routeParams, Profile, $location, $http, $route) {
        if($routeParams.uuid != 'new'){
            $scope.profile = Profile.get({uuid: $routeParams.uuid});
        }else{
            $scope.profile = new Profile();
        }
        $scope.send_days = [
            {id: 0, name: 'Monday'},
            {id: 1, name: 'Tuesday'},
            {id: 2, name: 'Wednesday'},
            {id: 3, name: 'Thursday'},
            {id: 4, name: 'Friday'},
            {id: 5, name: 'Saturday'},
            {id: 6, name: 'Sunday'}
        ];
        $scope.save = function(profile){
            profile.$save()
                   .then(function(profile){
                        $location.path('/profiles');
                   });
        };
        $scope.add = function(profile){
            profile.$add()
                   .then(function(profile){
                        $location.path('/profiles');
                   });
        };
        $scope.remove_message_profile = function(profile, msg_profile){
            url = '/web/api/message_profiles.json?uuid=' + msg_profile.uuid;
            $http.delete(url)
                 .then(function(){
                        $location.path('/profiles/' + profile.uuid);
                        $route.reload();
                   });
        };
}]);
