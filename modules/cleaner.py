import os
import tempfile
from pathlib import Path


def get_temp_files_info():
    """
    Calcula o tamanho ocupado por pastas temporárias do sistema de forma rápida e segura.
    Limita a varredura para evitar atrasos em pastas temp muito grandes.
    """
    temp_dirs = []

    user_temp = tempfile.gettempdir()
    if user_temp:
        temp_dirs.append(Path(user_temp))

    if os.name == 'nt':
        win_temp = Path(os.environ.get('SystemRoot', 'C:\\Windows')) / 'Temp'
        if win_temp.exists() and win_temp not in temp_dirs:
            temp_dirs.append(win_temp)
    else:
        system_temp = Path('/tmp')
        if system_temp.exists() and system_temp not in temp_dirs:
            temp_dirs.append(system_temp)

    total_bytes = 0
    file_count = 0
    detailed_dirs = []

    for d in temp_dirs:
        dir_bytes = 0
        dir_files = 0
        MAX_FILES_TO_SCAN = 3000  # Limite de segurança para rapidez

        try:
            for root, _, files in os.walk(d):
                if dir_files >= MAX_FILES_TO_SCAN:
                    break
                for f in files:
                    if dir_files >= MAX_FILES_TO_SCAN:
                        break
                    try:
                        fp = os.path.join(root, f)
                        size = os.path.getsize(fp)
                        dir_bytes += size
                        dir_files += 1
                    except (PermissionError, OSError, FileNotFoundError):
                        continue
        except (PermissionError, OSError):
            pass

        total_bytes += dir_bytes
        file_count += dir_files

        detailed_dirs.append({
            "path": str(d),
            "tamanho_mb": round(dir_bytes / (1024 * 1024), 2),
            "ficheiros": dir_files,
        })

    total_gb = round(total_bytes / (1024 ** 3), 2)

    return {
        "total_gb": total_gb,
        "total_files": file_count,
        "detalhes": detailed_dirs,
    }
