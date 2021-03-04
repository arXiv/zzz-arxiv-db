#!/bin/bash

set -evu

# Create a backend service
# This looks for a port named "http" on the instance group by default.
gcloud compute backend-services create modapi-backend \
       --project=$PROJ \
       --health-checks=modapi-health-check \
       --global

# WARNING: This is a place where socket.io could get messed up.
# What could max-rate mean with a long lived TCP socket connection?
#
# Add backend as a link to instance group
gcloud compute backend-services add-backend modapi-backend \
       --project=$PROJ \
       --instance-group=$MODAPI_MIG \
       --instance-group-zone=$ZONE \
       --balancing-mode=RATE \
       --max-rate=200 \
       --global



#################### Load Balancer ####################

gcloud compute ssl-certificates  create api-beta-arxiv-org-cert \
     --project=$PROJ \
     --certificate=api_beta_arxiv_org_cert.cer \
     --private-key=api.beta.arxiv.org.key \
     --global

# reserve an IP address
gcloud compute addresses create api-beta-arxiv-lb-ipv4 \
       --project=$PROJ \
       --ip-version=IPV4 \
       --global
       

#################### Phoenix load balancer ####################

# This becomes the name of the load balancer in the GCP UI
gcloud compute url-maps create $LOAD_BALANCER \
       --project=$PROJ \
       --default-service modapi-backend \
       --global

# Create a target HTTP(S) proxy to route requests to your URL map.
# The proxy is the portion of the load balancer that holds the SSL
# certificate.
gcloud compute target-https-proxies create api-beta-arxiv-target-https-proxy \
       --project=$PROJ \
       --ssl-certificates=api-beta-arxiv-org-cert \
       --url-map=$LOAD_BALANCER \
       --global


# Create the frontend of the LB
# Create a global forwarding rule to route incoming requests to the proxy.
gcloud compute forwarding-rules create api-beta-arxiv-lb-forwarding-rule \
       --project=$PROJ \
       --address=api-beta-arxiv-lb-ipv4 \
       --target-https-proxy=api-beta-arxiv-target-https-proxy \
       --ports=443 \
       --global

# If the load balancer doesn't work after about 60 sec.
# to to the GCP UI, go to load balancer, go to the load balancer that
# this script creates, click edit, click finalize and then save (or update)
# Even without changing anything this seems to kick the LB into working sometimes.


