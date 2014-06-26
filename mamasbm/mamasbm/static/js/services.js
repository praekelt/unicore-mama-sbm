var profilesServices = angular.module('profilesServices', ['ngResource']);

profilesServices.factory('Profile', ['$resource',
  function($resource){
    return $resource('/web/api/profiles.json?uuid=:uuid', {}, {
      query: {method:'GET', params:{uuid:''}, isArray:true}
    });
  }]);
