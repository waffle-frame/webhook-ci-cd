# Webhook CI/CD

A very simple implementation of CI/CD using GitHub webhooks

The logic is as follows:
- User pushes the code to the target branch.
- After which Github sends a signal to our backend, which in turn automatically pulls the target branch.
- The last step is to build the application, in this case the backend builds the frontend service.

One of the cases where this idea can help you is if you have your code stored in
Github, but the policy of the server on which the application is to be deployed limits the possibilities.
