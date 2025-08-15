#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 CHATBOT ESCOLAR COMPLETO
Sistema integrado de auto-atendimento com agendamento inteligente
"""

import json
import re
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time

# Importar sistemas
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.chatbot.chatbot_escola import ChatBotEscola
from src.sistema.sistema_agendamento import SistemaAgendamento

class ChatBotEscolaCompleto:
    def __init__(self):
        """Inicializa o sistema completo"""
        self.chatbot = ChatBotEscola()
        self.sistema_agendamento = SistemaAgendamento()
        self.conversas_ativas = {}
        self.historico_conversas = {}
        
    def processar_mensagem_completa(self, mensagem: str, nome_aluno: str = None) -> str:
        """Processa mensagem usando todos os sistemas integrados"""
        mensagem_lower = mensagem.lower().strip()
        
        # Verificar se é comando de agendamento
        if self.eh_comando_agendamento(mensagem_lower):
            return self.sistema_agendamento.processar_comando(mensagem, nome_aluno)
            
        # Verificar se quer falar com humano
        if 'humano' in mensagem_lower or 'atendente' in mensagem_lower:
            return self.escalar_para_humano()
            
        # Verificar se é pergunta sobre agendamento
        if self.eh_pergunta_agendamento(mensagem_lower):
            return self.responder_pergunta_agendamento(mensagem, nome_aluno)
            
        # Processar com chatbot normal
        return self.chatbot.processar_mensagem(mensagem, nome_aluno)
        
    def eh_comando_agendamento(self, mensagem: str) -> bool:
        """Verifica se a mensagem é um comando de agendamento"""
        comandos = [
            'solicitar reposição', 'solicitar reposicao',
            'confirmar', 'cancelar', 'listar agendamentos',
            'meus agendamentos', 'horários disponíveis',
            'horarios disponiveis', 'ajuda agendamento'
        ]
        
        return any(mensagem.startswith(comando) for comando in comandos)
        
    def eh_pergunta_agendamento(self, mensagem: str) -> bool:
        """Verifica se é uma pergunta sobre agendamento"""
        palavras_chave = [
            'reposição', 'reposicao', 'agendar', 'marcar', 'horário',
            'horario', 'disponível', 'disponivel', 'quando', 'como'
        ]
        
        return any(palavra in mensagem for palavra in palavras_chave)
        
    def responder_pergunta_agendamento(self, mensagem: str, nome_aluno: str) -> str:
        """Responde perguntas sobre agendamento de forma inteligente"""
        mensagem_lower = mensagem.lower()
        
        if 'quando' in mensagem_lower and 'reposição' in mensagem_lower:
            return self.responder_quando_reposicao()
        elif 'como' in mensagem_lower and 'solicitar' in mensagem_lower:
            return self.responder_como_solicitar()
        elif 'horários' in mensagem_lower or 'horarios' in mensagem_lower:
            return self.sistema_agendamento.listar_horarios_disponiveis()
        elif 'agendar' in mensagem_lower or 'marcar' in mensagem_lower:
            return self.responder_como_agendar()
        else:
            return self.responder_agendamento_geral()
            
    def responder_quando_reposicao(self) -> str:
        """Responde sobre quando solicitar reposições"""
        resposta = "📅 **QUANDO SOLICITAR REPOSIÇÕES**\n\n"
        resposta += "⏰ **Antecedência Mínima**: 48 horas\n"
        resposta += "📅 **Período Atual**: 18 a 22 de agosto de 2024\n\n"
        
        resposta += "🕐 **Horários Disponíveis**:\n"
        resposta += "• Segunda a Sexta: 14:00, 16:00, 19:00\n"
        resposta += "• Duração: 2 horas por aula\n\n"
        
        resposta += "💡 **Dicas**:\n"
        resposta += "• Solicite assim que souber que vai faltar\n"
        resposta += "• Evite deixar para última hora\n"
        resposta += "• Verifique disponibilidade antes de solicitar\n\n"
        
        resposta += "🔄 **Para solicitar agora**:\n"
        resposta += "Use: `solicitar reposição [dia] [horario] [motivo]`\n"
        resposta += "Exemplo: `solicitar reposição segunda-feira 14:00 consulta médica`"
        
        return resposta
        
    def responder_como_solicitar(self) -> str:
        """Responde sobre como solicitar reposições"""
        resposta = "📋 **COMO SOLICITAR REPOSIÇÃO**\n\n"
        
        resposta += "🔄 **Passo a Passo**:\n"
        resposta += "1️⃣ **Escolha o dia**: segunda, terça, quarta, quinta ou sexta\n"
        resposta += "2️⃣ **Escolha o horário**: 14:00, 16:00 ou 19:00\n"
        resposta += "3️⃣ **Informe o motivo**: por que você faltou\n"
        resposta += "4️⃣ **Confirme**: use o comando de confirmação\n\n"
        
        resposta += "📝 **Comando Completo**:\n"
        resposta += "`solicitar reposição [dia] [horario] [motivo]`\n\n"
        
        resposta += "💡 **Exemplos Práticos**:\n"
        resposta += "• `solicitar reposição segunda-feira 14:00 consulta médica`\n"
        resposta += "• `solicitar reposição quarta-feira 16:00 compromisso familiar`\n"
        resposta += "• `solicitar reposição sexta-feira 19:00 viagem`\n\n"
        
        resposta += "✅ **Após solicitar**:\n"
        resposta += "• Você receberá um ID de solicitação\n"
        resposta += "• Use `confirmar [ID]` para confirmar\n"
        resposta += "• Use `listar agendamentos` para ver seus agendamentos"
        
        return resposta
        
    def responder_como_agendar(self) -> str:
        """Responde sobre como agendar reposições"""
        resposta = "📅 **COMO AGENDAR REPOSIÇÃO**\n\n"
        
        resposta += "🎯 **Opções de Agendamento**:\n\n"
        
        resposta += "🔄 **Solicitação Manual**:\n"
        resposta += "• Use o comando completo\n"
        resposta += "• Escolha dia, horário e motivo\n"
        resposta += "• Confirme com o ID recebido\n\n"
        
        resposta += "⏰ **Ver Disponibilidade**:\n"
        resposta += "• Use: `horários disponíveis`\n"
        resposta += "• Veja vagas em tempo real\n"
        resposta += "• Escolha o melhor horário\n\n"
        
        resposta += "📋 **Gerenciar Agendamentos**:\n"
        resposta += "• `listar agendamentos` - Ver todos\n"
        resposta += "• `confirmar [ID]` - Confirmar solicitação\n"
        resposta += "• `cancelar [ID] [motivo]` - Cancelar\n\n"
        
        resposta += "💡 **Dica**: Comece verificando os horários disponíveis!"
        
        return resposta
        
    def responder_agendamento_geral(self) -> str:
        """Resposta geral sobre agendamento"""
        resposta = "🔄 **SISTEMA DE AGENDAMENTO**\n\n"
        
        resposta += "📚 **O que é**: Sistema para solicitar reposições de aulas perdidas\n\n"
        
        resposta += "🎯 **Funcionalidades**:\n"
        resposta += "• Solicitar reposições\n"
        resposta += "• Ver horários disponíveis\n"
        resposta += "• Gerenciar agendamentos\n"
        resposta += "• Cancelar quando necessário\n\n"
        
        resposta += "🚀 **Para começar**:\n"
        resposta += "• `horários disponíveis` - Ver opções\n"
        resposta += "• `como solicitar` - Aprender o processo\n"
        resposta += "• `ajuda agendamento` - Comandos completos\n\n"
        
        resposta += "💬 **Precisa de ajuda específica?**\n"
        resposta += "Pergunte: 'Como solicito reposição?' ou 'Quais horários estão disponíveis?'"
        
        return resposta
        
    def escalar_para_humano(self) -> str:
        """Escala conversa para atendente humano"""
        resposta = "🆘 **ESCALANDO PARA ATENDENTE HUMANO**\n\n"
        resposta += "⏰ **Tempo de Espera**: 2-5 minutos\n"
        resposta += "👨‍💼 **Atendente**: Erick Oliveira\n"
        resposta += "📱 **WhatsApp**: (82) 99999-9999\n\n"
        
        resposta += "🔄 **Enquanto isso, você pode**:\n"
        resposta += "• Verificar horários de aulas\n"
        resposta += "• Consultar calendário escolar\n"
        resposta += "• Acessar material didático\n"
        resposta += "• Solicitar reposições\n\n"
        
        resposta += "📞 **Sua conversa será transferida automaticamente**\n"
        resposta += "💡 **Dica**: Use este tempo para organizar suas dúvidas!"
        
        return resposta
        
    def iniciar_conversa_completa(self, nome_aluno: str = None) -> str:
        """Inicia uma conversa completa com todas as funcionalidades"""
        saudacao = self.chatbot.iniciar_conversa(nome_aluno)
        
        # Adicionar informações sobre agendamento
        resposta = saudacao + "\n\n"
        resposta += "🔄 **SISTEMA DE AGENDAMENTO INTEGRADO**\n"
        resposta += "• Solicite reposições automaticamente\n"
        resposta += "• Veja horários disponíveis em tempo real\n"
        resposta += "• Gerencie seus agendamentos\n\n"
        
        resposta += "💡 **Comandos de Agendamento**:\n"
        resposta += "• `horários disponíveis` - Ver opções\n"
        resposta += "• `como solicitar` - Aprender o processo\n"
        resposta += "• `ajuda agendamento` - Comandos completos\n\n"
        
        resposta += "🎯 **Exemplo de uso**:\n"
        resposta += "'Quero solicitar reposição para segunda-feira às 14:00 por consulta médica'"
        
        return resposta
        
    def gerar_relatorio_completo(self, nome_aluno: str = None) -> str:
        """Gera relatório completo do aluno"""
        if not nome_aluno:
            return "❌ Nome do aluno não informado."
            
        # Informações básicas
        resposta = f"📊 **RELATÓRIO COMPLETO - {nome_aluno.upper()}**\n"
        resposta += "=" * 50 + "\n\n"
        
        # Dados do aluno
        if nome_aluno in self.chatbot.alunos:
            aluno = self.chatbot.alunos[nome_aluno]
            resposta += f"👤 **Dados Pessoais**:\n"
            resposta += f"• Nome: {aluno['nome']}\n"
            resposta += f"• Turma: {aluno['turma']}\n"
            resposta += f"• Responsável: {aluno.get('responsavel', 'Não informado')}\n"
            resposta += f"• Número: {aluno['numero']}\n\n"
            
            resposta += f"📅 **Faltas Registradas**:\n"
            if aluno['faltas']:
                for falta in aluno['faltas']:
                    resposta += f"• {falta}\n"
            else:
                resposta += "• Nenhuma falta registrada\n"
            resposta += "\n"
            
        # Agendamentos
        resposta += f"🔄 **Agendamentos de Reposição**:\n"
        agendamentos = self.sistema_agendamento.listar_agendamentos_aluno(nome_aluno)
        resposta += agendamentos + "\n\n"
        
        # Estatísticas
        resposta += f"📈 **Estatísticas**:\n"
        total_reposicoes = len([a for a in self.sistema_agendamento.agendamentos.values() if a['aluno'] == nome_aluno])
        total_pendentes = len([s for s in self.sistema_agendamento.solicitacoes_pendentes.values() if s['aluno'] == nome_aluno])
        
        resposta += f"• Reposições confirmadas: {total_reposicoes}\n"
        resposta += f"• Solicitações pendentes: {total_pendentes}\n"
        resposta += f"• Total de solicitações: {total_reposicoes + total_pendentes}\n\n"
        
        resposta += "💡 **Próximos passos**:\n"
        if total_pendentes > 0:
            resposta += "• Confirme suas solicitações pendentes\n"
        resposta += "• Verifique horários disponíveis\n"
        resposta += "• Solicite novas reposições se necessário"
        
        return resposta
        
    def mostrar_menu_principal(self) -> str:
        """Mostra menu principal com todas as opções"""
        resposta = "🎯 **MENU PRINCIPAL - CHATBOT ESCOLAR**\n"
        resposta += "=" * 50 + "\n\n"
        
        resposta += "📚 **INFORMAÇÕES ACADÊMICAS**:\n"
        resposta += "• Horários de aulas\n"
        resposta += "• Calendário escolar\n"
        resposta += "• Material didático\n"
        resposta += "• Sistema de avaliação\n\n"
        
        resposta += "🔄 **SISTEMA DE REPOSIÇÕES**:\n"
        resposta += "• Solicitar reposições\n"
        resposta += "• Ver horários disponíveis\n"
        resposta += "• Gerenciar agendamentos\n"
        resposta += "• Cancelar agendamentos\n\n"
        
        resposta += "💰 **SERVIÇOS ADMINISTRATIVOS**:\n"
        resposta += "• Informações financeiras\n"
        resposta += "• Status de pagamentos\n"
        resposta += "• Documentos necessários\n\n"
        
        resposta += "🆘 **SUPORTE**:\n"
        resposta += "• FAQ automático\n"
        resposta += "• Atendente humano\n"
        resposta += "• Contatos de emergência\n\n"
        
        resposta += "💡 **COMO USAR**:\n"
        resposta += "• Pergunte naturalmente\n"
        resposta += "• Use comandos específicos para agendamentos\n"
        resposta += "• Digite 'humano' para atendente\n"
        resposta += "• Digite 'menu' para ver esta lista novamente"
        
        return resposta
        
    def processar_mensagem_inteligente(self, mensagem: str, nome_aluno: str = None) -> str:
        """Processa mensagem de forma inteligente e contextual"""
        mensagem_lower = mensagem.lower().strip()
        
        # Comandos especiais
        if mensagem_lower == 'menu':
            return self.mostrar_menu_principal()
        elif mensagem_lower == 'relatorio' or mensagem_lower == 'relatório':
            return self.gerar_relatorio_completo(nome_aluno)
        elif mensagem_lower == 'ajuda completa':
            return self.mostrar_ajuda_completa()
            
        # Processar com sistema integrado
        return self.processar_mensagem_completa(mensagem, nome_aluno)
        
    def mostrar_ajuda_completa(self) -> str:
        """Mostra ajuda completa do sistema"""
        resposta = "🆘 **AJUDA COMPLETA - CHATBOT ESCOLAR**\n"
        resposta += "=" * 50 + "\n\n"
        
        resposta += "🎯 **FUNCIONALIDADES PRINCIPAIS**:\n\n"
        
        resposta += "📚 **Informações Acadêmicas**:\n"
        resposta += "• 'Quais são os horários das aulas?'\n"
        resposta += "• 'Quando são as férias?'\n"
        resposta += "• 'Onde encontro o material didático?'\n"
        resposta += "• 'Como são calculadas as notas?'\n\n"
        
        resposta += "🔄 **Sistema de Reposições**:\n"
        resposta += "• 'Como solicito reposição?'\n"
        resposta += "• 'Quais horários estão disponíveis?'\n"
        resposta += "• 'solicitar reposição segunda-feira 14:00 consulta médica'\n"
        resposta += "• 'listar agendamentos'\n\n"
        
        resposta += "💰 **Serviços Administrativos**:\n"
        resposta += "• 'Quanto custa a mensalidade?'\n"
        resposta += "• 'Quais são as formas de pagamento?'\n"
        resposta += "• 'Quando vence a mensalidade?'\n\n"
        
        resposta += "🆘 **Suporte e Ajuda**:\n"
        resposta += "• 'Preciso de ajuda'\n"
        resposta += "• 'humano' - Falar com atendente\n"
        resposta += "• 'menu' - Ver menu principal\n"
        resposta += "• 'relatório' - Seu relatório completo\n\n"
        
        resposta += "💡 **DICAS DE USO**:\n"
        resposta += "• Pergunte naturalmente em português\n"
        resposta += "• Use comandos específicos para agendamentos\n"
        resposta += "• O sistema entende variações de linguagem\n"
        resposta += "• Sempre há opção de falar com humano\n\n"
        
        resposta += "📱 **Contatos de Emergência**:\n"
        resposta += "• WhatsApp: (82) 99999-9999\n"
        resposta += "• Email: contato@escola.com\n"
        resposta += "• Horário: Segunda a Sexta, 8h às 18h"
        
        return resposta

# Função principal para teste
def main():
    """Função principal para testar o sistema completo"""
    print("🤖 TESTANDO CHATBOT ESCOLAR COMPLETO")
    print("="*60)
    
    chatbot = ChatBotEscolaCompleto()
    
    # Testar início de conversa
    print("🚀 Iniciando conversa...")
    print(chatbot.iniciar_conversa_completa("João Gabriel"))
    print("\n" + "="*60)
    
    # Testar diferentes tipos de mensagens
    mensagens_teste = [
        "Oi, tudo bem?",
        "Quais são os horários das aulas?",
        "Como solicito reposição?",
        "Quais horários estão disponíveis?",
        "solicitar reposição segunda-feira 14:00 consulta médica",
        "menu",
        "relatório",
        "ajuda completa",
        "Tchau!"
    ]
    
    for mensagem in mensagens_teste:
        print(f"\n👤 **Usuário**: {mensagem}")
        resposta = chatbot.processar_mensagem_inteligente(mensagem, "João Gabriel")
        print(f"🤖 **Bot**: {resposta}")
        print("-" * 60)
        time.sleep(1)

if __name__ == "__main__":
    main()
