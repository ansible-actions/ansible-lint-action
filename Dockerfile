# hadolint ignore=DL3007
FROM python:3.13-trixie
# FROM python:latest

LABEL "maintainer"="L3D <l3d@c3woc.de>"
LABEL "repository"="https://github.com/ansible-actions/ansible-lint-action.git"
LABEL "homepage"="https://github.com/ansible-actions/ansible-lint-action"

# hadolint ignore=DL3008,DL3013,SC1091
RUN pip3 install --no-cache-dir ansible-lint ansible ansible-core

COPY ansible_docker.py /ansible_docker.py
CMD [ "python", "/ansible_docker.py"]
