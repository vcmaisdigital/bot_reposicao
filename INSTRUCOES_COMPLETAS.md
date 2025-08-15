# 🚀 CHATBOT ESCOLAR - INSTRUÇÕES COMPLETAS

## 📁 **ESTRUTURA DO PROJETO ORGANIZADA**

```
bot_reposicao/
├── 📁 src/                          # 🧠 CÓDIGO FONTE
│   ├── 📁 chatbot/                  # 🤖 SISTEMA DE CHATBOT
│   │   ├── __init__.py
│   │   ├── chatbot_escola.py        # ChatBot base
│   │   └── chatbot_escola_completo.py # Sistema integrado
│   ├── 📁 sistema/                  # 📅 SISTEMA DE AGENDAMENTO
│   │   ├── __init__.py
│   │   └── sistema_agendamento.py   # Gestão de reposições
│   └── 📁 utils/                    # 🛠️ FERRAMENTAS
│       ├── __init__.py
│       ├── whatsapp_bot_chatbot.py  # Bot WhatsApp principal
│       ├── whatsapp_bot_v3_completo.py # Bot antigo (referência)
│       ├── instalar_dependencias.py  # Instalador automático
│       └── instalar_simples.py      # Instalador manual
├── 📁 config/                       # ⚙️ CONFIGURAÇÕES
│   └── config_bot.py                # Configurações do bot
├── 📁 data/                         # 📊 DADOS
│   └── dados_alunos.py              # Lista de alunos
├── 📁 docs/                         # 📚 DOCUMENTAÇÃO
│   ├── COMO_USAR_WHATSAPP.md        # Guia WhatsApp
│   ├── README_CHATBOT_ESCOLAR.md    # Documentação completa
│   ├── COMO_USAR.md                 # Guia antigo
│   └── SOLUCAO_CODIFICACAO.md      # Solução de problemas
├── 📄 main.py                       # 🎯 ARQUIVO PRINCIPAL
├── 📄 requirements.txt               # 📦 DEPENDÊNCIAS
└── 📄 INSTRUCOES_COMPLETAS.md       # 📖 ESTE ARQUIVO
```

## 🎯 **COMO USAR O SISTEMA**

### **1️⃣ INSTALAÇÃO INICIAL**

```bash
# Opção 1: Instalação automática
python src/utils/instalar_dependencias.py

# Opção 2: Instalação manual (se a primeira falhar)
python src/utils/instalar_simples.py
```

### **2️⃣ EXECUÇÃO DO SISTEMA**

```bash
# Método recomendado (usando arquivo principal)
python main.py

# Método alternativo (executando diretamente)
python src/utils/whatsapp_bot_chatbot.py
```

### **3️⃣ CONFIGURAÇÃO**

#### **Editar Dados dos Alunos**
```bash
# Abrir arquivo
notepad data/dados_alunos.py

# Ou usar seu editor preferido
code data/dados_alunos.py
```

#### **Editar Configurações**
```bash
# Abrir arquivo
notepad config/config_bot.py
```

## 🔧 **FUNCIONALIDADES POR PASTA**

### **📁 `src/chatbot/` - Sistema de ChatBot**
- **`chatbot_escola.py`**: ChatBot base com IA simples
- **`chatbot_escola_completo.py`**: Sistema integrado completo

**Funcionalidades:**
- ✅ Processamento de linguagem natural
- ✅ Identificação de intenções
- ✅ Respostas automáticas inteligentes
- ✅ Sugestões contextuais
- ✅ Escalação para humano

### **📁 `src/sistema/` - Sistema de Agendamento**
- **`sistema_agendamento.py`**: Gestão completa de reposições

**Funcionalidades:**
- ✅ Solicitação de reposições
- ✅ Validação automática
- ✅ Confirmação e cancelamento
- ✅ Verificação de disponibilidade
- ✅ Gestão de horários

### **📁 `src/utils/` - Ferramentas e Utilitários**
- **`whatsapp_bot_chatbot.py`**: Bot WhatsApp principal
- **`instalar_dependencias.py`**: Instalador automático
- **`instalar_simples.py`**: Instalador manual

**Funcionalidades:**
- ✅ Integração com WhatsApp Web
- ✅ Auto-atendimento 24/7
- ✅ Captura automática de mensagens
- ✅ Respostas automáticas
- ✅ Histórico de conversas

### **📁 `config/` - Configurações**
- **`config_bot.py`**: Configurações gerais do sistema

**Configurável:**
- ✅ Nome da escola
- ✅ Informações do professor
- ✅ Horários de funcionamento
- ✅ Mensagens personalizadas

### **📁 `data/` - Dados do Sistema**
- **`dados_alunos.py`**: Base de dados dos alunos

**Informações:**
- ✅ Nome, turma, responsável
- ✅ Número de contato
- ✅ Histórico de faltas
- ✅ Dados acadêmicos

## 🚀 **FLUXO DE EXECUÇÃO**

### **1. Inicialização**
```
python main.py
    ↓
📱 Abre Chrome automaticamente
    ↓
🔗 Acessa WhatsApp Web
    ↓
📱 Aguarda QR Code
    ↓
✅ Conecta ao WhatsApp
```

### **2. Funcionamento**
```
📱 Aluno envia mensagem no WhatsApp
    ↓
🤖 Bot captura automaticamente
    ↓
🧠 Processa com IA inteligente
    ↓
📱 Envia resposta automática
    ↓
💾 Salva no histórico
    ↓
🔄 Aguarda próxima mensagem
```

## 📱 **FUNCIONALIDADES NO WHATSAPP**

### **🔄 Auto-Atendimento Automático**
- **Horários de aulas** por turma
- **Calendário escolar** com eventos
- **Material didático** e links
- **Informações financeiras**
- **Sistema de avaliação**

### **📅 Agendamento de Reposições**
- **Solicitação automática** com validação
- **Confirmação** com ID único
- **Cancelamento** com antecedência
- **Verificação de disponibilidade**
- **Gestão de horários**

### **🆘 Suporte Inteligente**
- **FAQ automático** para dúvidas comuns
- **Escalação para humano** quando necessário
- **Sugestões contextuais** para próximas perguntas
- **Menu principal** com todas as opções

## ⚠️ **IMPORTANTE - COMO FUNCIONA**

### **❌ NÃO FAZER:**
- **NÃO conversar** com o bot no terminal
- **NÃO fechar** o Chrome enquanto rodar
- **NÃO desligar** o computador durante funcionamento

### **✅ FAZER:**
- **DEIXAR o Chrome aberto** e funcionando
- **USAR o WhatsApp** para conversar com o bot
- **MONITORAR o terminal** apenas para logs

## 🔍 **SOLUÇÃO DE PROBLEMAS**

### **Problema: Erro de Importação**
```bash
# Solução: Verificar estrutura de pastas
python -c "import sys; sys.path.append('src'); from chatbot.chatbot_escola import ChatBotEscola"
```

### **Problema: Chrome não abre**
```bash
# Solução: Verificar instalação
python src/utils/instalar_dependencias.py
```

### **Problema: Erro de codificação**
```bash
# Solução: Usar instalador simples
python src/utils/instalar_simples.py
```

## 📊 **MONITORAMENTO**

### **No Terminal (Logs)**
- ✅ Status do bot
- 📱 Mensagens processadas
- 🤖 Respostas enviadas
- ❌ Erros e problemas

### **No WhatsApp (Funcionamento)**
- Alunos recebem respostas automáticas
- Sistema funciona 24/7
- Escalação automática para humanos

## 🎮 **COMANDOS DISPONÍVEIS**

### **📚 Informações Acadêmicas**
- "Quais são os horários das aulas?"
- "Quando são as férias?"
- "Onde encontro o material didático?"

### **🔄 Agendamento**
- `solicitar reposição segunda-feira 14:00 consulta médica`
- `horários disponíveis`
- `listar agendamentos`

### **🆘 Suporte**
- "Preciso de ajuda"
- "humano" (para atendente)
- "menu" (menu principal)

## 🎉 **RESULTADO FINAL**

- **Alunos**: Recebem atendimento **24/7** via WhatsApp
- **Escola**: **80% das consultas** resolvidas automaticamente
- **Atendentes**: Focam apenas em **casos complexos**
- **Sistema**: Funciona **continuamente** sem intervenção

## 🚀 **PARA COMEÇAR AGORA**

1. **Instale dependências**: `python src/utils/instalar_dependencias.py`
2. **Execute o sistema**: `python main.py`
3. **Escaneie QR Code** no WhatsApp
4. **Deixe o Chrome aberto**
5. **Use o WhatsApp** para testar
6. **Monitore o terminal** para logs

---

**🎯 O chatbot está funcionando no WhatsApp, não no terminal!**

**📱 Toda a conversa acontece no WhatsApp, o terminal só monitora!**
