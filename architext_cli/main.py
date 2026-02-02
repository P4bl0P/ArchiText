import typer
from pathlib import Path
from rich.console import Console
from .scanner import ProjectScanner
from .ai_engine import AIEngine
from .health import check_infrastructure

app = typer.Typer()
console = Console()

@app.callback(invoke_without_command=True)
def generate(
    ctx: typer.Context,
    path: Path = typer.Option(Path("."), "--path", "-p", help="Ruta del proyecto"),
    model: str = typer.Option("llama3", "--model", "-m", help="Modelo de IA"),
    lang: str = typer.Option("auto", "--lang", "-l", help="Idioma: 'es', 'en' o 'auto'"),
    custom_prompt: str = typer.Option("", "--prompt", "-pr", help="Instrucciones adicionales para la IA")
):
    """
    Comando principal: Genera o actualiza el README.md automáticamente.
    """
    # Si se ejecuta un subcomando (como scan), no ejecutamos la generación
    if ctx.invoked_subcommand:
        return

    if not check_infrastructure():
        raise typer.Exit(code=1)

    target_path = path.resolve()
    scanner = ProjectScanner(target_path)
    engine = AIEngine(model=model)

    console.print(f"[bold green]Architext[/bold green] Actualizando documentación en: [white]{target_path}[/white]")

    with console.status("[bold blue]Analizando cambios en el proyecto...[/bold blue]"):
        ecosystem = scanner.detect_ecosystem()
        structure = scanner.get_structure()
        context = scanner.get_key_contents()
        

        new_readme = engine.generate_readme(ecosystem, structure, context, lang=lang, extra_instructions=custom_prompt)

    if "Error" in new_readme or "⚠️" in new_readme:
        console.print(f"[bold red]{new_readme}[/bold red]")
    else:
        console.print("[bold green]✓ IA ha respondido con éxito.[/bold green]")
        # Opcional: ver los primeros 50 caracteres
        # console.print(f"[dim]{new_readme[:50]}...[/dim]")

    # Escritura del archivo en la raíz del proyecto analizado
    readme_path = target_path / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)

    console.print(f"[bold green]¡Hecho! {readme_path.name} ha sido actualizado en idioma '{lang}'.[/bold green]")

@app.command()
def scan(path: Path = typer.Argument(Path("."), help="Ruta a analizar")):
    """
    Función auxiliar: Solo muestra qué archivos detecta el scanner.
    """
    scanner = ProjectScanner(path.resolve())
    console.print(scanner.get_structure())

if __name__ == "__main__":
    app()