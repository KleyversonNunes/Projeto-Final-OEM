from playwright.sync_api import Page, expect
import yaml
from pathlib import Path

def carregar_config():
    caminho = Path(__file__).parent.parent / "config" / "cliente_zero.yml"
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo)

def test_persistencia_sessao(page: Page):
    """Regressão: Garante que os dados do cliente persistam após um recarregamento de página."""
    config = carregar_config()
    url = config["aplicacao"]["url"]
    
    # 1. Realiza login e insere produto no carrinho
    page.goto(url)
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    page.click("[data-test='login-button']")
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    
    # 2. Confirma o estado inicial (1 item marcado no badge vermelho)
    badge_carrinho = page.locator(".shopping_cart_badge")
    expect(badge_carrinho).to_have_text("1")
    
    # 3. Simula uma queda de conexão momentânea ou um "F5" do usuário
    page.reload()
    
    # 4. Valida a integridade dos dados (O produto não pode ter sumido)
    expect(badge_carrinho).to_have_text("1")