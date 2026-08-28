import config
from modules.recommendations import generate_recommendations


def evaluate_cpu(value):
    if value > config.CPU_CRITICAL:
        return "CRÍTICO"
    if value >= config.CPU_WARNING:
        return "AVISO"
    return "OK"


def evaluate_ram(value):
    if value > config.RAM_CRITICAL:
        return "CRÍTICO"
    if value >= config.RAM_WARNING:
        return "AVISO"
    return "OK"


def evaluate_disk(value):
    if value > config.DISK_CRITICAL:
        return "CRÍTICO"
    if value >= config.DISK_WARNING:
        return "AVISO"
    return "OK"


def evaluate_uptime(days):
    if days >= config.UPTIME_WARNING_DAYS:
        return "AVISO"
    return "OK"


def evaluate_connectivity(connected):
    if connected:
        return "OK"
    return "CRÍTICO"


def evaluate_temp_size(gb_size):
    if gb_size >= config.TEMP_SIZE_CRITICAL_GB:
        return "CRÍTICO"
    if gb_size >= config.TEMP_SIZE_WARNING_GB:
        return "AVISO"
    return "OK"


def evaluate_services(services):
    """Retorna o estado geral dos serviços (CRÍTICO se algum essencial estiver parado)."""
    has_stopped = False
    for s in services:
        if s.get("status") == "PARADO":
            has_stopped = True
            break
    return "AVISO" if has_stopped else "OK"


def get_all_recommendations(report_data):
    """Invoca o motor de geração de recomendações de solução."""
    return generate_recommendations(report_data)
