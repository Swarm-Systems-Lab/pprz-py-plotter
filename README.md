# pprz-py-plotter

Old repo: https://github.com/Pelochus/pprz-py-plotter

New version of Paparazzi's logplotter utility, focused around NumPy.

![GUI-Screenshot](https://github.com/Swarm-Systems-Lab/pprz-py-plotter/blob/master/img/screenshot.png)
_Screenshot under KDE Plasma 5, Breeze Dark theme_

## Quick Install (Ubuntu/Debian)

Run the following command:

```bash
curl https://raw.githubusercontent.com/Swarm-Systems-Lab/pprz-py-plotter/master/install.sh | sudo bash"
```

## Usage

First, install Python and NumPy on your system. If you didn't follow the quick install and are on Ubuntu/Debian based distros:

```bash
sudo apt install python3-full python3-numpy python3-matplotlib python3-lxml python3-pyqt5 -y
```

Then clone the repo:

```bash
git clone https://github.com/Swarm-Systems-Lab/pprz-py-plotter.git
cd pprz-py-plotter
```

Run with (GUI):

```bash
./pprz-py-plotter
```

Typical workflow will be as follows:

- Open pprz-py-plotter
- Select one folder which contains a `.log` file and a `.data` file. If there is more than one it will take the very first 2
- The program will parse for telemetry and datalink messages
- Inside the program select which ID do you want to see data for
- Select which variables do you want displayed with checkboxes. This is a little bit cumbersome to do, but works.
- Refresh the plot and see the data

Run (CLI):

```bash
./pprz-py-plotter-cli filename.data filename.log [-v/--verbose]
```

By default, this will convert the data to a NumPy array format, in a plain text file `.npy` file.
Results will be saved in the `output` folder, in folders, one with each message.
While running the CLI, you must enter manually which ID and message you want. The available messages and IDs will be listed.
For example, we want to extract the `INS` message from the example log, results will be like this:

```bash
output
└── INS
    ├── ins_xdd.npy
    ├── ins_xd.npy
    ├── ins_x.npy
    ├── ins_ydd.npy
    ├── ins_yd.npy
    ├── ins_y.npy
    ├── ins_zdd.npy
    ├── ins_zd.npy
    ├── ins_z.npy
    └── TIMESTAMP.npy
```

Where every file is a variable inside the message, plus the `TIMESTAMP` variable.
The `TIMESTAMP` variable **is NOT** part of the messages, it is extracted from the actual timestamp recorded by Paparazzi written into the `.data` file.

### Use of .npy files

To use `.npy` files output by the CLI version:

```python
import numpy as np
import matplotlib.pyplot as plt

var = np.loadtxt("ins_x.npy")
plt.plot(var)
plt.show()
```

You can also use the provided `matplotlib-example` file (instructions at the beginning of the file).

## Repo structure

This repository directory structure is as follows:

- `ìmg`: Contains the logo and image files
- `logs`: Example logs for testing. Extracted from a Bebop2's log in Paparazzi 6.4
- `pprzlogutils`: A small library for decoupling the functions and variables. Nothing too fancy.

## Useful Links

For usage with CLI, numpy and matplotlib:
- https://numpy.org/doc/stable/reference/generated/numpy.array.html
- https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html
