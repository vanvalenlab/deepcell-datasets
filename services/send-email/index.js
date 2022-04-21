// https://aws.amazon.com/blogs/architecture/create-dynamic-contact-forms-for-s3-static-websites-using-aws-lambda-amazon-api-gateway-and-amazon-ses/

var AWS = require('aws-sdk');
var ses = new AWS.SES();

var receiverEmail = process.env.RECEIVER_EMAIL || 'example@example.com';
var senderEmail = process.env.SENDER_EMAIL || 'example@example.com';

function sendEmail(event, done) {
  var data = JSON.parse(event.body);
  var params = {
    Destination: {
      ToAddresses: [receiverEmail],
    },
    Message: {
      Body: {
        Text: {
          Data: `
            Email: ${data.email}
            Name: ${data.name}

            Subject: ${data.subject}

            Body:
            ${data.message}`,
          Charset: 'UTF-8',
        },
      },
      Subject: {
        Data: `DeepCell Datasets Contact Form: ${data.name}`,
        Charset: 'UTF-8',
      },
    },
    Source: senderEmail,
  };
  ses.sendEmail(params, done);
}

exports.handler = (event, context, callback) => {
  console.log('Received event:', event);
  sendEmail(event, (err, data) => {
    const response = {
      statusCode: 200,
      body: JSON.stringify({ message: 'Hello World!' }),
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': true,
      },
    };
    callback(err, response);
  });
};
