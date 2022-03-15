eaUniversal.controller('customersListController', ['$scope', '$http', '$timeout', '$location', '$window',
    function($scope, $http, $timeout, $location, $window) {




        $scope.customers = null;
        $http.get('/api/v1/company/customers/')
        .success(function (data) {
            $scope.customers = data;
            console.log($scope.customers); // Log loaded

            $scope.customerID = data[0].user;
            console.log($scope.customerID);


        })
        .error(function (data, status, headers, config) {
            console.log("Error loading JSON");
        });

        $scope.orderCustomerListBy = "-created_at";

        $scope.goToCustomer = function(customer){
            // alert($scope.customers.indexOf(customer));
            $window.location = ('/customer/?t='+$scope.customers.indexOf(customer));
            // $location.url('/customer/?t='+$scope.customers.indexOf(customer));
            // $scope.$apply();
        }

        $scope.newCustSubmit = "Submit";
        $scope.newCust_country = "US";
        $scope.addCustomer = function(){
            $scope.newCustSubmit = "Loading...";

            if(!$scope.newCust_name | !$scope.newCust_address | !$scope.newCust_city | !$scope.newCust_postal | !$scope.newCust_country){
                $scope.showAlert('Error.', 'Please fill in all required fields then try again.');
                $scope.newCustSubmit = "Submit";

                return;
            }else{
                $http({
                    method : 'POST',
                    url : '/api/v1/company/customers/',
                    data : {
                        "name": $scope.newCust_name,
                        "description": $scope.newCust_description,
                        "website": $scope.newCust_url,
                        "address_line1": $scope.newCust_address,
                        "address_line2": $scope.newCust_address2,
                        "city": $scope.newCust_city,
                        "state_province": $scope.newCust_state,
                        "postal_code": $scope.newCust_postal,
                        "country": $scope.newCust_country,
                        "industry": $scope.newCust_industry,
                        "user": $scope.customerID,
                        "contacts": null,
                        "products": null
                    }

                }).success(function(data) {
                    $scope.newCustSubmit = "Submit";

                    // $scope.newCust_name = "";
                    // $scope.newCust_desc = "";
                    // $scope.newCust_url = "";
                    // $scope.newCust_address = "";
                    // $scope.newCust_address2 = "";
                    // $scope.newCust_city = "";
                    // $scope.newCust_state = "";
                    // $scope.newCust_postal = "";
                    // $scope.newCust_industry = "";
                    // $scope.customerID = "";
                    // $scope.showAlert('Success!', 'Your new customer has been added! The page will now reload.');
                    // $scope.closeModal()
                    $timeout(function() {
                        // location.reload();
                        $window.location = ('/customer/?t='+$scope.customers.length()+1);
                    }, 2000);
                    // $scope.reload();


                }).error(function(data){
                    $scope.newCustSubmit = "Submit";

                    $scope.showAlert('Error.', 'Something went wrong. Please check your answers and try again.');
                });
            }

        }





        $scope.industries = [
            'Chemical',
    		'Mining',
    		'Food',
    		'Basic Materials',
    		'Services',
    		'Transportation',
    		'Healthcare',
    		'Technology',
    		'Communication',
    		'Manufacturing'
        ]





}]);
