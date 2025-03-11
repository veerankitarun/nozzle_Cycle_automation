import os
import sys
import json
import time
import logging
import serial  
from datetime import datetime
import colorama 
from runtest import ask_retest, ask_cycles  

# Initialize colorama for Windows CMD support
colorama.init(autoreset=True)


class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[96m',     # Cyan
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[95m', # Magenta,
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_fmt = self.COLORS.get(record.levelname, self.RESET) + self._fmt + self.RESET
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

def load_config():
    config_path = os.path.join(sys.path[0], "config.json")
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            logger.info("Configuration loaded successfully.")
            return config
    except Exception as e:
        logger.error(f"Error loading configuration file: {e}")
        sys.exit(1)

def connect_to_arduino(com_port, baud_rate):
    try:
        arduino = serial.Serial(com_port, baud_rate, timeout=1)
        logger.info(f"Connected to Arduino on {com_port} at {baud_rate} baud.")
        return arduino
    except Exception as e:
        logger.error(f"Failed to connect to Arduino on {com_port}: {e}")
        sys.exit(1)

def send_command(arduino, command, timeout=10):

    try:
        logger.info(f"Sending command: {command}")
        
        arduino.reset_input_buffer()
        arduino.write((command + "\n").encode("utf-8"))
        start_time = time.time()
        while True:
            # Timeout handling
            if time.time() - start_time > timeout:
                logger.error(f"Timeout waiting for OK response for command: {command}")
                return False
            if arduino.in_waiting:
                response = arduino.readline().decode("utf-8", errors="replace").strip()
                logger.info(f"Received response: {response}")
                if response.upper() == "OK":
                    return True
            time.sleep(0.1)
    except Exception as e:
        logger.error(f"Error sending command '{command}': {e}")
        return False


def run_test_cycles(arduino, cycles):

    for cycle in range(1, cycles + 1):
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"=== Starting cycle {cycle} at {start_time} ===")
        
        # Test procedure commands:
        time.sleep(1)
        send_command(arduino, "AT+UP")
        time.sleep(2)
        send_command(arduino, "AT+ANG=-122")
        time.sleep(1)
        send_command(arduino, "AT+ANG=0")
        time.sleep(1)
        send_command(arduino, "AT+DOWN")
        time.sleep(2)
        
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"=== Completed cycle {cycle} at {end_time} ===")
        
        time.sleep(2)

def main():
    config = load_config()
    arduino_config = config.get("arduino", {})
    com_port = arduino_config.get("com_port")
    baud_rate = arduino_config.get("baud_rate", 9600)
    
    # Default cycles from config; may be overridden by GUI input later.
    cycles = config.get("cycles", 1)
    
    if not com_port:
        logger.error("COM port not specified in config.json under 'arduino'.")
        sys.exit(1)
    
    arduino = connect_to_arduino(com_port, baud_rate)
    
    # Loop the test cycles until the user decides not to retest
    while True:
        run_test_cycles(arduino, cycles)
        if ask_retest():
            new_cycles = ask_cycles()
            if new_cycles is None:  # If user cancels or doesn't provide a value, exit.
                break
            else:
                cycles = new_cycles
        else:
            break
    
    arduino.close()
    logger.info("Arduino connection closed.")

# --- Set up logging for both the CMD window and a file output ---
logger = logging.getLogger("ArduinoConnector")
logger.setLevel(logging.DEBUG)

formatter = ColorFormatter("%(asctime)s - %(levelname)s - %(message)s")

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler - logs to 'test_log.txt'
file_handler = logging.FileHandler("test_log.txt")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("Logger initialized in CMD window and log file.")

if __name__ == "__main__":
    main()
