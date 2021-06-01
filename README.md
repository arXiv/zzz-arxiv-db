# ModAPI 3

An API for use by moderation and administration tools

# Install and run

    git clone git@github.com:arXiv/modapi.git
    cd modapi
    python 3.8 -m venv ./modapi-venv  # or use pyenv
    source ./modapi-venv/bin/activate
    pip install poetry
    poetry install
    DEBUG=True CLASSIC_DB_URI='mysql+aiomysql://user:pw@host/arXiv' JWT_SECRET=yackyack python -m modapi.app
    chrome http://localhost:8000/docs

Config values will be read from environment variables or from the file env.

# To run tests
I had problems using the fast-api test client so test are run like this:

    JWT_SECRET=1234 python bin/launch_test_server.py &  # start test db, load test db, start API server
    JWT_SECRET=1234 pytest
    # At the end of the tests DB and API will still be running, end with:
    fg
    CTRL-C

# Docker build and run
You'll need a DB connection and you'll need to write a file named env_values.txt like

    DEBUG=True
    CLASSIC_DATABASE_URI=mysql://arxivrw:somepassword@127.0.0.1/arXiv
    JWT_SECRET=SomeSecretThatNeedsToMatchYourAuthService

Then run:

    docker build . -t arxiv/modapi
    docker run --env_list env_values.txt --network host arxiv/modapi

Then open a browser to http://localhost:8000/docs

# Deploy to arxiv-develop in GCP
Make sure the values in deploy/dev_env_values.txt are resonable.
Setup gcloud and then run:

    ./deploy/build-and-push.sh

    # Lots of output
    # last line:
    # latest: digest: sha256:1908...latest.hash...eece size: 3677
    # copy the latest hash

    cd deploy
    . dev-config.sh
    ./update-instance-group.sh gcr.io/arxiv-development/modapi@sha256:1908...lastest.hash...eece

# Testing with data from GCP
Testing modAPI on your develoopment laptop with data from GCP and the arxiv-check UI is tricky.

1. Setup GCP SQL proxy so you can access the GCP DB from your dev machine
2. ./cloud_sql_proxy -instances=arxiv-development:us-east4:arxiv-db-dev=tcp:0.0.0.0:1234
3. Run the mod API

   CLASSIC_DATABASE_URI=mysql+aiomysql://root:CLOUD_PW_1234abcd@127.0.0.1:1234/arXiv  \
   JWT_SECRET=fake_jwt_secret \
   python -m modapi.app

4. Config the arxiv-check UI in src/config.ts to use the mod3 API at localhost:8000
5. Config the arxiv-check UI in src/config.ts to use a modkey
6. Run the arxiv-check UI on a port other than 8000.
