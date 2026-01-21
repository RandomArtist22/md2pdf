import os
from collections.abc import Callable
from enum import Enum
from functools import wraps
from multiprocessing import Pool
from pathlib import Path
from typing import Any, TypeVar

import markdown
import typer
from pygments.formatters import HtmlFormatter
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.table import Table
from weasyprint import CSS, HTML  # type: ignore

app = typer.Typer(
    help="Convert Markdown files to beautifully styled PDFs", add_completion=False
)
console = Console()

# Styles directory
STYLES_DIR = Path(__file__).parent / "styles"


# Available themes
class Theme(str, Enum):
    github_dark = "github_dark"
    dracula = "dracula"
    nord = "nord"
    minimal_light = "minimal_light"
    professional_dark = "professional_dark"


# Theme descriptions for help
THEME_DESCRIPTIONS = {
    Theme.github_dark: "GitHub-inspired dark theme (default)",
    Theme.dracula: "Dracula color scheme with neon accents",
    Theme.nord: "Arctic-inspired, easy on the eyes",
    Theme.minimal_light: "Clean light theme for printing",
    Theme.professional_dark: "Sophisticated dark with blue accents",
}

# Map themes to Pygments styles for syntax highlighting
THEME_PYGMENTS_STYLES = {
    Theme.professional_dark: "github-dark",
    Theme.dracula: "dracula",
    Theme.minimal_light: "friendly",
    Theme.nord: "nord",
    Theme.github_dark: "github-dark",
}


def get_stylesheet_path(theme: Theme) -> Path:
    """Get the stylesheet path for the given theme."""
    return STYLES_DIR / f"{theme.value}.css"


F = TypeVar("F", bound=Callable[..., Any])


def starwrapper(func: F) -> Callable[[tuple[Any, ...]], Any]:
    @wraps(func)
    def wrapper(args: tuple[Any, ...]) -> Any:
        return func(*args)

    return wrapper


@starwrapper
def convert_md_to_pdf(input_file: Path, output_file: Path, theme: Theme) -> None:
    """
    Converts a single markdown file to PDF using the specified theme.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        # Generate Pygments CSS for syntax highlighting
        # Use theme-appropriate Pygments style
        pygments_style = THEME_PYGMENTS_STYLES.get(theme, "monokai")
        try:
            pygments_css = HtmlFormatter(style=pygments_style).get_style_defs(
                ".codehilite"
            )
        except Exception:
            # Fallback to monokai if the style is not available
            pygments_css = HtmlFormatter(style="monokai").get_style_defs(".codehilite")

        # Convert Markdown to HTML
        # Using extensions for tables, fenced code blocks, and syntax highlighting
        html_content = markdown.markdown(
            text,
            extensions=[
                "tables",
                "fenced_code",
                "codehilite",
                "toc",
                "sane_lists",
                "smarty",
                "admonition",
                "attr_list",
                "abbr",
                "def_list",
                "footnotes",
                "md_in_html",
            ],
        )

        # Read CSS content
        stylesheet_path = get_stylesheet_path(theme)
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            css_content = f.read()

        # Wrap in a full HTML document structure
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                {pygments_css}
                {css_content}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # Write to PDF
        HTML(string=full_html, base_url=str(input_file.parent)).write_pdf(output_file)

    except Exception as e:
        console.print(f"[bold red]Error converting {input_file.name}:[/bold red] {e}")


@app.command("convert")
def convert(
    input_path: Path = typer.Argument(
        ...,
        help="Markdown file or directory containing Markdown files to convert",
        exists=True,
        file_okay=True,
    ),
    output_dir: Path = typer.Argument(..., help="Directory to save the generated PDFs"),
    theme: Theme = typer.Option(
        Theme.github_dark, "--theme", "-t", help="CSS theme to use for styling"
    ),
) -> None:
    """
    Recursively converts a directory of Markdown files to PDFs.
    """

    # Verify theme stylesheet exists
    stylesheet_path = get_stylesheet_path(theme)
    if not stylesheet_path.exists():
        console.print(
            f"[bold red]Error:[/bold red] Theme stylesheet not found: {stylesheet_path}"
        )
        raise typer.Exit(1)

    # File finding
    md_files = []

    # Condition for single file running.
    if str(input_path).lower().endswith(".md"):
        md_files.append(input_path)
    else:
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(".md"):
                    md_files.append(Path(root) / file)

    if not md_files:
        console.print(
            "[yellow]No markdown files found in the specified directory.[/yellow]"
        )
        return

    # Display conversion info
    console.print(
        Panel.fit(
            f"[bold]Theme:[/bold] {theme.value}\n"
            f"[bold]Files:[/bold] {len(md_files)} markdown files\n"
            f"[bold]Output:[/bold] {output_dir}",
            title="📄 MD2PDF Conversion",
            border_style="blue",
        )
    )

    # Processing the files
    md_file_args = []

    for md_file in md_files:
        rel_path = md_file.relative_to(input_path)
        if rel_path.stem:
            out_file_path = output_dir / rel_path.with_suffix(".pdf")
        else:
            out_file_path = output_dir / Path(input_path.name).with_suffix(".pdf")
        out_file_path.parent.mkdir(parents=True, exist_ok=True)
        md_file_args.append((md_file, out_file_path, theme))

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        transient=True,
    ) as progress:

        with Pool(4) as pool:
            main_task = progress.add_task(
                description="Converting...", total=len(md_file_args)
            )

            for result in pool.imap_unordered(convert_md_to_pdf, md_file_args):
                progress.update(main_task, advance=1)

    console.print(
        f"\n[bold green]✓ Done![/bold green] PDFs saved to: [cyan]{output_dir}[/cyan]"
    )


@app.command("themes")
def list_themes() -> None:
    """
    List all available PDF themes with descriptions.
    """
    table = Table(
        title="🎨 Available Themes", show_header=True, header_style="bold magenta"
    )
    table.add_column("Theme Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    for theme in Theme:
        description = THEME_DESCRIPTIONS.get(theme, "No description available")
        table.add_row(theme.value, description)

    console.print(table)
    console.print(
        "\n[dim]Use --theme <name> with the convert command to select a theme.[/dim]"
    )


if __name__ == "__main__":
    app()
