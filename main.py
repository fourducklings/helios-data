import configparser
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb

import serial

config = configparser.ConfigParser()
config.read("config.ini")

try:
    PORT = config["DEFAULT"]["PORT"]
except KeyError:
    config["DEFAULT"]["PORT"] = "COM1"
    PORT = config["DEFAULT"]["PORT"]
    with open("config.ini", "w") as configfile:
        config.write(configfile)


root = tk.Tk()
root.title("Helios Data Extracter")
root.geometry("650x500")

ser = None


def open_version():
    mb.showinfo("Version Information", "v0.1.0\n18/11/26")


def append_text(message):
    text_out_ui.config(state="normal")
    text_out_ui.insert(tk.END, message + "\n")
    text_out_ui.see(tk.END)
    text_out_ui.config(state="disabled")


def read_serial():
    if ser and ser.is_open:
        try:
            while ser.in_waiting > 0:
                raw_line = ser.readline()
                decoded_line = raw_line.decode("utf-8", errors="replace").strip()
                # print(decoded_line)
                append_text(decoded_line)
                if decoded_line.find("CORR_COEFF") != -1:
                    save_as_csv()
        except serial.SerialException as e:
            append_text(f"Serial error: {e}")
            return

    root.after(10, read_serial)


def start_listener():
    global ser

    if ser is None or not ser.is_open:
        try:
            ser = serial.Serial(PORT, baudrate=9600, timeout=1)
            start_listen.config(state="disabled", text="Listening...")
            append_text(f"Connected to {PORT}")
            append_text("Go to VIEW RESULTS and press LIMS EXPORT")
            read_serial()
        except serial.SerialException as e:
            append_text(f"Error opening port: {e}")


def save_as_csv():
    raw_out = str(text_out_ui.get("3.0", tk.END))
    lines_out = raw_out.splitlines()

    parsed_data = {}

    for line in lines_out:
        try:
            key, value = line.split(":", 1)
            print(key, value)
            parsed_data[key.strip()] = value.strip()
        except ValueError:
            pass

    interval = int(float(parsed_data["INTERVAL"]))
    start_wavelength = int(float(parsed_data["START"]))
    end_wavelength = int(float(parsed_data["STOP"]))

    offset = raw_out.count("\n", 0, (raw_out.find("BENCH")))
    # print("offset =" + str(offset))

    datestamp_line = list(parsed_data).index("DATESTAMP") + offset
    start_absorbance_line = datestamp_line + 1
    end_absorbance_line = int(
        start_absorbance_line + ((end_wavelength - start_wavelength) / interval)
    )

    csv_out = "Wavelength [nm],Absorbance"
    current_wavelength = start_wavelength

    # print("start:" + str(start_absorbance_line), "end" + str(end_absorbance_line))
    # +1 since end is exclusive
    for abs_value in lines_out[start_absorbance_line : end_absorbance_line + 1]:
        csv_out += f"\n{str(current_wavelength)},{abs_value}"
        current_wavelength += interval

    csv_file = filedialog.asksaveasfile(
        defaultextension=".csv", filetypes=[("CSV file", ".csv")]
    )
    csv_file.write(csv_out)
    csv_file.close()

    clear_data(
        "Do you want to extract another sample? Make sure the .CSV file is OK, "
        "as this will reset the current session."
    )


def clear_data(message):
    confirm = mb.askyesno("Clear Data", message)
    if confirm:
        text_out_ui.config(state="normal")
        text_out_ui.delete("3.0", tk.END)
        text_out_ui.config(state="disabled")
        append_text("")


menubar = tk.Menu(root)
root["menu"] = menubar
menu_file = tk.Menu(menubar)
menubar.add_cascade(menu=menu_file, label="Info")
menu_file.add_command(label="Version", command=open_version)

help_text = tk.Label(
    root,
    text="Run a sample and press 'Start Listening' when measuring sample finishes.",
)
help_text.pack(pady=5)

start_listen = tk.Button(root, text="Start Listening..", command=start_listener)
start_listen.pack(pady=5)

text_frame = tk.Frame(root)
text_frame.pack(pady=10, padx=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

text_out_ui = tk.Text(
    text_frame, height=10, width=40, state="disabled", yscrollcommand=scrollbar.set
)
text_out_ui.pack(side="left", fill="both", expand=True)

scrollbar.config(command=text_out_ui.yview)

help_text3 = tk.Label(
    root, text="ONLY if some data was corrupted, etc. press 'Clear Data'"
)
help_text3.pack()

clear_data_ui = tk.Button(
    root,
    text="Clear Data",
    command=lambda: clear_data("Do you really want to clear ALL data?"),
)
clear_data_ui.pack()

if __name__ == "__main__":
    root.mainloop()
