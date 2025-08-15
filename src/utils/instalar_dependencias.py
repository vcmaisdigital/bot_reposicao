#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de instalação e teste das dependências do Bot de Reposição
Execute este script para configurar o ambiente automaticamente
"""

import subprocess
import sys
import os

def executar_comando(comando, descricao):
    """Executa um comando e retorna o resultado"""
    print(f"\n🔧 {descricao}...")
    print(f"Comando: {comando}")
    
    try:
        # Usar encoding específico para Windows e tratamento de erros
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding='cp1252',  # Encoding padrão do Windows
            errors='replace'    # Substituir caracteres problemáticos
        )
        
        if resultado.returncode == 0:
            print(f"✅ {descricao} concluído com sucesso!")
            return True
        else:
            print(f"❌ {descricao} falhou!")
            if resultado.stderr:
                print(f"Erro: {resultado.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False

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

def instalar_dependencias():
    """Instala as dependências do projeto"""
    print("\n📦 INSTALANDO DEPENDÊNCIAS")
    print("="*50)
    
    # Atualizar pip
    if not executar_comando("python -m pip install --upgrade pip", "Atualizando pip"):
        print("⚠️ Falha ao atualizar pip, continuando...")
    
    # Instalar selenium
    if not executar_comando("pip install selenium>=4.10.0,<4.16.0", "Instalando Selenium"):
        return False
    
    # Instalar webdriver-manager
    if not executar_comando("pip install webdriver-manager>=3.8.6,<4.0.0", "Instalando WebDriver Manager"):
        return False
    
    # Instalar pywhatkit
    if not executar_comando("pip install pywhatkit>=5.4", "Instalando PyWhatKit"):
        return False
    
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
        return False
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

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

def main():
    """Função principal"""
    print("🚀 CONFIGURADOR DO BOT DE REPOSIÇÃO")
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
