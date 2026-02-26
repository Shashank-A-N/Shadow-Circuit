# ShadowCircuit AI & Editor PRO

ShadowCircuit AI is a complete web-based application that allows users to seamlessly design, render, and annotate complex electronic circuit topologies through natural language and a built-in graphical editor.

The project is composed of two main modules:
1. **Circuit AI Generator (`app.py`)**: A Flask-based web interface that uses NLP to interpret plain-text descriptions of circuits (e.g., "A 12V source connected to a 500 ohm resistor") and dynamically compiles them into schematic images using the `lcapy` library.
2. **ShadowCircuit Editor PRO (`editor_app.py`)**: A dedicated editor suite that provides tools to modify, annotate, and export generated circuit schematics with stamps (resistors, capacitors, diodes, nodes), freehand drawing, shapes, and text layers.

## Key Features

- **Natural Language Circuit Generation**: Synthesize complete circuits like BJT Amplifiers, MOSFETs, Op-Amps, Diode Rectifiers, Passive Filters, and Transformers just by typing.
- **Support for Custom Topologies**: Define intricate node-by-node custom schematic connections.
- **Robust Schema Rendering**: Under the hood, Python's `lcapy` translates abstract logic into beautifully rendered, high-quality PNGs.
- **Interactive Annotation Editor**:
  - Pen, Line, Rectangle, Eraser, and Text tools for freehand editing.
  - Quick-stamp commonly used symbols (Ground, Nodes, Resistors).
  - Built-in Undo/Redo history tracking.
- **Download and Export Capabilities**: Quickly save your fully rendered and annotated schematic representations.

## Prerequisites

Before running the application, ensure you have the following installed on your system:
- **Python 3.8+**
- **LaTeX Distribution**: You must have `texlive` or a similar LaTeX distribution installed and accessible in your system's PATH, as `lcapy` relies on `pdflatex` to render the schematic images.
  - Windows: [MiKTeX](https://miktex.org/download) or [TeX Live](https://tug.org/texlive/)
  - Linux: `sudo apt-get install texlive-full`
  - macOS: [MacTeX](https://tug.org/mactex/)
- **Ghostscript**: Required by `lcapy` for image conversions (e.g., PDF to PNG).
- **dvisvgm / pdf2svg / poppler-utils**: Necessary dependencies for generating clean outputs.

### Python Dependencies

You can install the Python-side requirements using `pip`. Typically, you'll need:
```bash
pip install Flask lcapy
```

## Project Structure

```text
.
├── app.py                     # Main Generator Flask App (Port 5000)
├── editor_app.py              # Editor Backup/Save Flask App (Port 5001)
├── generate_dataset.py        # Core generation logic using lcapy models
├── index.html                 # Frontend: AI Circuit Generator UI
├── editor.html                # Frontend: Circuit Editor UI
├── static/                    # Frontend assets (CSS, JS)
├── circuit_dataset/
│   ├── images/                # Output folder for raw generated circuit PNGs
│   └── edited_images/         # Output folder for user-edited circuit PNGs
└── test_*.py / *.png          # Unit test files and reference outputs
```

## How to Run the Application

The application requires both backend servers running simultaneously for full AI + Editing capabilities to function.

1. **Start the AI Generator App**
   Open a terminal window and run:
   ```bash
   python app.py
   ```
   This process will start the primary server on **http://127.0.0.1:5000**. Visit this address in your browser to start generating schematics.

2. **Start the Editor Backend App**
   Open a second terminal window and run:
   ```bash
   python editor_app.py
   ```
   This process will start the secondary server on **http://127.0.0.1:5001**. This server is responsible for listing the images in the workspace and saving annotated / edited versions of the circuits.

## Usage Guide

### 1. Generating a Circuit
- Navigate to `http://127.0.0.1:5000/`.
- Enter a natural language prompt, such as: *"Design a 15V common-emitter BJT amplifier with 1k resistor"* or *"Show me a low-pass Pi-filter with 10V input"*.
- Click **Initialize**. The server will process your text, infer the parameters, build the schematic diagram, and render it to your screen.

### 2. Editing a Circuit
- Below the generated blueprint, click the **Edit Circuit** button to open the editor view (`/editor`).
- The editor automatically fetches generated circuits from the `circuit_dataset/images` directory.
- Select your circuit from the right sidebar.
- Use the **Toolbar** above the canvas to change colors, draw new traces, erase misalignments, or add text labels.
- Select **Components** from the library panel to stamp symbols like grounds or nodes directly onto your circuit drawing.
- Click **Save Image** to persist your progress. Edited images are saved locally to `circuit_dataset/edited_images/`.

### 3. Quick Tags
The generator includes *Quick Tags* on the home page. Clicking these automatically injects pre-optimized prompts into your console to give you instantaneous layouts of common topologies.

## Troubleshooting

- **Server Crash on Generation**: Check your system's `pdflatex` configuration. Run `pdflatex --version` in your terminal to ensure it is installed and present in your system's PATH.
- **Images Not Showing in Editor**: Ensure you're running `editor_app.py` in conjunction with `app.py`. The editor fetches its image lists through its own API endpoints.
- **API Discrepancy Error**: Make sure your `generate_dataset.py` file is synced correctly with the parameters in `app.py`. Ensure that ports `5000` and `5001` are not being blocked by a local firewall.
