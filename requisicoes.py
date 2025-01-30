from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time
import base64
import requests
import os

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": r"C:\Users\user\Desktop\boletos desktop",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", prefs)
service = Service(ChromeDriverManager().install())

BITRIX_WEBHOOK_URL = "https://marketingsolucoes.bitrix24.com.br/rest/35002/7a2nuej815yjx5bg" 
CATEGORY_ID = "60"
STAGE_ID = "C60:UC_YIDJWR"
PDF_FIELD = "UF_CRM_1723743445"

def fetch_bitrix_deals():
    try:
        response = requests.post(f"{BITRIX_WEBHOOK_URL}/crm.deal.list", json={
            "filter": {"CATEGORY_ID": CATEGORY_ID, "STAGE_ID": STAGE_ID},
            "select": ["ID", "UF_CRM_1697807353336"]
        })
        response_data = response.json()
        if "result" in response_data:
            return response_data["result"]
        else:
            print("Erro ao buscar negócios do Bitrix:", response_data)
            return []
    except Exception as e:
        print("Exceção ao buscar negócios do Bitrix:", e)
        return []

def format_boleto_value(value_str):
    try:
        formatted_value = value_str.replace("R$", "").strip().replace(",", ".")
        return f"{formatted_value}|BRL"
    except Exception as e:
        print(f"Erro ao formatar valor do boleto: {e}")
        return None

MAX_RETRIES = 3 

def process_cpf_with_retries(cpf, deal_id):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            print(f"Tentativa {retries + 1} para processar o CPF {cpf}")
            process_cpf_list(cpf, deal_id)
            return  
        except Exception as e:
            print(f"Erro ao processar CPF {cpf}: {e}")
            retries += 1
            if retries == MAX_RETRIES:
                print(f"CPF {cpf} não pôde ser processado após {MAX_RETRIES} tentativas.")

def format_date_to_iso(date_str):
    try:
        parsed_date = datetime.strptime(date_str, "%d/%m/%Y")
        iso_date = parsed_date.strftime("%Y-%m-%dT00:00:00+03:00")
        return iso_date
    except ValueError as e:
        print(f"Erro ao converter data: {e}")
        return None

def upload_pdf_as_base64_to_bitrix(deal_id, pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            encoded_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")

        file_data = {
            "fileData": [os.path.basename(pdf_path), encoded_pdf]
        }

        response = requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update",
            json={
                "id": deal_id,
                "fields": {PDF_FIELD: file_data},
            }
        )

        result = response.json()
        if result.get("result"):
            print(f"PDF enviado com sucesso para o negócio {deal_id}.")
        else:
            print(f"Erro ao enviar PDF para o negócio {deal_id}: {result}")

    except Exception as e:
        print(f"Exceção ao enviar PDF para o negócio {deal_id}: {e}")

def update_field_in_bitrix(deal_id, field_name, field_value):
    try:
        response = requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update",
            json={
                "id": deal_id,
                "fields": {field_name: field_value},
            }
        )
        result = response.json()
        if result.get("result"):
            print(f"Campo {field_name} atualizado com sucesso para o negócio {deal_id}.")
        else:
            print(f"Erro ao atualizar o campo {field_name} para o negócio {deal_id}: {result}")
    except Exception as e:
        print(f"Exceção ao atualizar o campo {field_name} para o negócio {deal_id}: {e}")

def process_cpf_list(cpf, deal_id):
    navegador = webdriver.Chrome(service=service, options=options)
    try:
        link = "https://sac.desktop.com.br/Cliente_Documento.jsp"
        navegador.get(link)

        cpf_field = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.NAME, 'doc'))
        )
        cpf_field.send_keys(cpf)  
        
        # Resolvendo CAPTCHA
        try:
            captcha_frame = WebDriverWait(navegador, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="recaptcha"]'))
            )
            navegador.switch_to.frame(captcha_frame)

            checkbox = navegador.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border')
            if "recaptcha-checkbox-checked" in checkbox.get_attribute("class"):
                print("CAPTCHA já marcado automaticamente.")
                navegador.switch_to.default_content()
            else:
                print("Resolvendo CAPTCHA manualmente.")
                navegador.switch_to.default_content()

                chave_captcha = navegador.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')

                solver = recaptchaV2Proxyless()
                solver.set_verbose(1)
                solver.set_key('77d7875264ef5018a80876cc2e41f658')  
                solver.set_website_url(link)
                solver.set_website_key(chave_captcha)

                resposta = solver.solve_and_return_solution()

            if resposta:
                print(f"Resposta do Captcha: {resposta}")
                navegador.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{resposta}";')
            else:
                raise Exception(f"Erro ao resolver Captcha: {solver.err_string}")
        except Exception as e:
            print("CAPTCHA não encontrado ou já resolvido:", e)

        time.sleep(2)

        # Clicando no botão 'Avançar'
        try:
            avancar_button = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[src="imagens/admavanc.gif"]'))
            )
            avancar_button.click()
        except NoSuchElementException:
            print("Botão 'Avançar' não encontrado.")
            return

        time.sleep(2)

        # Coletando informações do boleto
        try:
            vencimento_element = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, '//td[font[contains(text(), "/")]]'))
            )
            vencimento_text = vencimento_element.text.strip()
            print(f"Data de vencimento encontrada: {vencimento_text}")

            iso_vencimento = format_date_to_iso(vencimento_text)
            if iso_vencimento:
                update_field_in_bitrix(deal_id, "UF_CRM_1725913768700", iso_vencimento)

            valor_element = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, '//td[font[contains(text(), "R$")]]'))
            )
            valor_text = valor_element.text.strip()
            print(f"Valor do boleto encontrado: {valor_text}")

            formatted_value = format_boleto_value(valor_text)
            if formatted_value:
                update_field_in_bitrix(deal_id, "UF_CRM_1726782459459", formatted_value)
            else:
                print("Erro ao formatar o valor do boleto.")
        except Exception as e:
            update_field_in_bitrix(deal_id, "UF_CRM_1724090639394", "48514")
            print(f"Erro ao localizar ou processar dados do boleto: {e}")

        time.sleep(2)

        # Verificando o tipo de boleto
        try:
            normal_boleto_link = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "JavaScript:boleto_") and contains(@class, "lnk")]'))
            )
            print(f"Boleto normal encontrado: {normal_boleto_link.text}")
            normal_boleto_link.click()  # Clica para abrir o boleto
            update_field_in_bitrix(deal_id, "UF_CRM_1724090639394", "48512")  # Atualiza o status na Bitrix
        except NoSuchElementException:
            print("Boleto normal não encontrado, verificando boleto novo.")

            # Tenta encontrar o link do boleto novo
            try:
                novo_boleto_link = WebDriverWait(navegador, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//form[contains(@name, "boleto_")]//a'))
                )
                print(f"Boleto novo encontrado: {novo_boleto_link.text}")
                novo_boleto_link.click()  # Clica para baixar o boleto
                update_field_in_bitrix(deal_id, "UF_CRM_1724090639394", "48513")  # Atualiza o status na Bitrix
            except NoSuchElementException:
                print(f"Nenhum boleto encontrado para o negócio {deal_id}.")
                update_field_in_bitrix(deal_id, "UF_CRM_1724090639394", "48514")  # Atualiza o status na Bitrix

        # Processando o PDF após o download
        try:
            iframe_element = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
            )
            navegador.switch_to.frame(iframe_element)

            open_button = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.ID, 'open-button'))
            )
            print("Botão 'Abrir' localizado.")

            parent_a = open_button.find_element(By.XPATH, './ancestor::a')
            href_value = parent_a.get_attribute('href')

            if href_value.startswith("data:application/pdf;base64,"):
                base64_data = href_value.split(",")[1]
                pdf_data = base64.b64decode(base64_data)

                pdf_path = rf"C:\Users\user\Desktop\boletos desktop\{cpf.replace('.', '').replace('-', '')}.pdf"
                with open(pdf_path, "wb") as pdf_file:
                    pdf_file.write(pdf_data)

                print(f"PDF salvo com sucesso em: {pdf_path}")
                upload_pdf_as_base64_to_bitrix(deal_id, pdf_path)
            else:
                print("O link obtido não é um PDF base64 válido.")
        except Exception as e:
            print(f"Erro ao localizar o botão ou o link do PDF: {e}")

    finally:
        navegador.quit()

if __name__ == "__main__":
    try:
        deals = fetch_bitrix_deals()
        for deal in deals:
            cpf = deal.get("UF_CRM_1697807353336")
            deal_id = deal.get("ID")
            if cpf:
                process_cpf_with_retries(cpf, deal_id)
            else:
                print(f"Negócio {deal_id} não possui CPF associado.")
    except Exception as e:
        print(f"Erro inesperado na execução do script principal: {e}")