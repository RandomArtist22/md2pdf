# Mark2PDF

A CLI tool to recursively convert a directory of Markdown files into beautifully styled PDFs.

## Features

- 🎨 **Multiple Themes** - Choose from 5 professionally designed themes
- 📁 **Recursive Conversion** - Processes entire directory trees
- 🖍️ **Syntax Highlighting** - Full code block highlighting with Pygments
- 📝 **Rich Markdown Support** - Tables, admonitions, footnotes, TOC, and more

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

    *Note: You may need to install some system dependencies for `weasyprint` (like Pango, GDK-Pixbuf). On Arch/Manjaro/Linux: `sudo pacman -S pango gdk-pixbuf2` or on Debian/Ubuntu: `sudo apt install libpango-1.0-0 libgdk-pixbuf-2.0-0`.*

## Usage

### Basic Conversion

```bash
python main.py convert /path/to/markdown/files /path/to/output/pdfs
```

### With Theme Selection

```bash
python main.py convert /path/to/input /path/to/output --theme professional_dark
```

### List Available Themes

```bash
python main.py themes
```

## Available Themes

| Theme | Description |
|-------|-------------|
| `professional_dark` | Sophisticated dark theme with blue accents (default) |
| `dracula` | Popular Dracula color scheme with vibrant neon accents |
| `minimal_light` | Clean, professional light theme for formal documents |
| `nord` | Arctic-inspired blue-ish color scheme, easy on the eyes |
| `github_dark` | Familiar GitHub-inspired dark theme for developers |

## Examples

### Using the Professional Dark Theme (default)

```bash
python main.py convert ~/Documents/Notes ~/Documents/PDF_Notes
```

### Using the Nord Theme

```bash
python main.py convert ~/Documents/Notes ~/Documents/PDF_Notes -t nord
```

### Using the Light Theme for Printing

```bash
python main.py convert ~/Documents/Notes ~/Documents/PDF_Notes --theme minimal_light
```

The tool will mirror your directory structure in the output folder.

## Customizing Themes

All theme stylesheets are located in the `styles/` directory. You can modify existing themes or create new ones by adding a new `.css` file and registering it in `main.py`.
