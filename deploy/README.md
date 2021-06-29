# Deploy to production

Production is setup differently since it is not run on GCP.

TODO

You can investigate how this is running by sshing to arxiv-sync and doing =sudo journalctl -uf arxiv-modapi=

# To setup infrastructure and deploy to GCP:
This deploys to beta or to dev

To deploy to dev:

0. copy env_values.txt.example to dev_env_values.txt and set all TODOs in there to the correct values.
1. ln -s dev-config.sh config.sh
2. source config.sh
3. ./setupCompute.sh
4. ./setupLB.sh

5. Figure out which docker image you want to deploy, go to GCP container registry and get it's hash URL
./update-instance-group.sh gcr.io/arxiv-development/modapi@sha256:088eTHE-INSTANCE-HASHf404a

# On future deploys of just updates

    source ./deploy/dev-config.sh
    ./deploy/build-and-push.sh

    # Lots of output
    # last line:
    # latest: digest: sha256:1908...latest.hash...eece size: 3677

    ./deploy/update-instance-group.sh $(cat TAG.txt)
    
