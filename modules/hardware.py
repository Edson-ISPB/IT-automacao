import platform
import socket
import time
import psutil


def get_system_info():
    """Retorna informações gerais do sistema operacional e computador."""
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_days = round(uptime_seconds / 86400, 2)
    except Exception:
        uptime_days = 0.0

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor() or "Processador Genérico",
        "uptime_days": uptime_days,
    }


def get_cpu_info():
    """Retorna informações de contagem de núcleos e percentual de uso do CPU."""
    try:
        uso = psutil.cpu_percent(interval=1)
        cores_fisicos = psutil.cpu_count(logical=False) or psutil.cpu_count() or 1
        cores_logicos = psutil.cpu_count(logical=True) or 1
    except Exception:
        uso = 0.0
        cores_fisicos = 1
        cores_logicos = 1

    return {
        "cores_fisicos": cores_fisicos,
        "cores_logicos": cores_logicos,
        "uso_percentual": uso,
    }


def get_memory_info():
    """Retorna dados detalhados da memória RAM."""
    try:
        memory = psutil.virtual_memory()
        total_gb = round(memory.total / (1024 ** 3), 2)
        usada_gb = round(memory.used / (1024 ** 3), 2)
        disponivel_gb = round(memory.available / (1024 ** 3), 2)
        uso_percentual = memory.percent
    except Exception:
        total_gb = 0.0
        usada_gb = 0.0
        disponivel_gb = 0.0
        uso_percentual = 0.0

    return {
        "total_gb": total_gb,
        "usada_gb": usada_gb,
        "disponivel_gb": disponivel_gb,
        "uso_percentual": uso_percentual,
    }


def get_disk_info():
    """Retorna uso de disco por partição montada ativa."""
    disks = []
    for partition in psutil.disk_partitions(all=False):
        # Filtrar duto/cdrom no Windows para evitar bloqueio
        if "cdrom" in partition.opts or partition.fstype == "":
            continue

        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                "unidade": partition.mountpoint,
                "fstype": partition.fstype,
                "total_gb": round(usage.total / (1024 ** 3), 2),
                "livre_gb": round(usage.free / (1024 ** 3), 2),
                "usado_gb": round(usage.used / (1024 ** 3), 2),
                "uso_percentual": usage.percent,
            })
        except (PermissionError, OSError):
            continue

    return disks
