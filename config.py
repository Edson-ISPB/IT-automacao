# Configurações globais e limiares de diagnóstico (Thresholds)

# CPU
CPU_WARNING = 75
CPU_CRITICAL = 90

# RAM
RAM_WARNING = 80
RAM_CRITICAL = 90

# Disco
DISK_WARNING = 85
DISK_CRITICAL = 95

# Uptime (em dias)
UPTIME_WARNING_DAYS = 14

# Redes e Conectividade
NETWORK_HOST = "1.1.1.1"
NETWORK_PORT = 443
NETWORK_TIMEOUT = 3

# Top Processos
TOP_PROCESSES_COUNT = 5

# Ficheiros Temporários (em GB)
TEMP_SIZE_WARNING_GB = 5.0
TEMP_SIZE_CRITICAL_GB = 15.0

# Serviços do Windows a Monitorar (GTIC)
WINDOWS_SERVICES = [
    {"name": "Spooler", "display_name": "Serviço de Impressão (Spooler)"},
    {"name": "WinDefend", "display_name": "Antivírus (Windows Defender)"},
    {"name": "wuauserv", "display_name": "Windows Update"},
    {"name": "Dhcp", "display_name": "Cliente DHCP (Rede)"},
    {"name": "Dnscache", "display_name": "Cliente DNS (Rede)"},
]
