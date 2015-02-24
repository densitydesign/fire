'use strict';

angular.module('mean.emm').config(['$stateProvider',
  function($stateProvider) {
    $stateProvider.state('emm articles', {
      url: '/emm/articles/:article',
      templateUrl: 'emm/views/index.html'
    });
  }
]);
