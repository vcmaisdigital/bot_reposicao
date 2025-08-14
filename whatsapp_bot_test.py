from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime
from dados_alunos import ALUNOS_DADOS

class WhatsAppBot:
    def __init__(self):
        # Configurar opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        
        # Inicializar o driver com as opções
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Aumentar tempo de espera para 45 segundos
        self.wait = WebDriverWait(self.driver, 45)
        self.numero_teste = "+5582999915223"  # Seu número para testes
        self.respostas = {}
        self.carregar_respostas()
        
    def carregar_respostas(self):
        try:
            with open('respostas.json', 'r', encoding='utf-8') as f:
                self.respostas = json.load(f)
        except FileNotFoundError:
            self.respostas = {}
    
    def salvar_respostas(self):
        with open('respostas.json', 'w', encoding='utf-8') as f:
            json.dump(self.respostas, f, ensure_ascii=False, indent=4)
        
    def iniciar(self):
        self.driver.get("https://web.whatsapp.com")
        print("Por favor, escaneie o QR Code do WhatsApp Web")
        input("Pressione Enter após escanear o QR Code...")

    def coletar_respostas(self, aluno):
        """Coleta as últimas mensagens recebidas após enviar a mensagem"""
        try:
            # Espera por mensagens na conversa
            mensagens = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.message-in")
                )
            )
            
            # Coleta as últimas mensagens (posteriores ao envio)
            respostas = []
            for msg in mensagens[-3:]:  # Pegando as últimas 3 mensagens
                try:
                    texto = msg.find_element(By.CSS_SELECTOR, "span.selectable-text").text
                    timestamp = msg.find_element(By.CSS_SELECTOR, "div.copyable-text").get_attribute("data-pre-plain-text")
                    respostas.append({
                        "texto": texto,
                        "timestamp": timestamp,
                        "data_coleta": datetime.now().isoformat()
                    })
                except Exception as e:
                    print(f"Erro ao coletar mensagem: {str(e)}")
            
            # Salva as respostas
            if respostas:
                self.respostas[aluno["nome"]] = {
                    "turma": aluno["turma"],
                    "faltas": aluno["faltas"],
                    "mensagens": respostas
                }
                self.salvar_respostas()
                
        except TimeoutException:
            print("Nenhuma resposta encontrada no tempo esperado")
        except Exception as e:
            print(f"Erro ao coletar respostas: {str(e)}")

    def esperar_pagina_carregar(self):
        """Espera a página do WhatsApp carregar completamente"""
        try:
            # Espera o elemento de carregamento desaparecer
            self.wait.until_not(
                EC.presence_of_element_located((By.XPATH, '//*[@role="progressbar"]'))
            )
            time.sleep(2)  # Espera adicional para garantir
            return True
        except:
            return False

    def enviar_mensagem_teste(self, aluno, mensagem):
        tentativas = 0
        max_tentativas = 3
        
        while tentativas < max_tentativas:
            try:
                tentativas += 1
                print(f"\nTentativa {tentativas} de {max_tentativas}")
                
                # Sempre envia para o número de teste
                numero = self.numero_teste
                numero = numero.replace("+", "").replace(" ", "").replace("-", "")
                link = f"https://web.whatsapp.com/send?phone={numero}"
                
                print(f"\nAbrindo conversa para {aluno['nome']}...")
                self.driver.get(link)
                
                # Espera a página carregar
                if not self.esperar_pagina_carregar():
                    print("Erro: Página não carregou completamente")
                    continue
                
                # Verifica se o contato existe/está válido
                try:
                    self.wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]'))
                    )
                except:
                    print("Erro: Contato não encontrado ou número inválido")
                    continue
                    
                print("Procurando campo de mensagem...")
                
                # Tenta diferentes seletores para o campo de mensagem
                caixa_mensagem = None
                seletores = [
                    '//*[@id="main"]//div[@contenteditable="true"]',
                    '//footer//div[@contenteditable="true"]',
                    '//div[contains(@class, "selectable-text")][@contenteditable="true"]'
                ]
                
                for seletor in seletores:
                    try:
                        caixa_mensagem = self.wait.until(
                            EC.presence_of_element_located((By.XPATH, seletor))
                        )
                        print(f"Campo de mensagem encontrado usando seletor: {seletor}")
                        break
                    except:
                        continue
                        
                if not caixa_mensagem:
                    print("Erro: Não foi possível encontrar o campo de mensagem")
                    continue
                
                # Prepara a mensagem
                mensagem_completa = f"[TESTE - Mensagem para {aluno['nome']} da {aluno['turma']}]\n\n{mensagem}"
                
                # Limpa o campo e insere a mensagem usando send_keys
                print("Digitando mensagem...")
                caixa_mensagem.clear()
                caixa_mensagem.send_keys(mensagem_completa)
                time.sleep(2)
                
                # Tenta encontrar o botão de enviar
                try:
                    botao_enviar = self.driver.find_element(By.XPATH, '//span[@data-icon="send"]')
                    print("Botão de enviar encontrado, clicando...")
                    botao_enviar.click()
                except:
                    print("Botão de enviar não encontrado, usando Enter...")
                    caixa_mensagem.send_keys(Keys.ENTER)
                
                # Verifica se a mensagem foi realmente enviada
                try:
                    # Espera aparecer o duplo check (mensagem enviada)
                    self.wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@data-icon="msg-dblcheck" or @data-icon="msg-check"]'))
                    )
                    print("Mensagem enviada com sucesso! (confirmado pelo check)")
                    return True
                except:
                    print("Não foi possível confirmar o envio da mensagem")
                    continue
            
            except Exception as e:
                print(f"Erro na tentativa {tentativas}: {str(e)}")
                if tentativas < max_tentativas:
                    print("Tentando novamente...")
                    time.sleep(2)
                continue
        
        print(f"Falha após {max_tentativas} tentativas")
        return False
            
            print("Enviando mensagem...")
            # Envia a mensagem
            caixa_mensagem.send_keys(Keys.ENTER)
            
            # Espera a mensagem ser enviada
            time.sleep(3)
            
            # Verifica se a mensagem foi enviada procurando pelo checkmark
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Enviada" or @aria-label="Entregue" or @aria-label="Lida"]'))
                )
                print("Mensagem enviada com sucesso!")
            except:
                print("Aviso: Não foi possível confirmar o envio da mensagem")
            
            # Coleta respostas após enviar
            self.coletar_respostas(aluno)
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar mensagem teste para {aluno['nome']}: {str(e)}")
            return False

def gerar_mensagem(aluno):
    if aluno.get("enviar_para_responsavel"):
        destinatario = f"Ola! Tudo bem?\nO(A) {aluno['nome']}"
    else:
        destinatario = f"Ola, {aluno['nome']}! Tudo bem?\nVoce"

    if not aluno["faltas"]:
        return f"{destinatario} esteve presente em todas as aulas, nao ha reposicoes pendentes.\n— Erick Oliveira | Voce+ Digital"
    
    if len(aluno["faltas"]) == 1:
        return f"{destinatario} tem aula pendente no dia {aluno['faltas'][0]}.\nMe passe os dias e horarios disponiveis para reposicao.\nAguardo seu retorno!\n— Erick Oliveira | Voce+ Digital"
    
    faltas_texto = ", ".join(aluno["faltas"])
    return f"{destinatario} tem aulas pendentes nas datas: {faltas_texto}.\nMe envie seus dias e horarios disponiveis para reposicao.\nAguardo seu retorno!\n— Erick Oliveira | Voce+ Digital"

def main():
    bot = WhatsAppBot()
    bot.iniciar()
    
    for aluno in ALUNOS_DADOS:
        # Pula alunos que já receberam mensagem
        if aluno.get("ja_enviado"):
            print(f"Pulando {aluno['nome']} - mensagem já enviada anteriormente")
            continue
            
        mensagem = gerar_mensagem(aluno)
        print(f"\nEnviando mensagem de teste para {aluno['nome']} da {aluno['turma']}...")
        
        sucesso = bot.enviar_mensagem_teste(aluno, mensagem)
        
        if sucesso:
            print(f"Mensagem de teste enviada com sucesso para {aluno['nome']}!")
        else:
            print(f"Falha ao enviar mensagem de teste para {aluno['nome']}")
        
        # Espera entre mensagens para evitar bloqueios
        time.sleep(3)
        
        # A cada 5 mensagens, pergunta se quer continuar
        if ALUNOS_DADOS.index(aluno) % 5 == 4:
            resp = input("\nDeseja continuar enviando mensagens? (s/n): ")
            if resp.lower() != 's':
                print("Interrompendo envio de mensagens...")
                break

    print("\nProcesso finalizado!")
    print(f"As respostas coletadas foram salvas em 'respostas.json'")

if __name__ == "__main__":
    main()
