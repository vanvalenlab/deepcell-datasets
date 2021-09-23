# edu-email-domain

A simple function to test whether a Cognito user email is a valid `.edu` domain.
This is intended to be deployed using as a [pre sign-up Lambda trigger](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html).

**DEPRECATED** - .edu email validation is no longer a requirement for `deepcell-datasets` and will be removed from the AWS Cognito User Group.

## Configuration

The service can be configured via environment variables.

| Name | Description | Default Value |
| :--- | :--- | :--- |
| `DOMAIN_WHITELIST` | Comma-separated whitelist of email domains to validate.  | `.edu` |
