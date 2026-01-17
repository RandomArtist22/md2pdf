# Mark2PDF

A CLI tool to recursively convert a directory of Markdown files into formatted PDFs.

## Setup

1.  **Prerequisites:** 
    - Python 3 
2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

    *Note: You may need to install some system dependencies for `weasyprint` (like Pango, GDK-Pixbuf). On Arch/Manjaro/Linux: `sudo pacman -S pango gdk-pixbuf2` or `sudo apt install libpango-1.0-0 libpdk-pixbuf-2.0-0`.*

## Usage

Run the script pointing to your input folder and desired output folder:

```bash
python main.py /path/to/markdown/files /path/to/output/pdfs
```

### Example

```bash
python main.py ~/Documents/Notes ~/Documents/PDF_Notes
```

The tool will mirror your directory structure in the output folder.
