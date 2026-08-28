import platform
import psutil
import config


def get_services_status():
    """
    Verifica o estado dos serviços vitais do sistema.
    Compatível com Windows via psutil.win_service_iter(), com fallback gracioso para outros SOs.
    """
    results = []
    is_windows = platform.system().lower() == "windows"

    if is_windows:
        # Mapeamento rápido dos serviços do Windows
        service_map = {s["name"].lower(): s["display_name"] for s in config.WINDOWS_SERVICES}
        found_services = {}

        try:
            for sc in psutil.win_service_iter():
                try:
                    name_lower = sc.name().lower()
                    if name_lower in service_map:
                        status = sc.status()  # 'running', 'stopped', etc.
                        display_name = service_map[name_lower]
                        found_services[name_lower] = {
                            "name": sc.name(),
                            "display_name": display_name,
                            "status": "EM EXECUÇÃO" if status == "running" else "PARADO",
                            "raw_status": status,
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass

        # Garantir que todos os serviços configurados tenham um estado reportado
        for s in config.WINDOWS_SERVICES:
            s_name_lower = s["name"].lower()
            if s_name_lower in found_services:
                results.append(found_services[s_name_lower])
            else:
                results.append({
                    "name": s["name"],
                    "display_name": s["display_name"],
                    "status": "NÃO ENCONTRADO",
                    "raw_status": "not_found",
                })
    else:
        # Fallback para ambientes não-Windows (Linux / macOS)
        results.append({
            "name": "System Services",
            "display_name": "Serviços do Sistema (Não-Windows)",
            "status": "N/A (SO Não-Windows)",
            "raw_status": "n/a",
        })

    return results
