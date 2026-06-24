import pytest
from playwright.sync_api import Page, expect

def test_login_sucesso(page: Page):
    # 1. Acessa o site do "Cliente"
    page.goto("https://www.saucedemo.com/")
    
    # 2. Preenche os dados simulando um humano
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    
    # 3. Clica no botão de login
    page.click("[data-test='login-button']")
    
    # 4. Valida se a automação foi para a página correta (Dashboard)
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_login_falha(page: Page):
    # Este teste vai simular um erro para gerar uma falha bonita no nosso relatório
    page.goto("https://www.saucedemo.com/")
    page.fill("[data-test='username']", "usuario_errado")
    page.fill("[data-test='password']", "senha_errada")
    page.click("[data-test='login-button']")
    
    # Valida se a mensagem de erro apareceu na tela
    erro = page.locator("[data-test='error']")
    expect(erro).to_contain_text("Epic sadface")