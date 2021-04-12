GIT_V=$(git rev-parse --short HEAD)
docker build . --build-arg git_commit=$GIT_V -t gcr.io/arxiv-development/modapi
docker push gcr.io/arxiv-development/modapi
