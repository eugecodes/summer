// var eaDashboard = angular.module('eaDashboard', [], function($interpolateProvider){
//     $interpolateProvider.startSymbol('[[');
//     $interpolateProvider.endSymbol(']]');
// });
//
//
// eaDashboard.controller('dashboardController', ['$scope', '$http',
//     function($scope, $http) {
//
//
//         $scope.fromTheBlog = "";
//
//         $http.get('http://cors.io/?u=http://blog.exportabroad.com/?json=1')
//         .success(function (data) {
//             $scope.fromTheBlog = data.posts.slice(0,6);
//             console.log(data.posts);
//             // $scope.fromTheBlog = data.slice(0,6);
//         })
//         .error(function (data, status, headers, config) { // Error if problems with JSON
//             console.log("Error loading JSON");
//         });
//
//
//         $scope.showingModal = false;
//         $scope.modalTitle = "Modal Title";
//         $scope.modalBodyText = "This is the body text for the modal that pops up";
//         $scope.showModal = function(title, bodyText){
//             $scope.showingModal = true;
//             $scope.modalTitle = title;
//             $scope.modalBodyText = bodyText;
//         }
//
//
// }]);
//
//
// // Fill HTML - unsafe filter
// eaDashboard.filter('unsafe', function($sce) { return $sce.trustAsHtml; });



eaUniversal.controller('dashboardController', ['$scope', '$http', '$window',
    function($scope, $http, $window) {




        $scope.recentCustomers = null;
        $http.get('/api/v1/company/customers/')
        .success(function (data) {
            $scope.recentCustomers = data;
            console.log("Data success");
            // $scope.activityData = [];
            // for (var i = 0; i < $scope.recentCustomers.length; i++) {
            //     // console.log();
            //     $scope.activityData.push($scope.recentCustomers[i].created_at)
            //     console.log($scope.activityData);
            // }
        })
        .error(function (data, status, headers, config) {
            console.log("Error loading JSON");
        });


        // DATE FOR ACTIVITY
        // $scope.date = new Date();



        $scope.goToRecent = function(customer){
            $window.location = ('/customer/?t='+$scope.recentCustomers.indexOf(customer));
        }


        // $scope.fromTheBlog = "";
        //
        // $http.get('http://cors.io/?u=http://blog.exportabroad.com/?json=1')
        //     .success(function (data) {
        //         $scope.fromTheBlog = data.posts.slice(0,6);
        //         console.log(data.posts);
        //         // $scope.fromTheBlog = data.slice(0,6);
        //     })
        //     .error(function (data, status, headers, config) { // Error if problems with JSON
        //         console.log("Error loading JSON");
        //     });



        $http.get('https://api.fixer.io/latest?base=USD')
            .success(function (data) {
                $scope.currencyRates = data.rates;
            })
            .error(function (data, status, headers, config) { // Error if problems with JSON
                console.log("Error loading JSON");
            });




}]);
