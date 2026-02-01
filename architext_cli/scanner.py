import os

class ProjectScanner:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        # Carpetas que no se leen
        self.ignore_dirs = {
            '.git', '__pycache__', 'node_modules', 'venv', 
            '.venv', 'env', 'dist', 'build', '.next', '.idea'
        }
        
        self.ignore_exts = {
            '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', 
            '.pyc', '.exe', '.dll', '.so', '.bin', '.pdf'
        }

    def get_structure(self):
        """Genera un mapa visual de las carpetas del proyecto."""
        structure = []
        for root, dirs, files in os.walk(self.root_dir):
            # Filtrar carpetas ignoradas
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            level = root.replace(self.root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                if not any(f.endswith(ext) for ext in self.ignore_exts):
                    structure.append(f"{sub_indent}{f}")
        return "\n".join(structure)

    def get_key_files_content(self):
        """Lee archivos críticos para entender el proyecto."""
        # Archivos para entender el proyecto
        key_patterns = ['package.json', 'requirements.txt', 'Dockerfile', 'docker-compose.yml', 'main.py', 'index.js', 'App.js']
        content_summary = ""

        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            for f in files:
                if f in key_patterns:
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as content:
                            content_summary += f"\n--- Archivo: {f} ---\n"
                            
                            content_summary += "".join(content.readlines()[:100])
                    except Exception as e:
                        content_summary += f"\nError leyendo {f}: {e}\n"
        return content_summary