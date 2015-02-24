'use strict';


var articles = require('../controllers/article');

/* jshint -W098 */
// The Package is past automatically as first parameter
module.exports = function(Emm, app, auth, database) {

    app.route('/articles/:articleId')
        .get(articles.show);

    // Finish with setting up the articleId param
    app.param('articleId', articles.article);
};
