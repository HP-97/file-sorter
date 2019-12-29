# File-sorter

This python script uses the Watchdog API to observe a given directory for any modifications. If a change is detected, File-sorter will iterate through every file in the directory (top level only). File-sorter will check whether a file's extension has been defined in its .yaml config and will move the matching file to the specified directory.

# Prerequisites
Things you need to install the software and how to install them
```
Python3
```

# Installing
```
pip install -r requirements.txt
```

# Usage
## Example configuration file
```
# Define master destination folders here 
master_dest_folders:
  pictures: &pictures "/Users/{User}/Pictures"

# Target folder to track any new changes
folder_to_track: "/Users/{User}/Downloads"

# extension definitions to look out for. E.g. extension: destination folder.
# Use YAML anchors and aliases for good DRY practice
entries:
  .jpg: *pictures
```
``master_dest_folders`` is generally used to define a scalar anchor so directories can be defined once and referenced for multiple extensions.

## Example use

```
./file-sorter.py --config file-sorter_config.yaml --loglevel info
```
This will start the file-sorter script and will continuously run until manually terminated.