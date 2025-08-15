#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 CHATBOT ESCOLAR - ARQUIVO PRINCIPAL
Sistema completo de auto-atendimento escolar via WhatsApp
"""

import sys
import os

# Adicionar pastas ao path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.join(BASE_DIR, 'src'),
    os.path.join(BASE_DIR, 'data')  # Adiciona a pasta data ao path
])

def main():
    """Função principal do sistema"""
    print("🤖 CHATBOT ESCOLAR COMPLETO")
    print("="*50)
    print("🎯 Sistema de auto-atendimento escolar")
    print("📱 Integrado com WhatsApp")
    print("🧠 IA inteligente para respostas")
    print("📅 Sistema de agendamento automático")
    print("="*50)
    
    try:
        # Importar módulo de dados
        from dados_alunos import ALUNOS_DADOS
        print(f"✅ Dados carregados - {len(ALUNOS_DADOS)} alunos registrados")
        
        # Importar e executar o bot WhatsApp
        from utils.whatsapp_bot_chatbot import WhatsAppBotChatbot
        
        print("\n🚀 Iniciando bot WhatsApp...")
        bot = WhatsAppBotChatbot(ALUNOS_DADOS)  # Passa os dados para o bot
        
        if bot.iniciar_auto_atendimento():
            print("\n🎉 **BOT ATIVO E FUNCIONANDO!**")
            print("📱 Aguardando mensagens no WhatsApp...")
            print("\n💡 **Para parar**: Pressione Ctrl+C")
            print("📊 **Para estatísticas**: Use o método mostrar_estatisticas()")
            
            # Executar continuamente
            bot.executar_continuamente()
        else:
            print("❌ Falha ao iniciar o bot")
            return 1
            
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("🔧 Verifique se todas as dependências estão instaladas")
        print("💡 Execute: python src/utils/instalar_dependencias.py")
        return 1
        
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        print("🔧 Verifique se o Chrome está funcionando")
        return 1
        
    finally:
        print("\n🔚 Finalizando sistema...")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())