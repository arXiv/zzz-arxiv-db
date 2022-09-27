# Config vars for deploying to gcp

export PREFIX=modapi
export PROJ=arxiv-development
export PORT=8000
export MODAPI_MIG=$PREFIX

export ZONE=us-east1-d
export LOAD_BALANCER=api-beta-arxiv-lb
export SERVER_NAME="api.beta.arxiv.org"

# This should not be set to latest so the instance template is
# deterministic but there is probably a better way to do this.
export IMAGE_URL=gcr.io/arxiv-development/modapi@sha256:bdbc2237e0561458d30854944e097eecde11322d4c4a021aebc8ac1653add328

