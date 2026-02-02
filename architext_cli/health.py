import subprocess
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def check_infrastructure():
    """Verifica Ollama y Llama3. Retorna True si todo está listo."""
    
    # 1. Verificar si Ollama existe en el sistema
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("\n[bold red]❌ OLLAMA NO DETECTADO[/bold red]")
        console.print("Architext necesita [bold]Ollama[/bold] para funcionar como cerebro local.")
        console.print("Descárgalo e instálalo desde: [link=https://ollama.com]https://ollama.com[/link]")
        console.print("Después de instalarlo, vuelve a ejecutar este comando.\n")
        return False

    # 2. Verificar si Llama3 está descargado
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if "llama3" not in result.stdout:
        console.print("\n[yellow]⚠️ MODELO LLAMA3 NO ENCONTRADO[/yellow]")
        console.print("Voy a descargar Llama3 por ti. Esto ocupa ~4.7GB y solo ocurre una vez.")
        
        try:
            with console.status("[bold blue]Descargando Llama3... (esto puede tardar unos minutos)[/bold blue]", spinner="dots"):
                subprocess.run(["ollama", "pull", "llama3"], check=True)
            console.print("[green]✓ Modelo Llama3 descargado correctamente.[/green]\n")
        except Exception as e:
            console.print(f"[red]Error al descargar el modelo: {e}[/red]")
            return False
            
    return True