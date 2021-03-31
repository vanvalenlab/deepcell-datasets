# send-email

A service to send emails from the Contact Form using [AWS Lambda and AWS SES](https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/ses-examples-sending-email.html).

## Configuration

The service is configured using environment variables. Please find a table of all environment variables and their descriptions below.

| Name | Description | Default Value |
| :--- | :--- | :--- |
| `SENDER_EMAIL` | **REQUIRED**: A [verified email in SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html). | `"example@example.com"` |
| `RECEIVER_EMAIL` | **REQUIRED**: A [verified email in SES](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html). | `"example@example.com"` |
