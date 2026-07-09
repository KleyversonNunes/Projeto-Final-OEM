import yaml
from pathlib import Path

from playwright.sync_api import Page, expect


def carregar_config():
    raiz_projeto = Path(__file__).parent.parent
    caminho = raiz_projeto / "config" / "cliente_zero.yml"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo)


def test_login_sucesso(page: Page):

    config = carregar_config()

    url = config["aplicacao"]["url"]

    # 1. Acessa o ambiente do cliente
    page.goto(url)

    # 2. Preenche os dados simulando um humano
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")

    # 3. Clica no botão de login
    page.click("[data-test='login-button']")

    # 4. Valida se entrou no sistema

    expect(page).to_have_url(f"{url.rstrip('/')}/inventory.html")

def test_login_falha(page: Page):

    config = carregar_config()

    url = config["aplicacao"]["url"]

    # Acessa ambiente do cliente
    page.goto(url)

    page.fill("[data-test='username']", "usuario_errado")
    page.fill("[data-test='password']", "senha_errada")
    page.click("[data-test='login-button']")

    # Valida mensagem de erro
    erro = page.locator("[data-test='error']")
    expect(erro).to_contain_text("Epic sadface")