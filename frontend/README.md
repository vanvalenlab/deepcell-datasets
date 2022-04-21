# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## AWS Cognito and SES

This project uses AWS Cognito for user authentication and AWS SES to send and receive emails through the application.
[This guide](https://medium.com/responsetap-engineering/easily-create-email-addresses-for-your-route53-custom-domain-589d099dd0f2) was followed for setting up the custom domain emails.

## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

---

To build and deploy this project:

```bash
yarn build && sls s3sync
```

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

## Deploy to S3

First build the project with `yarn`, then push the files to S3.

```bash
yarn build

# If using a profile, include AWS_PROFILE=profile-name
yarn deploy:frontend:dev
```

## Configuration

The React application can be configured via several environment variables. These variables must be prefixed with `REACT_APP` to be parsed during the build process.

| Name                                | Description                                                        | Default Value |
| :---------------------------------- | :----------------------------------------------------------------- | :------------ |
| `REACT_APP_REGION`                  | **REQUIRED**: AWS region where the Cognito user pool is located.   | `""`          |
| `REACT_APP_USER_POOL_ID`            | **REQUIRED**: Cognito user pool ID.                                | `""`          |
| `REACT_APP_IDENTITY_POOL_ID`        | **REQUIRED**: Cognito identity pool ID.                            | `""`          |
| `REACT_APP_USER_POOL_WEB_CLIENT_ID` | **REQUIRED**: Cognito user pool web client ID.                     | `""`          |
| `REACT_APP_S3_BUCKET`               | **REQUIRED**: The bucket where the login-protected data is stored. | `""`          |
| `REACT_APP_SEND_EMAIL_API_ENDPOINT` | **REQUIRED**: API endpoint of the `send-email` service.            | `""`          |
