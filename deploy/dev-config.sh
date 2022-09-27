# Config vars for deploying to gcp

# Expected project is arxiv-development but
# this line doesn't work with github actions
#gcloud config set project arxiv-development

export TYPE=dev

export PREFIX=modapi
export PROJ=arxiv-development
export PORT=8000
export MODAPI_MIG=$TYPE-$PREFIX

export ZONE=us-east1-d

export HOST_PREFIX=services-dev-arxiv
export LOAD_BALANCER=services-dev-arxiv-lb
export SERVER_NAME="services.arxiv.org"
export LB_IP=services-dev-arxiv-lb-ipv4

export CERT=services-dev-arxiv-org-cert	
export DOMAIN_CERT=services_dev_arxiv_org_cert.cer
export DOMAIN_KEY=services_dev_arxiv_org.key

# This should not be set to latest so the instance template is
# deterministic but there is probably a better way to do this.
# Could we get the hash URL of :latest?
export IMAGE_URL=gcr.io/arxiv-development/modapi@sha256:088e1b699d6d71b0ac1cf1878fb303de187586ac242b788571d1b037687f404a

export VM_ENV_VALUES=deploy/dev_env_values.txt


