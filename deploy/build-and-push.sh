GIT_V=$(git describe --dirty --abbrev=7)
docker build . --build-arg git_commit=$GIT_V -t gcr.io/arxiv-development/modapi
docker push gcr.io/arxiv-development/modapi
