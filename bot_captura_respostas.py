from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime
from dados_alunos import ALUNOS_DADOS

class BotCapturaRespostas:
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
        """Carrega respostas existentes ou cria estrutura inicial"""
        try:
            with open('respostas.json', 'r', encoding='utf-8') as f:
                self.respostas = json.load(f)
                print(f"✅ Carregadas {len(self.respostas)} respostas existentes")
        except FileNotFoundError:
            # Cria estrutura inicial baseada nos dados dos alunos
            self.respostas = {}
            for aluno in ALUNOS_DADOS:
                self.respostas[aluno['nome']] = {
                    "turma": aluno['turma'],
                    "responsavel": aluno.get('responsavel', ''),
                    "numero": aluno['numero'],
                    "numero_responsavel": aluno.get('numero_responsavel', ''),
                    "faltas": aluno['faltas'],
                    "enviar_para_responsavel": aluno.get('enviar_para_responsavel', False),
                    "respostas": [],
                    "mensagem_enviada": True,  # Assumindo que já foi enviada
                    "data_envio": "Enviada anteriormente"
                }
            print("✅ Estrutura inicial criada para todos os alunos")
    
    def salvar_respostas(self):
        """Salva as respostas no arquivo JSON"""
        with open('respostas.json', 'w', encoding='utf-8') as f:
            json.dump(self.respostas, f, ensure_ascii=False, indent=4)
    
    def registrar_resposta(self, aluno, resposta, horario_preferido=None, status="respondido"):
        """Registra a resposta de um aluno no sistema"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verifica se já existe resposta igual para evitar duplicatas
        if aluno['nome'] in self.respostas:
            respostas_existentes = self.respostas[aluno['nome']].get('respostas', [])
            for resp in respostas_existentes:
                if resp['resposta'].strip() == resposta.strip():
                    print(f"⚠️ Resposta já registrada para {aluno['nome']}")
                    return False
        
        resposta_info = {
            "timestamp": timestamp,
            "resposta": resposta,
            "horario_preferido": horario_preferido,
            "status": status
        }
        
        self.respostas[aluno['nome']]["respostas"].append(resposta_info)
        self.salvar_respostas()
        
        print(f"✅ Nova resposta registrada para {aluno['nome']}: {resposta[:50]}...")
        return True
        
    def iniciar(self):
        """Inicia o WhatsApp Web"""
        self.driver.get("https://web.whatsapp.com")
        print("📱 Por favor, escaneie o QR Code do WhatsApp Web")
        input("Pressione Enter após escanear o QR Code...")

    def esperar_pagina_carregar(self):
        """Aguarda a página carregar completamente"""
        try:
            self.wait.until_not(
                EC.presence_of_element_located((By.XPATH, '//*[@role="progressbar"]'))
            )
            time.sleep(2)
            return True
        except:
            return False

    def verificar_respostas_aluno(self, aluno):
        """Verifica se há respostas do aluno e as registra"""
        try:
            print(f"\n🔍 Verificando {aluno['nome']}...")
            
            # Navega para a conversa do aluno
            if aluno.get("enviar_para_responsavel") and aluno.get("numero_responsavel"):
                numero = aluno["numero_responsavel"]
                destinatario = f"responsável {aluno.get('responsavel', '')}"
            else:
                numero = aluno["numero"]
                destinatario = "aluno(a)"
            
            numero = numero.replace("+", "").replace(" ", "").replace("-", "")
            link = f"https://web.whatsapp.com/send?phone={numero}"
            self.driver.get(link)
            
            if not self.esperar_pagina_carregar():
                print(f"   ❌ Página não carregou para {aluno['nome']}")
                return False
            
            # Aguarda carregar a conversa
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="main"]'))
                )
            except:
                print(f"   ❌ Conversa não carregou para {aluno['nome']}")
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
                        if self.registrar_resposta(aluno, ultima_mensagem, horario_preferido):
                            print(f"   ✅ Resposta capturada: {ultima_mensagem[:80]}...")
                            if horario_preferido:
                                print(f"   🕐 Horário preferido identificado: {horario_preferido}")
                        return True
                    else:
                        print(f"   ⚠️ Nenhuma mensagem válida encontrada para {aluno['nome']}")
                else:
                    print(f"   ⚠️ Nenhuma mensagem recebida para {aluno['nome']}")
                        
            except Exception as e:
                print(f"   ❌ Erro ao verificar mensagens: {str(e)}")
                
        except Exception as e:
            print(f"   ❌ Erro ao verificar {aluno['nome']}: {str(e)}")
        
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

    def verificar_todos_alunos(self):
        """Verifica respostas de todos os alunos"""
        print("\n🚀 Iniciando verificação de respostas...")
        
        total_alunos = len(ALUNOS_DADOS)
        respostas_capturadas = 0
        
        for i, aluno in enumerate(ALUNOS_DADOS, 1):
            print(f"\n[{i}/{total_alunos}] Verificando {aluno['nome']}...")
            
            if self.verificar_respostas_aluno(aluno):
                respostas_capturadas += 1
            
            # Espera entre verificações para evitar bloqueio
            if i < total_alunos:
                print("   ⏳ Aguardando 3 segundos...")
                time.sleep(3)
        
        print(f"\n✅ Verificação concluída!")
        print(f"📊 Total de alunos verificados: {total_alunos}")
        print(f"📝 Respostas capturadas nesta sessão: {respostas_capturadas}")
        
        return respostas_capturadas

def gerar_relatorio_atualizado():
    """Gera um relatório atualizado das respostas"""
    try:
        with open('respostas.json', 'r', encoding='utf-8') as f:
            respostas = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo de respostas não encontrado.")
        return
    
    print("\n" + "="*80)
    print("📊 RELATÓRIO ATUALIZADO DE RESPOSTAS")
    print("="*80)
    
    # Organiza por turma
    turmas = {}
    for nome, dados in respostas.items():
        turma = dados.get('turma', 'Sem turma')
        if turma not in turmas:
            turmas[turma] = []
        turmas[turma].append((nome, dados))
    
    total_respostas = 0
    total_alunos = len(respostas)
    
    for turma, alunos in turmas.items():
        print(f"\n🏫 {turma}")
        print("-" * 40)
        
        for nome, dados in alunos:
            num_respostas = len(dados.get('respostas', []))
            total_respostas += num_respostas
            
            if num_respostas > 0:
                status = f"✅ {num_respostas} resposta(s)"
                ultima_resposta = dados['respostas'][-1]
                print(f"\n👤 {nome} - {status}")
                print(f"   📅 Última resposta: {ultima_resposta['timestamp']}")
                print(f"   💬 Conteúdo: {ultima_resposta['resposta'][:100]}...")
                
                if ultima_resposta.get('horario_preferido'):
                    print(f"   🕐 Horário preferido: {ultima_resposta['horario_preferido']}")
            else:
                print(f"\n👤 {nome} - ⏳ Aguardando resposta")
    
    print("\n" + "="*80)
    print("📋 RESUMO GERAL")
    print("="*80)
    
    alunos_respondidos = sum(1 for dados in respostas.values() if dados.get('respostas'))
    
    print(f"Total de alunos: {total_alunos}")
    print(f"Alunos que responderam: {alunos_respondidos}")
    print(f"Total de respostas capturadas: {total_respostas}")
    print(f"Taxa de resposta: {(alunos_respondidos/total_alunos*100):.1f}%" if total_alunos > 0 else "0%")

def main():
    print("🤖 BOT DE CAPTURA DE RESPOSTAS - REPOSIÇÃO DE AULAS")
    print("="*60)
    print("📱 Este bot captura respostas dos alunos sobre reposição de aulas")
    print("💬 As mensagens já foram enviadas anteriormente")
    print("="*60)
    
    while True:
        print("\nEscolha uma opção:")
        print("1. 🔍 Verificar respostas de todos os alunos")
        print("2. 📊 Gerar relatório atualizado")
        print("3. 🔄 Verificar aluno específico")
        print("4. ❌ Sair")
        
        opcao = input("\nDigite sua opção (1-4): ").strip()
        
        if opcao == "1":
            bot = BotCapturaRespostas()
            bot.iniciar()
            
            respostas_capturadas = bot.verificar_todos_alunos()
            
            if respostas_capturadas > 0:
                print(f"\n🎉 {respostas_capturadas} nova(s) resposta(s) capturada(s)!")
                print("💡 Execute a opção 2 para ver o relatório atualizado")
            else:
                print("\nℹ️ Nenhuma nova resposta foi capturada")
            
            bot.driver.quit()
            
        elif opcao == "2":
            gerar_relatorio_atualizado()
            
        elif opcao == "3":
            print("\n👤 Digite o nome do aluno para verificar:")
            nome_aluno = input("Nome: ").strip()
            
            # Encontra o aluno
            aluno_encontrado = None
            for aluno in ALUNOS_DADOS:
                if nome_aluno.lower() in aluno['nome'].lower():
                    aluno_encontrado = aluno
                    break
            
            if aluno_encontrado:
                bot = BotCapturaRespostas()
                bot.iniciar()
                
                print(f"\n🔍 Verificando {aluno_encontrado['nome']}...")
                bot.verificar_respostas_aluno(aluno_encontrado)
                
                bot.driver.quit()
            else:
                print(f"❌ Aluno '{nome_aluno}' não encontrado")
            
        elif opcao == "4":
            print("👋 Saindo do bot...")
            break
            
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
