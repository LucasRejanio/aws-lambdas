'use strict';

const aws = require('aws-sdk');
const ssm = new aws.SSM({ region: 'us-east-1' });

exports.handler = async (event, context, callback) => {
    
    // Get request and request headers
    const request = event.Records[0].cf.request;
    const headers = request.headers;

    // Configure authentication
    const authUser = 'enjoei';
    const parameter = await ssm.getParameter({
     Name: "/enjuca/production/AUTH_SHERLOCK_PASSWORD",
     WithDecryption: true
    }).promise();

    const authPass = parameter['Parameter']['Value']

    // Construct the Basic Auth string
    const authString = 'Basic ' + new Buffer(authUser + ':' + authPass).toString('base64');

    // Require Basic authentication
    if (typeof headers.authorization == 'undefined' || headers.authorization[0].value != authString) {
        const body = 'Unauthorized';
        const response = {
            status: '401',
            statusDescription: 'Unauthorized',
            body: body,
            headers: {
                'www-authenticate': [{key: 'WWW-Authenticate', value:'Basic'}]
            },
        };
        callback(null, response);
    }

    // Continue request processing if authentication passed
    callback(null, request);
};

