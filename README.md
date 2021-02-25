# modapi
API for use by moderation and administration tools
# install and run

    git clone git@github.com:arXiv/modapi.git
    cd modapi
    python 3.8 -m venv ./modapi-venv  # or use pyenv
    source ./modapi-venv/bin/activate
    pip install poetry
    poetry install
    DEBUG=True python -m modapi.app

