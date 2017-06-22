'use strict';

console.log('Loading function');

var AWS = require('aws-sdk');
var request = require('request');

let tag = process.env.tag;
let application = process.env.application;
let url = process.env.url;
var headers = {
    'Content-Type':     'application/x-www-form-urlencoded'
}
var answer = false;

exports.handler = (event, context, callback) => {
    // Load the message passed into the Lambda function into a JSON object
    var eventText = JSON.stringify(event, null, 2);
    var messageText = "Received  " + event.clickType + " message from button ID: " + event.serialNumber;

    // Write the string to the console
    console.log("Message to send: " + messageText);

    if (event.clickType == "SINGLE") {
        console.log("Single click detected. Setting "+application+" to Business-Relevant in "+tag+" policy.");

        var options = {
          url: url,
          method: 'POST',
          headers: headers,
          form: { 'policy': tag, 'app': application, 'relevance': 'Business-Relevant' }
        }

        request(options,
          function(error, response, body) {
            console.log(response.statusCode);
            body = body.toString("utf-8");
            console.log(body);
            if (!error & response.statusCode == 200) {
              answer = true;
            } else {
              answer = false;
            }
          } );

    } else if (event.clickType == "DOUBLE") {
        console.log("Double click detected. Setting "+application+" to Business-Irrelevant in "+tag+"policy.");

        var options = {
          url: url,
          method: "POST",
          headers: headers,
          form: { 'policy': tag, 'app': application, 'relevance': 'Business-Irrelevant' }
        }

        request(options,
          function(error, response, body) {
            console.log(response.statusCode);
            body = body.toString("utf-8");
            console.log(body);
            if (!error & response.statusCode == 200) {
              answer = true;
            } else {
              answer = false;
            }
          } );
    }

    if (answer) {
      callback(null, 'Successfully changed state.');
    } else {
      callback(new Error('Unable to set state.'));
    }
};
