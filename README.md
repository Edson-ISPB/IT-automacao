# IT-Automacao - Diagnóstico Automático de TI (GTIC)

Sistema de automação em Python desenvolvido para diagnosticar de forma rápida, precisa e extensível a saúde de computadores (compatível com Windows, Linux e macOS).

Projeto desenvolvido para apoio ao dia a dia da **GTIC (Oficina de TI / Help Desk)** e suporte à defesa de **Relatório de Estágio**.

---

## 🚀 Funcionalidades

- **Informações do Sistema & Hardware:** Identificação do hostname, SO, arquitetura, processador e contagem de núcleos.
- **Monitorização de CPU & Memória RAM:** Consumo percentual com barras de progresso visuais.
- **Top Processos Consumidores:** Identificação automática dos 5 processos que mais utilizam CPU e Memória RAM (para diagnóstico de causa raiz).
- **Monitorização de Serviços Essenciais (GTIC):** Verificação de serviços vitais (Spooler de Impressão, Windows Defender, Windows Update, DHCP, DNS).
- **Análise de Ficheiros Temporários:** Cálculo do espaço ocupado em pastas temporárias (`%TEMP%`, `/tmp`).
- **Verificação de Armazenamento:** Leitura de todas as partições ativas com cálculo de espaço total, livre e usado.
- **Rede & Conectividade:** Identificação de endereços IPv4, máscaras de rede, estado da interface e medição de latência.
- **Uptime:** Identificação do tempo que o computador está ligado continuamente sem reiniciar.
- **Motor de Recomendações Automáticas:** Geração de ações preventivas/corretivas diretas para o técnico da GTIC.
- **Relatório HTML + JSON:** Relatórios visuais modernos com botão de impressão/PDF (`window.print()`) e exportação JSON para auditoria.
- **Compatibilidade Universal:** Funciona em qualquer computador (Windows, Linux, macOS) e trata graciosamente erros de permissão.

---

## 📂 Arquitetura do Projeto

```
c:\IT-Automacao\
├── config.py                   # Configurações globais e limiares (thresholds)
├── collectors.py               # Fachada de integração dos coletores
├── evaluator.py                # Regras de avaliação (OK, AVISO, CRÍTICO)
├── reporter.py                 # Gerador de relatórios HTML e JSON
├── main.py                     # Script principal de orquestração e CLI
├── requirements.txt            # Dependências (psutil)
├── modules/                    # Módulos especializados de coleta
│   ├── hardware.py             # CPU, RAM, Discos e Sistema
│   ├── network.py              # Interfaces de rede e conectividade
│   ├── processes.py            # Top consumidores de recursos
│   ├── services.py             # Monitor de serviços essenciais
│   ├── cleaner.py              # Cálculo de ficheiros temporários
│   └── recommendations.py      # Motor de geração de recomendações
├── tests/                      # Suíte de testes unitários
│   └── test_evaluator.py       # Testes de unidade
└── reports/                    # Relatórios gerados (.html e .json)
```

---

## 🛠️ Execução

### 1. Executar o Diagnóstico

```powershell
.\.venv\Scripts\python.exe main.py
```

### 2. Executar os Testes Unitários

```powershell
.\.venv\Scripts\python.exe -m unittest discover tests
```

---

## 📄 Relatórios Gerados

Ao terminar o diagnóstico, os seguintes ficheiros são gerados na pasta `reports/`:
- `diagnostico_latest.html`: Relatório visual mais recente.
- `diagnostico_HOSTNAME_DATAHORA.html`: Histórico individual do atendimento.
- `diagnostico_latest.json`: Dados em formato JSON para integração com outros sistemas.