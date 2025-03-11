import tkinter as tk
from tkinter import messagebox, simpledialog

def ask_retest():

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    answer = messagebox.askyesno("Retest", "Test cycles completed.\nDo you want to retest?")
    root.destroy()
    return answer

def ask_cycles():

    root = tk.Tk()
    root.withdraw()
    cycles = simpledialog.askinteger("Cycles", "Enter number of cycles:", minvalue=1)
    root.destroy()
    return cycles

def prompt_user_for_calibration():

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Calibrate Stepper Motor",
                        "Please set the nozzle orientation relative to the elbow.\n"
                        "Click OK when you are ready to calibrate.")
    root.destroy()

def pop_up_result(success):

    root = tk.Tk()
    root.withdraw()
    if success:
        messagebox.showinfo("Calibration", "Stepper motor calibrated successfully.")
    else:
        messagebox.showerror("Calibration", "Failed to calibrate stepper motor.")
    root.destroy()
