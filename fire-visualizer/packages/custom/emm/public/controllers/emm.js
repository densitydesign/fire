'use strict';
/* jshint -W098 */



angular.module('mean.emm').controller('EmmController', ['$scope', '$stateParams', 'Global', 'Emm',
  function($scope, $stateParams, Global, Emm) {
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
      });
  };

    $scope.findOne();

  }
]);
