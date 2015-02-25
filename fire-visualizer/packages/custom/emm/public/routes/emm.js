'use strict';

angular.module('mean.emm').config(['$stateProvider',
  function($stateProvider) {
    $stateProvider
        .state('emm articles', {
          url: '/emm/articles/',
          templateUrl: 'emm/views/index.html'
        })
        .state('emm article', {
          url: '/emm/article/:article',
          templateUrl: 'emm/views/article.html'
        });
  }
]);
