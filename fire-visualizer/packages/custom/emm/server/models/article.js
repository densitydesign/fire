'use strict';

/**
 * Module dependencies.
 */

var mongoose = require('mongoose'),
    Schema = mongoose.Schema;



var ArticleSchema = new Schema({

    title: {
        type: String,
        required: true,
        trim: true
    },
    lang: {
        type: String,
        required: true,
        trim: true
    },
    country: {
        type: String,
        required: true,
        trim: true
    },
    journal: {
        type: String,
        required: true,
        trim: true
    },
    link: {
        type: String,
        required: true,
        trim: true
    },
    date: {
        type: Date,
        required: true
    },
    fulltext: {
        type: String,
        required: true,
        trim: true
    },
   topics: {
        type: [Schema.Types.Mixed]
    },
    entities: {
        type: [Schema.Types.Mixed]
    }

},
    {
        collection : 'articles'
    });

ArticleSchema.statics.load = function(id, cb) {
    this.findOne({
        _id: id
    }).exec(cb);
};

mongoose.model('EmmArticle', ArticleSchema);
