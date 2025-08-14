#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para capturar APENAS respostas à mensagem de HOJE sobre reposição
Identifica a mensagem específica de hoje e ignora mensagens antigas
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
from datetime import datetime, timedelta
from dados_alunos import ALUNOS_DADOS

class CapturadorRespostasHoje:
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
        
        # Data de hoje para identificar mensagem específica
        self.hoje = datetime.now().date()
        
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
    
    def eh_mensagem_de_hoje(self, mensagem, timestamp_element):
        """Verifica se a mensagem é de HOJE sobre reposição de aulas"""
        mensagem_lower = mensagem.lower()
        
        # Palavras-chave que identificam mensagem sobre reposição
        palavras_chave_bot = [
            "aulas pendentes",
            "reposição de aulas",
            "reposicao de aulas",
            "faltas",
            "08:00 às 09:50",
            "10:00 às 11:50",
            "14:00 às 15:50",
            "16:00 às 17:50",
            "19:00 às 20:50",
            "erick oliveira",
            "você mais digital",
            "você+ digital"
        ]
        
        # Verifica se contém palavras-chave relevantes
        tem_palavras_chave = any(palavra in mensagem_lower for palavra in palavras_chave_bot)
        
        if not tem_palavras_chave:
            return False
        
        # Verifica se é uma mensagem ENVIADA (não recebida)
        if not timestamp_element:
            return False
        
        # Extrai a data/hora da mensagem
        try:
            # Procura por elementos de timestamp
            timestamp_text = timestamp_element.text.strip()
            
            # Verifica se é "Hoje" ou data de hoje
            if "hoje" in timestamp_text.lower():
                return True
            
            # Verifica se é uma data recente (últimos 2 dias)
            if ":" in timestamp_text:  # Formato de hora
                return True
                
        except Exception as e:
            print(f"   ⚠️ Erro ao verificar timestamp: {str(e)}")
            return False
        
        return False
    
    def eh_resposta_relevante(self, mensagem):
        """Captura TODAS as mensagens que vieram após a mensagem do bot de hoje"""
        # Agora captura TODAS as mensagens, independente do conteúdo
        # Isso permite organizar todas as demandas e processar cada uma
        return True
    
    def registrar_resposta_hoje(self, aluno, resposta, horario_preferido=None):
        """Registra uma resposta que veio DEPOIS da mensagem de HOJE"""
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
            "status": "resposta_hoje",
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

    def capturar_respostas_hoje_aluno(self, aluno):
        """Captura TODAS as mensagens que vieram DEPOIS da mensagem de HOJE"""
        try:
            print(f"\n🔍 Capturando respostas de HOJE de {aluno['nome']}...")
            
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
            encontrou_mensagem_hoje = False
            posicao_mensagem_hoje = -1
            
            # Procura por todas as mensagens na conversa
            try:
                todas_mensagens = self.driver.find_elements(
                    By.XPATH, '//div[@role="row"]'
                )
                
                if todas_mensagens:
                    print(f"   📝 Encontradas {len(todas_mensagens)} mensagens na conversa")
                    
                    # PRIMEIRA PASSADA: Encontrar a mensagem de HOJE sobre reposição
                    for i, mensagem in enumerate(todas_mensagens):
                        texto_mensagem = mensagem.text.strip()
                        
                        if not texto_mensagem or texto_mensagem == "Mensagem apagada":
                            continue
                        
                        mensagens_analisadas += 1
                        
                        # Procura pelo elemento de timestamp da mensagem
                        timestamp_element = None
                        try:
                            # Procura por elementos de timestamp
                            timestamp_elements = mensagem.find_elements(
                                By.XPATH, './/span[contains(@class, "copyable-text")]//span'
                            )
                            for elem in timestamp_elements:
                                if ":" in elem.text and len(elem.text) <= 10:
                                    timestamp_element = elem
                                    break
                        except:
                            pass
                        
                        # Verifica se é a mensagem de HOJE sobre reposição
                        if self.eh_mensagem_de_hoje(texto_mensagem, timestamp_element):
                            print(f"   🤖 MENSAGEM DE HOJE ENCONTRADA na posição {i}: {texto_mensagem[:80]}...")
                            encontrou_mensagem_hoje = True
                            posicao_mensagem_hoje = i
                            break
                    
                    # SEGUNDA PASSADA: Capturar respostas que vieram DEPOIS da mensagem de HOJE
                    if encontrou_mensagem_hoje and posicao_mensagem_hoje >= 0:
                        print(f"   🔍 Procurando respostas DEPOIS da posição {posicao_mensagem_hoje}...")
                        
                        # Itera pelas mensagens que vieram DEPOIS da mensagem de HOJE
                        for i in range(posicao_mensagem_hoje + 1, len(todas_mensagens)):
                            mensagem = todas_mensagens[i]
                            texto_mensagem = mensagem.text.strip()
                            
                            if not texto_mensagem or texto_mensagem == "Mensagem apagada":
                                continue
                            
                            # Verifica se é uma mensagem recebida (não enviada)
                            if mensagem.find_elements(By.XPATH, './/div[contains(@class, "message-in")]'):
                                print(f"   📨 Mensagem recebida encontrada: {texto_mensagem[:60]}...")
                                
                                # Captura TODAS as mensagens que vieram após a mensagem do bot
                                horario_preferido = self.extrair_horario_preferido(texto_mensagem)
                                if self.registrar_resposta_hoje(aluno, texto_mensagem, horario_preferido):
                                    respostas_capturadas += 1
                                    print(f"   ✅ Mensagem capturada: {texto_mensagem[:60]}...")
                                    if horario_preferido:
                                        print(f"      🕐 Horário identificado: {horario_preferido}")
                                else:
                                    print(f"   ⚠️ Mensagem já existia: {texto_mensagem[:40]}...")
                            else:
                                print(f"   📤 Mensagem enviada (ignorada): {texto_mensagem[:40]}...")
                
                if not encontrou_mensagem_hoje:
                    print(f"   ⚠️ Mensagem de HOJE sobre reposição NÃO encontrada para {aluno['nome']}")
                    print(f"   💡 Verifique se a mensagem foi enviada HOJE para este aluno")
                
            except Exception as e:
                print(f"   ⚠️ Erro ao analisar mensagens: {str(e)}")
            
            print(f"   📊 Mensagens analisadas: {mensagens_analisadas}")
            print(f"   📊 Mensagens de HOJE capturadas: {respostas_capturadas}")
            
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

    def capturar_respostas_hoje_todos(self):
        """Captura TODAS as mensagens de HOJE de todos os alunos"""
        print("\n🚀 Iniciando captura de mensagens de HOJE...")
        print("🎯 Capturando TODAS as mensagens que vieram após a mensagem de HOJE sobre reposição")
        print("🔍 Identificando mensagem específica de hoje e ignorando mensagens antigas")
        print("📅 Data de referência:", self.hoje.strftime("%d/%m/%Y"))
        
        total_alunos = len(ALUNOS_DADOS)
        total_respostas_capturadas = 0
        
        for i, aluno in enumerate(ALUNOS_DADOS, 1):
            print(f"\n[{i}/{total_alunos}] Processando {aluno['nome']}...")
            
            respostas_capturadas = self.capturar_respostas_hoje_aluno(aluno)
            total_respostas_capturadas += respostas_capturadas
            
            print(f"   📊 Mensagens de HOJE capturadas nesta sessão: {respostas_capturadas}")
            
            # Espera entre verificações para evitar bloqueio
            if i < total_alunos:
                print("   ⏳ Aguardando 5 segundos...")
                time.sleep(5)
        
        print(f"\n✅ Captura de mensagens de HOJE concluída!")
        print(f"📊 Total de alunos processados: {total_alunos}")
        print(f"📝 Total de mensagens de HOJE capturadas: {total_respostas_capturadas}")
        
        return total_respostas_capturadas

def main():
    print("📚 CAPTURADOR DE RESPOSTAS DE HOJE - REPOSIÇÃO DE AULAS")
    print("="*70)
    print("🎯 Este script captura TODAS as mensagens que vieram após a mensagem de HOJE sobre reposição")
    print("🤖 Identifica a mensagem específica de hoje (não mensagens antigas)")
    print("💬 Captura TODAS as mensagens posteriores à mensagem de hoje (para organizar demandas)")
    print("📅 Ignora completamente mensagens antigas sobre reposição")
    print("⚠️ ATENÇÃO: O processo pode demorar dependendo do número de alunos")
    print("="*70)
    
    print("\nEscolha uma opção:")
    print("1. 🔍 Capturar respostas de HOJE de todos os alunos")
    print("2. 👤 Capturar respostas de HOJE de aluno específico")
    print("3. ❌ Sair")
    
    opcao = input("\nDigite sua opção (1-3): ").strip()
    
    if opcao == "1":
        capturador = CapturadorRespostasHoje()
        capturador.iniciar()
        
        total_capturadas = capturador.capturar_respostas_hoje_todos()
        
        if total_capturadas > 0:
            print(f"\n🎉 {total_capturadas} mensagem(ns) de HOJE capturada(s)!")
            print("💡 Execute o bot principal para ver o relatório atualizado")
        else:
            print("\nℹ️ Nenhuma mensagem de HOJE foi capturada")
        
        capturador.driver.quit()
        
    elif opcao == "2":
        print("\n👤 Digite o nome do aluno para capturar respostas de HOJE:")
        nome_aluno = input("Nome: ").strip()
        
        # Encontra o aluno
        aluno_encontrado = None
        for aluno in ALUNOS_DADOS:
            if nome_aluno.lower() in aluno['nome'].lower():
                aluno_encontrado = aluno
                break
        
        if aluno_encontrado:
            capturador = CapturadorRespostasHoje()
            capturador.iniciar()
            
            print(f"\n🔍 Capturando respostas de HOJE de {aluno_encontrado['nome']}...")
            respostas_capturadas = capturador.capturar_respostas_hoje_aluno(aluno_encontrado)
            
            if respostas_capturadas > 0:
                print(f"\n✅ {respostas_capturadas} mensagem(ns) de HOJE capturada(s)!")
            else:
                print(f"\nℹ️ Nenhuma mensagem de HOJE foi capturada")
            
            capturador.driver.quit()
        else:
            print(f"❌ Aluno '{nome_aluno}' não encontrado")
    
    elif opcao == "3":
        print("👋 Saindo do capturador...")
    
    else:
        print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
