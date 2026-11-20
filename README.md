# Helios Data Extractor

(First project!) A simple Python program to save scan graphs via RS232 from the Helios α-δ (Alpha, Beta, Gamma, and Delta) series. The program saves the graph as a `.csv` file, which can be opened by most modern plotting/data analysis programs. 

## Requirements

* [A custom RS232 null-modem cable](RS232pinout.md)
* Helios α-δ (Alpha-Gamma) spectrophotometer
* A computer with a RS232 port (or an USB-RS232 adapter might work)
* Python

> [!WARNING]
> This program was only tested with the Helios Beta model, but will probably work with the Alpha, Delta, and Gamma models.

## Hardware setup

Connect the **custom** RS232 cable from your computer to the spectrophotometer.

## Software setup

1. Install Python if you haven't already.

2. Clone the repository:
  ```
  git clone https://github.com/fourducklings/helios-data
  cd helios-data
  ```

3. Install dependencies in the requirements.txt file:
  ```
  pip install -r requirements.txt
  ```

4. Run the main.py file:
  ```
  python main.py
  ```
> [!IMPORTANT]
> By default, the program tries to connect to COM1. If you connected the spectrophotometer to another port, you can change this by editing the `config.ini` file generated on the first run of the program and changing the `PORT` value to your desired port.

## How to use

To start saving the scan graph from the device, open the `main.py` file and press 'Start Listening'.

Afterwards, it should say `Connected to COM1` (or the set port in the `config.ini` file) in the text output below.

To start to actually start sending data from your spectrophotometer to the computer, run a scan and wait for it to finish, and press `VIEW RESULTS` and then `LIMS EXPORT`. If set up correctly, you will see text coming to the output area of the program. Wait for it to finish, and it will automatically prompt you to save it as a `.csv` file. Finally, open it in your desired plotting software.

## Limitations

This program will only work with the `SCAN` option on the spectrophotometer.

## Compatibility list

| Model | Status |
|:--------:|:--------:|
| Helios α (Alpha) | Not tested |
| Helios β (Beta) | Tested and working with `SCAN`|
| Helios γ (Gamma) | Not tested |
| Helios δ (Delta) | Not tested |

Other models such as the Unicam UV300, and Unicam UV500 may also work, but data is needed.
