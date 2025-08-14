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
from dados_teste import ALUNOS_TESTE  # Importando os dados de teste

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
        
        # Inicializar o driver com as opções
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 45)
        self.respostas = {}
        self.carregar_respostas()
        
    def carregar_respostas(self):
        try:
            with open('respostas_teste.json', 'r', encoding='utf-8') as f:
                self.respostas = json.load(f)
        except FileNotFoundError:
            self.respostas = {}
    
    def salvar_respostas(self):
        with open('respostas_teste.json', 'w', encoding='utf-8') as f:
            json.dump(self.respostas, f, ensure_ascii=False, indent=4)
        
    def iniciar(self):
        self.driver.get("https://web.whatsapp.com")
        print("Por favor, escaneie o QR Code do WhatsApp Web")
        input("Pressione Enter após escanear o QR Code...")

    def esperar_pagina_carregar(self):
        try:
            self.wait.until_not(
                EC.presence_of_element_located((By.XPATH, '//*[@role="progressbar"]'))
            )
            time.sleep(2)
            return True
        except:
            return False

    def enviar_mensagem(self, aluno, mensagem):
        tentativas = 0
        max_tentativas = 3
        
        while tentativas < max_tentativas:
            try:
                tentativas += 1
                print(f"\nTentativa {tentativas} de {max_tentativas}")
                
                # Define o número baseado no tipo de destinatário
                if aluno.get("enviar_para_responsavel") and aluno.get("numero_responsavel"):
                    numero = aluno["numero_responsavel"]
                else:
                    numero = aluno["numero"]
                numero = numero.replace("+", "").replace(" ", "").replace("-", "")
                
                # Mostra informações detalhadas do envio
                destinatario = "responsável " + aluno.get("responsavel", "") if aluno.get("enviar_para_responsavel") else "aluno(a)"
                print(f"Enviando mensagem para {aluno['nome']} ({destinatario}) no número {numero}...")
                
                link = f"https://web.whatsapp.com/send?phone={numero}"
                self.driver.get(link)
                
                if not self.esperar_pagina_carregar():
                    print("Página não carregou completamente")
                    continue
                
                print("Aguardando carregar a conversa...")
                try:
                    self.wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]'))
                    )
                except:
                    print("Conversa não carregou")
                    continue
                
                print("Procurando campo de mensagem...")
                try:
                    caixa_mensagem = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]//div[@contenteditable="true"]'))
                    )
                except:
                    print("Campo de mensagem não encontrado")
                    continue
                
                print("Digitando mensagem...")
                try:
                    caixa_mensagem.clear()
                    # Divide a mensagem em linhas e envia com quebras corretas
                    linhas = mensagem.split('\n')
                    for i, linha in enumerate(linhas):
                        if linha.strip():  # Ignora linhas vazias
                            caixa_mensagem.send_keys(linha)
                            if i < len(linhas) - 1:  # Não adiciona quebra na última linha
                                caixa_mensagem.send_keys(Keys.SHIFT + Keys.ENTER)
                    time.sleep(1)
                except:
                    print("Erro ao digitar mensagem")
                    continue
                
                print("Enviando...")
                try:
                    caixa_mensagem.send_keys(Keys.ENTER)
                    
                    # Espera o check de enviado aparecer
                    self.wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@data-icon="msg-check" or @data-icon="msg-dblcheck"]'))
                    )
                    print("Mensagem enviada com sucesso! (confirmado)")
                    time.sleep(2)  # Espera adicional para garantir
                    return True
                except:
                    print("Não foi possível confirmar o envio")
                    continue
            
            except Exception as e:
                print(f"Erro na tentativa {tentativas}: {str(e)}")
                if tentativas < max_tentativas:
                    print("Tentando novamente...")
                    time.sleep(2)
        
        print(f"Falha após {max_tentativas} tentativas")
        return False

def identificar_genero(nome):
    nomes_femininos = ['beatriz', 'maria']
    primeiro_nome = nome.lower().split()[0]
    
    if primeiro_nome in nomes_femininos:
        return 'feminino'
    elif primeiro_nome[-1] == 'a' and primeiro_nome not in ['erick', 'jalbas']:
        return 'feminino'
    else:
        return 'masculino'

def gerar_mensagem(aluno):
    nome = aluno['nome'].split()[0]
    genero = identificar_genero(nome)
    
    if aluno.get("enviar_para_responsavel"):
        destinatario = f"Olá! Tudo bem?\n{nome}"
    else:
        destinatario = f"Olá, {nome}! Tudo bem?\nVocê"

    horarios_disponiveis = """Horários disponíveis para reposição (18 a 22 de agosto):

Segunda-feira:
• Manhã: 08:00 às 09:50 ou 10:00 às 11:50
• Tarde: 14:00 às 15:50 ou 16:00 às 17:50

Terça-feira:
• Manhã: 08:00 às 09:50 ou 10:00 às 11:50
• Noite: 19:00 às 20:50

Quarta-feira:
• Manhã: 08:00 às 09:50 ou 10:00 às 11:50
• Tarde: 14:00 às 15:50 ou 16:00 às 17:50"""

    if not aluno["faltas"]:
        return f"{destinatario} esteve presente em todas as aulas, não há reposições pendentes.\n— Erick Oliveira | Você+ Digital"
    
    if len(aluno["faltas"]) == 1:
        frase = "está" if genero == "feminino" else "está"
        return f"{destinatario} {frase} com uma aula pendente do dia {aluno['faltas'][0]}.\n\n{horarios_disponiveis}\n\nPor favor, me informe qual desses horários seria melhor para você.\nAguardo seu retorno!\n— Erick Oliveira | Você+ Digital"
    
    faltas_texto = ", ".join(aluno["faltas"])
    frase = "está" if genero == "feminino" else "está"
    return f"{destinatario} {frase} com aulas pendentes das seguintes datas: {faltas_texto}.\n\n{horarios_disponiveis}\n\nPor favor, me informe quais desses horários seriam melhores para você.\nAguardo seu retorno!\n— Erick Oliveira | Você+ Digital"

def main():
    bot = WhatsAppBot()
    bot.iniciar()
    
    # Pergunta se quer prosseguir com o teste
    print("\nVamos enviar mensagens para 3 alunos de teste:")
    for aluno in ALUNOS_TESTE:
        print(f"- {aluno['nome']} ({aluno['numero']})")
    
    confirma = input("\nDeseja prosseguir com o envio de teste? (s/n): ")
    if confirma.lower() != 's':
        print("Teste cancelado!")
        return
    
    for aluno in ALUNOS_TESTE:
        mensagem = gerar_mensagem(aluno)
        print(f"\nEnviando mensagem para {aluno['nome']} da {aluno['turma']}...")
        
        sucesso = bot.enviar_mensagem(aluno, mensagem)
        
        if sucesso:
            print(f"Mensagem enviada com sucesso para {aluno['nome']}!")
        else:
            print(f"Falha ao enviar mensagem para {aluno['nome']}")
        
        # Pergunta se quer continuar após cada envio
        if ALUNOS_TESTE.index(aluno) < len(ALUNOS_TESTE) - 1:
            continuar = input("\nDeseja continuar com o próximo envio? (s/n): ")
            if continuar.lower() != 's':
                print("Teste interrompido!")
                break

    print("\nTeste finalizado!")
    print("Se os testes foram bem sucedidos, você pode proceder com o envio para todos os alunos usando whatsapp_bot_v3.py")

if __name__ == "__main__":
    main()
