# Deploy to production

Production is setup differently since it is not run on GCP. It is
running behind nginx on a CIT server.

    ssh arxiv-sync.serverfarm.cornell.edu
    git_for_eprints # do whatever you do to get git credentials
    sudo su e-prints
    source /tmp/ep
    cd /users/e-prints/modapi
    git pull
    exit
    sudo systemctl restart arxiv-modapi.service

# Viewing the logs for production
You can view the logs:

    sudo journalctl -uf arxiv-modapi

The nginx config is at /etc/nginx/nginx.conf

# To setup infrastructure and deploy to GCP:
This deploys to beta or to dev

To deploy to dev:

    cp --no-clobber deploy/env_values.txt.example deploy/dev_env_values.txt
    vim deploy/dev_env_values.txt  # set all TODOs in there to the correct values, see lastpass "services.dev.arxiv.org modapi3"
    source dev-config.sh
    ./setupCompute.sh
    ./setupLB.sh

    # Figure out which docker image you want to deploy, go to GCP container registry and get it's hash URL
    ./update-instance-group.sh gcr.io/arxiv-development/modapi@sha256:088eTHE-INSTANCE-HASHf404a

# On future deploys of just updates

    source ./deploy/dev-config.sh
    ./deploy/build-and-push.sh

    # Lots of output
    # last line:
    # latest: digest: sha256:1908...latest.hash...eece size: 3677

    ./deploy/update-instance-group.sh $(cat TAG.txt)
    
# Viewing the logs for dev
To to the GCP arxiv-develop and to to "compute engines" -> "instance
groups". Then look for the instance group named "dev-modapi" click on
that.  Under instance group members there should be only one
instance. Click on that, and then click on "cloud logging" to get the
logs for that instance.
