def generate_recommendations(data):
    """
    Motor de recomendações da GTIC.
    Analisa os estados coletados e gera soluções recomendadas em linguagem clara.
    """
    recommendations = []

    # 1. Recomendação sobre Uptime
    uptime = data.get("uptime", 0)
    if data.get("uptime_status") == "AVISO":
        recommendations.append({
            "categoria": "Sistema / Uptime",
            "prioridade": "MÉDIA",
            "mensagem": f"O sistema está ligado há {uptime} dias sem reiniciar. Recomenda-se reiniciar a máquina para aplicar atualizações pendentes e libertar recursos de memória."
        })

    # 2. Recomendação sobre CPU
    if data.get("cpu_status") in ("AVISO", "CRÍTICO"):
        top_cpu_name = "desconhecido"
        top_cpu_pct = 0
        if "top_processes" in data and data["top_processes"]["top_cpu"]:
            top_proc = data["top_processes"]["top_cpu"][0]
            top_cpu_name = top_proc["name"]
            top_cpu_pct = top_proc["cpu_percent"]

        recommendations.append({
            "categoria": "Processador (CPU)",
            "prioridade": "ALTA" if data.get("cpu_status") == "CRÍTICO" else "MÉDIA",
            "mensagem": f"Alto uso de CPU ({data.get('cpu')}%). O processo '{top_cpu_name}' está a consumir {top_cpu_pct}% da CPU. Verifique se a aplicação travou ou finalize o processo."
        })

    # 3. Recomendação sobre RAM
    if data.get("ram_status") in ("AVISO", "CRÍTICO"):
        top_ram_name = "desconhecido"
        top_ram_mb = 0
        if "top_processes" in data and data["top_processes"]["top_ram"]:
            top_proc = data["top_processes"]["top_ram"][0]
            top_ram_name = top_proc["name"]
            top_ram_mb = top_proc["ram_mb"]

        recommendations.append({
            "categoria": "Memória RAM",
            "prioridade": "ALTA" if data.get("ram_status") == "CRÍTICO" else "MÉDIA",
            "mensagem": f"Uso elevado de RAM ({data.get('ram')}%). O processo '{top_ram_name}' está a utilizar {top_ram_mb} MB. Considere fechar separadores no navegador ou adicionar mais RAM física."
        })

    # 4. Recomendação sobre Discos
    for disk in data.get("disks", []):
        if disk.get("status") in ("AVISO", "CRÍTICO"):
            recommendations.append({
                "categoria": f"Armazenamento ({disk.get('unidade')})",
                "prioridade": "ALTA" if disk.get("status") == "CRÍTICO" else "MÉDIA",
                "mensagem": f"Pouco espaço livre na unidade {disk.get('unidade')} ({disk.get('livre_gb')} GB livres, {disk.get('uso_percentual')}% em uso). Execute a Limpeza de Disco e remova ficheiros desnecessários."
            })

    # 5. Recomendação sobre Conectividade
    if data.get("network_status") == "CRÍTICO":
        recommendations.append({
            "categoria": "Rede / Conectividade",
            "prioridade": "ALTA",
            "mensagem": "Sem conexão à rede/internet ou o gateway não responde. Verifique os cabos de rede, Wi-Fi e configurações de IP/DNS."
        })

    # 6. Recomendação sobre Ficheiros Temporários
    if data.get("temp_status") in ("AVISO", "CRÍTICO"):
        temp_gb = data.get("temp_info", {}).get("total_gb", 0)
        recommendations.append({
            "categoria": "Ficheiros Temporários",
            "prioridade": "MÉDIA",
            "mensagem": f"Acúmulo significativo de ficheiros temporários ({temp_gb} GB ocupados). Esvazie a pasta %TEMP% e a Lixeira para libertar espaço."
        })

    # 7. Recomendação sobre Serviços Parados
    for service in data.get("services", []):
        if service.get("status") == "PARADO":
            recommendations.append({
                "categoria": f"Serviço {service.get('display_name')}",
                "prioridade": "ALTA" if service.get('name') in ['Spooler', 'WinDefend'] else "MÉDIA",
                "mensagem": f"O serviço '{service.get('display_name')}' está PARADO. Tente reiniciar o serviço através do gestor services.msc."
            })

    # Se tudo estiver OK
    if not recommendations:
        recommendations.append({
            "categoria": "Geral",
            "prioridade": "INFO",
            "mensagem": "Todos os parâmetros analisados estão dentro dos limites normais de funcionamento. Nenhuma ação corretiva imediata é necessária."
        })

    return recommendations
