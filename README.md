<div align="center">

# 📄 markd2pdf

**Transform your Markdown into beautifully styled PDFs**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Features](#-features) •
[Installation](#-installation) •
[Usage](#-usage) •
[Themes](#-themes) •
[Configuration](#%EF%B8%8F-configuration)

</div>

---

## ✨ Features

- 🎨 **5 Themes** — Professional dark, Dracula, Nord, GitHub Dark, and Minimal Light
- 📁 **Batch Processing** — Convert entire directory trees recursively
- 🖍️ **Syntax Highlighting** — Full code block highlighting powered by Pygments
- 📝 **Rich Markdown** — Tables, admonitions, footnotes, TOC, abbreviations, and more
- ⚡ **Parallel Processing** — Multi-threaded conversion for speed
- 🎯 **Single File Mode** — Convert individual files or entire directories

---

## 📦 Installation

### Prerequisites

- **Python 3.12+**
- **System dependencies** for WeasyPrint:

  ```bash
  # Arch / Manjaro
  sudo pacman -S pango gdk-pixbuf2

  # Debian / Ubuntu
  sudo apt install libpango-1.0-0 libgdk-pixbuf-2.0-0

  # macOS
  brew install pango gdk-pixbuf
  ```

### Install from PyPI

```bash
pip install markd2pdf
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install markd2pdf
```

### Install from Source (Development)

```bash
git clone https://github.com/ramcharan/markd2pdf.git
cd markd2pdf
uv sync  # or: pip install -e .
```

---

## 🚀 Usage

### Quick Start

```bash
# Convert a single file
markd2pdf convert README.md ./output

# Convert an entire directory
markd2pdf convert ./docs ./pdf-output

# Use a specific theme
markd2pdf convert ./docs ./output --theme dracula
```

### Commands

```
Usage: markd2pdf [OPTIONS] COMMAND [ARGS]...

Commands:
  convert   Convert Markdown files to PDFs
  themes    List all available themes
```

### Convert Command

```
Usage: markd2pdf convert [OPTIONS] INPUT_PATH OUTPUT_DIR

Arguments:
  INPUT_PATH  Markdown file or directory to convert  [required]
  OUTPUT_DIR  Directory to save the generated PDFs   [required]

Options:
  -t, --theme [github_dark|dracula|nord|minimal_light|professional_dark]
              CSS theme to use for styling  [default: github_dark]
  --help      Show this message and exit
```

### Examples

```bash
# Convert all markdown files in a directory
markd2pdf convert ~/Documents/notes ~/Documents/pdfs

# Convert with the Nord theme
markd2pdf convert ~/notes ~/pdfs -t nord

# Convert a single file with Dracula theme
markd2pdf convert ./README.md ./output --theme dracula

# List available themes
markd2pdf themes
```

---

## 🎨 Themes

| Theme | Description |
|:------|:------------|
| `github_dark` | GitHub-inspired dark theme **(default)** |
| `dracula` | Dracula color scheme with neon accents |
| `nord` | Arctic-inspired, easy on the eyes |
| `minimal_light` | Clean light theme for printing |
| `professional_dark` | Sophisticated dark with blue accents |

Preview themes:

```bash
markd2pdf themes
```

```
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Theme Name        ┃ Description                          ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ github_dark       │ GitHub-inspired dark theme (default) │
│ dracula           │ Dracula color scheme with neon       │
│ nord              │ Arctic-inspired, easy on the eyes    │
│ minimal_light     │ Clean light theme for printing       │
│ professional_dark │ Sophisticated dark with blue accents │
└───────────────────┴──────────────────────────────────────┘
```

---

## ⚙️ Configuration

### Customizing Themes

All theme stylesheets are in the `styles/` directory. To create a custom theme:

1. **Create a new CSS file:**
   ```bash
   cp styles/professional_dark.css styles/my_theme.css
   ```

2. **Edit the theme in `main.py`:**
   ```python
   class Theme(str, Enum):
       professional_dark = "professional_dark"
       dracula = "dracula"
       minimal_light = "minimal_light"
       nord = "nord"
       github_dark = "github_dark"
       my_theme = "my_theme"  # Add your theme
   ```

3. **Add a description:**
   ```python
   THEME_DESCRIPTIONS = {
       # ...existing themes...
       Theme.my_theme: "My custom theme description",
   }
   ```

### Markdown Extensions

markd2pdf supports these Markdown extensions out of the box:

| Extension | Description |
|:----------|:------------|
| `tables` | GitHub-style tables |
| `fenced_code` | Triple-backtick code blocks |
| `codehilite` | Syntax highlighting |
| `toc` | Table of contents with `[TOC]` |
| `admonition` | Note/warning/tip blocks |
| `footnotes` | Footnote references |
| `attr_list` | HTML attributes on elements |
| `def_list` | Definition lists |
| `abbr` | Abbreviations |
| `md_in_html` | Markdown inside HTML blocks |

---

## 🛠️ Development

```bash
# Clone the repo
git clone https://github.com/yourusername/markd2pdf.git
cd markd2pdf

# Install dev dependencies
uv sync --group dev

# Run linters
uv run black main.py
uv run isort main.py
uv run mypy main.py

# Run pre-commit hooks
uv run pre-commit run --all-files
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Made with ❤️ and Python**

[⬆ Back to top](#-markd2pdf)

</div>
