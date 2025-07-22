# PDF Toolbox – PDF File Manipulation with Python

**PDF Toolbox** is an open-source project that provides a complete suite of tools for manipulating, analyzing, and transforming PDF files using Python. It is designed for both beginners and advanced users looking to automate or simplify tasks related to PDF documents.

---

## Contents

* [Overview](#overview)
* [Features](#features)
* [Project Structure and File Usage](#project-structure-and-file-usage)
* [Installation](#installation)
* [Usage](#usage)

  * [Using Jupyter Notebooks](#using-jupyter-notebooks)
  * [Using the GUI Application](#using-the-gui-application)
* [Possible Extensions](#possible-extensions)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgements](#acknowledgements)

---

## Overview

The project aims to:

* Merge, split, extract text or images, protect, compress, and edit PDFs.
* Provide two approaches: through educational Jupyter notebooks and a user-friendly GUI application (Tkinter).

---

##  Features

Key functionalities available in the toolbox:

*  Add password protection
*  Remove password protection
*  Merge multiple PDF files
*  Split a PDF into several files
*  Extract text from pages
*  Extract embedded images
*  Reorganize or rotate pages
*  Delete specific pages
*  Read/modify metadata
*  Compress to reduce file size

---

## Project Structure and File Usage

### Jupyter Notebooks

Each notebook demonstrates a specific functionality with practical examples:

* **1\_combine\_multiple\_PDF\_files\_into\_one.ipynb** – Merge multiple PDF files into a single document.
* **2\_Split\_single\_PDF\_into\_multiple\_PDFs.ipynb** – Split one PDF into several (one file per page).
* **3\_Extract\_text\_content\_from\_PDF\_pages.ipynb** – Extract text content from each page.
* **4\_Extract\_embedded\_images\_from\_PDF\_files.ipynb** – Extract all embedded images from a PDF.
* **5\_Add\_password\_protection\_to\_PDF\_files.ipynb** – Add password protection to a PDF.
* **6\_Remove\_password\_protection\_from\_PDF\_files.ipynb** – Remove password protection.
* **7\_Reorder\_or\_delete\_pages\_within\_PDF.ipynb** – Reorder or delete specific pages.
* **8\_Rotate\_Individual\_Pages\_in\_PDF.ipynb** – Rotate one or more pages.
* **9\_Read\_add\_modify\_metadata\_in\_PDF.ipynb** – Read, add or edit metadata.
* **Compres\_optimize\_PDF\_files\_for\_reduced\_file\_size.ipynb** – Compress and optimize PDF size.

### Folders

* **data/** – Contains sample PDF files for testing.
* **out/** – Output directory for generated files.
* **tools/** – Contains the GUI tool: `pdf_toolbox.py`

---

## Installation

### Prerequisites

* Python 3.7 or higher

### Install dependencies

```bash
pip install PyPDF2 PyMuPDF
```

> **Note:**
>
> * `tkinter` is included by default on Windows and macOS.
> * On Linux, install it if necessary:
>
>   * Ubuntu/Debian: `sudo apt install python3-tk`
>   * Fedora: `sudo dnf install python3-tkinter`
>   * Arch: `sudo pacman -S tk`

### (Optional) For improved UI appearance:

```bash
pip install ttkthemes
```

---

## Usage

### Using Jupyter Notebooks

1. Open the desired notebook in Jupyter.
2. Follow the instructions and adjust paths if needed.
3. Outputs will be saved in the `out/` folder.

### Using the GUI Application

```bash
python tools/pdf_toolbox.py
```

* Use the interface to select your files and apply operations.
* Outputs can be saved wherever you choose.

---

## Possible Extensions

* Add OCR support using `pytesseract` or `pdfplumber`
* Add theming system or multilingual interface
* Add digital signature or annotation tools
* Generate automated PDF analysis reports

---

## Contributing

**Contributions are welcome!**
Whether it's fixing a bug, enhancing a feature, or suggesting a new one:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/your-username/pdf-toolbox.git`
3. **Create a branch**: `git checkout -b feature/improvement`
4. **Submit a pull request**

Feel free to open **issues** for questions or ideas.

---

## License

This project is licensed under the **MIT License**.

---

## Acknowledgements

Developed with ❤️ by [**Oussama Taghlaoui**](https://github.com/Ouss-tagh-dev)  
© 2025 – Free and open-source project

---
