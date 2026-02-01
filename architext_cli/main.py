import typer
from rich.console import Console
from rich.panel import Panel
from .scanner import ProjectScanner

# Inicializamos la consola de Rich y la app de Typer
app = typer.Typer(name="Architext", help="Generador automático de documentación técnica.")
console = Console()

@app.command()
def scan(path: str = typer.Argument(".", help="Ruta del proyecto a analizar")):
    """
    Analiza un directorio y muestra qué información enviaría a la IA.
    """
    console.print(Panel.fit("🔍 [bold blue]Architext[/bold blue] - Escaneando proyecto...", border_style="blue"))
    
    scanner = ProjectScanner(path)
    
    # 1. Obtener estructura
    structure = scanner.get_structure()
    console.print("\n[bold yellow]📂 Estructura detectada:[/bold yellow]")
    console.print(structure)
    
    # 2. Obtener archivos clave
    console.print("\n[bold yellow]📄 Analizando archivos de configuración...[/bold yellow]")
    content = scanner.get_key_files_content()
    
    if content:
        console.print("[green]✅ Archivos clave encontrados y leídos.[/green]")
    else:
        console.print("[red]⚠ No se encontraron archivos de configuración clave.[/red]")

    console.print("\n[bold green]Listo.[/bold green] El scanner funciona correctamente.")

if __name__ == "__main__":
    app()