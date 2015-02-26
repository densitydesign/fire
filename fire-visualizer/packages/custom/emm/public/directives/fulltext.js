'use strict';

angular.module('mean.emm').directive('fulltxt', function($compile){
    return {
        restrict: 'A',
        template: '<div class="col-md-9 fulltext"></div>',
        replace: true,
        /*scope: {
            'txt': '=',
            'ents': '='
        },*/
        link: function postLink(scope,element, attrs) {


            scope.$watch('filtent',function(newValue,oldValue){


                    var l = newValue.length;

                    scope.topents = [];
                    if (l > 20) {
                        scope.topents = newValue.slice(0, 20);
                    }
                    else {
                        scope.topents = newValue;
                    }
                var el = angular.element('<span/>');
                var txt = scope.article.fulltext;

                    scope.topents.forEach(function (e, i) {

                        var re = new RegExp(e.text, 'gi');
                        console.log(re);

                        txt = txt.replace(re, '<span ng-style="{\'background\':\'rgba(204, 255, 51, '+ e.confidence/14+')\'}" ng-class="{\'not-imp\':'+e.relevance+'<=0.33,\'v-imp\':'+e.relevance+'>=0.66}" class="entity">' + e.text + '</span>');

                    });

                    el.append(txt);
                    $compile(el)(scope);

                    element.append(el);

            });
        }
    };
});