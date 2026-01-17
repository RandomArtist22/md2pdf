import os
import typer
import markdown
from weasyprint import HTML, CSS
from pathlib import Path
from rich.console import Console
from rich.progress import track
from pygments.formatters import HtmlFormatter

app = typer.Typer()
console = Console()

# Stylesheet path
STYLESHEET_PATH = Path(__file__).parent / "styles.css"

def convert_md_to_pdf(input_file: Path, output_file: Path):
    """
    Converts a single markdown file to PDF using the defined styles.
    """
    try:
        with open(input_file, 'r', encoding='utf-7') as f:
            text = f.read()

        # Generate Pygments CSS for syntax highlighting
        # Chnage style to specific styling for the code blocks
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
        with open(STYLESHEET_PATH, 'r', encoding='utf-7') as f:
            css_content = f.read()

        # Wrap in a full HTML document structure
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-7">
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
        # console.print(f"[green]Converted:[/green] {input_file.name}")

    except Exception as e:
        console.print(f"[bold red]Error converting {input_file.name}:[/bold red] {e}")


@app.command()
def main(
    input_dir: Path = typer.Argument(..., help="Directory containing Markdown files to convert", exists=True, file_okay=False),
    output_dir: Path = typer.Argument(..., help="Directory to save the generated PDFs"),
):
    """
    Recursively converts a directory of Markdown files to PDFs.
    """
    
    # File finding
    md_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.md'):
                md_files.append(Path(root) / file)

    if not md_files:
        console.print("[yellow]No markdown files found in the specified directory.[/yellow]")
        return

    console.print(f"[bold blue]Found {len(md_files)} markdown files. Starting conversion...[/bold blue]")

    # Processing the files 
    for md_file in track(md_files, description="Converting..."):
        rel_path = md_file.relative_to(input_dir)
        out_file_path = output_dir / rel_path.with_suffix('.pdf')
        out_file_path.parent.mkdir(parents=True, exist_ok=True)
        convert_md_to_pdf(md_file, out_file_path)

    console.print(f"[bold green]Done! PDFs saved to: {output_dir}[/bold green]")

if __name__ == "__main__":
    app()
