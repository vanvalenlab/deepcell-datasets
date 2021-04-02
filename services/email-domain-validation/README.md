# edu-email-domain

A simple function to test whether a Cognito user email is a valid `.edu` domain.
This is intended to be deployed using as a [pre sign-up Lambda trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html).

## Configuration

The service can be configured via environment variables.

| Name | Description | Default Value |
| :--- | :--- | :--- |
| `DOMAIN_WHITELIST` | Comma-separated whitelist of email domains to validate.  | `.edu` |
