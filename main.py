import sys
import logging
from datetime import datetime
from pathlib import Path

from collectors import (
    get_system_info,
    get_cpu_info,
    get_memory_info,
    get_disk_info,
    get_network_info,
    check_connectivity,
    get_top_processes,
    get_services_status,
    get_temp_files_info,
)

from evaluator import (
    evaluate_cpu,
    evaluate_ram,
    evaluate_disk,
    evaluate_uptime,
    evaluate_connectivity,
    evaluate_temp_size,
    evaluate_services,
    get_all_recommendations,
)

from reporter import generate_html_report, generate_json_report

# Configurar sistema de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    print("=" * 65)
    print("GTIC - DIAGNÓSTICO AUTOMÁTICO DE TI E SUPORTE TÉCNICO")
    print("=" * 65)

    logging.info("Iniciando coleta de dados do computador...")

    # 1. COLETA DE DADOS
    system = get_system_info()
    cpu = get_cpu_info()
    memory = get_memory_info()
    disks = get_disk_info()
    network = get_network_info()
    connectivity = check_connectivity()
    top_processes = get_top_processes()
    services = get_services_status()
    temp_info = get_temp_files_info()

    logging.info("Avaliando estado das métricas...")

    # 2. AVALIAÇÃO DE ESTADOS
    cpu_status = evaluate_cpu(cpu["uso_percentual"])
    ram_status = evaluate_ram(memory["uso_percentual"])
    uptime_status = evaluate_uptime(system["uptime_days"])
    network_status = evaluate_connectivity(connectivity["conectado"])
    temp_status = evaluate_temp_size(temp_info["total_gb"])
    services_status = evaluate_services(services)

    evaluated_disks = []
    for disk in disks:
        disk_status = evaluate_disk(disk["uso_percentual"])
        evaluated_disks.append({
            **disk,
            "status": disk_status
        })

    # 3. CÁLCULO DO STATUS GERAL
    statuses = [
        cpu_status,
        ram_status,
        uptime_status,
        network_status,
        temp_status,
        services_status,
    ]
    statuses += [disk["status"] for disk in evaluated_disks]

    if "CRÍTICO" in statuses:
        general_status = "CRÍTICO"
    elif "AVISO" in statuses:
        general_status = "AVISO"
    else:
        general_status = "OK"

    # 4. PREPARAR DADOS CONSOLIDADOS
    report_data = {
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "hostname": system["hostname"],
        "os": system["os"],
        "os_version": system["os_version"],
        "architecture": system["architecture"],
        "status_geral": general_status,

        "cpu": cpu["uso_percentual"],
        "cpu_status": cpu_status,
        "cpu_info": cpu,

        "ram": memory["uso_percentual"],
        "ram_status": ram_status,
        "ram_info": memory,

        "uptime": system["uptime_days"],
        "uptime_status": uptime_status,

        "latencia": (
            connectivity["latencia_ms"]
            if connectivity["latencia_ms"] is not None
            else "N/D"
        ),
        "network_status": network_status,
        "connectivity_info": connectivity,

        "temp_status": temp_status,
        "temp_info": temp_info,

        "disks": evaluated_disks,
        "network": network,
        "top_processes": top_processes,
        "services": services,
        "services_status": services_status,
    }

    # Gerar recomendações automáticas
    report_data["recommendations"] = get_all_recommendations(report_data)

    # 5. GERAR RELATÓRIOS
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    hostname_clean = "".join(c for c in system["hostname"] if c.isalnum() or c in ("-", "_"))

    if getattr(sys, "frozen", False):
        output_dir = Path.home() / "Documents" / "GTIC-Relatorios"
    else:
        output_dir = Path(__file__).resolve().parent / "reports"

    output_html_timestamped = output_dir / f"diagnostico_{hostname_clean}_{now_str}.html"
    output_html_latest = output_dir / "diagnostico_latest.html"
    output_json_latest = output_dir / "diagnostico_latest.json"

    logging.info("Gerando relatórios HTML e JSON...")

    generate_html_report(report_data, output_html_timestamped)
    generate_html_report(report_data, output_html_latest)
    generate_json_report(report_data, output_json_latest)

    # 6. EXIBIR RESUMO NO TERMINAL
    print("\n" + "-" * 65)
    print(f"HOST: {system['hostname']} ({system['os']} {system['architecture']})")
    print(f"ESTADO GERAL DA MÁQUINA: [{general_status}]")
    print("-" * 65)
    print(f" • CPU: {cpu['uso_percentual']}% [{cpu_status}]")
    print(f" • RAM: {memory['uso_percentual']}% [{ram_status}]")
    print(f" • Uptime: {system['uptime_days']} dias [{uptime_status}]")
    print(f" • Conectividade: {report_data['latencia']} ms [{network_status}]")
    print(f" • Ficheiros Temp: {temp_info['total_gb']} GB [{temp_status}]")
    print("-" * 65)

    print("\nRECOMENDAÇÕES DA GTIC:")
    for rec in report_data["recommendations"]:
        print(f" [{rec['prioridade']}] ({rec['categoria']}) {rec['mensagem']}")

    print("\nRELATÓRIOS GERADOS:")
    print(f" • Histórico HTML: {output_html_timestamped.resolve()}")
    print(f" • Mais Recente HTML: {output_html_latest.resolve()}")
    print(f" • Dados Brutos JSON: {output_json_latest.resolve()}")
    print("-" * 65)
    print("Diagnóstico efetuado com sucesso!\n")


if __name__ == "__main__":
    main()