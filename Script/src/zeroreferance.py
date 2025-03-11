import sys
import time
import tkinter as tk
from tkinter import messagebox
import logging
import colorama
from runtest import pop_up_result 


colorama.init(autoreset=True)


from Main import load_config, connect_to_arduino, send_command

# Set up logger for calibration
logger = logging.getLogger("CalibrateStepper")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def prompt_user_for_calibration():
    """
    Display a Tkinter popup that instructs the user to set the nozzle orientation
    relative to the elbow. The process continues once the user clicks OK.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Calibrate Stepper Motor",
                        "Please set the nozzle orientation relative to the elbow.\n"
                        "Click OK when you are ready to calibrate.")
    root.destroy()

# def pop_up_result(success):


#     root = tk.Tk()
#     root.withdraw()  
#     if success:
#         messagebox.showinfo("Calibration", "Stepper motor calibrated successfully.")
#     else:
#         messagebox.showerror("Calibration", "Failed to calibrate stepper motor.")
#     root.destroy()

def calibrate_stepper_motor():
    # Load configuration parameters using shared load_config()
    config = load_config()
    arduino_config = config.get("arduino", {})
    com_port = arduino_config.get("com_port")
    baud_rate = arduino_config.get("baud_rate", 9600)
    
    if not com_port:
        logger.error("COM port not specified in config.json under 'arduino'.")
        sys.exit(1)
    
    
    arduino = connect_to_arduino(com_port, baud_rate)
    
    # Prompt the user to set the nozzle orientation
    prompt_user_for_calibration()
    

    time.sleep(1)
    
    
    result = send_command(arduino, "AT+CZO")
    if result:
        logger.info("Stepper motor calibrated successfully.")
    else:
        logger.error("Failed to calibrate stepper motor.")
    
    
    pop_up_result(result)
    
    arduino.close()
    logger.info("Arduino connection closed.")

if __name__ == "__main__":
    calibrate_stepper_motor()
