# 📱 GUIA DE CAPTURA DE RESPOSTAS - REPOSIÇÃO DE AULAS

## 🎯 **Situação Atual**
✅ **Mensagens já foram enviadas** para todos os alunos
🆕 **Agora precisamos capturar as respostas** que já recebeu e as futuras

---

## 🚀 **Scripts Disponíveis**

### 1. **`bot_captura_respostas.py`** - Bot Principal de Captura
- **Captura respostas novas** que chegam
- **Verifica status** de todos os alunos
- **Gera relatórios** atualizados
- **Ideal para uso diário** e acompanhamento

### 2. **`capturar_historico.py`** - Capturador de Histórico
- **Captura TODAS as respostas** já recebidas no histórico
- **Processa conversas antigas** para não perder nada
- **Ideal para primeira execução** e captura inicial

---

## 📋 **Fluxo Recomendado**

### **PRIMEIRA EXECUÇÃO (Capturar Histórico)**
```bash
python capturar_historico.py
```
**Escolha Opção 1** para capturar histórico de todos os alunos
- ⚠️ **Pode demorar** dependendo do número de alunos
- 🔍 **Captura todas as respostas** já recebidas
- 💾 **Salva no arquivo** `respostas.json`

### **USO DIÁRIO (Capturar Novas Respostas)**
```bash
python bot_captura_respostas.py
```
**Escolha Opção 1** para verificar respostas de todos os alunos
- ⚡ **Mais rápido** (só verifica novas mensagens)
- 📝 **Captura respostas** que chegaram desde a última verificação
- 📊 **Gera relatórios** atualizados

---

## 🔍 **Funcionalidades dos Scripts**

### **Bot Principal (`bot_captura_respostas.py`)**
- 🔍 **Verificar respostas** de todos os alunos
- 📊 **Gerar relatório** atualizado
- 🔄 **Verificar aluno específico**
- 💾 **Salvamento automático** das respostas

### **Capturador de Histórico (`capturar_historico.py`)**
- 📚 **Captura histórico completo** de cada aluno
- 🔍 **Processa todas as mensagens** recebidas
- ⚠️ **Evita duplicatas** automaticamente
- 📝 **Marca origem** como "capturado_do_historico"

---

## 📊 **O que é Capturado Automaticamente**

✅ **Todas as mensagens** dos alunos/responsáveis
✅ **Horários preferidos** identificados automaticamente
✅ **Timestamps** de cada resposta
✅ **Status** de cada aluno (respondido/pendente)
✅ **Organização por turma** para facilitar gestão

---

## 🕐 **Identificação Inteligente de Horários**

O bot reconhece automaticamente:
- **Dias**: Segunda-feira, Terça-feira, Quarta-feira
- **Períodos**: Manhã, Tarde, Noite
- **Horários**: 08:00, 10:00, 14:00, 16:00, 19:00

### **Exemplos de Mensagens Reconhecidas:**
- "Posso fazer na segunda-feira de manhã"
- "Quarta-feira às 16:00 seria ótimo"
- "Terça-feira à noite funciona bem"

---

## 📁 **Arquivos Gerados**

### **`respostas.json`** - Arquivo principal
```json
{
    "Nome do Aluno": {
        "turma": "Turma I",
        "responsavel": "Nome do Responsável",
        "numero": "+55 82 99999-9999",
        "faltas": ["12/07", "19/07"],
        "respostas": [
            {
                "timestamp": "2024-08-15 14:30:25",
                "resposta": "Mensagem completa do aluno",
                "horario_preferido": "Segunda-feira, Manhã, 08:00 às 09:50",
                "status": "capturado_do_historico"
            }
        ],
        "mensagem_enviada": true,
        "data_envio": "Enviada anteriormente"
    }
}
```

---

## ⚠️ **IMPORTANTE**

1. **Sempre escaneie o QR Code** quando solicitado
2. **Mantenha o WhatsApp Web aberto** durante a execução
3. **Não feche o navegador** enquanto o bot funcionar
4. **Use intervalos** entre verificações para evitar bloqueios
5. **Primeira execução**: Use o capturador de histórico
6. **Uso diário**: Use o bot principal de captura

---

## 🎯 **Benefícios da Nova Abordagem**

✅ **Não perde respostas** já recebidas
✅ **Captura histórico completo** automaticamente
✅ **Identifica horários** preferidos inteligentemente
✅ **Organiza demandas** por turma
✅ **Relatórios atualizados** em tempo real
✅ **Fácil acompanhamento** do status dos alunos

---

## 🚀 **Comece Agora**

### **Passo 1: Capturar Histórico**
```bash
python capturar_historico.py
```

### **Passo 2: Verificar Novas Respostas (Diário)**
```bash
python bot_captura_respostas.py
```

### **Passo 3: Analisar Dados**
```bash
python analisar_respostas.py
```

---

**🎉 Agora você pode capturar todas as respostas e organizar as demandas de reposição automaticamente!**
