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
