# PythonProjectWithAI_2

This project implements a Tic-Tac-Toe game in Python with three modes:

- Console (command-line)
- GUI (using tkinter)
- Web (using Flask)

## Usage

Run the desired mode from the terminal:

```
python main.py console   # Console mode
python main.py gui       # GUI mode
python main.py web       # Web mode (Flask)
```

## Requirements
- Python 3.x
- tkinter (usually included with Python)
- Flask (for web mode)

Install Flask if needed:
```
pip install flask
```

## Project Structure
- `main.py` - Main application file with all game logic and modes
- `tic_tac_toe.html` - HTML template for the web version

## Features
- Abstract base class for shared game logic
- Console, GUI, and web interfaces
- Web mode uses a separate HTML template

## License
MIT

