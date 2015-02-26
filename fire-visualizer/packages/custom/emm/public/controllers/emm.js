'use strict';
/* jshint -W098 */



angular.module('mean.emm').controller('EmmController', ['$scope', '$stateParams', '$filter', 'Global', 'Emm',
  function($scope, $stateParams, $filter, Global, Emm) {
    $scope.global = Global;
    $scope.package = {
      name: 'emm'
    };

      $scope.texpand = true;
      $scope.eexpand = true;

  $scope.findOne = function() {
      Emm.get({
          articleId: $stateParams.article
      }, function(article) {

          $scope.article = article;
          console.log(article);

          $scope.filtent = $scope.article.entities.sort(function(a,b){
              var r1 = a.relevance;
              var r2 = b.relevance;
              var c1 = a.confidence;
              var c2 = b.confidence;

              if (r1 < r2) return 1;
              if (r1 > r2) return -1;
              if (c1 < c2) return 1;
              if (c1 > c2) return -1;
              return 0;
          });

          $scope.filtent = $filter('unique')($scope.filtent,'id');
      });
  };

    $scope.findOne();

  }
]);
