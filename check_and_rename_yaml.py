import os
import re
import yaml
from packaging.version import Version

def check_and_rename_yaml(root_dir):
    file_pattern = re.compile(r'^(.+)-(\d+\.\d+\.\d+)\.yaml$')

    for folder, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.yaml'):
                file_path = os.path.join(folder, file)
                try:
                    with open(file_path, 'r') as f:
                        content = yaml.safe_load(f)
                except Exception as e:
                    raise Exception(f"Invalid YAML file: {file_path}. Error: {e}")

                name = content.get('name') or content.get('title')
                version = content.get('version')

                if not (name and version):
                    raise Exception(f"Missing name/title or version in YAML file: {file_path}")

                match = file_pattern.match(file)
                if not match or match.group(1) != name or match.group(2) != version:
                    new_file_name = f"{name}-{version}.yaml"
                    new_file_path = os.path.join(folder, new_file_name)
                    os.rename(file_path, new_file_path)
                    print(f"Renamed {file_path} to {new_file_path}")

                    # Bump minor version if there are changes
                    current_version = Version(version)
                    bumped_version = current_version.base_version + "." + str(current_version.release[1] + 1)
                    content['version'] = bumped_version

                    # Rename the file with bumped version
                    bumped_file_name = f"{name}-{bumped_version}.yaml"
                    bumped_file_path = os.path.join(folder, bumped_file_name)
                    os.rename(new_file_path, bumped_file_path)
                    print(f"Bumped version and renamed {new_file_path} to {bumped_file_path}")

                    # Update the version in the YAML content
                    with open(bumped_file_path, 'w') as f:
                        yaml.safe_dump(content, f)

if __name__ == '__main__':
    repo_root = os.environ['GITHUB_WORKSPACE']
    check_and_rename_yaml(repo_root)

