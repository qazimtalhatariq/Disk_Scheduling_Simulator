# Disk Scheduling Simulator

A modern Python desktop app for visualizing disk scheduling algorithms. This simulator uses Tkinter for the GUI and Matplotlib for graph visualization.

## Features

- Responsive dark-themed interface
- Disk request and head position input
- Supports algorithms:
  - `FCFS` (First Come First Served)
  - `SSTF` (Shortest Seek Time First)
  - `SCAN` (Elevator Algorithm)
  - `C-SCAN` (Circular SCAN)
- Fullscreen toggle with `F11` / `Esc`
- Live plot of disk head movement and track sequence

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/qazimtalhatariq/Disk_Scheduling_Simulator.git
   cd Disk_Scheduling_Simulator
   ```

2. Install dependencies:
   ```bash
   pip install matplotlib
   ```

## Usage

Run the simulator:

```bash
python main.py
```

Enter disk requests as a comma-separated list and set the starting head position. Select an algorithm, then click **Simulate** or press **Enter**.

## Notes

- The GUI is optimized for readability with larger fonts and a clean layout.
- `C-SCAN` is included as a circular scan algorithm with a jump from one disk end to the opposite end.

## Files

- `main.py` — main application file
- `README.md` — project overview and usage

## Requirements

- Python 3.8+
- `tkinter` (bundled with Python on most platforms)
- `matplotlib`

## License

This repository is provided as-is for learning and demonstration purposes.