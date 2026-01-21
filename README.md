# markd2pdf

A command-line tool to convert Markdown files to PDF with customizable themes.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Features

- Convert single files or entire directories recursively
- 5 built-in themes (github_dark, dracula, nord, minimal_light, professional_dark)
- Syntax highlighting for code blocks
- Support for tables, footnotes, admonitions, and table of contents
- Parallel processing for batch conversions

## Installation

### Prerequisites

WeasyPrint requires system dependencies:

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

### Install from source

```bash
git clone https://github.com/ramcharan/markd2pdf.git
cd markd2pdf
pip install -e .
```

## Usage

### Convert a single file

```bash
markd2pdf convert document.md ./output
```

### Convert a directory

```bash
markd2pdf convert ./docs ./output
```

### Specify a theme

```bash
markd2pdf convert document.md ./output --theme dracula
```

### List available themes

```bash
markd2pdf themes
```

## Themes

| Theme | Description |
|-------|-------------|
| `github_dark` | GitHub-style dark theme (default) |
| `dracula` | Dracula color scheme |
| `nord` | Nord color palette |
| `minimal_light` | Light theme for printing |
| `professional_dark` | Dark theme with blue accents |

## Custom Themes

Themes are CSS files located in the `styles/` directory. To create a custom theme:

1. Copy an existing theme file
2. Modify the CSS
3. Register the theme in `cli.py` by adding it to the `Theme` enum

## Supported Markdown Extensions

- Tables
- Fenced code blocks with syntax highlighting
- Table of contents (`[TOC]`)
- Admonitions
- Footnotes
- Definition lists
- Abbreviations

## Development

```bash
git clone https://github.com/ramcharan/markd2pdf.git
cd markd2pdf
uv sync --group dev

# Run linters
uv run black src/
uv run mypy src/
```

## License

MIT License. See [LICENSE](LICENSE) for details.
