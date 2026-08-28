import json
from pathlib import Path
from html import escape


def generate_json_report(data, output_path):
    """Exporta o relatório consolidado em formato JSON para auditoria / integração."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def generate_html_report(data, output_path):
    """Gera um relatório HTML profissional com visual moderno, barras de progresso e botão de impressão."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    status_class = {
        "OK": "ok",
        "AVISO": "warning",
        "CRÍTICO": "critical"
    }

    priority_class = {
        "ALTA": "critical",
        "MÉDIA": "warning",
        "INFO": "ok"
    }

    html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagnóstico de TI - GTIC - {escape(str(data["hostname"]))}</title>
    <style>
        :root {{
            --primary: #1e293b;
            --bg: #f8fafc;
            --card-bg: #ffffff;
            --text: #334155;
            --ok-bg: #dcfce7;
            --ok-text: #166534;
            --warn-bg: #fef9c3;
            --warn-text: #854d0e;
            --crit-bg: #fee2e2;
            --crit-text: #991b1b;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 20px;
        }}

        .container {{
            max-width: 1100px;
            margin: auto;
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--primary);
            color: white;
            padding: 20px 30px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}

        .header p {{
            margin: 5px 0 0 0;
            font-size: 14px;
            color: #94a3b8;
        }}

        .btn-print {{
            background: #3b82f6;
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
        }}

        .btn-print:hover {{
            background: #2563eb;
        }}

        .cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .card {{
            background: var(--card-bg);
            padding: 18px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }}

        .card h3 {{
            margin-top: 0;
            font-size: 14px;
            color: #64748b;
            text-transform: uppercase;
        }}

        .card-value {{
            font-size: 22px;
            font-weight: bold;
            margin: 10px 0;
        }}

        .status {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 12px;
            text-transform: uppercase;
        }}

        .ok {{ background: var(--ok-bg); color: var(--ok-text); }}
        .warning {{ background: var(--warn-bg); color: var(--warn-text); }}
        .critical {{ background: var(--crit-bg); color: var(--crit-text); }}

        /* Progress Bar */
        .progress-bar {{
            background: #e2e8f0;
            border-radius: 8px;
            height: 10px;
            overflow: hidden;
            margin-top: 8px;
        }}

        .progress-fill {{
            height: 100%;
            border-radius: 8px;
            transition: width 0.3s;
        }}

        .progress-fill.ok {{ background: #22c55e; }}
        .progress-fill.warning {{ background: #eab308; }}
        .progress-fill.critical {{ background: #ef4444; }}

        section {{
            margin-top: 25px;
        }}

        section h2 {{
            font-size: 18px;
            color: var(--primary);
            border-bottom: 2px solid #cbd5e1;
            padding-bottom: 8px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--card-bg);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            margin-top: 10px;
        }}

        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #f1f5f9;
            font-size: 14px;
        }}

        th {{
            background: #f1f5f9;
            color: #475569;
            font-weight: 600;
        }}

        .rec-item {{
            background: var(--card-bg);
            border-left: 4px solid #3b82f6;
            padding: 14px 18px;
            margin-bottom: 10px;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .rec-item.ALTA {{ border-left-color: #ef4444; }}
        .rec-item.MÉDIA {{ border-left-color: #eab308; }}
        .rec-item.INFO {{ border-left-color: #22c55e; }}

        @media print {{
            .btn-print {{ display: none; }}
            body {{ padding: 0; background: white; }}
            .card, table {{ box-shadow: none; border: 1px solid #ccc; }}
        }}
    </style>
</head>
<body>

<div class="container">

    <div class="header">
        <div>
            <h1>GTIC - Diagnóstico Automático de TI</h1>
            <p>Computador: <strong>{escape(str(data["hostname"]))}</strong> | SO: {escape(str(data["os"]))} ({escape(str(data["architecture"]))}) | Data/Hora: {escape(str(data["data_hora"]))}</p>
        </div>
        <button class="btn-print" onclick="window.print()">🖨️ Imprimir / Salvar PDF</button>
    </div>

    <!-- Status Geral -->
    <div style="margin-top: 20px;" class="card">
        <span style="font-size: 16px;">Estado Geral da Máquina: </span>
        <span class="status {status_class[data["status_geral"]]}">{data["status_geral"]}</span>
    </div>

    <!-- Métrica Principal Cards -->
    <div class="cards">
        <div class="card">
            <h3>Processador (CPU)</h3>
            <div class="card-value">{data["cpu"]}%</div>
            <span class="status {status_class[data["cpu_status"]]}">{data["cpu_status"]}</span>
            <div class="progress-bar">
                <div class="progress-fill {status_class[data["cpu_status"]]}" style="width: {min(data["cpu"], 100)}%;"></div>
            </div>
            <p style="font-size: 11px; color: #64748b; margin-top: 6px;">{data["cpu_info"]["cores_logicos"]} Núcleos Lógicos ({data["cpu_info"]["cores_fisicos"]} Físicos)</p>
        </div>

        <div class="card">
            <h3>Memória RAM</h3>
            <div class="card-value">{data["ram"]}%</div>
            <span class="status {status_class[data["ram_status"]]}">{data["ram_status"]}</span>
            <div class="progress-bar">
                <div class="progress-fill {status_class[data["ram_status"]]}" style="width: {min(data["ram"], 100)}%;"></div>
            </div>
            <p style="font-size: 11px; color: #64748b; margin-top: 6px;">{data["ram_info"]["usada_gb"]} GB usados de {data["ram_info"]["total_gb"]} GB</p>
        </div>

        <div class="card">
            <h3>Tempo Ligado (Uptime)</h3>
            <div class="card-value">{data["uptime"]} dias</div>
            <span class="status {status_class[data["uptime_status"]]}">{data["uptime_status"]}</span>
        </div>

        <div class="card">
            <h3>Conectividade</h3>
            <div class="card-value">{data["latencia"]} ms</div>
            <span class="status {status_class[data["network_status"]]}">{data["network_status"]}</span>
            <p style="font-size: 11px; color: #64748b; margin-top: 6px;">Host: {escape(str(data["connectivity_info"]["host_testado"]))}</p>
        </div>

        <div class="card">
            <h3>Ficheiros Temp</h3>
            <div class="card-value">{data["temp_info"]["total_gb"]} GB</div>
            <span class="status {status_class[data["temp_status"]]}">{data["temp_status"]}</span>
            <p style="font-size: 11px; color: #64748b; margin-top: 6px;">{data["temp_info"]["total_files"]} ficheiros acumulados</p>
        </div>
    </div>

    <!-- Recomendações da GTIC -->
    <section>
        <h2>💡 Ações e Recomendações Técnicas (GTIC)</h2>
"""

    for rec in data["recommendations"]:
        p_class = priority_class.get(rec["prioridade"], "ok")
        html += f"""
        <div class="rec-item {rec["prioridade"]}">
            <div>
                <strong>[{escape(str(rec["categoria"]))}]</strong> {escape(str(rec["mensagem"]))}
            </div>
            <span class="status {p_class}">{rec["prioridade"]}</span>
        </div>
"""

    html += """
    </section>

    <!-- Top Processos -->
    <section>
        <h2>📊 Top Processos Consumidores</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div>
                <h3>Mais CPU</h3>
                <table>
                    <tr><th>PID</th><th>Processo</th><th>Uso CPU</th></tr>
"""
    for p in data["top_processes"]["top_cpu"]:
        html += f"<tr><td>{p['pid']}</td><td>{escape(str(p['name']))}</td><td><strong>{p['cpu_percent']}%</strong></td></tr>\n"

    html += """
                </table>
            </div>
            <div>
                <h3>Mais RAM</h3>
                <table>
                    <tr><th>PID</th><th>Processo</th><th>Uso RAM</th></tr>
"""
    for p in data["top_processes"]["top_ram"]:
        html += f"<tr><td>{p['pid']}</td><td>{escape(str(p['name']))}</td><td><strong>{p['ram_mb']} MB</strong></td></tr>\n"

    html += """
                </table>
            </div>
        </div>
    </section>

    <!-- Serviços do Sistema -->
    <section>
        <h2>🛠️ Estado dos Serviços Essenciais do Sistema</h2>
        <table>
            <tr>
                <th>Serviço</th>
                <th>Nome Técnico</th>
                <th>Estado</th>
            </tr>
"""

    for s in data["services"]:
        s_class = "ok" if s["status"] == "EM EXECUÇÃO" else "warning" if s["status"] == "PARADO" else "critical"
        html += f"""
            <tr>
                <td>{escape(str(s["display_name"]))}</td>
                <td><code>{escape(str(s["name"]))}</code></td>
                <td><span class="status {s_class}">{s["status"]}</span></td>
            </tr>
"""

    html += """
        </table>
    </section>

    <!-- Armazenamento -->
    <section>
        <h2>💾 Armazenamento (Partições de Disco)</h2>
        <table>
            <tr>
                <th>Unidade</th>
                <th>Tipo</th>
                <th>Total (GB)</th>
                <th>Livre (GB)</th>
                <th>Uso (%)</th>
                <th>Estado</th>
            </tr>
"""

    for disk in data["disks"]:
        status = disk["status"]
        html += f"""
            <tr>
                <td><strong>{escape(str(disk["unidade"]))}</strong></td>
                <td>{escape(str(disk.get("fstype", "N/D")))}</td>
                <td>{disk["total_gb"]} GB</td>
                <td>{disk["livre_gb"]} GB</td>
                <td>
                    {disk["uso_percentual"]}%
                    <div class="progress-bar">
                        <div class="progress-fill {status_class[status]}" style="width: {min(disk["uso_percentual"], 100)}%;"></div>
                    </div>
                </td>
                <td><span class="status {status_class[status]}">{status}</span></td>
            </tr>
"""

    html += """
        </table>
    </section>

    <!-- Rede -->
    <section>
        <h2>🌐 Interfaces de Rede Detectadas</h2>
        <table>
            <tr>
                <th>Interface</th>
                <th>Endereço IPv4</th>
                <th>Máscara de Rede</th>
                <th>Estado</th>
            </tr>
"""

    for net in data["network"]:
        net_status = "EM EXECUÇÃO" if net.get("ativa", True) else "INATIVA"
        net_class = "ok" if net.get("ativa", True) else "critical"
        html += f"""
            <tr>
                <td><strong>{escape(str(net["interface"]))}</strong></td>
                <td><code>{escape(str(net["ip"]))}</code></td>
                <td>{escape(str(net["netmask"]))}</td>
                <td><span class="status {net_class}">{net_status}</span></td>
            </tr>
"""

    html += """
        </table>
    </section>

    <footer style="margin-top: 40px; text-align: center; font-size: 12px; color: #94a3b8;">
        Relatório gerado automaticamente pelo Sistema de Diagnóstico da GTIC (Oficina de TI)
    </footer>

</div>

</body>
</html>
"""

    output.write_text(html, encoding="utf-8")
