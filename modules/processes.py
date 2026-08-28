import psutil
import config


def get_top_processes(count=config.TOP_PROCESSES_COUNT):
    """
    Retorna os processos que mais consomem CPU e RAM.
    Trata erros de permissão e processos encerrados dinamicamente.
    """
    processes = []

    # Primeira passagem para inicializar cpu_percent se necessário
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
        try:
            info = proc.info
            # Filtrar dados válidos
            pid = info.get('pid')
            name = info.get('name') or "Desconhecido"
            cpu = info.get('cpu_percent') or 0.0
            ram_percent = info.get('memory_percent') or 0.0

            mem_info = info.get('memory_info')
            ram_mb = round(mem_info.rss / (1024 * 1024), 1) if mem_info else 0.0

            processes.append({
                "pid": pid,
                "name": name,
                "cpu_percent": round(cpu, 1),
                "ram_percent": round(ram_percent, 1),
                "ram_mb": ram_mb,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Ordenar por CPU
    top_cpu = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:count]

    # Ordenar por RAM
    top_ram = sorted(processes, key=lambda p: p['ram_mb'], reverse=True)[:count]

    return {
        "top_cpu": top_cpu,
        "top_ram": top_ram,
    }
