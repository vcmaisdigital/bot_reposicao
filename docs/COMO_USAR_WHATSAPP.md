# 📱 COMO USAR O CHATBOT ESCOLAR NO WHATSAPP

## 🎯 **VISÃO GERAL**

O **ChatBot Escolar** funciona **APENAS no WhatsApp** e **NÃO no terminal**. O terminal é usado apenas para **iniciar o bot** e **ver logs**.

## 🚀 **COMO FUNCIONA:**

### **1. Iniciar o Bot (Terminal)**
```bash
python whatsapp_bot_chatbot.py
```

### **2. Escanear QR Code**
- O Chrome abrirá automaticamente
- Escaneie o QR Code com seu WhatsApp
- **NÃO feche o Chrome** - ele deve ficar rodando

### **3. Bot Funcionando (WhatsApp)**
- O bot fica **ativo no WhatsApp**
- Responde **automaticamente** às mensagens
- Funciona **24/7** enquanto o Chrome estiver aberto

## 📱 **FUNCIONALIDADES NO WHATSAPP:**

### **🔄 Auto-Atendimento Automático**
- **Aluno envia**: "Quais são os horários das aulas?"
- **Bot responde**: Horários completos da turma
- **Aluno envia**: "Como solicito reposição?"
- **Bot responde**: Passo a passo completo

### **📅 Sistema de Agendamento**
- **Aluno envia**: `solicitar reposição segunda-feira 14:00 consulta médica`
- **Bot responde**: Confirmação com ID
- **Aluno envia**: `confirmar [ID]`
- **Bot responde**: Agendamento confirmado

### **🆘 Escalação para Humano**
- **Aluno envia**: "humano" ou "atendente"
- **Bot responde**: Transfere para atendente humano
- **Atendente**: Recebe notificação para responder

## 🎮 **COMANDOS DISPONÍVEIS:**

### **📚 Informações Acadêmicas**
- "Quais são os horários das aulas?"
- "Quando são as férias?"
- "Onde encontro o material didático?"
- "Como são calculadas as notas?"

### **🔄 Agendamento de Reposições**
- `solicitar reposição [dia] [horario] [motivo]`
- `horários disponíveis`
- `listar agendamentos`
- `confirmar [ID]`
- `cancelar [ID] [motivo]`

### **💰 Serviços Administrativos**
- "Quanto custa a mensalidade?"
- "Quais são as formas de pagamento?"
- "Quando vence a mensalidade?"

### **🆘 Suporte e Ajuda**
- "Preciso de ajuda"
- "humano" (para atendente)
- "menu" (menu principal)
- "relatório" (seu relatório)

## 🔧 **CONFIGURAÇÃO:**

### **1. Instalar Dependências**
```bash
python instalar_dependencias.py
```

### **2. Configurar Dados**
- Editar `dados_alunos.py` - Lista de alunos
- Editar `config_bot.py` - Configurações da escola
- Editar `chatbot_escola.py` - Base de conhecimento

### **3. Executar Bot**
```bash
python whatsapp_bot_chatbot.py
```

## 📊 **MONITORAMENTO:**

### **No Terminal (Logs)**
- ✅ Status do bot
- 📱 Mensagens processadas
- 🤖 Respostas enviadas
- ❌ Erros e problemas

### **No WhatsApp (Funcionamento)**
- Alunos recebem respostas automáticas
- Sistema funciona 24/7
- Escalação automática para humanos

## ⚠️ **IMPORTANTE:**

### **❌ NÃO FAZER:**
- **NÃO fechar o Chrome** enquanto o bot estiver rodando
- **NÃO desligar o computador** durante o funcionamento
- **NÃO usar o terminal** para conversar com o bot

### **✅ FAZER:**
- **DEIXAR o Chrome aberto** e funcionando
- **USAR o WhatsApp** para conversar com o bot
- **MONITORAR o terminal** apenas para logs

## 🎯 **EXEMPLO DE USO REAL:**

### **Cenário: Aluno quer saber horários**
1. **Aluno envia no WhatsApp**: "Oi, tudo bem?"
2. **Bot responde automaticamente**: Saudação + opções disponíveis
3. **Aluno envia**: "Quais são os horários das aulas?"
4. **Bot responde**: Horários completos da turma do aluno
5. **Aluno envia**: "Obrigado!"
6. **Bot responde**: Despedida + sugestões

### **Cenário: Aluno quer agendar reposição**
1. **Aluno envia**: "Como solicito reposição?"
2. **Bot responde**: Explicação completa do processo
3. **Aluno envia**: `solicitar reposição segunda-feira 14:00 consulta médica`
4. **Bot responde**: Confirmação com ID único
5. **Aluno envia**: `confirmar [ID]`
6. **Bot responde**: Agendamento confirmado + detalhes

## 🔄 **FLUXO COMPLETO:**

```
📱 ALUNO ENVIA MENSAGEM NO WHATSAPP
    ↓
🤖 BOT PROCESSA COM IA INTELIGENTE
    ↓
🧠 IDENTIFICA INTENÇÃO E GERA RESPOSTA
    ↓
📱 ENVIA RESPOSTA AUTOMÁTICA
    ↓
💾 SALVA NO HISTÓRICO
    ↓
🔄 AGUARDA PRÓXIMA MENSAGEM
```

## 🎉 **RESULTADO FINAL:**

- **Alunos**: Recebem atendimento **24/7** via WhatsApp
- **Escola**: **80% das consultas** resolvidas automaticamente
- **Atendentes**: Focam apenas em **casos complexos**
- **Sistema**: Funciona **continuamente** sem intervenção

## 🚀 **PARA COMEÇAR AGORA:**

1. **Execute**: `python whatsapp_bot_chatbot.py`
2. **Escaneie** o QR Code
3. **Deixe o Chrome aberto**
4. **Use o WhatsApp** para testar
5. **Monitore o terminal** para logs

**O chatbot está funcionando no WhatsApp, não no terminal! 🎯**
