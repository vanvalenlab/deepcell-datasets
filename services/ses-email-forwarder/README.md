# ses-email-forwarder

An AWS Lambda function that forwards emails from a verified email or domain to a list of subscriber emails. This is based upon [`aws-lambda-ses-forwarder`](https://github.com/arithmetric/aws-lambda-ses-forwarder) and it's Serverless wrapper [`serverless-ses-forwarder`](https://github.com/tonycapone/serverless-ses-forwarder).

[This blog post](https://medium.com/responsetap-engineering/easily-create-email-addresses-for-your-route53-custom-domain-589d099dd0f2) was very helpful in setting up verified emails in AWS SES.

## Configuration

While `serverless-ses-forwarder` uses a `config.yml` file to configure multiple mappings and receivers, this function relies on environment variables to create the mapping. We chose to configure via environment variables for better security, as the environment variables will never be committed to git.

Unfortunately, this means that currently only one forwarding mapping is supported.

| Name | Description | Default Value |
| :--- | :--- | :--- |
| `FORWARDED_EMAIL` | **Required** Emails sent to this address will be forwarded to `RECEIVER_EMAILS`.  | `info@example.com` |
| `RECEIVER_EMAILS` | **Required** Comma-separated whitelist of email domains to validate.  | `john.doe@example.com` |
| `SUBJECT_PREFIX` | Prefix the subject of each email that is forwarded.  | `""` |
| `EMAIL_KEY_PREFIX` | Save the emails under this key inside the bucket.  | `""` |
