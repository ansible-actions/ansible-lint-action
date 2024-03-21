 Action Ansible Linting
========================

Linting ansible roles or collections using the ansible-lint package directly from pypi.

Optionally it is possible to install some requirements like ansible collections, roles or pip packages. For more details about it, have a look at the Variables

## Usage

Example of ``.github/workflows/ansible-linting-check.yml``
```yaml
---
name: Ansible Lint check

# yamllint disable-line rule:truthy
on: [push, pull_request]

jobs:
  build:
    name: Ansible Lint
    runs-on: ubuntu-latest

    steps:
      - name: Checkout git repo
        uses: actions/checkout@v4
        with:
          submodules: true
          fetch-depth: 0

      - name: Run ansible-lint
        uses: ansible-actions/ansible-lint-action@v1.0.3
        with:
          target: "./"
```

This will run the command ``ansible-lint ./``

You can install some reuqirements, example:
```yml
[...]
        with:
          target: "./"
          required_collections: 'community.general'
          python_dependency: 'jmespath'
```
*This will install the community.general collections as well as the jmespath pip package.*

## Variables

| name | required | description | example values |
| --- | --- | --- | --- |
| ``target`` | true | Target for ansible linter | ``./`` or ``site.yml`` or ``path/to/ansible/`` |
| ``required_collections`` | - | define one ansible collection to install | ``community.general`` |
| ``collections_yml`` | - | define path of yml file for installing multiple ansible collections | ``requirements.yml`` |
| ``required_roles`` | - | define one ansible role to install | ``namespace.rolename`` |
| ``python_dependency`` | - | define one pip package to install | ``jmespath`` |
| ``python_dependency_file`` | - | define path of txt file for installing multiple python packages | ``requirements.txt`` |
