'use strict';

angular.module('mean.emm').factory('Emm', ['$resource',
    function($resource) {
        return $resource('articles/:articleId', {
            articleId: '@_id'
        }, {
            update: {
                method: 'PUT'
            }
        });
    }
]);
