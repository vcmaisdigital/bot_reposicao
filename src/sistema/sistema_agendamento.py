#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📅 Sistema de Agendamento Inteligente para Reposições
Sistema automatizado para agendar e gerenciar reposições de aulas
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random

class SistemaAgendamento:
    def __init__(self):
        self.carregar_configuracoes()
        self.agendamentos = {}
        self.solicitacoes_pendentes = {}
        
    def carregar_configuracoes(self):
        """Carrega configurações do sistema de agendamento"""
        self.config = {
            'horarios_disponiveis': {
                'Segunda-feira': ['14:00', '16:00', '19:00'],
                'Terça-feira': ['14:00', '16:00', '19:00'],
                'Quarta-feira': ['14:00', '16:00', '19:00'],
                'Quinta-feira': ['14:00', '16:00', '19:00'],
                'Sexta-feira': ['14:00', '16:00', '19:00']
            },
            'duracao_aula': 120,  # minutos
            'antecedencia_minima': 48,  # horas
            'max_reposicoes_semana': 2,
            'max_alunos_por_horario': 8,
            'periodo_atual': '18 a 22 de agosto de 2024'
        }
        
        # Carregar dados dos alunos
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
        from data.dados_alunos import ALUNOS_DADOS
        self.alunos = {aluno['nome']: aluno for aluno in ALUNOS_DADOS}
        
    def validar_solicitacao(self, nome_aluno: str, dia: str, horario: str, motivo: str) -> Tuple[bool, str]:
        """Valida uma solicitação de reposição"""
        # Verificar se o aluno existe
        if nome_aluno not in self.alunos:
            return False, "❌ Aluno não encontrado no sistema."
            
        # Verificar se o dia é válido
        if dia not in self.config['horarios_disponiveis']:
            return False, "❌ Dia da semana inválido."
            
        # Verificar se o horário é válido
        if horario not in self.config['horarios_disponiveis'][dia]:
            return False, "❌ Horário não disponível para este dia."
            
        # Verificar antecedência mínima
        data_solicitacao = datetime.now()
        data_reposicao = self.calcular_data_reposicao(dia, horario)
        
        if data_reposicao <= data_solicitacao + timedelta(hours=self.config['antecedencia_minima']):
            return False, f"❌ Reposição deve ser solicitada com pelo menos {self.config['antecedencia_minima']}h de antecedência."
            
        # Verificar limite de reposições por semana
        if self.verificar_limite_semanal(nome_aluno):
            return False, "❌ Limite de reposições semanais atingido."
            
        # Verificar disponibilidade do horário
        if not self.verificar_disponibilidade_horario(dia, horario):
            return False, "❌ Horário já está lotado."
            
        # Verificar se não há conflito com horário regular
        if self.verificar_conflito_horario_regular(nome_aluno, dia, horario):
            return False, "❌ Conflito com horário regular de aula."
            
        return True, "✅ Solicitação válida!"
        
    def calcular_data_reposicao(self, dia: str, horario: str) -> datetime:
        """Calcula a data da reposição baseada no dia da semana"""
        hoje = datetime.now()
        dias_semana = {
            'Segunda-feira': 0,
            'Terça-feira': 1,
            'Quarta-feira': 2,
            'Quinta-feira': 3,
            'Sexta-feira': 4
        }
        
        dia_desejado = dias_semana[dia]
        dias_para_adicionar = (dia_desejado - hoje.weekday()) % 7
        
        # Se for hoje, adicionar 7 dias
        if dias_para_adicionar == 0:
            dias_para_adicionar = 7
            
        data_reposicao = hoje + timedelta(days=dias_para_adicionar)
        
        # Adicionar horário
        hora, minuto = map(int, horario.split(':'))
        data_reposicao = data_reposicao.replace(hour=hora, minute=minuto, second=0, microsecond=0)
        
        return data_reposicao
        
    def verificar_limite_semanal(self, nome_aluno: str) -> bool:
        """Verifica se o aluno atingiu o limite de reposições semanais"""
        semana_atual = datetime.now().isocalendar()[1]
        reposicoes_semana = 0
        
        for agendamento in self.agendamentos.values():
            if (agendamento['aluno'] == nome_aluno and 
                agendamento['data'].isocalendar()[1] == semana_atual):
                reposicoes_semana += 1
                
        return reposicoes_semana >= self.config['max_reposicoes_semana']
        
    def verificar_disponibilidade_horario(self, dia: str, horario: str) -> bool:
        """Verifica se há vagas disponíveis no horário"""
        alunos_no_horario = 0
        
        for agendamento in self.agendamentos.values():
            if (agendamento['dia'] == dia and 
                agendamento['horario'] == horario):
                alunos_no_horario += 1
                
        return alunos_no_horario < self.config['max_alunos_por_horario']
        
    def verificar_conflito_horario_regular(self, nome_aluno: str, dia: str, horario: str) -> bool:
        """Verifica se há conflito com o horário regular de aula"""
        aluno = self.alunos[nome_aluno]
        turma = aluno['turma']
        
        # Horários regulares das turmas
        horarios_regulares = {
            'Turma I': '08:00',
            'Turma II': '10:00',
            'Turma III': '15:00'
        }
        
        horario_regular = horarios_regulares.get(turma)
        if horario_regular and horario_regular == horario:
            return True
            
        return False
        
    def criar_solicitacao(self, nome_aluno: str, dia: str, horario: str, motivo: str) -> Tuple[bool, str]:
        """Cria uma nova solicitação de reposição"""
        # Validar solicitação
        valida, mensagem = self.validar_solicitacao(nome_aluno, dia, horario, motivo)
        if not valida:
            return False, mensagem
            
        # Gerar ID único
        id_solicitacao = f"REP_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        
        # Criar solicitação
        solicitacao = {
            'id': id_solicitacao,
            'aluno': nome_aluno,
            'turma': self.alunos[nome_aluno]['turma'],
            'dia': dia,
            'horario': horario,
            'motivo': motivo,
            'data_solicitacao': datetime.now(),
            'data_reposicao': self.calcular_data_reposicao(dia, horario),
            'status': 'pendente',
            'confirmada': False
        }
        
        self.solicitacoes_pendentes[id_solicitacao] = solicitacao
        
        return True, f"✅ Solicitação criada com sucesso!\n📋 **ID**: {id_solicitacao}\n📅 **Data**: {solicitacao['data_reposicao'].strftime('%d/%m/%Y às %H:%M')}"
        
    def confirmar_agendamento(self, id_solicitacao: str) -> Tuple[bool, str]:
        """Confirma um agendamento de reposição"""
        if id_solicitacao not in self.solicitacoes_pendentes:
            return False, "❌ Solicitação não encontrada."
            
        solicitacao = self.solicitacoes_pendentes[id_solicitacao]
        
        # Verificar se ainda está válida
        valida, mensagem = self.validar_solicitacao(
            solicitacao['aluno'], 
            solicitacao['dia'], 
            solicitacao['horario'], 
            solicitacao['motivo']
        )
        
        if not valida:
            # Remover solicitação inválida
            del self.solicitacoes_pendentes[id_solicitacao]
            return False, f"❌ Solicitação expirou: {mensagem}"
            
        # Confirmar agendamento
        solicitacao['status'] = 'confirmada'
        solicitacao['confirmada'] = True
        solicitacao['data_confirmacao'] = datetime.now()
        
        # Mover para agendamentos confirmados
        self.agendamentos[id_solicitacao] = solicitacao
        del self.solicitacoes_pendentes[id_solicitacao]
        
        # Gerar confirmação
        confirmacao = self.gerar_confirmacao_agendamento(solicitacao)
        
        return True, confirmacao
        
    def gerar_confirmacao_agendamento(self, agendamento: Dict) -> str:
        """Gera mensagem de confirmação do agendamento"""
        resposta = "🎉 **REPOSIÇÃO CONFIRMADA!**\n\n"
        resposta += f"👤 **Aluno**: {agendamento['aluno']}\n"
        resposta += f"📚 **Turma**: {agendamento['turma']}\n"
        resposta += f"📅 **Data**: {agendamento['data_reposicao'].strftime('%A, %d/%m/%Y')}\n"
        resposta += f"⏰ **Horário**: {agendamento['horario']}\n"
        resposta += f"📍 **Local**: Sala de Reposição\n"
        resposta += f"👨‍🏫 **Professor**: Erick Oliveira\n\n"
        
        resposta += "📋 **Informações Importantes**:\n"
        resposta += "• Chegue com 10 minutos de antecedência\n"
        resposta += "• Traga material de estudo\n"
        resposta += "• Em caso de imprevisto, avise com 24h de antecedência\n\n"
        
        resposta += "🔔 **Lembretes**:\n"
        resposta += "• Você receberá lembretes por WhatsApp\n"
        resposta += "• Confirme sua presença 2h antes da aula\n\n"
        
        resposta += "📱 **Contato**: (82) 99999-9999"
        
        return resposta
        
    def cancelar_agendamento(self, id_solicitacao: str, motivo_cancelamento: str) -> Tuple[bool, str]:
        """Cancela um agendamento confirmado"""
        if id_solicitacao not in self.agendamentos:
            return False, "❌ Agendamento não encontrado."
            
        agendamento = self.agendamentos[id_solicitacao]
        
        # Verificar se pode cancelar (mínimo 24h antes)
        tempo_restante = agendamento['data_reposicao'] - datetime.now()
        if tempo_restante.total_seconds() < 24 * 3600:
            return False, "❌ Cancelamento deve ser feito com pelo menos 24h de antecedência."
            
        # Cancelar agendamento
        agendamento['status'] = 'cancelado'
        agendamento['motivo_cancelamento'] = motivo_cancelamento
        agendamento['data_cancelamento'] = datetime.now()
        
        # Remover dos agendamentos ativos
        del self.agendamentos[id_solicitacao]
        
        return True, "✅ Agendamento cancelado com sucesso!"
        
    def listar_agendamentos_aluno(self, nome_aluno: str) -> str:
        """Lista todos os agendamentos de um aluno"""
        agendamentos_aluno = []
        
        # Agendamentos confirmados
        for agendamento in self.agendamentos.values():
            if agendamento['aluno'] == nome_aluno:
                agendamentos_aluno.append(agendamento)
                
        # Solicitações pendentes
        for solicitacao in self.solicitacoes_pendentes.values():
            if solicitacao['aluno'] == nome_aluno:
                agendamentos_aluno.append(solicitacao)
                
        if not agendamentos_aluno:
            return "📋 **Nenhum agendamento encontrado.**\n\n💡 Para solicitar uma reposição, use o comando de agendamento."
            
        # Ordenar por data
        agendamentos_aluno.sort(key=lambda x: x['data_reposicao'])
        
        resposta = f"📋 **Agendamentos de {nome_aluno}**\n\n"
        
        for i, agendamento in enumerate(agendamentos_aluno, 1):
            status_emoji = {
                'pendente': '⏳',
                'confirmada': '✅',
                'cancelada': '❌'
            }
            
            resposta += f"{i}. {status_emoji.get(agendamento['status'], '❓')} "
            resposta += f"**{agendamento['dia']} às {agendamento['horario']}**\n"
            resposta += f"   📅 {agendamento['data_reposicao'].strftime('%d/%m/%Y')}\n"
            resposta += f"   📚 {agendamento['turma']}\n"
            resposta += f"   📝 Motivo: {agendamento['motivo']}\n"
            
            if agendamento['status'] == 'pendente':
                resposta += f"   🆔 ID: {agendamento['id']}\n"
                resposta += f"   💡 **Confirme com**: confirmar {agendamento['id']}\n"
            elif agendamento['status'] == 'confirmada':
                resposta += f"   🆔 ID: {agendamento['id']}\n"
                resposta += f"   🚫 **Para cancelar**: cancelar {agendamento['id']} [motivo]\n"
                
            resposta += "\n"
            
        return resposta
        
    def listar_horarios_disponiveis(self, dia: str = None) -> str:
        """Lista horários disponíveis para reposições"""
        if dia and dia not in self.config['horarios_disponiveis']:
            return "❌ Dia da semana inválido."
            
        resposta = "⏰ **Horários Disponíveis para Reposições**\n\n"
        
        if dia:
            # Mostrar apenas o dia específico
            resposta += f"📅 **{dia}**\n"
            horarios = self.config['horarios_disponiveis'][dia]
            vagas_disponiveis = self.calcular_vagas_disponiveis(dia)
            
            for horario in horarios:
                vagas = vagas_disponiveis.get(horario, self.config['max_alunos_por_horario'])
                emoji_vagas = "🟢" if vagas > 0 else "🔴"
                resposta += f"  {emoji_vagas} **{horario}** - {vagas} vagas\n"
        else:
            # Mostrar todos os dias
            for dia_semana, horarios in self.config['horarios_disponiveis'].items():
                resposta += f"📅 **{dia_semana}**\n"
                vagas_disponiveis = self.calcular_vagas_disponiveis(dia_semana)
                
                for horario in horarios:
                    vagas = vagas_disponiveis.get(horario, self.config['max_alunos_por_horario'])
                    emoji_vagas = "🟢" if vagas > 0 else "🔴"
                    resposta += f"  {emoji_vagas} **{horario}** - {vagas} vagas\n"
                resposta += "\n"
                
        resposta += "\n💡 **Como solicitar**:\n"
        resposta += "• Use: solicitar reposição [dia] [horario] [motivo]\n"
        resposta += "• Exemplo: solicitar reposição segunda-feira 14:00 falta médica"
        
        return resposta
        
    def calcular_vagas_disponiveis(self, dia: str) -> Dict[str, int]:
        """Calcula vagas disponíveis para cada horário de um dia"""
        vagas = {}
        
        for horario in self.config['horarios_disponiveis'][dia]:
            alunos_agendados = 0
            
            # Contar agendamentos confirmados
            for agendamento in self.agendamentos.values():
                if agendamento['dia'] == dia and agendamento['horario'] == horario:
                    alunos_agendados += 1
                    
            vagas_disponiveis = self.config['max_alunos_por_horario'] - alunos_agendados
            vagas[horario] = max(0, vagas_disponiveis)
            
        return vagas
        
    def processar_comando(self, comando: str, nome_aluno: str) -> str:
        """Processa comandos de agendamento"""
        comando = comando.lower().strip()
        
        # Comando: solicitar reposição
        if comando.startswith('solicitar reposição') or comando.startswith('solicitar reposicao'):
            return self.processar_solicitacao(comando, nome_aluno)
            
        # Comando: confirmar
        elif comando.startswith('confirmar'):
            return self.processar_confirmacao(comando, nome_aluno)
            
        # Comando: cancelar
        elif comando.startswith('cancelar'):
            return self.processar_cancelamento(comando, nome_aluno)
            
        # Comando: listar agendamentos
        elif comando.startswith('listar') or comando.startswith('meus agendamentos'):
            return self.listar_agendamentos_aluno(nome_aluno)
            
        # Comando: horários disponíveis
        elif comando.startswith('horários') or comando.startswith('horarios'):
            return self.listar_horarios_disponiveis()
            
        # Comando: ajuda
        elif comando.startswith('ajuda') or comando.startswith('help'):
            return self.mostrar_ajuda()
            
        else:
            return "❓ **Comando não reconhecido.**\n\n💡 **Comandos disponíveis**:\n• solicitar reposição [dia] [horario] [motivo]\n• confirmar [ID]\n• cancelar [ID] [motivo]\n• listar agendamentos\n• horários disponíveis\n• ajuda"
            
    def processar_solicitacao(self, comando: str, nome_aluno: str) -> str:
        """Processa comando de solicitação de reposição"""
        # Extrair parâmetros do comando
        partes = comando.split()
        
        if len(partes) < 5:
            return "❌ **Formato incorreto.**\n\n💡 **Uso correto**:\nsolicitar reposição [dia] [horario] [motivo]\n\n📝 **Exemplo**:\nsolicitar reposição segunda-feira 14:00 falta médica"
            
        # Extrair dia, horário e motivo
        dia = partes[2] + "-feira" if partes[2] in ['segunda', 'terca', 'quarta', 'quinta', 'sexta'] else None
        horario = partes[3] if len(partes) > 3 else None
        motivo = " ".join(partes[4:]) if len(partes) > 4 else "Não informado"
        
        if not dia or not horario:
            return "❌ **Dia ou horário inválido.**\n\n💡 **Dias válidos**: segunda, terça, quarta, quinta, sexta\n💡 **Horários válidos**: 14:00, 16:00, 19:00"
            
        # Criar solicitação
        sucesso, mensagem = self.criar_solicitacao(nome_aluno, dia, horario, motivo)
        return mensagem
        
    def processar_confirmacao(self, comando: str, nome_aluno: str) -> str:
        """Processa comando de confirmação"""
        partes = comando.split()
        
        if len(partes) < 2:
            return "❌ **ID da solicitação não informado.**\n\n💡 **Uso**: confirmar [ID]"
            
        id_solicitacao = partes[1]
        sucesso, mensagem = self.confirmar_agendamento(id_solicitacao)
        return mensagem
        
    def processar_cancelamento(self, comando: str, nome_aluno: str) -> str:
        """Processa comando de cancelamento"""
        partes = comando.split()
        
        if len(partes) < 2:
            return "❌ **ID do agendamento não informado.**\n\n💡 **Uso**: cancelar [ID] [motivo]"
            
        id_solicitacao = partes[1]
        motivo = " ".join(partes[2:]) if len(partes) > 2 else "Cancelado pelo aluno"
        
        sucesso, mensagem = self.cancelar_agendamento(id_solicitacao, motivo)
        return mensagem
        
    def mostrar_ajuda(self) -> str:
        """Mostra ajuda do sistema de agendamento"""
        resposta = "🆘 **SISTEMA DE AGENDAMENTO - AJUDA**\n\n"
        
        resposta += "📋 **COMANDOS DISPONÍVEIS**:\n\n"
        resposta += "🔄 **Solicitar Reposição**:\n"
        resposta += "• solicitar reposição [dia] [horario] [motivo]\n"
        resposta += "• Exemplo: solicitar reposição segunda-feira 14:00 falta médica\n\n"
        
        resposta += "✅ **Confirmar Agendamento**:\n"
        resposta += "• confirmar [ID]\n"
        resposta += "• Exemplo: confirmar REP_20240815_1430_1234\n\n"
        
        resposta += "❌ **Cancelar Agendamento**:\n"
        resposta += "• cancelar [ID] [motivo]\n"
        resposta += "• Exemplo: cancelar REP_20240815_1430_1234 imprevisto\n\n"
        
        resposta += "📋 **Listar Agendamentos**:\n"
        resposta += "• listar agendamentos\n"
        resposta += "• meus agendamentos\n\n"
        
        resposta += "⏰ **Ver Horários**:\n"
        resposta += "• horários disponíveis\n"
        resposta += "• horarios disponiveis\n\n"
        
        resposta += "📅 **DIAS DISPONÍVEIS**:\n"
        resposta += "• Segunda-feira\n"
        resposta += "• Terça-feira\n"
        resposta += "• Quarta-feira\n"
        resposta += "• Quinta-feira\n"
        resposta += "• Sexta-feira\n\n"
        
        resposta += "⏰ **HORÁRIOS DISPONÍVEIS**:\n"
        resposta += "• 14:00 - 16:00\n"
        resposta += "• 16:00 - 18:00\n"
        resposta += "• 19:00 - 21:00\n\n"
        
        resposta += "⚠️ **REGRAS IMPORTANTES**:\n"
        resposta += "• Solicite com 48h de antecedência\n"
        resposta += "• Máximo 2 reposições por semana\n"
        resposta += "• Cancelamento com 24h de antecedência\n"
        resposta += "• Máximo 8 alunos por horário"
        
        return resposta

# Função principal para teste
def main():
    """Função principal para testar o sistema"""
    print("📅 TESTANDO SISTEMA DE AGENDAMENTO")
    print("="*50)
    
    sistema = SistemaAgendamento()
    
    # Testar solicitação
    print("🔄 Testando solicitação...")
    sucesso, msg = sistema.criar_solicitacao("João Gabriel", "Segunda-feira", "14:00", "Consulta médica")
    print(f"Resultado: {msg}")
    
    if sucesso:
        # Extrair ID da mensagem
        id_match = re.search(r'REP_\d+_\d+', msg)
        if id_match:
            id_solicitacao = id_match.group()
            
            print(f"\n✅ Confirmando agendamento {id_solicitacao}...")
            sucesso, msg = sistema.confirmar_agendamento(id_solicitacao)
            print(f"Resultado: {msg}")
            
            print(f"\n📋 Listando agendamentos...")
            msg = sistema.listar_agendamentos_aluno("João Gabriel")
            print(msg)
    
    print(f"\n⏰ Horários disponíveis:")
    msg = sistema.listar_horarios_disponiveis()
    print(msg)

if __name__ == "__main__":
    main()
