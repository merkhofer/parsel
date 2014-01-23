var flask_ftm_server = "http://127.0.0.1:7000/";

var FileTarModule = angular.module("fileTarModule", ["ngResource","angularBootstrapNavTree"]);

FileTarModule.factory("AngularFTMService", function($resource){
    return {
        // Don't use JSONP: deserialization problems.
        //content_list: $resource(flask_ftm_server + "source/:source/listing/:ltype/?callback=placeholder", 
        source_list: $resource(flask_ftm_server + "source/:source/listing/:ltype/ ", 
             //{format:'json'},
             {source: '@source', ltype:'@this_doesnt_seem_to_matter'},
             {query: {/*cache:true,*/ method:'GET', params:{}, isArray:false}}
        ),
        source_list_startswith: $resource(flask_ftm_server + "source/:source/listing/:ltype/startswith/:sometext ", 
             //{format:'json'},
             {source: '@source', ltype:'@listing_type', sometext:'@sometext'},
             {query: {/*cache:true,*/ method:'GET', params:{}, isArray:false}}
        ),
        files_startswith: $resource(flask_ftm_server + "contents/:startswith/dir/:directory ", 
             //{format:'json'},
             {startswith: '@someregex', directory:'@abs_dir'},
             {query: {/*cache:true,*/ method:'GET', params:{}, isArray:false}}
        ),
       }
    });

var fileTarController = function($scope,$http,AngularFTMService) {
    $http.defaults.useXDomain = true; // Necessary for external services.

    var api_failed = function(failure) {
        console.log("API call failed!: " + failure.toSource());
        }

    $scope.fileTarScope = {source:null, listing_type:null, sometext:null,
        someregex:null, abs_dir:null, source_list:[]};

    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // Calls to resources
    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    $scope.fileTarScope.get_source_list = function() {
        AngularFTMService["source_list"].query(
            {source:$scope.fileTarScope.source, ltype:$scope.fileTarScope.listing_type},
            function(data) {
                // Success of some kind
                $scope.fileTarScope.source_list = data;
                //$scope.fileTarScope.dir_structure = data.results.dir_structure;
                //$scope.fileTarScope.content_list.all_files = [];
                },
            function(failure) {
                // failure
                $scope.fileTarScope.source_list = [];
                //$scope.fileTarScope.dir_structure = [];
                if(failure.status == 404) {
                    console.log("File/Tar list not found:" + failure.toSource());
                    }
                else {
                    console.log("File/Tar list call failed!:" + failure.toSource());
                    }
                });
        } 
    };
    /*
    $scope.fileTarScope.get_contents = function() {
        $scope.fileTarScope.contents = CTSAPI["contents"].query({container_id:$scope.fileTarScope.container_id});
        }

    $scope.fileTarScope.get_file_by_name = function() {
        $scope.fileTarScope.by_name_results = CTSAPI["file_by_name"].query({container_id:$scope.fileTarScope.container_id,file_path_name:$scope.fileTarScope.file_path_name});
        }

    $scope.fileTarScope.get_file_by_url = function() {
        $scope.fileTarScope.by_url_results = CTSAPI["file_by_url"].query({container_id:$scope.fileTarScope.container_id,file_url:$scope.fileTarScope.file_url});
        }
     */
    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    // Watch events
    //~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    /*$scope.$watch('fileTarScope.content_list', function(newVal) {
        alert("New Data", newVal);
        $scope.x = newVal;
        }); */

    //};
