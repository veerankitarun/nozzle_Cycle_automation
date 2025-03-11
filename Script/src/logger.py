import logging
from datetime import datetime, timezone
import os
import json
import sys

DEBUG = False
DEEP_DEBUG = False
SHARED_LOGGER = True

if DEBUG:
    FORMAT = "%(asctime)s - %(name)s :: %(message)s"
    if DEEP_DEBUG:
        DEBUG_LEVEL = logging.DEBUG
    else:
        DEBUG_LEVEL = logging.INFO
    INPUT_NAME = " - input "
    print_input_date = True
else:
    FORMAT = "%(message)s"
    DEBUG_LEVEL = logging.INFO
    INPUT_NAME = " "
    print_input_date = False

DATEFMT = "%H:%M:%S"
FILE_FORMAT = "%(asctime)s - %(levelname)s - %(name)s :: %(message)s"
FILE_DATEFMT = "%Y-%m-%d %H:%M:%S"
FILE_DEBUG_LEVEL = logging.DEBUG

config = {}
with open(os.path.join(sys.path[0], "config.json"), "r") as f:
    config = json.load(f)

# Define custom logging levels
PASS_LEVEL = 25
TEXT_LEVEL = 26
FAIL_LEVEL = 27
logging.addLevelName(PASS_LEVEL, 'PASS')
logging.addLevelName(TEXT_LEVEL, 'TEXT')
logging.addLevelName(FAIL_LEVEL, 'FAIL')

# Extend the Logger class to add methods for the custom levels
def passed(self, message, *args, **kwargs):
    if self.isEnabledFor(PASS_LEVEL):
        self._log(PASS_LEVEL, message, args, **kwargs)

def text(self, message, *args, **kwargs):
    if self.isEnabledFor(TEXT_LEVEL):
        self._log(TEXT_LEVEL, message, args, **kwargs)

def fail(self, message, *args, **kwargs):
    if self.isEnabledFor(FAIL_LEVEL):
        self._log(FAIL_LEVEL, message, args, **kwargs)

logging.Logger.passed = passed
logging.Logger.text = text
logging.Logger.fail = fail

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',  # Blue
        'INFO': '\033[96m',   # Cyan
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',  # Red
        'CRITICAL': '\033[95m',  # Magenta
        'TEXT': '\033[97m',    # White  
        'PASS': '\033[92m',    # Green
        'FAIL': '\033[91m',    # Red
    }
    RESET = '\033[0m'

    def format(self, record):
        log_fmt = self.COLORS.get(record.levelname, self.RESET) + self._fmt + self.RESET
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def Logger(name:str,shared_logger=SHARED_LOGGER):
    if shared_logger:
        logger = logging.getLogger()
    else:
        logger = logging.getLogger(name)
    logger.setLevel(FILE_DEBUG_LEVEL)

    if shared_logger:
        
        if not logger.hasHandlers():
            # Create the handlers
            logger = create_handlers(logger)
    else:
        
        if logger.hasHandlers():
            logger.handlers.clear()
        
        
        logger = create_handlers(logger)

    return logger

def create_handlers(logger):
    '''
    Creates stream and file handlers for the logger
    '''
    #Create the parent folder
    global config
    path = config["model"]["path"]
    #Check if valid directory path
    if not os.path.isdir(path):
        path = sys.path[0]
    
    # Navigate two directories up
    path = os.path.abspath(os.path.join(path, '..', '..'))

    staging_folder_name = 'BASE_SOUNDNESS_Results\\STAGING\\Output_logs'
    production_folder_name = 'BASE_SOUNDNESS_Results\\PROD\\Output_logs'

    staging_folder_path = os.path.join(path, "Logs", staging_folder_name)
    os.makedirs(staging_folder_path, exist_ok=True)
    production_folder_path = os.path.join(path, "Logs", production_folder_name)
    os.makedirs(production_folder_path, exist_ok=True)

    #Create folders for each date
    curr_date = datetime.now(timezone.utc)
    date = curr_date.date().strftime("%Y%m%d")

    staging_log_dir = os.path.join(staging_folder_path, date)
    os.makedirs(staging_log_dir, exist_ok=True)
    production_log_dir = os.path.join(production_folder_path, date)
    os.makedirs(production_log_dir, exist_ok=True)

    #Create the filepath
    timestamp = int(datetime.now().timestamp())
    if config["db"] == "STAGING":
        filepath = os.path.join(staging_log_dir, f"{timestamp}_Base_soundness_output.log")
    elif config["db"] == "PROD":
        filepath = os.path.join(production_log_dir, f"{timestamp}_Base_soundness_output.log")

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filepath, mode="w")

    console_handler.setLevel(DEBUG_LEVEL)
    file_handler.setLevel(FILE_DEBUG_LEVEL)

    formatter = ColorFormatter(FORMAT, datefmt=DATEFMT)
    file_formatter = logging.Formatter(FILE_FORMAT, datefmt=FILE_DATEFMT)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def LoggerConfigs():
    logging.basicConfig(
        format=FORMAT,
        datefmt=DATEFMT,
        level=DEBUG_LEVEL
    )

def setModuleLoggingLevel():
    logging.getLogger("pyftdi.i2c").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger("bleak").setLevel(logging.ERROR)

def LoggerInput(prompt:str)->str:
    '''
    Prompts the tester for input
    '''
    # logging.info("="*60)
    if print_input_date:
        time = datetime.now().time().strftime("%H:%M:%S")
        res = input(f"{time}{INPUT_NAME}:: {prompt}")
    else:
        if prompt.startswith('\n'):
            prompt = prompt[2:]
        res = input(prompt)
    # logging.info("="*60)
    return res