#!/bin/bash

set -evu

# Long time out on the LB to support socket.io
# The default of 30s causes websockets to close
# with an error code of 1006 on the server.
$TIMEOUT=1h

# Create a backend service
# This looks for a port named "http" on the instance group by default.
gcloud compute backend-services create $TYPE-$PREFIX-backend \
       --project=$PROJ \
       --health-checks=modapi-health-check \
       --timeout=$TIMEOUT \
       --global

# Add backend as a link to instance group
gcloud compute backend-services add-backend $TYPE-$PREFIX-backend \
       --project=$PROJ \
       --instance-group=$MODAPI_MIG \
       --instance-group-zone=$ZONE \
       --balancing-mode=RATE \
       --max-rate=200 \
       --global



#################### Load Balancer ####################

gcloud compute ssl-certificates create $CERT \
     --project=$PROJ \
     --certificate=$DOMAIN_CERT \
     --private-key=$DOMAIN_KEY \
     --global

# reserve an IP address
gcloud compute addresses create $LB_IP \
       --project=$PROJ \
       --ip-version=IPV4 \
       --global
       

#################### Phoenix load balancer ####################

# This becomes the name of the load balancer in the GCP UI
gcloud compute url-maps create $LOAD_BALANCER \
       --project=$PROJ \
       --default-service $TYPE-$PREFIX-backend \
       --global

# Create a target HTTP(S) proxy to route requests to your URL map.
# The proxy is the portion of the load balancer that holds the SSL
# certificate.
gcloud compute target-https-proxies create $TYPE-$PREFIX-target-https-proxy \
       --project=$PROJ \
       --ssl-certificates=$CERT \
       --url-map=$LOAD_BALANCER \
       --global


# Create the frontend of the LB
# Create a global forwarding rule to route incoming requests to the proxy.
gcloud compute forwarding-rules create $TYPE-$PREFIX-lb-forwarding-rule \
       --project=$PROJ \
       --address=$LB_IP \
       --target-https-proxy=$TYPE-$PREFIX-target-https-proxy \
       --ports=443 \
       --global

# If the load balancer doesn't work after about 60 sec.
# to to the GCP UI, go to load balancer, go to the load balancer that
# this script creates, click edit, click finalize and then save (or update)
# Even without changing anything this seems to kick the LB into working sometimes.


