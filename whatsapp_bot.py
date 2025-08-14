from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WhatsAppBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 30)
        
    def iniciar(self):
        self.driver.get("https://web.whatsapp.com")
        print("Por favor, escaneie o QR Code do WhatsApp Web")
        input("Pressione Enter após escanear o QR Code...")

    def enviar_mensagem(self, numero, mensagem):
        try:
            # Formata o número para o link do WhatsApp
            numero = numero.replace("+", "").replace(" ", "").replace("-", "")
            link = f"https://web.whatsapp.com/send?phone={numero}"
            
            # Abre a conversa
            self.driver.get(link)
            
            # Espera a caixa de mensagem aparecer
            caixa_mensagem = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@title="Mensagem"]'))
            )
            
            # Divide a mensagem em linhas e envia cada linha
            for linha in mensagem.split('\n'):
                if linha.strip():  # Ignora linhas vazias
                    caixa_mensagem.send_keys(linha)
                    caixa_mensagem.send_keys(Keys.SHIFT + Keys.ENTER)  # Nova linha sem enviar
            
            # Envia a mensagem
            caixa_mensagem.send_keys(Keys.ENTER)
            time.sleep(2)  # Espera um pouco entre mensagens
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar mensagem para {numero}: {str(e)}")
            return False

from dados_alunos import ALUNOS_DADOS

def gerar_mensagem(aluno):
    if aluno.get("enviar_para_responsavel"):
        destinatario = f"Olá! Tudo bem? 😊\nO(A) {aluno['nome']}"
    else:
        destinatario = f"Olá, {aluno['nome']}! Tudo bem? 😊\nVocê"

    if not aluno["faltas"]:
        return f"{destinatario} esteve presente em todas as aulas, não há reposições pendentes. 🙌\n— Erick Oliveira | Você+ Digital"
    
    if len(aluno["faltas"]) == 1:
        return f"{destinatario} tem aula pendente no dia {aluno['faltas'][0]}.\nMe passe os dias e horários disponíveis para reposição.\nAguardo seu retorno!\n— Erick Oliveira | Você+ Digital"
    
    faltas_texto = ", ".join(aluno["faltas"])
    return f"{destinatario} tem aulas pendentes nas datas: {faltas_texto}.\nMe envie seus dias e horários disponíveis para reposição.\nAguardo seu retorno!\n— Erick Oliveira | Você+ Digital"

def main():
    bot = WhatsAppBot()
    bot.iniciar()
    
    for aluno in ALUNOS_DADOS:
        # Pula alunos que já receberam mensagem
        if aluno.get("ja_enviado"):
            print(f"Pulando {aluno['nome']} - mensagem já enviada anteriormente")
            continue
            
        mensagem = gerar_mensagem(aluno)
        print(f"\nEnviando mensagem para {aluno['nome']} da {aluno['turma']}...")
        
        # Decide qual número usar (do aluno ou do responsável)
        numero = aluno.get("numero_responsavel") if aluno.get("enviar_para_responsavel") and aluno.get("numero_responsavel") else aluno["numero"]
        
        sucesso = bot.enviar_mensagem(numero, mensagem)
        
        if sucesso:
            print(f"Mensagem enviada com sucesso para {aluno['nome']}!")
        else:
            print(f"Falha ao enviar mensagem para {aluno['nome']}")
        
        # Espera entre mensagens para evitar bloqueios
        time.sleep(3)

if __name__ == "__main__":
    main()
