#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ChatBot de Auto-Atendimento Escolar
Sistema inteligente para automatizar o atendimento aos alunos
"""

import json
import re
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time

class ChatBotEscola:
    def __init__(self):
        self.carregar_dados()
        self.carregar_respostas()
        self.conversas_ativas = {}
        
    def carregar_dados(self):
        """Carrega todos os dados necessários para o chatbot"""
        # Dados dos alunos
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
        from data.dados_alunos import ALUNOS_DADOS
        self.alunos = {aluno['nome']: aluno for aluno in ALUNOS_DADOS}
        
        # Base de conhecimento
        self.base_conhecimento = {
            'horarios': {
                'Turma I': {
                    'Segunda': '08:00 - 10:00',
                    'Terça': '08:00 - 10:00',
                    'Quarta': '08:00 - 10:00',
                    'Quinta': '08:00 - 10:00',
                    'Sexta': '08:00 - 10:00'
                },
                'Turma II': {
                    'Segunda': '10:00 - 12:00',
                    'Terça': '10:00 - 12:00',
                    'Quarta': '10:00 - 12:00',
                    'Quinta': '10:00 - 12:00',
                    'Sexta': '10:00 - 12:00'
                },
                'Turma III': {
                    'Segunda': '15:00 - 17:00',
                    'Terça': '15:00 - 17:00',
                    'Quarta': '15:00 - 17:00',
                    'Quinta': '15:00 - 17:00',
                    'Sexta': '15:00 - 17:00'
                }
            },
            'calendario': {
                '2024': {
                    'Janeiro': ['01 - Ano Novo', '15 - Início das Aulas'],
                    'Fevereiro': ['12 - Carnaval', '20 - Reunião de Pais'],
                    'Março': ['08 - Dia da Mulher', '25 - Páscoa'],
                    'Abril': ['21 - Tiradentes', '30 - Reunião Pedagógica'],
                    'Maio': ['01 - Dia do Trabalho', '15 - Festa Junina'],
                    'Junho': ['24 - São João', '30 - Férias Escolares'],
                    'Julho': ['15 - Retorno das Aulas', '28 - Dia dos Avós'],
                    'Agosto': ['11 - Dia dos Pais', '25 - Semana da Pátria'],
                    'Setembro': ['07 - Independência', '21 - Primavera'],
                    'Outubro': ['12 - Dia das Crianças', '28 - Dia do Professor'],
                    'Novembro': ['02 - Finados', '15 - Proclamação da República'],
                    'Dezembro': ['25 - Natal', '31 - Ano Novo']
                }
            },
            'reposicoes': {
                'horarios_disponiveis': [
                    'Segunda-feira: 14:00 - 16:00',
                    'Terça-feira: 14:00 - 16:00',
                    'Quarta-feira: 14:00 - 16:00',
                    'Quinta-feira: 14:00 - 16:00',
                    'Sexta-feira: 14:00 - 16:00'
                ],
                'periodo_atual': '18 a 22 de agosto de 2024'
            },
            'material_didatico': {
                'links_importantes': [
                    '📚 Biblioteca Digital: https://biblioteca.escola.com',
                    '📖 Apostilas: https://apostilas.escola.com',
                    '🎥 Vídeos Aulas: https://videos.escola.com',
                    '📝 Exercícios: https://exercicios.escola.com'
                ]
            }
        }
        
    def carregar_respostas(self):
        """Carrega as respostas padrão do chatbot"""
        self.respostas = {
            'saudacoes': [
                "Olá! 👋 Sou o assistente virtual da escola. Como posso ajudar você hoje?",
                "Oi! 😊 Bem-vindo ao sistema de auto-atendimento. Em que posso ser útil?",
                "Olá! 🎓 Sou seu assistente escolar. Como posso te ajudar?"
            ],
            'despedidas': [
                "Até logo! 👋 Se precisar de mais alguma coisa, estarei aqui!",
                "Tchau! 😊 Tenha um ótimo dia de estudos!",
                "Até a próxima! 🎓 Bons estudos!"
            ],
            'nao_entendi': [
                "Desculpe, não entendi sua pergunta. 🤔 Pode reformular?",
                "Hmm, não consegui entender. 😅 Pode explicar de outra forma?",
                "Não captei bem. 🤷‍♂️ Pode tentar de outra maneira?"
            ],
            'opcoes_disponiveis': [
                "📅 **Calendário e Datas**",
                "⏰ **Horários de Aulas**", 
                "🔄 **Reposições de Aulas**",
                "📚 **Material Didático**",
                "💰 **Financeiro**",
                "📊 **Notas e Frequência**",
                "🆘 **Suporte Humano**"
            ]
        }
        
    def identificar_intencao(self, mensagem: str) -> Tuple[str, float]:
        """Identifica a intenção da mensagem usando NLP simples"""
        mensagem = mensagem.lower().strip()
        
        # Padrões para cada intenção
        padroes = {
            'saudacao': [
                r'\b(oi|ola|hey|hi|hello|bom dia|boa tarde|boa noite)\b',
                r'\b(tudo bem|como vai|como esta)\b'
            ],
            'despedida': [
                r'\b(tchau|ate|ate logo|ate mais|bye|goodbye)\b',
                r'\b(sair|encerrar|finalizar)\b'
            ],
            'horarios': [
                r'\b(horario|horarios|aula|aulas|grade|curricular)\b',
                r'\b(que horas|quando|dia da semana)\b',
                r'\b(segunda|terca|quarta|quinta|sexta)\b'
            ],
            'calendario': [
                r'\b(calendario|data|datas|evento|eventos|feriado|feriados)\b',
                r'\b(quando|dia|mes|ano)\b',
                r'\b(inicio|fim|termino|reuniao|festa)\b'
            ],
            'reposicoes': [
                r'\b(reposicao|reposicoes|faltou|perdeu|recuperar)\b',
                r'\b(aula perdida|falta|ausencia|recuperacao)\b',
                r'\b(quando|horario|agendar|marcar)\b'
            ],
            'material': [
                r'\b(material|apostila|livro|livros|exercicio|exercicios)\b',
                r'\b(link|site|url|download|baixar)\b',
                r'\b(biblioteca|digital|online)\b'
            ],
            'financeiro': [
                r'\b(pagamento|mensalidade|boleto|valor|preco)\b',
                r'\b(parcela|vencimento|multa|juros)\b',
                r'\b(conta|debito|credito|pix)\b'
            ],
            'notas': [
                r'\b(nota|notas|prova|provas|avaliacao|avaliacoes)\b',
                r'\b(pontuacao|media|conceito|resultado)\b',
                r'\b(frequencia|presenca|ausencia)\b'
            ],
            'ajuda': [
                r'\b(ajuda|help|socorro|problema|dificuldade)\b',
                r'\b(nao sei|como|o que|quando|onde)\b',
                r'\b(duvida|duvidas|pergunta|questao)\b'
            ]
        }
        
        # Calcular score para cada intenção
        scores = {}
        for intencao, padroes_intencao in padroes.items():
            score = 0
            for padrao in padroes_intencao:
                matches = re.findall(padrao, mensagem)
                score += len(matches) * 0.5
            scores[intencao] = score
            
        # Retornar intenção com maior score
        if scores:
            melhor_intencao = max(scores, key=scores.get)
            melhor_score = scores[melhor_intencao]
            return melhor_intencao, melhor_score
            
        return 'nao_entendi', 0.0
        
    def gerar_resposta(self, mensagem: str, nome_aluno: str = None) -> str:
        """Gera resposta baseada na intenção identificada"""
        intencao, score = self.identificar_intencao(mensagem)
        
        # Se score muito baixo, não entendeu
        if score < 0.3:
            return random.choice(self.respostas['nao_entendi'])
            
        # Gerar resposta baseada na intenção
        if intencao == 'saudacao':
            return random.choice(self.respostas['saudacoes'])
            
        elif intencao == 'despedida':
            return random.choice(self.respostas['despedidas'])
            
        elif intencao == 'horarios':
            return self.responder_horarios(nome_aluno)
            
        elif intencao == 'calendario':
            return self.responder_calendario()
            
        elif intencao == 'reposicoes':
            return self.responder_reposicoes()
            
        elif intencao == 'material':
            return self.responder_material()
            
        elif intencao == 'financeiro':
            return self.responder_financeiro()
            
        elif intencao == 'notas':
            return self.responder_notas()
            
        elif intencao == 'ajuda':
            return self.responder_ajuda()
            
        else:
            return random.choice(self.respostas['nao_entendi'])
            
    def responder_horarios(self, nome_aluno: str = None) -> str:
        """Responde sobre horários de aulas"""
        if nome_aluno and nome_aluno in self.alunos:
            turma = self.alunos[nome_aluno]['turma']
            horarios_turma = self.base_conhecimento['horarios'].get(turma, {})
            
            resposta = f"📚 **Horários da {turma}**\n\n"
            for dia, horario in horarios_turma.items():
                resposta += f"• **{dia}**: {horario}\n"
            resposta += f"\n📍 **Local**: Sala Principal\n👨‍🏫 **Professor**: Erick Oliveira"
            
        else:
            resposta = "⏰ **Horários Disponíveis**\n\n"
            for turma, horarios in self.base_conhecimento['horarios'].items():
                resposta += f"**{turma}**:\n"
                for dia, horario in horarios.items():
                    resposta += f"  • {dia}: {horario}\n"
                resposta += "\n"
                
        return resposta
        
    def responder_calendario(self) -> str:
        """Responde sobre calendário escolar"""
        ano_atual = str(datetime.now().year)
        calendario_ano = self.base_conhecimento['calendario'].get(ano_atual, {})
        
        resposta = f"📅 **Calendário Escolar {ano_atual}**\n\n"
        
        mes_atual = datetime.now().month
        meses = list(calendario_ano.keys())
        
        for i, mes in enumerate(meses):
            if i + 1 >= mes_atual - 1:  # Mostrar mês atual e próximos
                resposta += f"**{mes}**:\n"
                for evento in calendario_ano[mes]:
                    resposta += f"  • {evento}\n"
                resposta += "\n"
                
        resposta += "📱 **Lembrete**: Configure notificações para não perder datas importantes!"
        return resposta
        
    def responder_reposicoes(self) -> str:
        """Responde sobre reposições de aulas"""
        reposicoes = self.base_conhecimento['reposicoes']
        
        resposta = "🔄 **Sistema de Reposições**\n\n"
        resposta += f"📅 **Período Atual**: {reposicoes['periodo_atual']}\n\n"
        resposta += "⏰ **Horários Disponíveis**:\n"
        
        for horario in reposicoes['horarios_disponiveis']:
            resposta += f"  • {horario}\n"
            
        resposta += "\n📋 **Como Solicitar**:\n"
        resposta += "1. Informe sua turma\n"
        resposta += "2. Escolha o horário preferido\n"
        resposta += "3. Confirme a solicitação\n\n"
        resposta += "💡 **Dica**: Reposições devem ser solicitadas com até 48h de antecedência"
        
        return resposta
        
    def responder_material(self) -> str:
        """Responde sobre material didático"""
        material = self.base_conhecimento['material_didatico']
        
        resposta = "📚 **Material Didático Disponível**\n\n"
        resposta += "🔗 **Links Importantes**:\n"
        
        for link in material['links_importantes']:
            resposta += f"  {link}\n"
            
        resposta += "\n📱 **Acesso Mobile**: Todos os materiais são compatíveis com dispositivos móveis\n"
        resposta += "💾 **Download**: Você pode baixar os materiais para uso offline\n"
        resposta += "🔄 **Atualizações**: Os materiais são atualizados semanalmente"
        
        return resposta
        
    def responder_financeiro(self) -> str:
        """Responde sobre questões financeiras"""
        resposta = "💰 **Informações Financeiras**\n\n"
        resposta += "📊 **Mensalidade**: R$ 150,00\n"
        resposta += "📅 **Vencimento**: Todo dia 10 de cada mês\n"
        resposta += "💳 **Formas de Pagamento**:\n"
        resposta += "  • PIX (preferencial)\n"
        resposta += "  • Boleto bancário\n"
        resposta += "  • Cartão de crédito (parcelado)\n\n"
        resposta += "📞 **Para dúvidas específicas**: Entre em contato com a secretaria\n"
        resposta += "📧 **Email**: financeiro@escola.com\n"
        resposta += "📱 **WhatsApp**: (82) 99999-9999"
        
        return resposta
        
    def responder_notas(self) -> str:
        """Responde sobre notas e frequência"""
        resposta = "📊 **Sistema de Avaliação**\n\n"
        resposta += "📝 **Critérios de Avaliação**:\n"
        resposta += "  • Prova 1: 30%\n"
        resposta += "  • Prova 2: 30%\n"
        resposta += "  • Trabalhos: 20%\n"
        resposta += "  • Participação: 20%\n\n"
        resposta += "📈 **Frequência Mínima**: 75%\n"
        resposta += "🎯 **Média para Aprovação**: 7,0\n\n"
        resposta += "📱 **Consulta Online**: Acesse o portal do aluno\n"
        resposta += "🔔 **Notificações**: Receba alertas sobre suas notas"
        
        return resposta
        
    def responder_ajuda(self) -> str:
        """Responde com opções de ajuda"""
        resposta = "🆘 **Como Posso Ajudar?**\n\n"
        resposta += "Escolha uma das opções abaixo:\n\n"
        
        for opcao in self.respostas['opcoes_disponiveis']:
            resposta += f"{opcao}\n"
            
        resposta += "\n💡 **Dica**: Você pode perguntar naturalmente, como:\n"
        resposta += "• 'Quais são os horários das aulas?'\n"
        resposta += "• 'Quando são as férias?'\n"
        resposta += "• 'Como solicito reposição?'\n\n"
        resposta += "🆘 **Suporte Humano**: Digite 'humano' para falar com um atendente"
        
        return resposta
        
    def processar_mensagem(self, mensagem: str, nome_aluno: str = None) -> str:
        """Processa mensagem e retorna resposta"""
        # Verificar se quer falar com humano
        if 'humano' in mensagem.lower() or 'atendente' in mensagem.lower():
            return self.escalar_para_humano()
            
        # Gerar resposta automática
        resposta = self.gerar_resposta(mensagem, nome_aluno)
        
        # Adicionar sugestões de próximas perguntas
        sugestoes = self.gerar_sugestoes(mensagem)
        if sugestoes:
            resposta += f"\n\n💭 **Perguntas Relacionadas**:\n{sugestoes}"
            
        return resposta
        
    def escalar_para_humano(self) -> str:
        """Escala conversa para atendente humano"""
        resposta = "🆘 **Escalando para Atendente Humano**\n\n"
        resposta += "⏰ **Tempo de Espera**: 2-5 minutos\n"
        resposta += "👨‍💼 **Atendente**: Erick Oliveira\n"
        resposta += "📱 **WhatsApp**: (82) 99999-9999\n\n"
        resposta += "🔄 **Enquanto isso, você pode**:\n"
        resposta += "• Consultar o FAQ\n"
        resposta += "• Verificar horários\n"
        resposta += "• Acessar materiais\n\n"
        resposta += "📞 **Sua conversa será transferida automaticamente**"
        
        return resposta
        
    def gerar_sugestoes(self, mensagem_original: str) -> str:
        """Gera sugestões de próximas perguntas"""
        sugestoes = []
        
        if 'horario' in mensagem_original.lower():
            sugestoes.extend([
                "• 'Qual é o calendário de eventos?'",
                "• 'Como solicito reposição de aula?'",
                "• 'Onde encontro o material didático?'"
            ])
        elif 'calendario' in mensagem_original.lower():
            sugestoes.extend([
                "• 'Quais são os horários das aulas?'",
                "• 'Quando são as próximas férias?'",
                "• 'Há eventos especiais este mês?'"
            ])
        elif 'reposicao' in mensagem_original.lower():
            sugestoes.extend([
                "• 'Quais são os horários disponíveis?'",
                "• 'Como funciona o sistema de reposições?'",
                "• 'Qual é o prazo para solicitar?'"
            ])
        else:
            sugestoes.extend([
                "• 'Quais são os horários das aulas?'",
                "• 'Quando são as próximas férias?'",
                "• 'Como solicito reposição de aula?'"
            ])
            
        return '\n'.join(sugestoes[:3])  # Máximo 3 sugestões
        
    def iniciar_conversa(self, nome_aluno: str = None) -> str:
        """Inicia uma nova conversa"""
        saudacao = random.choice(self.respostas['saudacoes'])
        
        if nome_aluno:
            saudacao = saudacao.replace("!", f", {nome_aluno}!")
            
        resposta = f"{saudacao}\n\n"
        resposta += "🎯 **Principais Funcionalidades**:\n"
        
        for opcao in self.respostas['opcoes_disponiveis']:
            resposta += f"  {opcao}\n"
            
        resposta += "\n💡 **Dica**: Pergunte naturalmente! Exemplo:\n"
        resposta += "'Quais são os horários das aulas?' ou 'Quando são as férias?'"
        
        return resposta

# Função principal para teste
def main():
    """Função principal para testar o chatbot"""
    print("🤖 INICIANDO CHATBOT ESCOLAR")
    print("="*50)
    
    chatbot = ChatBotEscola()
    
    # Simular conversa
    print(chatbot.iniciar_conversa("João"))
    print("\n" + "="*50)
    
    # Testar diferentes tipos de perguntas
    perguntas_teste = [
        "Oi, tudo bem?",
        "Quais são os horários das aulas?",
        "Quando são as férias?",
        "Como solicito reposição?",
        "Onde encontro o material?",
        "Quanto custa a mensalidade?",
        "Como são calculadas as notas?",
        "Preciso de ajuda",
        "Tchau!"
    ]
    
    for pergunta in perguntas_teste:
        print(f"\n👤 **Usuário**: {pergunta}")
        resposta = chatbot.processar_mensagem(pergunta, "João")
        print(f"🤖 **Bot**: {resposta}")
        print("-" * 50)
        time.sleep(1)

if __name__ == "__main__":
    main()
