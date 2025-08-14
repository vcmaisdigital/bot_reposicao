#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script FILTRADO para capturar apenas respostas sobre reposição de aulas
Versão que identifica e filtra apenas mensagens relevantes
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

class CapturadorHistoricoFiltrado:
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
    
    def registrar_resposta_historico(self, aluno, resposta, horario_preferido=None):
        """Registra uma resposta do histórico apenas se for relevante"""
        # Verifica se é uma resposta relevante
        if not self.eh_resposta_relevante(resposta):
            return False
        
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
            "status": "capturado_do_historico",
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

    def capturar_historico_aluno(self, aluno):
        """Captura apenas respostas RELEVANTES do histórico de um aluno"""
        try:
            print(f"\n🔍 Capturando histórico de {aluno['nome']}...")
            
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
            
            # Método 1: Procura por mensagens com classe específica
            try:
                mensagens_recebidas = self.driver.find_elements(
                    By.XPATH, '//div[contains(@class, "message-in")]//div[@dir="ltr"]'
                )
                
                if mensagens_recebidas:
                    print(f"   📝 Método 1: Encontradas {len(mensagens_recebidas)} mensagens")
                    for i, mensagem in enumerate(mensagens_recebidas):
                        texto_mensagem = mensagem.text.strip()
                        if texto_mensagem and texto_mensagem != "Mensagem apagada":
                            mensagens_analisadas += 1
                            
                            # Verifica se é uma resposta relevante
                            if self.eh_resposta_relevante(texto_mensagem):
                                horario_preferido = self.extrair_horario_preferido(texto_mensagem)
                                if self.registrar_resposta_historico(aluno, texto_mensagem, horario_preferido):
                                    respostas_capturadas += 1
                                    print(f"   ✅ Resposta {i+1} RELEVANTE capturada: {texto_mensagem[:60]}...")
                                    if horario_preferido:
                                        print(f"      🕐 Horário identificado: {horario_preferido}")
                                else:
                                    print(f"   ⚠️ Resposta {i+1} já existia: {texto_mensagem[:40]}...")
                            else:
                                print(f"   ❌ Resposta {i+1} NÃO RELEVANTE: {texto_mensagem[:40]}...")
            except Exception as e:
                print(f"   ⚠️ Método 1 falhou: {str(e)}")
            
            # Método 2: Procura por mensagens com atributo data-pre-plain-text
            if respostas_capturadas == 0:
                try:
                    mensagens_recebidas = self.driver.find_elements(
                        By.XPATH, '//div[@data-pre-plain-text]'
                    )
                    
                    if mensagens_recebidas:
                        print(f"   📝 Método 2: Encontradas {len(mensagens_recebidas)} mensagens")
                        for i, mensagem in enumerate(mensagens_recebidas):
                            # Verifica se é uma mensagem recebida (não enviada)
                            data_attr = mensagem.get_attribute('data-pre-plain-text')
                            if data_attr and '[' in data_attr and ']' in data_attr:
                                texto_mensagem = mensagem.text.strip()
                                if texto_mensagem and texto_mensagem != "Mensagem apagada":
                                    mensagens_analisadas += 1
                                    
                                    # Verifica se é uma resposta relevante
                                    if self.eh_resposta_relevante(texto_mensagem):
                                        horario_preferido = self.extrair_horario_preferido(texto_mensagem)
                                        if self.registrar_resposta_historico(aluno, texto_mensagem, horario_preferido):
                                            respostas_capturadas += 1
                                            print(f"   ✅ Resposta {i+1} RELEVANTE capturada: {texto_mensagem[:60]}...")
                                            if horario_preferido:
                                                print(f"      🕐 Horário identificado: {horario_preferido}")
                                        else:
                                            print(f"   ⚠️ Resposta {i+1} já existia: {texto_mensagem[:40]}...")
                                    else:
                                        print(f"   ❌ Resposta {i+1} NÃO RELEVANTE: {texto_mensagem[:40]}...")
                except Exception as e:
                    print(f"   ⚠️ Método 2 falhou: {str(e)}")
            
            # Método 3: Procura por mensagens com role="row" e verifica se é recebida
            if respostas_capturadas == 0:
                try:
                    todas_mensagens = self.driver.find_elements(
                        By.XPATH, '//div[@role="row"]'
                    )
                    
                    mensagens_recebidas = []
                    for msg in todas_mensagens:
                        # Verifica se a mensagem tem elementos que indicam que foi recebida
                        if msg.find_elements(By.XPATH, './/div[contains(@class, "message-in")]'):
                            mensagens_recebidas.append(msg)
                    
                    if mensagens_recebidas:
                        print(f"   📝 Método 3: Encontradas {len(mensagens_recebidas)} mensagens")
                        for i, mensagem in enumerate(mensagens_recebidas):
                            texto_mensagem = mensagem.text.strip()
                            if texto_mensagem and texto_mensagem != "Mensagem apagada":
                                mensagens_analisadas += 1
                                
                                # Verifica se é uma resposta relevante
                                if self.eh_resposta_relevante(texto_mensagem):
                                    horario_preferido = self.extrair_horario_preferido(texto_mensagem)
                                    if self.registrar_resposta_historico(aluno, texto_mensagem, horario_preferido):
                                        respostas_capturadas += 1
                                        print(f"   ✅ Resposta {i+1} RELEVANTE capturada: {texto_mensagem[:60]}...")
                                        if horario_preferido:
                                            print(f"      🕐 Horário identificado: {horario_preferido}")
                                    else:
                                        print(f"   ⚠️ Resposta {i+1} já existia: {texto_mensagem[:40]}...")
                                else:
                                    print(f"   ❌ Resposta {i+1} NÃO RELEVANTE: {texto_mensagem[:40]}...")
                except Exception as e:
                    print(f"   ⚠️ Método 3 falhou: {str(e)}")
            
            print(f"   📊 Mensagens analisadas: {mensagens_analisadas}")
            print(f"   📊 Respostas RELEVANTES capturadas: {respostas_capturadas}")
            
            return respostas_capturadas
                        
        except Exception as e:
            print(f"   ❌ Erro ao capturar histórico de {aluno['nome']}: {str(e)}")
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

    def capturar_historico_todos(self):
        """Captura histórico de todos os alunos - APENAS RESPOSTAS RELEVANTES"""
        print("\n🚀 Iniciando captura FILTRADA do histórico de respostas...")
        print("🎯 Capturando APENAS respostas relevantes sobre reposição de aulas")
        print("🔧 Usando filtros para mensagens importantes")
        
        total_alunos = len(ALUNOS_DADOS)
        total_respostas_capturadas = 0
        
        for i, aluno in enumerate(ALUNOS_DADOS, 1):
            print(f"\n[{i}/{total_alunos}] Processando {aluno['nome']}...")
            
            respostas_capturadas = self.capturar_historico_aluno(aluno)
            total_respostas_capturadas += respostas_capturadas
            
            print(f"   📊 Respostas RELEVANTES capturadas nesta sessão: {respostas_capturadas}")
            
            # Espera entre verificações para evitar bloqueio
            if i < total_alunos:
                print("   ⏳ Aguardando 5 segundos...")
                time.sleep(5)
        
        print(f"\n✅ Captura FILTRADA de histórico concluída!")
        print(f"📊 Total de alunos processados: {total_alunos}")
        print(f"📝 Total de respostas RELEVANTES capturadas: {total_respostas_capturadas}")
        
        return total_respostas_capturadas

def main():
    print("📚 CAPTURADOR DE HISTÓRICO FILTRADO - REPOSIÇÃO DE AULAS")
    print("="*70)
    print("🎯 Este script captura APENAS respostas relevantes sobre reposição")
    print("🔍 Filtra mensagens antigas e irrelevantes")
    print("💬 Captura apenas respostas sobre horários e disponibilidade")
    print("⚠️ ATENÇÃO: O processo pode demorar dependendo do número de alunos")
    print("="*70)
    
    print("\nEscolha uma opção:")
    print("1. 🔍 Capturar histórico FILTRADO de todos os alunos")
    print("2. 👤 Capturar histórico FILTRADO de aluno específico")
    print("3. ❌ Sair")
    
    opcao = input("\nDigite sua opção (1-3): ").strip()
    
    if opcao == "1":
        capturador = CapturadorHistoricoFiltrado()
        capturador.iniciar()
        
        total_capturadas = capturador.capturar_historico_todos()
        
        if total_capturadas > 0:
            print(f"\n🎉 {total_capturadas} resposta(s) RELEVANTE(S) capturada(s) do histórico!")
            print("💡 Execute o bot principal para ver o relatório atualizado")
        else:
            print("\nℹ️ Nenhuma resposta relevante foi capturada do histórico")
        
        capturador.driver.quit()
        
    elif opcao == "2":
        print("\n👤 Digite o nome do aluno para capturar histórico FILTRADO:")
        nome_aluno = input("Nome: ").strip()
        
        # Encontra o aluno
        aluno_encontrado = None
        for aluno in ALUNOS_DADOS:
            if nome_aluno.lower() in aluno['nome'].lower():
                aluno_encontrado = aluno
                break
        
        if aluno_encontrado:
            capturador = CapturadorHistoricoFiltrado()
            capturador.iniciar()
            
            print(f"\n🔍 Capturando histórico FILTRADO de {aluno_encontrado['nome']}...")
            respostas_capturadas = capturador.capturar_historico_aluno(aluno_encontrado)
            
            if respostas_capturadas > 0:
                print(f"\n✅ {respostas_capturadas} resposta(s) RELEVANTE(S) capturada(s) do histórico!")
            else:
                print(f"\nℹ️ Nenhuma resposta relevante foi capturada")
            
            capturador.driver.quit()
        else:
            print(f"❌ Aluno '{nome_aluno}' não encontrado")
    
    elif opcao == "3":
        print("👋 Saindo do capturador...")
    
    else:
        print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
