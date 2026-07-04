from playwright.sync_api import Page, expect

def test_checkout_sucesso(page: Page):
    """
    Testa o fluxo completo de compra de um usuário no e-commerce.
    Valida a adição ao carrinho, preenchimento de dados e conclusão do pedido.
    """
    # 1. Realiza o Login (Pré-requisito)
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()

    # 2. Adiciona o produto "Sauce Labs Backpack" ao carrinho
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()

    # 3. Acessa o carrinho e valida se o produto está lá
    page.locator(".shopping_cart_link").click()
    expect(page.locator(".inventory_item_name")).to_have_text("Sauce Labs Backpack")

    # 4. Inicia o processo de Checkout (Informações do Cliente)
    page.locator("[data-test='checkout']").click()
    page.locator("[data-test='firstName']").fill("Squad")
    page.locator("[data-test='lastName']").fill("Operacoes")
    page.locator("[data-test='postalCode']").fill("66075-110") # CEP genérico
    page.locator("[data-test='continue']").click()

    # 5. Confirma os valores e finaliza a compra
    page.locator("[data-test='finish']").click()

    # 6. Validação (A prova de que a compra deu certo)
    expect(page.locator(".complete-header")).to_have_text("Thank you for your order!")