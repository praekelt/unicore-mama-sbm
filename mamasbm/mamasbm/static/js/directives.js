var profilesDirectives = angular.module('profilesDirectives',[]);

profilesDirectives.directive('multiselectDropdown', [function() {
    return function(scope, element, attributes) {
        console.log(element);
        // Below setup the dropdown:

        element.multiselect({
            buttonClass : 'btn btn-sm btn-default',
            buttonWidth : '200px',
            buttonContainer : '<div class="btn-group" />',
            maxHeight : 230,
            enableFiltering : false,
            buttonText : function(options) {
                if (options.length === 0) {
                    return element.data()['placeholder'] + ' <b class="caret"></b>';
                } else if (options.length > 1) {
                    return _.first(options).text + ' + ' + (options.length - 1) + ' more selected <b class="caret"></b>';
                } else {
                    return _.first(options).text + ' <b class="caret"></b>';
                }
            },
            // Replicate the native functionality on the elements so
            // that angular can handle the changes for us.
            onChange: function (optionElement, checked) {
                optionElement.removeAttr('selected');
                if (checked) {
                    optionElement.prop('selected', 'selected');
                }
                element.change();
            }

        });
        // Watch for any changes to the length of our select element
        scope.$watch(function () {
            return element[0].length;
        }, function () {
            element.multiselect('rebuild');
        });

        // Watch for any changes from outside the directive and refresh
        scope.$watch(attributes.ngModel, function () {
            element.multiselect('refresh');
        });

        // Below maybe some additional setup
    };
}]);
