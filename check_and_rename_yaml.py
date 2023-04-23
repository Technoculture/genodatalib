#!/usr/bin/env python3

import os
import re
import yaml
from packaging.version import Version, InvalidVersion
from yaml.parser import ParserError
from yaml.scanner import ScannerError

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class InvalidYamlFileError(Exception):
    pass

class MissingNameVersionError(Exception):
    pass

class InvalidNameError(Exception):
    pass

class InvalidVersionError(Exception):
    pass

def is_yaml_file(filename):
    return filename.endswith('.yaml')

def load_yaml_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except (ParserError, ScannerError) as e:
        raise InvalidYamlFileError(f"Invalid YAML file: {file_path}. Error: {e}")

def format_name(name):
    name = name.strip().lower()
    name = re.sub(r'\s+', '_', name)
    return re.split(r'\W+', name)[0]

def validate_name(name, file_path):
    if not re.match(r'^\w+$', name):
        raise InvalidNameError(f"Invalid name/title: {name} in YAML file: {file_path}. Only alphanumeric characters and underscores are allowed.")

def validate_version(version, file_path):
    try:
        Version(version)
    except InvalidVersion:
        raise InvalidVersionError(f"Invalid version: {version} in YAML file: {file_path}. Must be a valid SemVer.")

def check_name_version(content, file_path):
    if content is None:
        raise MissingNameVersionError(f"YAML file is empty or contains only comments: {file_path}")

    name = content.get('name') or content.get('title')
    version = content.get('version')

    if not (name and version):
        raise MissingNameVersionError(f"Missing name/title or version in YAML file: {file_path}")

    name = format_name(name)
    validate_name(name, file_path)
    validate_version(version, file_path)

    logger.debug(name)

    return name, version

def process_yaml_file(file_path, independent_file_pattern, common_pattern):
    content = load_yaml_file(file_path)
    name, _ = check_name_version(content, file_path)
    filename = os.path.basename(file_path)

    match = independent_file_pattern.match(filename) or common_pattern.match(filename)
    logger.debug(match)

    if not match:
        if name in ["nodes", "modules", "tools"]:
            new_file_name = f"{name}.lib.yaml"
        elif content.get('type') == "tree":
            new_file_name = f"{name}.tree.yaml"
        elif content.get('type') == "workflow":
            new_file_name = f"{name}.wflow.yaml"
        elif content.get('type') == "lut":
            new_file_name = f"{name}.lut.yaml"
        else:
            raise InvalidNameError(f"Invalid name/title: {name} in YAML file: {file_path}. The file name does not match the required pattern.")

        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        os.rename(file_path, new_file_path)
        logger.debug(f"Renamed {file_path} to {new_file_path}")

def check_and_rename_yaml(root_dir):
    independent_file_pattern = re.compile(r'^(.+)\.(tree|lut|wflow)\.yaml$')
    common_pattern = re.compile(r'^(nodes|modules|tools)\.lib\.yaml$')

    common_files = {"nodes.lib.yaml": 0, "modules.lib.yaml": 0, "tools.lib.yaml": 0}

    for folder, _, files in os.walk(root_dir):
        # Skip everything in the .github folder
        if ".github" in folder:
            continue

        for file in files:
            if is_yaml_file(file):
                file_path = os.path.join(folder, file)
                process_yaml_file(file_path, independent_file_pattern, common_pattern)
                if file in common_files:
                    common_files[file] += 1

    for common_file, count in common_files.items():
        if count != 1:
            raise Exception(f"Exactly one {common_file} is required, but found {count}.")

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))
    check_and_rename_yaml(root_dir)

