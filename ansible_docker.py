#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action to run ansible linter
"""
import subprocess
import os
import sys

class EnvironmentManager:
    """
    Parsing Enviroment Variables
    """
    def __init__(self, env_var_name):
        self.env_var_name = env_var_name
        self.env_var_value = os.getenv(env_var_name)

    def check_required_environment_variable(self):
        """
        Check if required Variable is defined.
        exit if undefined
        """
        if self.env_var_value is not None:
            print(f"The value of {self.env_var_name} is: {self.env_var_value}")
            return f"{self.env_var_value}"
        print(f"The variable {self.env_var_name} is not set but needs to be defined.\nFAILED")
        sys.exit(1)

    def check_optional_environment_variable(self):
        """
        Check if optional Variable is defined.
        exit if undefined
        """
        if self.env_var_value is not None:
            print(f"The value of {self.env_var_name} is: {self.env_var_value}")
            return f"{self.env_var_value}"
        return False

# pylint: disable=R0903
class AnsibleCommandExecution:
    """
    running ansible commands
    """
    def run_command(self, command):
        """
        Running command as subprocess.
        Printing error on fail and exit
        """
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as error:
            print(f"Error running Ansible command: {error}\n\n{error.stdout}\n{error.stderr}")
            sys.exit(1)

if __name__ == "__main__":
    # define known enviroment vars
    ENV_TARGET_NAME = "TARGET"
    ENV_REQUIRED_COLLECTION_NAME = "REQCOLLECTIONS"
    ENV_REQUIRED_ROLE_NAME = "REROLE"

    # check for target variable
    env_target = EnvironmentManager(ENV_TARGET_NAME)
    target = env_target.check_required_environment_variable()

    # check for required collection variable
    env_collection = EnvironmentManager(ENV_REQUIRED_COLLECTION_NAME)
    reqired_collection = env_collection.check_optional_environment_variable()

    # check for required role variable
    env_role = EnvironmentManager(ENV_REQUIRED_ROLE_NAME)
    reqired_role = env_role.check_optional_environment_variable()

    # run ansible commands
    ansible_version_checker = AnsibleCommandExecution()

    # Optionally install required ansible collections
    if bool(reqired_collection):
        ansible_command = ["ansible-galaxy", "collection", "install", f"{reqired_collection}", "--upgrade"]
        version_info = ansible_version_checker.run_command(ansible_command)
        print(f"COLLECTION INSTALL SUCCESSFUL\n{version_info}")

    # Optionally install required ansible roles
    if  bool(reqired_role):
        ansible_command = ["ansible-galaxy", "role", "install", f"{reqired_role}", "--upgrade"]
        version_info = ansible_version_checker.run_command(ansible_command)
        print(f"ROLE INSTALL SUCCESSFUL\n{version_info}")

    # run ansible lint
    ansible_command = ["ansible-lint", f"{target}"]
    version_info = ansible_version_checker.run_command(ansible_command)
