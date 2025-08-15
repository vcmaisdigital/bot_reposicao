#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador Simples para o Bot de Reposição
Versão alternativa que evita problemas de codificação no Windows
"""

import os
import sys

def verificar_python():
    """Verifica a versão do Python"""
    print("🐍 Verificando versão do Python...")
    versao = sys.version_info
    print(f"Python {versao.major}.{versao.minor}.{versao.micro}")
    
    if versao.major < 3 or (versao.major == 3 and versao.minor < 7):
        print("❌ Python 3.7 ou superior é necessário!")
        return False
    
    print("✅ Versão do Python compatível!")
    return True

def verificar_chrome():
    """Verifica se o Chrome está instalado"""
    print("\n🌐 VERIFICANDO GOOGLE CHROME")
    print("="*50)
    
    caminhos_chrome = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    
    chrome_encontrado = False
    for caminho in caminhos_chrome:
        if os.path.exists(caminho):
            print(f"✅ Chrome encontrado em: {caminho}")
            chrome_encontrado = True
            break
    
    if not chrome_encontrado:
        print("❌ Google Chrome não encontrado!")
        print("🔧 Por favor, instale o Google Chrome:")
        print("   https://www.google.com/chrome/")
        return False
    
    return True

def instalar_dependencias():
    """Instala as dependências usando comandos diretos"""
    print("\n📦 INSTALANDO DEPENDÊNCIAS")
    print("="*50)
    
    print("🔧 Atualizando pip...")
    print("Execute: python -m pip install --upgrade pip")
    input("Pressione Enter após atualizar o pip...")
    
    print("\n🔧 Instalando Selenium...")
    print("Execute: pip install selenium>=4.10.0,<4.16.0")
    input("Pressione Enter após instalar o Selenium...")
    
    print("\n🔧 Instalando WebDriver Manager...")
    print("Execute: pip install webdriver-manager>=3.8.6,<4.0.0")
    input("Pressione Enter após instalar o WebDriver Manager...")
    
    print("\n🔧 Instalando PyWhatKit...")
    print("Execute: pip install pywhatkit>=5.4")
    input("Pressione Enter após instalar o PyWhatKit...")
    
    return True

def testar_selenium():
    """Testa se o Selenium está funcionando"""
    print("\n🧪 TESTANDO SELENIUM")
    print("="*50)
    
    try:
        print("🔧 Testando importação do Selenium...")
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print("✅ Importação do Selenium bem-sucedida!")
        
        print("🔧 Testando criação de opções do Chrome...")
        options = Options()
        options.add_argument("--headless")  # Modo headless para teste
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        print("✅ Opções do Chrome criadas com sucesso!")
        
        print("🔧 Testando WebDriver Manager...")
        from webdriver_manager.chrome import ChromeDriverManager
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver encontrado em: {driver_path}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("🔧 Execute os comandos de instalação novamente")
        return False
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 CONFIGURADOR SIMPLES DO BOT DE REPOSIÇÃO")
    print("="*50)
    print("⚠️ Este instalador evita problemas de codificação no Windows")
    print("="*50)
    
    # Verificar Python
    if not verificar_python():
        sys.exit(1)
    
    # Verificar Chrome
    if not verificar_chrome():
        sys.exit(1)
    
    # Instalar dependências
    if not instalar_dependencias():
        print("\n❌ Falha na instalação das dependências!")
        sys.exit(1)
    
    # Testar Selenium
    if not testar_selenium():
        print("\n❌ Falha no teste do Selenium!")
        print("\n🔧 SOLUÇÕES:")
        print("1. Execute os comandos manualmente no PowerShell")
        print("2. Verifique se não há erros de rede")
        print("3. Tente executar como Administrador")
        sys.exit(1)
    
    print("\n🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*50)
    print("✅ Todas as dependências foram instaladas")
    print("✅ Selenium está funcionando")
    print("✅ Chrome foi detectado")
    print("\n🚀 Agora você pode executar o bot:")
    print("   python whatsapp_bot_v3_completo.py")
    
    print("\n⚠️ IMPORTANTE:")
    print("- Certifique-se de que o Chrome está atualizado")
    print("- Execute o bot em um terminal/PowerShell limpo")
    print("- Se houver problemas, reinicie o terminal")

if __name__ == "__main__":
    main()
