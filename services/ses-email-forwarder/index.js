"use strict";
var LambdaForwarder = require('aws-lambda-ses-forwarder');

// parse environment variables
var emailBucket = process.env.EMAIL_BUCKET;
// var fromEmail = process.env.FROM_EMAIL || 'no-reply@example.com';
var forwardedEmail = process.env.FORWARDED_EMAIL || 'info@example.com';
var receiverEmails = (process.env.RECEIVER_EMAILS || 'john.doe@example.com').split(',');
var subjectPrefix = process.env.SUBJECT_PREFIX || '';
var emailKeyPrefix = process.env.EMAIL_KEY_PREFIX || '';

exports.handler = function(event, context, callback) {
  // See aws-lambda-ses-forwarder/index.js for all options.
  var overrides = {
    config: {
      // fromEmail: fromEmail,
      emailBucket: emailBucket,
      subjectPrefix: subjectPrefix,
      emailKeyPrefix: emailKeyPrefix,
      forwardMapping: {
        [forwardedEmail]: receiverEmails,
      }
    }
  };
  LambdaForwarder.handler(event, context, callback, overrides);
};
