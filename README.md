# Webhook CI/CD

A very simple implementation of CI/CD using GitHub webhooks

The logic is as follows:

- User pushes the code to the target branch.
- After which Github sends a signal to our backend, which in turn automatically pulls the target branch.
- The last step is to build the application, in this case the backend builds the frontend service.

One of the cases where this idea can help you is if you have your code stored in Github, but the policy of the server on which the application is to be deployed limits the possibilities.

## Installation

### Clone project from GitHub

```bash
git clone https://github.com/waffle-frame/webhook-ci-cd
cd webhook-ci-cd
```

### Setting up the environment

Initialization virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install requirements

```bash
pip3 install -r requirements.txt
```

Setting environment variables

```bash
cp example.env .env
```

### Run

```bash
python3 webhook.py
```

TODO:

- [ ] Logging
- [ ] Error handling and reportin
