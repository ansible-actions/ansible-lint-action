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
    ENV_PIPPACKAGE_NAME = "PIPPACKAGE"
    ENV_PIPPACKAGE_TXT_NAME = "PIPPACKAGETXT"
    ENV_COLLECTIONS_YML_NAME = "COLLECTIONSYML"

    # check for TARGET variable
    env_target = EnvironmentManager(ENV_TARGET_NAME)
    TARGET = env_target.check_required_environment_variable()
    if TARGET == "":
        print("Target needs to be defined")
        sys.exit(1)

    # check for required collection variable
    env_collection = EnvironmentManager(ENV_REQUIRED_COLLECTION_NAME)
    reqired_collection = env_collection.check_optional_environment_variable()

    # check for required collection variable
    env_collection_yml = EnvironmentManager(ENV_COLLECTIONS_YML_NAME)
    reqired_collection_yml = env_collection_yml.check_optional_environment_variable()

    # check for required role variable
    env_role = EnvironmentManager(ENV_REQUIRED_ROLE_NAME)
    reqired_role = env_role.check_optional_environment_variable()

    # check for install pip packages variable
    env_pip = EnvironmentManager(ENV_PIPPACKAGE_NAME)
    pip_pkg = env_pip.check_optional_environment_variable()

    # check for install packages.txt variable
    env_pip_txt = EnvironmentManager(ENV_PIPPACKAGE_TXT_NAME)
    pip_pkg_txt = env_pip_txt.check_optional_environment_variable()

    # execute ansible commands
    execute = AnsibleCommandExecution()

    # Optionally install required ansible collections directly
    if bool(reqired_collection):
        collection_install_command = ["ansible-galaxy", "collection", "install",
                          f"{reqired_collection}", "--upgrade"]
        collection_install_info = execute.run_command(collection_install_command)
        print(f"{collection_install_info}\nSINGLE COLLECTION INSTALL SUCCESSFUL")

    # Optionally install required ansible collections from yml file
    if bool(reqired_collection_yml):
        collections_install_command = ["ansible-galaxy", "install", "--role-file",
                          f"{reqired_collection_yml}", "--force"]
        collections_install_info = execute.run_command(collections_install_command)
        print(f"{collections_install_info}\nCOLLECTION.YML INSTALL SUCCESSFUL")

    # Optionally install required ansible roles
    if  bool(reqired_role):
        role_install_command = ["ansible-galaxy", "role", "install", f"{reqired_role}", "--force"]
        role_install_info = execute.run_command(role_install_command)
        print(f"{role_install_info}\nSINGLE ROLE INSTALL SUCCESSFUL")

    # Optionally install pip package directly
    if  bool(pip_pkg):
        pip_install_command = ["pip", "install", "--upgrade", f"{pip_pkg}"]
        pip_install_info = execute.run_command(pip_install_command)
        print(f"{pip_install_info}\nPIP PACKAGE INSTALL SUCCESSFUL")

    # Optionally install pip package from file
    if  bool(pip_pkg_txt):
        pip_requirements_command = ["pip", "install", "--upgrade", "-r",  f"{pip_pkg_txt}"]
        pip_requirements_info = execute.run_command(pip_requirements_command)
        print(f"{pip_requirements_info}\nPIP PACKAGE.TXT INSTALL SUCCESSFUL")

    # run ansible lint
    ansible_command = ["ansible-lint", f"{TARGET}"]
    linter_run = execute.run_command(ansible_command)
    print(f"---start+linter---\n{linter_run}\nAnsible run successful\n---end+linter---")
