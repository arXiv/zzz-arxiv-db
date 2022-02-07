# ModAPI 3

An API for use by moderation and administration tools

# Install and run

    git clone git@github.com:arXiv/modapi.git
    cd modapi
    python3.8 -m venv ./modapi-venv  # or use pyenv
    source ./modapi-venv/bin/activate
    pip install poetry
    poetry install
    DEBUG=True CLASSIC_DB_URI='mysql://user:pw@host/arXiv' JWT_SECRET=yackyack python -m modapi.app
    chrome http://localhost:8000/docs

# To run tests
Test were simplified to use fixtures for a test db. Running the tests
is just:

    pytest

# Docker build and run
You'll need a DB connection and you'll need to write a file named env_values.txt like

    DEBUG=True
    CLASSIC_DATABASE_URI=mysql://arxivrw:somepassword@127.0.0.1/arXiv
    JWT_SECRET=SomeSecretThatNeedsToMatchYourAuthService

Then run:

    docker build . -t arxiv/modapi
    docker run --env_list env_values.txt --network host arxiv/modapi

Then open a browser to http://localhost:8000/docs

# Testing with data from a DB on GCP
Testing modAPI on your develoopment laptop with data from GCP and the arxiv-check UI is tricky.

1. Setup GCP SQL proxy so you can access the GCP DB from your dev machine
2. ./cloud_sql_proxy -instances=arxiv-development:us-east4:arxiv-db-dev=tcp:0.0.0.0:1234
3. Run the mod API

   CLASSIC_DATABASE_URI=mysql://root:CLOUD_PW_1234abcd@127.0.0.1:1234/arXiv  \
   JWT_SECRET=fake_jwt_secret \
   DEBUG=True \
   python -m modapi.app

4. Config the arxiv-check UI in src/config.ts to use the mod3 API at localhost:8000
5. Config the arxiv-check UI in src/config.ts to use a modkey
6. Run the arxiv-check UI on a port other than 8000.

# Testing email functionality

If you want to test sending emails via localhost, you can create a tunnel to nexus:
```bash
ssh arxiv-nexus -2 -L 25:127.0.0.1:25 -q -N -g
```
Note that `config.allow_emails` must be set to `True`. Be careful not to
accidentally send emails to submitters.
