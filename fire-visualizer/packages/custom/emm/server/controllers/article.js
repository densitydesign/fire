'use strict';

/**
 * Module dependencies.
 */
var mongoose = require('mongoose'),
    Article = mongoose.model('EmmArticle');
   // _ = require('lodash');



/**
 * Find article by id
 */
exports.article = function(req, res, next, id) {
    console.log('got here!');
    Article.load(id, function(err, article) {
        if (err) return next(err);
        if (!article) return next(new Error('Failed to load article ' + id));
        req.article = article;
        next();
    });
};

exports.show = function(req, res) {
    res.json(req.article);
};