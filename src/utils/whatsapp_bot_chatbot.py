#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 WHATSAPP BOT COM CHATBOT ESCOLAR INTEGRADO
Sistema completo de auto-atendimento via WhatsApp
"""

import json
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Importar o chatbot escolar
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.chatbot.chatbot_escola_completo import ChatBotEscolaCompleto

class WhatsAppBotChatbot:
    def __init__(self):
        """Inicializa o bot WhatsApp com chatbot escolar"""
        self.configurar_chrome()
        self.chatbot = ChatBotEscolaCompleto()
        self.conversas_ativas = {}
        self.historico_mensagens = {}
        
    def configurar_chrome(self):
        """Configura o Chrome para WhatsApp Web"""
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

            # Inicializar Chrome
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 45)
            
            print("✅ Chrome configurado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao configurar Chrome: {e}")
            raise
            
    def abrir_whatsapp(self):
        """Abre o WhatsApp Web"""
        try:
            print("🌐 Abrindo WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com/")
            
            # Aguardar QR Code
            print("📱 Escaneie o QR Code no seu celular...")
            self.wait.until(EC.presence_of_element_located((By.ID, "side")))
            print("✅ WhatsApp Web conectado!")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao abrir WhatsApp: {e}")
            return False
            
    def processar_mensagem_whatsapp(self, mensagem: str, nome_contato: str = None):
        """Processa mensagem usando o chatbot escolar"""
        try:
            # Processar com chatbot inteligente
            resposta = self.chatbot.processar_mensagem_inteligente(mensagem, nome_contato)
            
            # Salvar no histórico
            if nome_contato not in self.historico_mensagens:
                self.historico_mensagens[nome_contato] = []
                
            self.historico_mensagens[nome_contato].append({
                'timestamp': datetime.now(),
                'mensagem': mensagem,
                'resposta': resposta
            })
            
            return resposta
            
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
            return "❌ Desculpe, ocorreu um erro. Tente novamente ou digite 'humano' para falar com um atendente."
            
    def enviar_mensagem_whatsapp(self, numero: str, mensagem: str):
        """Envia mensagem via WhatsApp"""
        try:
            # Formatar número
            if not numero.startswith('55'):
                numero = '55' + numero.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
                
            # Abrir chat
            url = f"https://web.whatsapp.com/send?phone={numero}"
            self.driver.get(url)
            
            # Aguardar carregamento
            time.sleep(3)
            
            # Localizar campo de mensagem
            campo_mensagem = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            ))
            
            # Enviar mensagem
            campo_mensagem.clear()
            campo_mensagem.send_keys(mensagem)
            
            # Pressionar Enter
            campo_mensagem.send_keys('\n')
            
            # Aguardar envio
            time.sleep(2)
            
            print(f"✅ Mensagem enviada para {numero}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            return False
            
    def capturar_mensagens_recebidas(self):
        """Captura mensagens recebidas no WhatsApp"""
        try:
            # Localizar chats não lidos
            chats_nao_lidos = self.driver.find_elements(
                By.XPATH, '//div[contains(@class, "unread")]'
            )
            
            mensagens_capturadas = []
            
            for chat in chats_nao_lidos:
                try:
                    # Clicar no chat
                    chat.click()
                    time.sleep(2)
                    
                    # Capturar nome do contato
                    nome_element = self.driver.find_element(
                        By.XPATH, '//span[@data-testid="conversation-title"]'
                    )
                    nome_contato = nome_element.text
                    
                    # Capturar última mensagem
                    mensagens = self.driver.find_elements(
                        By.XPATH, '//div[contains(@class, "message-in")]//span[@dir="ltr"]'
                    )
                    
                    if mensagens:
                        ultima_mensagem = mensagens[-1].text
                        
                        # Processar com chatbot
                        resposta = self.processar_mensagem_whatsapp(ultima_mensagem, nome_contato)
                        
                        # Enviar resposta
                        self.enviar_resposta_automatica(nome_contato, resposta)
                        
                        mensagens_capturadas.append({
                            'contato': nome_contato,
                            'mensagem': ultima_mensagem,
                            'resposta': resposta
                        })
                        
                except Exception as e:
                    print(f"⚠️ Erro ao processar chat: {e}")
                    continue
                    
            return mensagens_capturadas
            
        except Exception as e:
            print(f"❌ Erro ao capturar mensagens: {e}")
            return []
            
    def enviar_resposta_automatica(self, nome_contato: str, resposta: str):
        """Envia resposta automática para o contato"""
        try:
            # Localizar campo de mensagem
            campo_mensagem = self.driver.find_element(
                By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'
            )
            
            # Enviar resposta
            campo_mensagem.clear()
            campo_mensagem.send_keys(resposta)
            campo_mensagem.send_keys('\n')
            
            print(f"🤖 Resposta automática enviada para {nome_contato}")
            
        except Exception as e:
            print(f"❌ Erro ao enviar resposta automática: {e}")
            
    def iniciar_auto_atendimento(self):
        """Inicia o sistema de auto-atendimento"""
        print("🚀 INICIANDO AUTO-ATENDIMENTO ESCOLAR VIA WHATSAPP")
        print("="*60)
        
        # Abrir WhatsApp
        if not self.abrir_whatsapp():
            return False
            
        print("\n🎯 **SISTEMA ATIVO**")
        print("• Chatbot escolar funcionando")
        print("• Auto-atendimento ativo")
        print("• Escalação para humano disponível")
        print("\n💡 **Funcionalidades**:")
        print("• Horários de aulas")
        print("• Calendário escolar")
        print("• Agendamento de reposições")
        print("• Informações financeiras")
        print("• Suporte automático")
        
        return True
        
    def executar_ciclo_atendimento(self):
        """Executa um ciclo de atendimento"""
        try:
            # Capturar mensagens
            mensagens = self.capturar_mensagens_recebidas()
            
            if mensagens:
                print(f"\n📱 {len(mensagens)} mensagens processadas")
                for msg in mensagens:
                    print(f"👤 {msg['contato']}: {msg['mensagem'][:50]}...")
                    
            # Aguardar próximo ciclo
            time.sleep(30)  # Verificar a cada 30 segundos
            
        except Exception as e:
            print(f"❌ Erro no ciclo de atendimento: {e}")
            
    def executar_continuamente(self):
        """Executa o bot continuamente"""
        print("🔄 Executando bot continuamente...")
        print("⏹️ Pressione Ctrl+C para parar")
        
        try:
            while True:
                self.executar_ciclo_atendimento()
                
        except KeyboardInterrupt:
            print("\n⏹️ Bot interrompido pelo usuário")
            self.fechar_bot()
            
    def fechar_bot(self):
        """Fecha o bot e limpa recursos"""
        try:
            print("🔒 Fechando bot...")
            self.driver.quit()
            print("✅ Bot fechado com sucesso!")
            
        except Exception as e:
            print(f"⚠️ Erro ao fechar bot: {e}")
            
    def mostrar_estatisticas(self):
        """Mostra estatísticas do atendimento"""
        print("\n📊 **ESTATÍSTICAS DO ATENDIMENTO**")
        print("="*40)
        
        total_conversas = len(self.historico_mensagens)
        total_mensagens = sum(len(msgs) for msgs in self.historico_mensagens.values())
        
        print(f"👥 **Contatos atendidos**: {total_conversas}")
        print(f"💬 **Total de mensagens**: {total_mensagens}")
        
        if self.historico_mensagens:
            print("\n📋 **Últimas conversas**:")
            for contato, mensagens in list(self.historico_mensagens.items())[-5:]:
                print(f"• {contato}: {len(mensagens)} mensagens")
                
        return total_conversas, total_mensagens

# Função principal para executar o bot
def main():
    """Função principal para executar o bot WhatsApp"""
    print("🤖 WHATSAPP BOT COM CHATBOT ESCOLAR")
    print("="*50)
    
    try:
        # Criar bot
        bot = WhatsAppBotChatbot()
        
        # Iniciar auto-atendimento
        if bot.iniciar_auto_atendimento():
            print("\n🎉 **BOT ATIVO E FUNCIONANDO!**")
            print("📱 Aguardando mensagens no WhatsApp...")
            
            # Executar continuamente
            bot.executar_continuamente()
            
        else:
            print("❌ Falha ao iniciar o bot")
            
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        print("🔧 Verifique se o Chrome está funcionando")
        
    finally:
        print("\n🔚 Finalizando...")

if __name__ == "__main__":
    main()
