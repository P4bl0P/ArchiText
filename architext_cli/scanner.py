from pathlib import Path

class ProjectScanner:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        # Carpetas
        self.ignore_dirs = {
            '.git', '__pycache__', 'node_modules', 'venv', '.venv', 
            'dist', 'build', 'architext.egg-info', '.vscode'
        }
        # Archivos
        self.ignore_files = {
            '.gitignore', 'pyproject.toml', 'LICENSE', '.env', 'package-lock.json', "README_ARCHITEXT.md"
        }
        # Extensiones
        self.ignore_exts = {
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', 
            '.pyc', '.exe', '.dll', '.so', '.bin', '.pdf'
        }

    def get_structure(self) -> str:
        """Genera un mapa visual del proyecto usando Path.rglob."""
        lines = [f"{self.root_path.name}/"]
        
        # Ordenamos para que el resultado sea predecible
        paths = sorted(self.root_path.rglob("*"))
        
        for path in paths:
            # Comprobar si el path o alguno de sus padres está en la lista de ignorados
            if any(part in self.ignore_dirs for part in path.parts):
                continue
            if path.name in self.ignore_files or path.suffix in self.ignore_exts:
                continue

            # Calcular nivel de profundidad para la indentación
            depth = len(path.relative_to(self.root_path).parts)
            indent = "    " * depth
            
            if path.is_dir():
                lines.append(f"{indent}{path.name}/")
            else:
                lines.append(f"{indent}{path.name}")
                
        return "\n".join(lines)

    def get_key_contents(self) -> str:
        """Busca y lee los archivos de configuración más importantes."""
        key_files = ['package.json', 'requirements.txt', 'Dockerfile', 'main.py']
        summary = ""
        
        for name in key_files:
            # Buscamos el archivo en cualquier lugar del proyecto (que no esté ignorado)
            for path in self.root_path.rglob(name):
                if any(part in self.ignore_dirs for part in path.parts):
                    continue
                
                try:
                    content = path.read_text(encoding='utf-8').splitlines()[:100]
                    summary += f"\n--- Archivo: {path.relative_to(self.root_path)} ---\n"
                    summary += "\n".join(content) + "\n"
                except Exception as e:
                    summary += f"\nError leyendo {name}: {e}\n"
        return summary