var eaUniversal = angular.module('eaUniversal', ['ngAnimate'], function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');

});
eaUniversal.config(['$httpProvider', '$locationProvider', function($httpProvider, $locationProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    $locationProvider.html5Mode({
      enabled: true,
      requireBase: false
    });
}]);



eaUniversal.controller('universalController', ['$scope', '$http',
    function($scope, $http) {


        $scope.showingModal = false;
        $scope.modalTitle = "";
        $scope.modalBody = "";
        $scope.showModal = function(title, body){
            $scope.showingModal = true;
            $scope.modalTitle = title;
            $scope.modalBody = body;
        }

        $scope.closeModal = function(){
            $scope.showingModal = false;
        }

        $scope.showingAlert = false;
        $scope.alertTitle = "";
        $scope.alertBody = "";
        $scope.showAlert = function(title, body){
            $scope.showingAlert = true;
            $scope.alertTitle = title;
            $scope.alertBody = body;
        }

        $scope.closeAlert = function(){
            $scope.showingAlert = false;
        }




}]);




// Fill HTML - unsafe filter
eaUniversal.filter('unsafe', function($sce) { return $sce.trustAsHtml; });
