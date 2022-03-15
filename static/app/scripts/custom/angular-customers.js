eaUniversal.controller('customersController', ['$scope', '$http', '$timeout', '$location',
    function($scope, $http, $timeout, $location) {

        // Get Customer
        $scope.location = $location;
        $scope.customerPos = "0";

        $scope.$watch('location.search()', function() {
            $scope.customerPos = ($location.search()).t;
        }, true);




        $scope.customer = null;
        $http.get('/api/v1/company/customers/')
        .success(function (data) {
            $scope.customer = data[$scope.customerPos];
            console.log($scope.customer); // Log loaded

        })
        .error(function (data, status, headers, config) {
            console.log("Error loading JSON");
        });








}]);
