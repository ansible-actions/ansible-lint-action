 Action Ansible Linting
===============================

Linting Ansible roles...

Work in Progress...

```yml
inputs:
  target:
    description: |
      Target for ansible linter
      For example './', 'roles/my_role/' or 'site.yml'
    required: true
  required_collections:
    description: |
      You can define a required ansible collection here.
      They will be installed using ansible-galaxy collection install <YourInput>.
    required: false
  required_roles:
    description: |
      You can define a required ansible role here.
      They will be installed using ansible-galaxy role install <YourInput>.
    required: false
```

## Example Setup
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
      - name: 'checkout git repo'
        uses: actions/checkout@v4
        with:
          lfs: true
          submodules: true
          fetch-depth: 0

      - name: Run ansible-lint
        uses: ansible-actions/ansible-lint-action@v0.0.2
        with:
          target: "site.yml"
```
