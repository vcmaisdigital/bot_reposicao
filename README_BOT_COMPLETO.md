# 🤖 Bot de Reposição de Aulas - Versão Completa

Este bot foi desenvolvido para automatizar o envio de mensagens sobre reposição de aulas e **capturar as respostas dos alunos/responsáveis** para organizar as demandas.

## ✨ Funcionalidades Principais

### 1. **Envio de Mensagens**
- Envia mensagens personalizadas para cada aluno
- Identifica automaticamente o gênero para usar a linguagem correta
- Suporte para envio direto ao aluno ou ao responsável
- Confirmação de envio com checks do WhatsApp

### 2. **Captura de Respostas** 🆕
- **Verifica automaticamente** se os alunos responderam
- **Salva todas as respostas** em arquivo JSON
- **Extrai horários preferidos** das mensagens dos alunos
- **Organiza por turma** para facilitar o acompanhamento

### 3. **Organização de Demandas** 🆕
- **Relatório completo** de status de cada aluno
- **Controle de mensagens enviadas** vs. respondidas
- **Estatísticas** de taxa de resposta
- **Horários preferidos** organizados e identificados

## 🚀 Como Usar

### Instalação
```bash
pip install -r requirements.txt
```

### Execução
```bash
python whatsapp_bot_v3_completo.py
```

### Menu de Opções

O bot oferece um menu interativo com 4 opções:

#### **Opção 1: Enviar Mensagens**
- Envia mensagens para todos os alunos que ainda não receberam
- Pula alunos marcados como `ja_enviado: true`
- Confirma cada envio com checks do WhatsApp
- Salva automaticamente o status de envio

#### **Opção 2: Verificar Respostas**
- Navega pelas conversas dos alunos
- Captura mensagens recebidas
- Extrai horários preferidos automaticamente
- Salva todas as respostas no arquivo `respostas.json`

#### **Opção 3: Gerar Relatório**
- Mostra status completo de todos os alunos
- Organiza por turma
- Exibe estatísticas gerais
- Lista horários preferidos identificados

#### **Opção 4: Sair**
- Encerra o programa

## 📊 Estrutura dos Dados Salvos

O bot salva todas as informações no arquivo `respostas.json`:

```json
{
    "Nome do Aluno": {
        "turma": "Turma I",
        "responsavel": "Nome do Responsável",
        "numero": "+55 82 99999-9999",
        "numero_responsavel": "+55 82 88888-8888",
        "faltas": ["12/07", "19/07"],
        "enviar_para_responsavel": true,
        "respostas": [
            {
                "timestamp": "2024-08-15 14:30:25",
                "resposta": "Mensagem completa do aluno",
                "horario_preferido": "Segunda-feira, Manhã, 08:00 às 09:50",
                "status": "respondido"
            }
        ],
        "mensagem_enviada": true,
        "data_envio": "2024-08-15 14:25:10"
    }
}
```

## 🔍 Como o Bot Identifica Horários

O bot analisa automaticamente as mensagens dos alunos para identificar:

- **Dias da semana**: Segunda-feira, Terça-feira, Quarta-feira
- **Períodos**: Manhã, Tarde, Noite
- **Horários específicos**: 08:00, 10:00, 14:00, 16:00, 19:00

### Exemplos de Mensagens Reconhecidas:
- "Posso fazer na segunda-feira de manhã"
- "Quarta-feira às 16:00 seria ótimo"
- "Terça-feira à noite funciona bem"

## 📋 Fluxo de Trabalho Recomendado

1. **Primeira execução**: Use a Opção 1 para enviar mensagens
2. **Aguarde respostas**: Deixe os alunos responderem (pode levar horas/dias)
3. **Verifique respostas**: Use a Opção 2 para capturar as respostas
4. **Organize demandas**: Use a Opção 3 para gerar relatórios
5. **Repita verificação**: Use a Opção 2 periodicamente para novas respostas

## ⚠️ Importante

- **Sempre escaneie o QR Code** quando solicitado
- **Mantenha o WhatsApp Web aberto** durante a execução
- **Não feche o navegador** enquanto o bot estiver funcionando
- **Use intervalos** entre verificações para evitar bloqueios
- **Backup**: O arquivo `respostas.json` é criado automaticamente

## 🎯 Benefícios da Versão Completa

✅ **Automatização completa** do processo de envio e captura
✅ **Organização automática** das demandas por turma
✅ **Identificação inteligente** de horários preferidos
✅ **Relatórios detalhados** para acompanhamento
✅ **Histórico completo** de todas as interações
✅ **Fácil gestão** de alunos que já responderam vs. pendentes

## 📞 Suporte

Para dúvidas ou problemas, verifique:
1. Se o Chrome está atualizado
2. Se o WhatsApp Web está funcionando
3. Se os números dos alunos estão corretos
4. Se há conexão estável com a internet

---

**Desenvolvido para facilitar a organização de reposições de aulas e melhorar o acompanhamento dos alunos! 🎓**
