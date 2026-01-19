import os
from enum import Enum
import typer
import markdown
from weasyprint import HTML, CSS
from pathlib import Path
from rich.console import Console
from rich.progress import track
from rich.panel import Panel
from rich.table import Table
from pygments.formatters import HtmlFormatter

app = typer.Typer(
    help="Convert Markdown files to beautifully styled PDFs",
    add_completion=False
)
console = Console()

# Styles directory
STYLES_DIR = Path(__file__).parent / "styles"

# Available themes
class Theme(str, Enum):
    professional_dark = "professional_dark"
    dracula = "dracula"
    minimal_light = "minimal_light"
    nord = "nord"
    github_dark = "github_dark"

# Theme descriptions for help
THEME_DESCRIPTIONS = {
    Theme.professional_dark: "Sophisticated dark theme with blue accents (default)",
    Theme.dracula: "Popular Dracula color scheme with vibrant neon accents",
    Theme.minimal_light: "Clean, professional light theme for formal documents",
    Theme.nord: "Arctic-inspired blue-ish color scheme, easy on the eyes",
    Theme.github_dark: "Familiar GitHub-inspired dark theme for developers",
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

def convert_md_to_pdf(input_file: Path, output_file: Path, theme: Theme):
    """
    Converts a single markdown file to PDF using the specified theme.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Generate Pygments CSS for syntax highlighting
        # Use theme-appropriate Pygments style
        pygments_style = THEME_PYGMENTS_STYLES.get(theme, "monokai")
        try:
            pygments_css = HtmlFormatter(style=pygments_style).get_style_defs('.codehilite')
        except Exception:
            # Fallback to monokai if the style is not available
            pygments_css = HtmlFormatter(style='monokai').get_style_defs('.codehilite')

        # Convert Markdown to HTML
        # Using extensions for tables, fenced code blocks, and syntax highlighting
        html_content = markdown.markdown(
            text, 
            extensions=[
                'tables', 
                'fenced_code', 
                'codehilite', 
                'toc',
                'sane_lists',
                'smarty',
                'admonition',
                'attr_list',
                'abbr',
                'def_list',
                'footnotes',
                'md_in_html'
            ]
        )

        # Read CSS content
        stylesheet_path = get_stylesheet_path(theme)
        with open(stylesheet_path, 'r', encoding='utf-8') as f:
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
    input_dir: Path = typer.Argument(..., help="Directory containing Markdown files to convert", exists=True, file_okay=True),
    output_dir: Path = typer.Argument(..., help="Directory to save the generated PDFs"),
    theme: Theme = typer.Option(Theme.professional_dark, "--theme", "-t", help="CSS theme to use for styling"),
):
    """
    Recursively converts a directory of Markdown files to PDFs.
    """
    
    # Verify theme stylesheet exists
    stylesheet_path = get_stylesheet_path(theme)
    if not stylesheet_path.exists():
        console.print(f"[bold red]Error:[/bold red] Theme stylesheet not found: {stylesheet_path}")
        raise typer.Exit(1)
    
    # File finding
    md_files = []

    # Conditon for single file running.
    if str(input_dir).lower().endswith('.md'):
        md_files.append(input_dir)
    else:
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith('.md'):
                    md_files.append(Path(root) / file)

    if not md_files:
        console.print("[yellow]No markdown files found in the specified directory.[/yellow]")
        return

    # Display conversion info
    console.print(Panel.fit(
        f"[bold]Theme:[/bold] {theme.value}\n"
        f"[bold]Files:[/bold] {len(md_files)} markdown files\n"
        f"[bold]Output:[/bold] {output_dir}",
        title="📄 MD2PDF Conversion",
        border_style="blue"
    ))

    # Processing the files 
    for md_file in track(md_files, description="Converting..."):
        rel_path = md_file.relative_to(input_dir)
        if rel_path.stem:
            out_file_path = output_dir / rel_path.with_suffix('.pdf')
        else:
            out_file_path = output_dir / Path(input_dir.name).with_suffix('.pdf')
        out_file_path.parent.mkdir(parents=True, exist_ok=True)
        convert_md_to_pdf(md_file, out_file_path, theme)

    console.print(f"\n[bold green]✓ Done![/bold green] PDFs saved to: [cyan]{output_dir}[/cyan]")


@app.command("themes")
def list_themes():
    """
    List all available PDF themes with descriptions.
    """
    table = Table(title="🎨 Available Themes", show_header=True, header_style="bold magenta")
    table.add_column("Theme Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    
    for theme in Theme:
        description = THEME_DESCRIPTIONS.get(theme, "No description available")
        table.add_row(theme.value, description)
    
    console.print(table)
    console.print("\n[dim]Use --theme <name> with the convert command to select a theme.[/dim]")


if __name__ == "__main__":
    app()
