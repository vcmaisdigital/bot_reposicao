from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
import sys
from datetime import datetime
from dados_alunos import ALUNOS_DADOS

class WhatsAppBot:
    def __init__(self):
        try:
            # Configurar opções do Chrome
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            # Tentar diferentes métodos de inicialização
            self.driver = None
            
            # Método 1: Usar webdriver-manager (recomendado)
            try:
                print("🔧 Inicializando Chrome com webdriver-manager...")
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ Chrome inicializado com sucesso!")
            except Exception as e1:
                print(f"⚠️ Método 1 falhou: {e1}")
                
                # Método 2: Tentar usar Chrome diretamente
                try:
                    print("🔧 Tentando usar Chrome diretamente...")
                    self.driver = webdriver.Chrome(options=chrome_options)
                    print("✅ Chrome inicializado diretamente!")
                except Exception as e2:
                    print(f"⚠️ Método 2 falhou: {e2}")
                    
                    # Método 3: Usar caminho específico do Chrome
                    try:
                        print("🔧 Tentando usar caminho específico do Chrome...")
                        chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                        self.driver = webdriver.Chrome(options=chrome_options)
                        print("✅ Chrome inicializado com caminho específico!")
                    except Exception as e3:
                        print(f"❌ Todos os métodos falharam. Erro final: {e3}")
                        print("\n🔧 SOLUÇÕES POSSÍVEIS:")
                        print("1. Verifique se o Google Chrome está instalado")
                        print("2. Atualize o Chrome para a versão mais recente")
                        print("3. Execute: pip install --upgrade selenium webdriver-manager")
                        print("4. Reinicie o terminal/PowerShell")
                        sys.exit(1)
            
            self.wait = WebDriverWait(self.driver, 45)
            self.respostas = {}
            self.carregar_respostas()
            
        except Exception as e:
            print(f"❌ Erro crítico na inicialização: {e}")
            print("🔧 Verifique se o Chrome está instalado e atualizado")
            sys.exit(1)
    
    def carregar_respostas(self):
        try:
            with open('respostas.json', 'r', encoding='utf-8') as f:
                self.respostas = json.load(f)
        except FileNotFoundError:
            self.respostas = {}
    
    def salvar_respostas(self):
        with open('respostas.json', 'w', encoding='utf-8') as f:
            json.dump(self.respostas, f, ensure_ascii=False, indent=4)
    
    def registrar_resposta(self, aluno, resposta, horario_preferido=None, status="respondido"):
        """Registra a resposta de um aluno no sistema"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if aluno['nome'] not in self.respostas:
            self.respostas[aluno['nome']] = {
                "turma": aluno['turma'],
                "responsavel": aluno.get('responsavel', ''),
                "numero": aluno['numero'],
                "numero_responsavel": aluno.get('numero_responsavel', ''),
                "faltas": aluno['faltas'],
                "enviar_para_responsavel": aluno.get('enviar_para_responsavel', False),
                "respostas": []
            }
        
        resposta_info = {
            "timestamp": timestamp,
            "resposta": resposta,
            "horario_preferido": horario_preferido,
            "status": status
        }
        
        self.respostas[aluno['nome']]["respostas"].append(resposta_info)
        self.salvar_respostas()
        
        print(f"✅ Resposta registrada para {aluno['nome']}: {resposta[:50]}...")
    
    def marcar_mensagem_enviada(self, aluno):
        """Marca que a mensagem foi enviada para um aluno"""
        if aluno['nome'] not in self.respostas:
            self.respostas[aluno['nome']] = {
                "turma": aluno['turma'],
                "responsavel": aluno.get('responsavel', ''),
                "numero": aluno['numero'],
                "numero_responsavel": aluno.get('numero_responsavel', ''),
                "faltas": aluno['faltas'],
                "enviar_para_responsavel": aluno.get('enviar_para_responsavel', False),
                "respostas": [],
                "mensagem_enviada": True,
                "data_envio": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            self.respostas[aluno['nome']]["mensagem_enviada"] = True
            self.respostas[aluno['nome']]["data_envio"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.salvar_respostas()
        
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

    def enviar_mensagem_teste(self, aluno, mensagem):
        tentativas = 0
        max_tentativas = 3
        
        while tentativas < max_tentativas:
            try:
                tentativas += 1
                print(f"\nTentativa {tentativas} de {max_tentativas}")
                
                # Usa o número do responsável se for o caso, senão usa o número do aluno
                if aluno.get("enviar_para_responsavel") and aluno.get("numero_responsavel"):
                    numero = aluno["numero_responsavel"]
                else:
                    numero = aluno["numero"]
                numero = numero.replace("+", "").replace(" ", "").replace("-", "")
                link = f"https://web.whatsapp.com/send?phone={numero}"
                
                destinatario = "responsável " + aluno.get("responsavel", "") if aluno.get("enviar_para_responsavel") else "aluno(a)"
                numero_destino = aluno.get("numero_responsavel") if aluno.get("enviar_para_responsavel") and aluno.get("numero_responsavel") else aluno["numero"]
                print(f"Enviando mensagem para {aluno['nome']} ({destinatario}) no número {numero_destino}...")
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
                    
                    # Marca que a mensagem foi enviada
                    self.marcar_mensagem_enviada(aluno)
                    
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

    def verificar_respostas(self, aluno):
        """Verifica se há respostas do aluno e as registra"""
        try:
            # Navega para a conversa do aluno
            if aluno.get("enviar_para_responsavel") and aluno.get("numero_responsavel"):
                numero = aluno["numero_responsavel"]
            else:
                numero = aluno["numero"]
            
            numero = numero.replace("+", "").replace(" ", "").replace("-", "")
            link = f"https://web.whatsapp.com/send?phone={numero}"
            self.driver.get(link)
            
            if not self.esperar_pagina_carregar():
                return False
            
            # Aguarda carregar a conversa
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="main"]'))
                )
            except:
                return False
            
            # Procura por mensagens recebidas
            try:
                mensagens_recebidas = self.driver.find_elements(
                    By.XPATH, '//div[contains(@class, "message-in")]//div[@dir="ltr"]'
                )
                
                if mensagens_recebidas:
                    # Pega a última mensagem recebida
                    ultima_mensagem = mensagens_recebidas[-1].text.strip()
                    
                    if ultima_mensagem and ultima_mensagem != "Mensagem apagada":
                        # Analisa a mensagem para extrair horários preferidos
                        horario_preferido = self.extrair_horario_preferido(ultima_mensagem)
                        
                        # Registra a resposta
                        self.registrar_resposta(aluno, ultima_mensagem, horario_preferido)
                        return True
                        
            except Exception as e:
                print(f"Erro ao verificar mensagens: {str(e)}")
                
        except Exception as e:
            print(f"Erro ao verificar respostas de {aluno['nome']}: {str(e)}")
        
        return False
    
    def extrair_horario_preferido(self, mensagem):
        """Extrai horários preferidos da mensagem do aluno"""
        mensagem_lower = mensagem.lower()
        horarios = []
        
        # Padrões para identificar horários
        padroes = [
            ("segunda", "Segunda-feira"),
            ("terça", "Terça-feira"),
            ("quarta", "Quarta-feira"),
            ("manhã", "Manhã"),
            ("tarde", "Tarde"),
            ("noite", "Noite"),
            ("08:00", "08:00 às 09:50"),
            ("10:00", "10:00 às 11:50"),
            ("14:00", "14:00 às 15:50"),
            ("16:00", "16:00 às 17:50"),
            ("19:00", "19:00 às 20:50")
        ]
        
        for padrao, horario in padroes:
            if padrao in mensagem_lower:
                horarios.append(horario)
        
        if horarios:
            return ", ".join(horarios)
        return None

def identificar_genero(nome):
    # Lista de nomes femininos comuns que terminam diferente de 'a'
    nomes_femininos = ['beatriz', 'maria']
    
    # Pega o primeiro nome em caso de nomes compostos
    primeiro_nome = nome.lower().split()[0]
    
    # Verifica se é um nome conhecido feminino
    if primeiro_nome in nomes_femininos:
        return 'feminino'
    # Se termina em 'a', provavelmente é feminino (com exceções como Erick, Jalbas, etc)
    elif primeiro_nome[-1] == 'a' and primeiro_nome not in ['erick', 'jalbas']:
        return 'feminino'
    else:
        return 'masculino'

def gerar_mensagem(aluno):
    nome = aluno['nome'].split()[0]  # Pega só o primeiro nome
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

def gerar_relatorio_demandas():
    """Gera um relatório organizado das demandas de reposição"""
    try:
        with open('respostas.json', 'r', encoding='utf-8') as f:
            respostas = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo de respostas não encontrado. Execute o bot primeiro.")
        return
    
    print("\n" + "="*80)
    print("📊 RELATÓRIO DE DEMANDAS DE REPOSIÇÃO")
    print("="*80)
    
    # Organiza por turma
    turmas = {}
    for nome, dados in respostas.items():
        turma = dados.get('turma', 'Sem turma')
        if turma not in turmas:
            turmas[turma] = []
        turmas[turma].append((nome, dados))
    
    for turma, alunos in turmas.items():
        print(f"\n🏫 {turma}")
        print("-" * 40)
        
        for nome, dados in alunos:
            status = "✅ Respondido" if dados.get('respostas') else "⏳ Aguardando"
            mensagem = "✅ Enviada" if dados.get('mensagem_enviada') else "❌ Não enviada"
            
            print(f"\n👤 {nome}")
            print(f"   Status: {status} | Mensagem: {mensagem}")
            
            if dados.get('responsavel'):
                print(f"   Responsável: {dados['responsavel']}")
            
            if dados.get('faltas'):
                print(f"   Faltas: {', '.join(dados['faltas'])}")
            
            if dados.get('respostas'):
                ultima_resposta = dados['respostas'][-1]
                print(f"   Última resposta: {ultima_resposta['timestamp']}")
                print(f"   Conteúdo: {ultima_resposta['resposta'][:100]}...")
                
                if ultima_resposta.get('horario_preferido'):
                    print(f"   Horário preferido: {ultima_resposta['horario_preferido']}")
    
    print("\n" + "="*80)
    print("📋 RESUMO GERAL")
    print("="*80)
    
    total_alunos = len(respostas)
    mensagens_enviadas = sum(1 for dados in respostas.values() if dados.get('mensagem_enviada'))
    alunos_respondidos = sum(1 for dados in respostas.values() if dados.get('respostas'))
    
    print(f"Total de alunos: {total_alunos}")
    print(f"Mensagens enviadas: {mensagens_enviadas}")
    print(f"Alunos que responderam: {alunos_respondidos}")
    print(f"Taxa de resposta: {(alunos_respondidos/total_alunos*100):.1f}%" if total_alunos > 0 else "0%")

def main():
    print("🤖 BOT DE REPOSIÇÃO DE AULAS - VERSÃO COMPLETA")
    print("="*50)
    
    while True:
        print("\nEscolha uma opção:")
        print("1. Enviar mensagens para todos os alunos")
        print("2. Verificar respostas dos alunos")
        print("3. Gerar relatório de demandas")
        print("4. Sair")
        
        opcao = input("\nDigite sua opção (1-4): ").strip()
        
        if opcao == "1":
            bot = WhatsAppBot()
            bot.iniciar()
            
            for aluno in ALUNOS_DADOS:
                if aluno.get("ja_enviado"):
                    print(f"Pulando {aluno['nome']} - mensagem já enviada anteriormente")
                    continue
                    
                mensagem = gerar_mensagem(aluno)
                print(f"\nEnviando mensagem para {aluno['nome']} da {aluno['turma']}...")
                
                sucesso = bot.enviar_mensagem_teste(aluno, mensagem)
                
                if sucesso:
                    print(f"Mensagem enviada com sucesso para {aluno['nome']}!")
                else:
                    print(f"Falha ao enviar mensagem para {aluno['nome']}")
                
                # Espera entre mensagens para evitar bloqueio
                time.sleep(3)
            
            print("\nProcesso de envio finalizado!")
            bot.driver.quit()
            
        elif opcao == "2":
            bot = WhatsAppBot()
            bot.iniciar()
            
            print("\nVerificando respostas dos alunos...")
            for aluno in ALUNOS_DADOS:
                if not aluno.get("ja_enviado"):
                    print(f"\nVerificando {aluno['nome']}...")
                    bot.verificar_respostas(aluno)
                    time.sleep(2)
            
            print("\nVerificação de respostas finalizada!")
            bot.driver.quit()
            
        elif opcao == "3":
            gerar_relatorio_demandas()
            
        elif opcao == "4":
            print("👋 Saindo do bot...")
            break
            
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
