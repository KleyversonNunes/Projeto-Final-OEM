import yaml
from pathlib import Path

from playwright.sync_api import Page, expect


def carregar_config():
    raiz_projeto = Path(__file__).parent.parent
    caminho = raiz_projeto / "config" / "cliente_zero.yml"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return yaml.safe_load(arquivo)


def test_checkout_sucesso(page: Page):

    config = carregar_config()

    url = config["aplicacao"]["url"]

    # 1. Acessa o ambiente do cliente
    page.goto(url)

    # 2. Realiza o login
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    page.click("[data-test='login-button']")

    # 3. Valida se entrou no sistema
    expect(page).to_have_url(f"{url.rstrip('/')}/inventory.html")

    # 4. Adiciona o produto ao carrinho
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")

    # 5. Acessa o carrinho
    page.click(".shopping_cart_link")

    # 6. Valida se o produto foi adicionado
    expect(page.locator(".inventory_item_name")).to_have_text(
        "Sauce Labs Backpack"
    )

    # 7. Inicia o checkout
    page.click("[data-test='checkout']")

    # 8. Preenche os dados do comprador
    page.fill("[data-test='firstName']", "Squad")
    page.fill("[data-test='lastName']", "Operacoes")
    page.fill("[data-test='postalCode']", "66075-110")

    # 9. Continua o processo
    page.click("[data-test='continue']")

    # 10. Finaliza a compra
    page.click("[data-test='finish']")

    # 11. Valida a conclusão do pedido
    expect(page.locator(".complete-header")).to_have_text(
        "Thank you for your order!"
    )