# 🚀 Como Usar o Bot de Reposição de Aulas

## 📋 Pré-requisitos
- Python 3.7 ou superior
- Google Chrome instalado
- Conexão com internet estável

## ⚙️ Instalação Automática (RECOMENDADO)

**Para instalação automática e teste das dependências:**
```bash
python instalar_dependencias.py
```

Este script irá:
- ✅ Verificar a versão do Python
- ✅ Detectar o Google Chrome
- ✅ Instalar todas as dependências
- ✅ Testar se o Selenium está funcionando
- ✅ Configurar o ambiente automaticamente

## ⚙️ Instalação Manual

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Configure os dados dos alunos:**
   - Edite o arquivo `dados_alunos.py` se necessário
   - Verifique se os números estão corretos

3. **Configure as mensagens:**
   - Edite o arquivo `config_bot.py` para personalizar mensagens e horários

## 🎯 Execução

**Execute o bot principal:**
```bash
python whatsapp_bot_v3_completo.py
```

## 📱 Funcionalidades Disponíveis

### **Opção 1: Enviar Mensagens**
- Envia mensagens para alunos que ainda não receberam
- Confirma cada envio com checks do WhatsApp
- Salva automaticamente o status de envio

### **Opção 2: Verificar Respostas**
- Captura mensagens recebidas dos alunos
- Extrai automaticamente horários preferidos
- Salva todas as respostas no arquivo `respostas.json`

### **Opção 3: Gerar Relatório**
- Mostra status completo de todos os alunos
- Organiza por turma
- Exibe estatísticas e horários preferidos

### **Opção 4: Sair**
- Encerra o programa

## ⚠️ Importante

- **Sempre escaneie o QR Code** quando solicitado
- **Mantenha o WhatsApp Web aberto** durante a execução
- **Não feche o navegador** enquanto o bot estiver funcionando
- **Use intervalos** entre verificações para evitar bloqueios

## 🚨 Solução de Problemas

### **Erro: "UnicodeDecodeError" (Problema de Codificação)**
Este erro é comum no **Windows com Python 3.13**. **Soluções:**

1. **Use o instalador simples (RECOMENDADO):**
```bash
python instalar_simples.py
```

2. **Instalação manual direta:**
```bash
# Execute cada comando separadamente
python -m pip install --upgrade pip
pip install selenium>=4.10.0,<4.16.0
pip install webdriver-manager>=3.8.6,<4.0.0
pip install pywhatkit>=5.4
```

3. **Execute o PowerShell como Administrador**

**📖 Guia completo:** `SOLUCAO_CODIFICACAO.md`

### **Erro: "não é um aplicativo Win32 válido"**
Este erro indica problema com o ChromeDriver. **Soluções:**

1. **Execute o instalador automático:**
```bash
python instalar_dependencias.py
```

2. **Atualize o Chrome** para a versão mais recente

3. **Reinicie o terminal/PowerShell** após instalação

4. **Verifique se o Chrome está instalado** em:
   - `C:\Program Files\Google\Chrome\Application\chrome.exe`
   - `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`

### **Erro: "ChromeDriver not found"**
```bash
pip install --upgrade webdriver-manager
```

### **Erro: "Selenium not found"**
```bash
pip install --upgrade selenium
```

### **Problemas de Permissão no Windows**
- Execute o PowerShell como **Administrador**
- Verifique se o antivírus não está bloqueando

## 📊 Arquivos do Projeto

- **`whatsapp_bot_v3_completo.py`** - Bot principal
- **`config_bot.py`** - Configurações e mensagens
- **`dados_alunos.py`** - Dados dos alunos
- **`respostas.json`** - Respostas capturadas (criado automaticamente)
- **`requirements.txt`** - Dependências Python
- **`instalar_dependencias.py`** - Instalador automático

## 🔧 Personalização

### Alterar Mensagens
Edite o arquivo `config_bot.py`:
- Nome do professor
- Horários disponíveis
- Período de reposição

### Alterar Dados dos Alunos
Edite o arquivo `dados_alunos.py`:
- Adicionar/remover alunos
- Alterar números de telefone
- Configurar responsáveis

## 📞 Suporte

Para problemas:
1. **Execute primeiro:** `python instalar_dependencias.py`
2. Verifique se o Chrome está atualizado
3. Confirme se o WhatsApp Web está funcionando
4. Verifique se os números estão corretos
5. Teste a conexão com a internet

## 🔄 Atualizações

**Para atualizar as dependências:**
```bash
python instalar_dependencias.py
```

---

**Projeto limpo, organizado e com instalação automática! 🎉**
