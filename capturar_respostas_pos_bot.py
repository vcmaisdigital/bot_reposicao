#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para capturar APENAS respostas que vieram DEPOIS da mensagem do bot
Identifica a mensagem de reposição e captura respostas posteriores
"""

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

class CapturadorRespostasPosBot:
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
                    "mensagem_enviada": True,
                    "data_envio": "Enviada anteriormente"
                }
            print("✅ Estrutura inicial criada para todos os alunos")
    
    def salvar_respostas(self):
        """Salva as respostas no arquivo JSON"""
        with open('respostas.json', 'w', encoding='utf-8') as f:
            json.dump(self.respostas, f, ensure_ascii=False, indent=4)
    
    def eh_mensagem_do_bot(self, mensagem):
        """Verifica se a mensagem é do bot sobre reposição de aulas"""
        mensagem_lower = mensagem.lower()
        
        # Palavras-chave que identificam mensagem do bot sobre reposição
        palavras_chave_bot = [
            "aulas pendentes",
            "reposição de aulas",
            "reposicao de aulas",
            "faltas",
            "segunda-feira",
            "terça-feira",
            "quarta-feira",
            "08:00 às 09:50",
            "10:00 às 11:50",
            "14:00 às 15:50",
            "16:00 às 17:50",
            "19:00 às 20:50",
            "erick oliveira",
            "você mais digital",
            "você+ digital"
        ]
        
        # Verifica se contém palavras-chave do bot
        for palavra in palavras_chave_bot:
            if palavra in mensagem_lower:
                return True
        
        return False
    
    def eh_resposta_relevante(self, mensagem):
        """Verifica se a mensagem é uma resposta relevante sobre reposição de aulas"""
        mensagem_lower = mensagem.lower()
        
        # Palavras-chave que indicam resposta sobre horários/aulas
        palavras_chave = [
            "segunda", "terça", "quarta", "quinta", "sexta",
            "manhã", "tarde", "noite", "manha", "noite",
            "08:00", "10:00", "14:00", "16:00", "19:00",
            "pode", "consigo", "disponível", "disponivel",
            "horário", "horario", "aula", "reposição", "reposicao",
            "ok", "certo", "blz", "beleza", "sim", "não", "nao",
            "não posso", "nao posso", "não consigo", "nao consigo"
        ]
        
        # Verifica se contém palavras-chave relevantes
        for palavra in palavras_chave:
            if palavra in mensagem_lower:
                return True
        
        # Verifica se é uma resposta curta e direta (comum em WhatsApp)
        if len(mensagem.strip()) <= 50 and any(palavra in mensagem_lower for palavra in ["ok", "certo", "blz", "beleza", "sim", "não", "nao"]):
            return True
        
        return False
    
    def registrar_resposta_pos_bot(self, aluno, resposta, horario_preferido=None):
        """Registra uma resposta que veio DEPOIS da mensagem do bot"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Verifica se já existe resposta igual para evitar duplicatas
        if aluno['nome'] in self.respostas:
            respostas_existentes = self.respostas[aluno['nome']].get('respostas', [])
            for resp in respostas_existentes:
                if resp['resposta'].strip() == resposta.strip():
                    return False  # Resposta já existe
        
        resposta_info = {
            "timestamp": timestamp,
            "resposta": resposta,
            "horario_preferido": horario_preferido,
            "status": "resposta_pos_bot",
            "relevante": True
        }
        
        self.respostas[aluno['nome']]["respostas"].append(resposta_info)
        self.salvar_respostas()
        
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

    def capturar_respostas_pos_bot_aluno(self, aluno):
        """Captura apenas respostas que vieram DEPOIS da mensagem do bot"""
        try:
            print(f"\n🔍 Capturando respostas POS-BOT de {aluno['nome']}...")
            
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
                return 0
            
            # Aguarda carregar a conversa
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="main"]'))
                )
            except:
                print(f"   ❌ Conversa não carregou para {aluno['nome']}")
                return 0
            
            respostas_capturadas = 0
            mensagens_analisadas = 0
            encontrou_mensagem_bot = False
            
            # Procura por todas as mensagens na conversa
            try:
                todas_mensagens = self.driver.find_elements(
                    By.XPATH, '//div[@role="row"]'
                )
                
                if todas_mensagens:
                    print(f"   📝 Encontradas {len(todas_mensagens)} mensagens na conversa")
                    
                    # Itera pelas mensagens de baixo para cima (mais recentes primeiro)
                    for i, mensagem in enumerate(reversed(todas_mensagens)):
                        texto_mensagem = mensagem.text.strip()
                        
                        if not texto_mensagem or texto_mensagem == "Mensagem apagada":
                            continue
                        
                        mensagens_analisadas += 1
                        
                        # Verifica se é a mensagem do bot
                        if self.eh_mensagem_do_bot(texto_mensagem):
                            print(f"   🤖 MENSAGEM DO BOT ENCONTRADA: {texto_mensagem[:80]}...")
                            encontrou_mensagem_bot = True
                            break
                        
                        # Se ainda não encontrou a mensagem do bot, continua procurando
                        if not encontrou_mensagem_bot:
                            continue
                        
                        # Se encontrou a mensagem do bot, agora procura por respostas
                        # Verifica se é uma mensagem recebida (não enviada)
                        if mensagem.find_elements(By.XPATH, './/div[contains(@class, "message-in")]'):
                            # Verifica se é uma resposta relevante
                            if self.eh_resposta_relevante(texto_mensagem):
                                horario_preferido = self.extrair_horario_preferido(texto_mensagem)
                                if self.registrar_resposta_pos_bot(aluno, texto_mensagem, horario_preferido):
                                    respostas_capturadas += 1
                                    print(f"   ✅ Resposta POS-BOT capturada: {texto_mensagem[:60]}...")
                                    if horario_preferido:
                                        print(f"      🕐 Horário identificado: {horario_preferido}")
                                else:
                                    print(f"   ⚠️ Resposta já existia: {texto_mensagem[:40]}...")
                            else:
                                print(f"   ❌ Resposta não relevante: {texto_mensagem[:40]}...")
                
                if not encontrou_mensagem_bot:
                    print(f"   ⚠️ Mensagem do bot NÃO encontrada para {aluno['nome']}")
                    print(f"   💡 Verifique se a mensagem foi enviada para este aluno")
                
            except Exception as e:
                print(f"   ⚠️ Erro ao analisar mensagens: {str(e)}")
            
            print(f"   📊 Mensagens analisadas: {mensagens_analisadas}")
            print(f"   📊 Respostas POS-BOT capturadas: {respostas_capturadas}")
            
            return respostas_capturadas
                        
        except Exception as e:
            print(f"   ❌ Erro ao capturar respostas de {aluno['nome']}: {str(e)}")
            return 0
    
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

    def capturar_respostas_pos_bot_todos(self):
        """Captura respostas POS-BOT de todos os alunos"""
        print("\n🚀 Iniciando captura de respostas POS-BOT...")
        print("🎯 Capturando APENAS respostas que vieram DEPOIS da mensagem do bot")
        print("🔍 Identificando mensagem de reposição e capturando respostas posteriores")
        
        total_alunos = len(ALUNOS_DADOS)
        total_respostas_capturadas = 0
        
        for i, aluno in enumerate(ALUNOS_DADOS, 1):
            print(f"\n[{i}/{total_alunos}] Processando {aluno['nome']}...")
            
            respostas_capturadas = self.capturar_respostas_pos_bot_aluno(aluno)
            total_respostas_capturadas += respostas_capturadas
            
            print(f"   📊 Respostas POS-BOT capturadas nesta sessão: {respostas_capturadas}")
            
            # Espera entre verificações para evitar bloqueio
            if i < total_alunos:
                print("   ⏳ Aguardando 5 segundos...")
                time.sleep(5)
        
        print(f"\n✅ Captura de respostas POS-BOT concluída!")
        print(f"📊 Total de alunos processados: {total_alunos}")
        print(f"📝 Total de respostas POS-BOT capturadas: {total_respostas_capturadas}")
        
        return total_respostas_capturadas

def main():
    print("📚 CAPTURADOR DE RESPOSTAS POS-BOT - REPOSIÇÃO DE AULAS")
    print("="*70)
    print("🎯 Este script captura APENAS respostas que vieram DEPOIS da mensagem do bot")
    print("🤖 Identifica a mensagem de reposição enviada pelo bot")
    print("💬 Captura apenas respostas posteriores sobre horários e disponibilidade")
    print("⚠️ ATENÇÃO: O processo pode demorar dependendo do número de alunos")
    print("="*70)
    
    print("\nEscolha uma opção:")
    print("1. 🔍 Capturar respostas POS-BOT de todos os alunos")
    print("2. 👤 Capturar respostas POS-BOT de aluno específico")
    print("3. ❌ Sair")
    
    opcao = input("\nDigite sua opção (1-3): ").strip()
    
    if opcao == "1":
        capturador = CapturadorRespostasPosBot()
        capturador.iniciar()
        
        total_capturadas = capturador.capturar_respostas_pos_bot_todos()
        
        if total_capturadas > 0:
            print(f"\n🎉 {total_capturadas} resposta(s) POS-BOT capturada(s)!")
            print("💡 Execute o bot principal para ver o relatório atualizado")
        else:
            print("\nℹ️ Nenhuma resposta POS-BOT foi capturada")
        
        capturador.driver.quit()
        
    elif opcao == "2":
        print("\n👤 Digite o nome do aluno para capturar respostas POS-BOT:")
        nome_aluno = input("Nome: ").strip()
        
        # Encontra o aluno
        aluno_encontrado = None
        for aluno in ALUNOS_DADOS:
            if nome_aluno.lower() in aluno['nome'].lower():
                aluno_encontrado = aluno
                break
        
        if aluno_encontrado:
            capturador = CapturadorRespostasPosBot()
            capturador.iniciar()
            
            print(f"\n🔍 Capturando respostas POS-BOT de {aluno_encontrado['nome']}...")
            respostas_capturadas = capturador.capturar_respostas_pos_bot_aluno(aluno_encontrado)
            
            if respostas_capturadas > 0:
                print(f"\n✅ {respostas_capturadas} resposta(s) POS-BOT capturada(s)!")
            else:
                print(f"\nℹ️ Nenhuma resposta POS-BOT foi capturada")
            
            capturador.driver.quit()
        else:
            print(f"❌ Aluno '{nome_aluno}' não encontrado")
    
    elif opcao == "3":
        print("👋 Saindo do capturador...")
    
    else:
        print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
