# Config vars for deploying to gcp
gcloud config set project arxiv-development
export TYPE=beta

export PREFIX=modapi
export PROJ=arxiv-development
export PORT=8000
export MODAPI_MIG=$TYPE-$PREFIX

export ZONE=us-east1-d

export HOST_PREFIX=api-beta-arxiv
export LOAD_BALANCER=api-beta-arxiv-lb
export SERVER_NAME="api.beta.arxiv.org"
export LB_IP=api-beta-arxiv-lb-ipv4

export CERT=api-beta-arxiv-org-cert
export DOMAIN_CERT=api_beta_arxiv_org_cert.cer
export DOMAIN_KEY=api.beta.arxiv.org.key

# This should not be set to latest so the instance template is
# deterministic but there is probably a better way to do this.
export IMAGE_URL=gcr.io/arxiv-development/modapi@sha256:088e1b699d6d71b0ac1cf1878fb303de187586ac242b788571d1b037687f404a


export VM_ENV_VALUES=beta_env_values.txt
