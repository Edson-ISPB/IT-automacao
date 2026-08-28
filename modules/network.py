import socket
import time
import psutil
import config


def get_network_info():
    """Retorna a lista de interfaces de rede ativas com seus respetivos IPs."""
    ipv4_addresses = []

    try:
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        for interface, addresses in interfaces.items():
            # Verificar se a interface está ativa/up
            is_up = stats[interface].isup if interface in stats else True

            for address in addresses:
                if address.family == socket.AF_INET:
                    # Ignorar loopback se houver outras interfaces
                    ipv4_addresses.append({
                        "interface": interface,
                        "ip": address.address,
                        "netmask": address.netmask or "N/D",
                        "ativa": is_up
                    })
    except Exception:
        pass

    return ipv4_addresses


def check_connectivity(host=config.NETWORK_HOST, port=config.NETWORK_PORT, timeout=config.NETWORK_TIMEOUT):
    """Testa a conectividade de rede e mede a latência em ms."""
    start = time.perf_counter()

    try:
        with socket.create_connection((host, port), timeout=timeout):
            latency = (time.perf_counter() - start) * 1000
            return {
                "conectado": True,
                "latencia_ms": round(latency, 2),
                "host_testado": f"{host}:{port}",
            }
    except OSError:
        return {
            "conectado": False,
            "latencia_ms": None,
            "host_testado": f"{host}:{port}",
        }
