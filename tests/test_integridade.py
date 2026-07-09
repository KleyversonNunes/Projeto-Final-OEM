from playwright.sync_api import Page, expect
import requests
import yaml
from pathlib import Path

def carregar_config():
    # Caminho dinâmico adaptado para a nova pasta 'tests/'
    caminho = Path(__file__).parent.parent / "config" / "cliente_zero.yml"
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo)

def test_integridade_servidor():
    """Valida a integração da infraestrutura verificando se o servidor responde (Health Check)."""
    config = carregar_config()
    url = config["aplicacao"]["url"]
    
    # Realiza um "ping" no servidor antes de abrir a interface
    resposta = requests.get(url)
    assert resposta.status_code == 200, f"Gargalo Técnico: Servidor indisponível (Erro {resposta.status_code})"

def test_integridade_seguranca(page: Page):
    """Valida a integridade do bloqueio contra acessos não autorizados (Garantia de Taxa de Escape = Zero)."""
    config = carregar_config()
    url = config["aplicacao"]["url"]
    
    # Tenta burlar o sistema acessando a página interna diretamente sem login
    page.goto(f"{url.rstrip('/')}/inventory.html")
    
    # Valida se o sistema blindou a rota e retornou a mensagem de erro
    expect(page.locator("[data-test='error']")).to_contain_text(
        "Epic sadface: You can only access '/inventory.html' when you are logged in."
    )