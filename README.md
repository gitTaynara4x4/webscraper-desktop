# 📄 Webcraper de Extração de Boletos PDF no Bitrix24 🇧🇷  
_(Scroll down for English version 🇺🇸)_

Este projeto automatiza a extração de boletos PDF do site SAC Desktop usando o CPF/CNPJ associado a negócios no Bitrix24. Utiliza web scraping com Selenium, resolve reCAPTCHA via AntiCaptcha, e atualiza campos personalizados no Bitrix24, enviando o boleto em base64.

---

### ✅ O que ele faz?

- Busca negócios no Bitrix24 com CPF/CNPJ preenchido.  
- Acessa o site SAC Desktop e insere o CPF/CNPJ para localizar boletos.  
- Resolve automaticamente o reCAPTCHA para acessar as informações.  
- Baixa o boleto em PDF e codifica em base64.  
- Atualiza o negócio no Bitrix24 com o PDF e dados como vencimento e valor.  

---

### 🔧 Como funciona?

1. Conecta-se ao Bitrix24 via webhook para listar negócios em estágio específico.  
2. Navega no SAC Desktop usando Selenium para buscar boletos pelo CPF/CNPJ.  
3. Usa AntiCaptcha para resolver o reCAPTCHA e prosseguir.  
4. Extrai os dados do boleto e baixa o PDF.  
5. Envia o PDF e os dados de volta para o Bitrix24 atualizando os campos personalizados.  

---

### 🛡️ Segurança

- Usa chaves e webhooks protegidos para acesso ao Bitrix24 e AntiCaptcha.  
- O reCAPTCHA é resolvido automaticamente, evitando bloqueios manuais.  
- Possui tratamento de erros e tentativas múltiplas para maior robustez.  

---

### 📈 Benefícios para sua empresa

- Elimina tarefas manuais de consulta e download de boletos.  
- Integra dados financeiros direto no CRM para controle centralizado.  
- Automatiza processos financeiros e reduz erros humanos.  

> Quer automatizar essa integração no seu Bitrix24? Fale comigo para personalizar esse fluxo para sua operação! 😉

---

# 📄 PDF Boleto Extraction Automation for Bitrix24 🇺🇸

This project automates PDF boleto extraction from SAC Desktop using CPF/CNPJ linked to Bitrix24 deals. It performs web scraping with Selenium, solves reCAPTCHA via AntiCaptcha, and updates custom Bitrix24 fields with base64 PDFs.

---

### ✅ What does it do?

- Fetches deals with CPF/CNPJ from Bitrix24.  
- Navigates SAC Desktop to find boletos by CPF/CNPJ.  
- Automatically solves reCAPTCHA challenges.  
- Downloads boleto PDFs and encodes them in base64.  
- Updates Bitrix24 deals with PDFs and boleto info like due date and amount.  

---

### 🔧 How does it work?

1. Connects to Bitrix24 via webhook to get deals in a specific stage.  
2. Uses Selenium to scrape boleto data from SAC Desktop by CPF/CNPJ.  
3. Resolves reCAPTCHA via AntiCaptcha service automatically.  
4. Extracts boleto details and downloads the PDF.  
5. Uploads the PDF and data back to Bitrix24 custom fields.  

---

### 🛡️ Security

- Uses secure keys and webhooks for Bitrix24 and AntiCaptcha access.  
- Automated reCAPTCHA solving prevents manual intervention.  
- Includes error handling and retry logic for reliability.  

---

### 📈 Business Benefits

- Eliminates manual boleto fetching and downloading tasks.  
- Centralizes financial data directly in your CRM.  
- Automates financial workflows and reduces human errors.  

> Want to automate this integration in your Bitrix24? Contact me to customize this workflow for your business! 😉
