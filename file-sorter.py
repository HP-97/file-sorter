import yaml
import time
import os
import logging
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Create and configure logger
# TODO: Make log path configurable
log = logging.getLogger(__name__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
dirpath = os.path.dirname(__file__)
logging.basicConfig(filename="{}/{}.log".format(dirpath, script_name),
                    format='%(asctime)s.%(msecs)03d [%(funcName)s:%(lineno)d] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='w')

# Log level checking
def check_log_level(log_level):
    log_levels = ["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if log_level.upper() not in log_levels:
        return False
    return True

def set_log_level(log_level):
    if log_level.upper() == "NOTSET":
        return logging.NOTSET
    elif log_level.upper() == "DEBUG":
        return logging.DEBUG
    elif log_level.upper() == "INFO":
        return logging.INFO
    elif log_level.upper() == "WARNING":
        return logging.WARNING
    elif log_level.upper() == "ERROR":
        return log_level.ERROR
    elif log_level.upper() == "CRITICAL":
        return log_level.CRITICAL
    else:
        log.critical("{} is not a valid log level. Returning None".format(log_level))
        return None

class FileHandler(FileSystemEventHandler):
    def __init__(self, config_path):
        if os.path.isfile(config_path):
            with open(config_path, 'r') as stream:
                try:
                    self.config = yaml.safe_load(stream)
                    self.folder_to_track = self.config["folder_to_track"]
                    log.info("{} config successfully loaded!".format(config_path))
                    log.info("Target directory: {} ".format(self.folder_to_track))
                except yaml.YAMLError as exc:
                    print(exc)
                    exit(1)
        else:
            print("config_path {} does not exist".format(config_path))
    
    def on_modified(self, event):
        for filename_ext in os.listdir(self.folder_to_track):
            filename, extension = os.path.splitext(filename_ext)
            # check if filename_ext's extension is defined in .yaml config
            if extension not in self.config["entries"].keys():
                log.debug("{} has extension {}. Not defined in .yaml config. Skipping".format(filename_ext, extension))
                pass
            else:
                print("{}: extension {} MATCH!".format(filename_ext, extension))
                src = self.folder_to_track + "/" + filename_ext
                dest = self.config["entries"][extension] + "/" + filename_ext
                if os.path.isfile(dest):
                    log.debug("{} already exists. Skipping file".format(filename_ext))
                else:
                    log.info("Moving {} to {}".format(src, dest))
                    os.rename(src, dest)
            
            
            
if __name__ == "__main__":
    log.setLevel(logging.INFO)
    log.critical("[START] {}".format(os.path.basename(__file__)))
    arg = argparse.ArgumentParser()
    arg.add_argument("--config", required=True, help="The .yaml config which will determine where to organise a file according to its extension")
    arg.add_argument("--loglevel", help="The log level that is to be outputted to the log file.", type=check_log_level)
    args = arg.parse_args()
    # Default values
    if args.loglevel is None:
        log.setLevel(logging.INFO)
    else:
        log_level = set_log_level(args.loglevel)
        if log_level is not None:
            log.setLevel(log_level)
        else:
            log.error("{} is not a valid log level. Exiting".format(args.loglevel))
            exit(1)
    # Handle config
    if not os.path.isfile(args.config):
        log.error("\"{}\" config file could not be found. Exiting".format(args.config))
        exit(1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

    event_handler = FileHandler(args.config)
    observer = Observer()
    observer.schedule(event_handler, event_handler.folder_to_track, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log.critical("[END] Program terminated")
    observer.join()
    
    
             