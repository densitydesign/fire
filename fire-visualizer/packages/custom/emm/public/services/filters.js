'use strict';
<<<<<<< HEAD
=======
/* jshint -W098 */
>>>>>>> cf4a7f846e9769a1d000ad16891cf021d026552e

angular.module('mean.emm').filter('unique', function() {
    return function(collection, keyname) {
        var output = [],
            keys = [];

        angular.forEach(collection, function(item) {
            var key = item[keyname];
            if(keys.indexOf(key) === -1) {
                keys.push(key);
                output.push(item);
            }
        });

        return output;
    };
});