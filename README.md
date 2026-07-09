# 🚀 QAaaS - Quality Assurance as a Service (MVP)

> **Projeto da Disciplina de Organização e Métodos (O&M) -** 
> Bacharelado em Sistemas de Informação<br>
> **Diretoria Fundadora:** Breno Y. S. Sawaki, Jorge M. S. R. Araujo, Kleyverson N. Silva

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-Automated_Testing-2EAD33.svg)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF.svg)
![Status](https://img.shields.io/badge/Status-MVP_Conclu%C3%ADdo-success.svg)

## 📌 Visão Geral do Negócio
A **QAaaS** é uma startup de *Quality Assurance as a Service* que oferece serviços de garantia de qualidade para software sob demanda, com foco em automação de testes, melhoria contínua e redução de falhas em produção.

Nossa proposta de valor (Oceano Azul) diferencia-se pela engenharia profunda: integramos scripts de automação diretamente na pipeline CI/CD do ambiente Linux/Cloud do cliente, projetando reduzir falhas críticas em produção em até 40%. A monetização é feita via assinatura mensal (SaaS), com planos definidos por volumetria de testes e complexidade da infraestrutura.

Este repositório contém o Produto Mínimo Viável (MVP) que prova a viabilidade operacional e técnica do nosso serviço.

---

## 📊 Governança e O&M
O modelo de negócios foi estruturado para garantir escalabilidade financeira e controle técnico, baseado em:
* **Processo Crítico Mapeado:** Fluxo de *Onboarding* modelado via BPMN, abrangendo desde o contrato assinado pelo comercial até o *setup* técnico de infraestrutura pelo CTO.
* **Garantia de SLA:** Execução da bateria de testes de regressão e entrega de um *Dashboard* analítico com SLA rigoroso de 24 horas.
* **Gestão Orientada a Dados (KPIs):** Monitoramento semanal analítico e quantitativo, como o controle de *Lead Time* (< 7 dias) sob gestão do CTO e o *SLA de Entrega* (> 98%) sob gestão da equipe de QA.

---

## ⚙️ Arquitetura Técnica (O MVP)

Para validar nosso processo crítico na prática, este MVP executa testes automatizados críticos de regressão (ex: fluxos de login) no sistema de demonstração `saucedemo.com` ("Cliente Zero"). A infraestrutura garante isolamento, velocidade e independência de hardware local.

### Tecnologias Utilizadas
* **Linguagem:** `Python 3.10+`
* **Motor de Testes Web:** `Playwright` + `Pytest`
* **Relatórios:** `pytest-html` (Geração do Dashboard de SLA)
* **Orquestração de Nuvem:** `GitHub Actions` (Containers Ubuntu)

### Estrutura de Diretórios e Configuração Dinâmica
O projeto foi desenhado para escalabilidade (padrão SaaS), separando regras de negócio da execução de código:
* **Pasta `config/`:** Contém o arquivo `cliente_zero.yml`. É através deste arquivo que o time Comercial/Onboarding injeta dinamicamente a URL do cliente na automação, sem a necessidade de alterar ou conhecer programação.
* **Pasta `tests/`:** Isola todos os scripts de validação (`test_login.py`, `test_checkout.py`, `test_integridade.py`, `test_persistencia.py`), mantendo a raiz do projeto limpa e pronta para receber novos clientes.

### Como a Esteira CI/CD Funciona
A execução ocorre de forma 100% autônoma. Sempre que há uma alteração no código (*push*), o GitHub Actions engatilha nossa pipeline que realiza os seguintes passos:
1. Provisiona um container Linux isolado.
2. Configura o ambiente Python e as bibliotecas base do sistema.
3. Instala os motores dos navegadores em modo *headless*.
4. Executa os testes de regressão simulando o comportamento de um usuário real (e tentativas de invasão para atestar a segurança).
5. Gera e disponibiliza o artefato final (`relatorio_qaaas.html`) na aba **Actions**, automatizando o *output* do nosso SLA de 24h.

---

## 🛠️ Como Executar Localmente

Caso seja necessário depurar ou rodar os testes localmente em ambientes Linux (como Ubuntu ou distribuições baseadas em Arch), siga os passos abaixo:

**1. Clone o repositório:**
```bash
git clone https://github.com/KleyversonNunes/Projeto-Final-OEM.git
cd Projeto-Final-OEM
```

**2. Crie e ative o ambiente virtual:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
playwright install --with-deps
```

**4. Execute os testes e gere o Dashboard:**
```bash
pytest --html=relatorio_qaaas.html --self-contained-html
```
---

## 🌳 Padrões do Repositório
Para garantir a maturidade do nosso ciclo de desenvolvimento de software, operamos neste repositório único utilizando as seguintes diretrizes:

Branch `main`: Palco de apresentação e fonte da verdade. Contém apenas a versão final estável que aciona a esteira de CI/CD para o cliente.

Branch `develop`: Ambiente de desenvolvimento contínuo, correções e laboratório de infraestrutura.

Commits: Adotamos estritamente a convenção de Conventional Commits (ex: `feat:`, `fix:`, `docs:`) para manter um histórico rastreável, previsível e profissional.