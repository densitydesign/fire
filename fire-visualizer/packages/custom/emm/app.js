'use strict';

/*
 * Defining the Package
 */
var Module = require('meanio').Module;

var Emm = new Module('emm');

/*
 * All MEAN packages require registration
 * Dependency injection is used to define required modules
 */
Emm.register(function(app, auth, database) {

  //We enable routing. By default the Package Object is passed to the routes
  Emm.routes(app, auth, database);

  //We are adding a link to the main menu for all authenticated users
  Emm.menus.add({
    title: 'emm articles',
    link: 'emm articles',
    menu: 'main'
  });
  
  Emm.aggregateAsset('css', 'emm.css');

  /**
    //Uncomment to use. Requires meanio@0.3.7 or above
    // Save settings with callback
    // Use this for saving data from administration pages
    Emm.settings({
        'someSetting': 'some value'
    }, function(err, settings) {
        //you now have the settings object
    });

    // Another save settings example this time with no callback
    // This writes over the last settings.
    Emm.settings({
        'anotherSettings': 'some value'
    });

    // Get settings. Retrieves latest saved settigns
    Emm.settings(function(err, settings) {
        //you now have the settings object
    });
    */

  return Emm;
});
