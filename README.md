# modapi

API for use by moderation and administration tools

# install and run

    git clone git@github.com:arXiv/modapi.git
    cd modapi
    python 3.8 -m venv ./venv  # or use pyenv
    source ./modapi-venv/bin/activate
    pip install poetry
    poetry install
    DEBUG=True CLASSIC_DATABASE_URI='mysql://user:pw@host/arXiv' JWT_SECRET=yackyack python -m modapi.app

# Docker build and run
You'll need a DB connection and you'll need to write a file named env_values.txt like

    DEBUG=True
    CLASSIC_DATABASE_URI=mysql://arxivrw:somepassword@127.0.0.1/arXiv
    JWT_SECRET=SomeSecretThatNeedsToMatchYourAuthService

Then run:

    docker build . -t arxiv/modapi
    docker run --env_list env_values.txt --network host arxiv/modapi

Then open a browser to http://localhost:8000/docs
