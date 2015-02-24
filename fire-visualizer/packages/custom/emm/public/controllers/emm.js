'use strict';
/* jshint -W098 */



angular.module('mean.emm').controller('EmmController', ['$scope', '$stateParams', 'Global', 'Emm',
  function($scope, $stateParams, Global, Emm) {
    $scope.global = Global;
    $scope.package = {
      name: 'emm'
    };
  $scope.findOne = function() {
      Emm.get({
          articleId: $stateParams.article
      }, function(article) {
          console.log(article);
          $scope.article = article;
      });
  };

    $scope.findOne();

  }
]);
