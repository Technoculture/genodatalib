import os
import re
import yaml
from packaging.version import Version, InvalidVersion
from yaml.parser import ParserError
from yaml.scanner import ScannerError

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

    return name, version

def process_yaml_file(file_path, file_pattern):
    content = load_yaml_file(file_path)
    name, version = check_name_version(content, file_path)
    filename = os.path.basename(file_path)

    match = file_pattern.match(filename)
    if not match or match.group(1) != name or match.group(2) != version:
        new_file_name = f"{name}-{version}.yaml"
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        os.rename(file_path, new_file_path)
        print(f"Renamed {file_path} to {new_file_path}")

        # Bump minor version if there are changes
        current_version = Version(version)
        bumped_version = f"{current_version.release[0]}.{current_version.release[1]}.{current_version.release[2] + 1}"
        content['version'] = bumped_version

        # Rename the file with bumped version
        bumped_file_name = f"{name}-{bumped_version}.yaml"
        bumped_file_path = os.path.join(os.path.dirname(file_path), bumped_file_name)
        os.rename(new_file_path, bumped_file_path)
        print(f"Bumped version and renamed {new_file_path} to {bumped_file_path}")

        # Update the version in the YAML content
        with open(bumped_file_path, 'w') as f:
            yaml.safe_dump(content, f)

def check_and_rename_yaml(root_dir):
    file_pattern = re.compile(r'^(.+)-(\d+\.\d+\.\d+)\.yaml$')

    for folder, _, files in os.walk(root_dir):
        # Skip everything in the .github folder
        if ".github" in folder:
            continue

        for file in files:
            if is_yaml_file(file):
                file_path = os.path.join(folder, file)
                process_yaml_file(file_path, file_pattern)

if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))
    check_and_rename_yaml(root_dir)

