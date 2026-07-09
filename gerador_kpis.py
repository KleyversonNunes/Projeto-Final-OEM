import xml.etree.ElementTree as ET
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.align import Align

def gerar_relatorio_gerencial(xml_path="resultados.xml"):
    console = Console()
    
    if not os.path.exists(xml_path):
        console.print("[bold red]❌ Erro: Arquivo de resultados XML não encontrado. Execute o pytest primeiro.[/bold red]")
        sys.exit(1)

    # Leitura do XML do Pytest
    tree = ET.parse(xml_path)
    testsuite = tree.find('.//testsuite')
    
    if testsuite is None:
        if tree.getroot().tag == 'testsuite':
            testsuite = tree.getroot()
        else:
            console.print("[bold red]❌ Erro: Estrutura do XML inválida.[/bold red]")
            sys.exit(1)

    # Extração de dados da execução
    total_testes = int(testsuite.get('tests', 0))
    falhas = int(testsuite.get('failures', 0))
    erros = int(testsuite.get('errors', 0))
    tempo_execucao = float(testsuite.get('time', 0))
    falhas_criticas = falhas + erros

    # Cálculo dos Indicadores (KPIs)
    taxa_escape = falhas_criticas
    
    # Se houver falha, o SLA de Entrega Perfeita cai. Caso contrário, é 100%.
    sla_entrega = 100 if total_testes > 0 and falhas_criticas == 0 else max(0, 100 - (falhas_criticas * 20))
    if total_testes == 0:
        sla_entrega = 0
        
    lead_time_segundos = tempo_execucao

    # Construção da Tabela Visual (Rich)
    table = Table(
        title="\n[bold cyan]Indicadores Operacionais e Estratégicos (KR4)[/bold cyan]", 
        box=box.DOUBLE_EDGE, 
        expand=True,
        title_justify="center"
    )
    
    table.add_column("KPI", style="bold white", justify="left")
    table.add_column("Resultado Atual", justify="center")
    table.add_column("Meta Padrão", style="dim", justify="center")
    table.add_column("Status", justify="center")

    # Linha 1: Lead Time (Operacional)
    status_lead = "[bold green]✅ SUCESSO[/bold green]" if lead_time_segundos < 604800 else "[bold red]❌ ALERTA[/bold red]"
    table.add_row(
        "Lead Time (Tempo de Execução)", 
        f"{lead_time_segundos:.2f} seg", 
        "< 7 dias", 
        status_lead
    )

    # Linha 2: SLA de Conformidade (Estratégico)
    status_sla = "[bold green]✅ SUCESSO[/bold green]" if sla_entrega >= 98 else "[bold red]❌ QUEBRA DE CONTRATO[/bold red]"
    table.add_row(
        "SLA de Conformidade", 
        f"{sla_entrega}%", 
        "> 98%", 
        status_sla
    )

    # Linha 3: Taxa de Escape (Estratégico)
    status_escape = "[bold green]✅ BLINDADO[/bold green]" if taxa_escape == 0 else "[bold red]❌ RISCO CRÍTICO[/bold red]"
    table.add_row(
        "Taxa de Escape (Falhas/Invasões)", 
        f"{taxa_escape} falha(s)", 
        "Zero", 
        status_escape
    )

    # Subtítulo listando a cobertura dos 4 arquivos de testes
    modulos_validados = f"""
[bold yellow]Módulos Validados ({total_testes} Cenários):[/bold yellow]
🛡️ [white]Segurança e Infraestrutura (Integridade)[/white]
🛒 [white]Regressão de Interface (Login e Checkout)[/white]
💾 [white]Estabilidade de Sessão (Persistência)[/white]
"""

    # Painel Principal Envolvendo a Tabela
    painel = Panel(
        Align.center(table), 
        title="[bold blue]🚀 QAaaS - Dashboard Executivo[/bold blue]", 
        subtitle=modulos_validados,
        border_style="blue",
        padding=(1, 2)
    )

    console.print("\n")
    console.print(painel)
    console.print("\n")

if __name__ == "__main__":
    gerar_relatorio_gerencial()