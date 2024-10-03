FROM ubuntu:latest
LABEL authors="walik"

ENTRYPOINT ["top", "-b"]