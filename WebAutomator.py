import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options
import time
import os

class webautomator:
    def __init__(self, url: str, user: str, password: str, download_dir: str = "downloads_nfse"):
        self.url = url
        self.user = user
        self.password = password
        self.download_dir = download_dir
        self.driver = None

        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def WebRobot(self):
        chrome_options = Options()
        prefs = {
            "download.default_directory": os.path.abspath(self.download_dir),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safeBrowse.enabled": True 
        }
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=chrome_options) 
        self.driver.get(self.url)

        wait = WebDriverWait(self.driver, 20)

        try:
            print("Tentando clicar no botão 'Fazer login'...")
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Fazer login']/..")))
            login_button.click()
            print("Botão 'Fazer login' clicado.")
            time.sleep(2)

            print("Inserindo usuário e senha...")
            user_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
            user_input.send_keys(self.user)

            password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
            password_input.send_keys(self.password)
            print("Usuário e senha inseridos.")
            time.sleep(2)

            print("Clicando no botão de submit do login...")
            submit_button = wait.until(EC.element_to_be_clickable((By.ID, "botao-entrar")))
            submit_button.click()
            print("Botão de login clicado.")
            time.sleep(2)

            print("Clicando no link de pesquisa (ícone da lupa)...")
            search_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//i[@class='fa fa-search']]")))
            search_link.click()
            print("Link de pesquisa clicado.")
            time.sleep(3)

            print("Iniciando loop para buscar e baixar NFSEs...")
            for number in range(1, 351):
                try:
                    print(f"\n--- Processando número: {number} ---")
                    
                    search_input = wait.until(EC.presence_of_element_located((By.ID, "consultarnfseForm:numNfse")))
                    search_input.clear()
                    search_input.send_keys(str(number))
                    print(f"Número {number} inserido no campo de busca.")
                    time.sleep(1)

                    consult_button = wait.until(EC.element_to_be_clickable((By.ID, "consultarnfseForm:j_id235")))
                    consult_button.click()
                    print("Botão 'Consultar' clicado.")
                    time.sleep(2)

                    visualizar_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Visualizar']")))
                    visualizar_link.click()
                    print("Link 'Visualizar' clicado.")
                    time.sleep(2)

                    exportar_pdf_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Exportar PDF']")))
                    exportar_pdf_button.click()
                    print("Botão 'Exportar PDF' clicado. O download deve iniciar na pasta configurada.")
                    time.sleep(3)

                    voltar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Voltar']")))
                    voltar_button.click()
                    print("Botão 'Voltar' clicado.")
                    time.sleep(2)
                
                except Exception as loop_e:
                    print(f"Erro ao processar o número {number}: {loop_e}")
                    print("Tentando voltar para continuar o loop...")
                    try:
                        back_to_search_button = self.driver.find_element(By.XPATH, "//input[@value='Voltar']")
                        if back_to_search_button.is_displayed() and back_to_search_button.is_enabled():
                            back_to_search_button.click()
                            time.sleep(2)
                        else:
                            print("Botão 'Voltar' não disponível para recuperação de erro. Tentando navegar de volta.")
                            self.driver.get(self.url)
                            time.sleep(5)
                            print("Navegado de volta para a URL principal.")

                    except Exception as back_e:
                        print(f"Não foi possível voltar para a página de busca após erro: {back_e}")
                        print("Pode ser necessário reiniciar o processo ou ajustar a lógica de recuperação de erro.")
                        break

        except Exception as main_e:
            print(f"Ocorreu um erro geral no processo: {main_e}")

        finally:
            print("\nAutomação finalizada.")
            self.driver.quit()