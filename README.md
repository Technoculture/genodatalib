# genodatalib

[![Check and Rename YAML files](https://github.com/TechnocultureResearch/genodatalib/actions/workflows/check_and_rename_yaml.yaml/badge.svg)](https://github.com/TechnocultureResearch/genodatalib/actions/workflows/check_and_rename_yaml.yaml)

⚠️ NOTE: **THIS REPO IS ONLY FOR CONFIGURATION RELATED DATA**. THE ONLY CODE IN THIS REPO IS RELATED TO MINOR VALIDATION OF DATA FILES.

# Setup
## Setup for YAML Development
- If all you need to do is write yaml files, either directly or using scripts, you can simply clone this repo and place it anywhere in your system.
- For this process, it is advisable to use VS Code as it will provide some partial autocompletion. In order to do this correctly open the entire directory (genodatalib) in vs code.
    - This will suggest you to install some extensions within vs code, which you should
Should work on Linux/MacOS/Windows.

## Setup for Firmware Development
Genotyper Firmware applications load all these yaml files when they are started. They look for this folder/repo at this absolute path: `/tmp/tcr/genodatalib`.
- Clone this repo in `/tmp/tcr/`.
    If `/tmp/tcr` does not exist, create a directory under `/tmp` named `tcr`
    ```sh
    cd /tmp/tcr
    git clone https://github.com/TechnocultureResearch/genodatalib.git
    ```
- If you are on windows or a sytem without access to `/tmp`:
    Create the folder in your home directory: `~/tmp/tcr`
    > Note: These are intended for use in the robotic platform, hence genotyper firmware repos only supports linux and tries to support MacOS. NOT TESTED ON WINDOWS. A windows user may use a Linux VM(advisable), or WSL.

