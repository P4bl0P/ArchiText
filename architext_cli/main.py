import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from .scanner import ProjectScanner

app = typer.Typer(help="Architext - Generador de Documentación Profesional.")
console = Console()

@app.command()
def scan(
    path: Path = typer.Option(Path("."), help="Ruta del proyecto a analizar")
):
    """Analiza la estructura de un directorio."""
    
    # Normalizamos la ruta absoluta
    target_path = path.resolve()
    
    if not target_path.exists():
        console.print(f"[bold red]Error:[/bold red] La ruta '{target_path}' no existe.")
        raise typer.Exit(1)

    console.print(Panel.fit(
        f"🔍 [bold blue]Architext[/bold blue]\n[dim]Escaneando:[/dim] [white]{target_path}[/white]", 
        border_style="blue"
    ))

    scanner = ProjectScanner(target_path)
    
    with console.status("[bold yellow]Analizando estructura...[/bold yellow]"):
        structure = scanner.get_structure()
    
    console.print("\n[bold yellow]📂 Estructura detectada:[/bold yellow]")
    console.print(structure)
    
    console.print("\n[bold yellow]📄 Buscando contenido clave...[/bold yellow]")
    content = scanner.get_key_contents()
    
    if content:
        console.print("[bold green]✅ Archivos clave analizados correctamente.[/bold green]")
    else:
        console.print("[bold red]⚠ No se encontraron archivos de configuración conocidos.[/bold red]")

if __name__ == "__main__":
    app()