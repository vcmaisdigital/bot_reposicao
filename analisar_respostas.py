#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar e organizar as respostas capturadas pelo bot de reposição
"""

import json
from datetime import datetime
from collections import defaultdict

def carregar_respostas():
    """Carrega o arquivo de respostas"""
    try:
        with open('respostas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo 'respostas.json' não encontrado!")
        print("Execute o bot primeiro para capturar respostas.")
        return None

def analisar_horarios_preferidos(respostas):
    """Analisa os horários preferidos dos alunos"""
    print("\n" + "="*60)
    print("🕐 ANÁLISE DE HORÁRIOS PREFERIDOS")
    print("="*60)
    
    horarios_contagem = defaultdict(int)
    alunos_por_horario = defaultdict(list)
    
    for nome, dados in respostas.items():
        if dados.get('respostas'):
            for resposta in dados['respostas']:
                if resposta.get('horario_preferido'):
                    horario = resposta['horario_preferido']
                    horarios_contagem[horario] += 1
                    alunos_por_horario[horario].append(nome)
    
    if not horarios_contagem:
        print("❌ Nenhum horário preferido identificado ainda.")
        return
    
    # Ordena por quantidade de preferências
    horarios_ordenados = sorted(horarios_contagem.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n📊 Total de horários identificados: {len(horarios_contagem)}")
    print(f"👥 Total de alunos com preferências: {len(set([aluno for alunos in alunos_por_horario.values() for aluno in alunos]))}")
    
    for horario, quantidade in horarios_ordenados:
        print(f"\n🕐 {horario}")
        print(f"   Preferido por {quantidade} aluno(s):")
        for aluno in alunos_por_horario[horario]:
            print(f"   • {aluno}")

def analisar_status_turmas(respostas):
    """Analisa o status por turma"""
    print("\n" + "="*60)
    print("🏫 ANÁLISE POR TURMA")
    print("="*60)
    
    turmas = defaultdict(lambda: {
        'total': 0,
        'enviados': 0,
        'respondidos': 0,
        'pendentes': 0
    })
    
    for nome, dados in respostas.items():
        turma = dados.get('turma', 'Sem turma')
        turmas[turma]['total'] += 1
        
        if dados.get('mensagem_enviada'):
            turmas[turma]['enviados'] += 1
        
        if dados.get('respostas'):
            turmas[turma]['respondidos'] += 1
        else:
            turmas[turma]['pendentes'] += 1
    
    for turma, stats in turmas.items():
        print(f"\n🏫 {turma}")
        print(f"   Total de alunos: {stats['total']}")
        print(f"   Mensagens enviadas: {stats['enviados']} ({(stats['enviados']/stats['total']*100):.1f}%)")
        print(f"   Alunos que responderam: {stats['respondidos']} ({(stats['respondidos']/stats['total']*100):.1f}%)")
        print(f"   Pendentes de resposta: {stats['pendentes']} ({(stats['pendentes']/stats['total']*100):.1f}%)")

def listar_alunos_pendentes(respostas):
    """Lista alunos que ainda não responderam"""
    print("\n" + "="*60)
    print("⏳ ALUNOS PENDENTES DE RESPOSTA")
    print("="*60)
    
    pendentes = []
    for nome, dados in respostas.items():
        if dados.get('mensagem_enviada') and not dados.get('respostas'):
            pendentes.append((nome, dados))
    
    if not pendentes:
        print("✅ Todos os alunos que receberam mensagem já responderam!")
        return
    
    print(f"\n📋 Total de alunos pendentes: {len(pendentes)}")
    
    # Organiza por turma
    turmas_pendentes = defaultdict(list)
    for nome, dados in pendentes:
        turma = dados.get('turma', 'Sem turma')
        turmas_pendentes[turma].append((nome, dados))
    
    for turma, alunos in turmas_pendentes.items():
        print(f"\n🏫 {turma} ({len(alunos)} pendentes):")
        for nome, dados in alunos:
            responsavel = dados.get('responsavel', '')
            if responsavel:
                print(f"   • {nome} (Responsável: {responsavel})")
            else:
                print(f"   • {nome}")

def gerar_resumo_executivo(respostas):
    """Gera um resumo executivo das demandas"""
    print("\n" + "="*60)
    print("📋 RESUMO EXECUTIVO")
    print("="*60)
    
    total_alunos = len(respostas)
    mensagens_enviadas = sum(1 for dados in respostas.values() if dados.get('mensagem_enviada'))
    alunos_respondidos = sum(1 for dados in respostas.values() if dados.get('respostas'))
    alunos_pendentes = mensagens_enviadas - alunos_respondidos
    
    # Calcula taxa de resposta
    taxa_resposta = (alunos_respondidos / mensagens_enviadas * 100) if mensagens_enviadas > 0 else 0
    
    print(f"\n📊 ESTATÍSTICAS GERAIS:")
    print(f"   Total de alunos no sistema: {total_alunos}")
    print(f"   Mensagens enviadas: {mensagens_enviadas}")
    print(f"   Alunos que responderam: {alunos_respondidos}")
    print(f"   Alunos pendentes: {alunos_pendentes}")
    print(f"   Taxa de resposta: {taxa_resposta:.1f}%")
    
    # Status das mensagens
    if mensagens_enviadas > 0:
        print(f"\n📤 STATUS DAS MENSAGENS:")
        print(f"   ✅ Enviadas com sucesso: {mensagens_enviadas}")
        print(f"   ❌ Não enviadas: {total_alunos - mensagens_enviadas}")
    
    # Status das respostas
    if mensagens_enviadas > 0:
        print(f"\n📥 STATUS DAS RESPOSTAS:")
        print(f"   ✅ Respondidos: {alunos_respondidos}")
        print(f"   ⏳ Aguardando resposta: {alunos_pendentes}")
        print(f"   📊 Taxa de resposta: {taxa_resposta:.1f}%")

def exportar_dados_organizados(respostas):
    """Exporta os dados organizados para facilitar a gestão"""
    print("\n" + "="*60)
    print("💾 EXPORTANDO DADOS ORGANIZADOS")
    print("="*60)
    
    # Organiza por status
    dados_organizados = {
        'respondidos': [],
        'pendentes': [],
        'nao_enviados': []
    }
    
    for nome, dados in respostas.items():
        aluno_info = {
            'nome': nome,
            'turma': dados.get('turma', ''),
            'responsavel': dados.get('responsavel', ''),
            'faltas': dados.get('faltas', []),
            'numero': dados.get('numero', ''),
            'numero_responsavel': dados.get('numero_responsavel', '')
        }
        
        if dados.get('respostas'):
            # Aluno que respondeu
            ultima_resposta = dados['respostas'][-1]
            aluno_info.update({
                'status': 'respondido',
                'ultima_resposta': ultima_resposta.get('resposta', ''),
                'horario_preferido': ultima_resposta.get('horario_preferido', ''),
                'data_resposta': ultima_resposta.get('timestamp', '')
            })
            dados_organizados['respondidos'].append(aluno_info)
            
        elif dados.get('mensagem_enviada'):
            # Mensagem enviada mas sem resposta
            aluno_info.update({
                'status': 'pendente',
                'data_envio': dados.get('data_envio', '')
            })
            dados_organizados['pendentes'].append(aluno_info)
            
        else:
            # Mensagem não enviada
            aluno_info.update({
                'status': 'nao_enviado'
            })
            dados_organizados['nao_enviados'].append(aluno_info)
    
    # Salva dados organizados
    with open('dados_organizados.json', 'w', encoding='utf-8') as f:
        json.dump(dados_organizados, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Dados exportados para 'dados_organizados.json'")
    print(f"   📝 Respondidos: {len(dados_organizados['respondidos'])}")
    print(f"   ⏳ Pendentes: {len(dados_organizados['pendentes'])}")
    print(f"   ❌ Não enviados: {len(dados_organizados['nao_enviados'])}")

def main():
    print("🔍 ANALISADOR DE RESPOSTAS - BOT DE REPOSIÇÃO")
    print("="*60)
    
    # Carrega dados
    respostas = carregar_respostas()
    if not respostas:
        return
    
    print(f"✅ Dados carregados com sucesso!")
    print(f"📊 Total de alunos no sistema: {len(respostas)}")
    
    while True:
        print("\nEscolha uma análise:")
        print("1. 📊 Resumo executivo")
        print("2. 🏫 Análise por turma")
        print("3. 🕐 Análise de horários preferidos")
        print("4. ⏳ Listar alunos pendentes")
        print("5. 💾 Exportar dados organizados")
        print("6. ❌ Sair")
        
        opcao = input("\nDigite sua opção (1-6): ").strip()
        
        if opcao == "1":
            gerar_resumo_executivo(respostas)
        elif opcao == "2":
            analisar_status_turmas(respostas)
        elif opcao == "3":
            analisar_horarios_preferidos(respostas)
        elif opcao == "4":
            listar_alunos_pendentes(respostas)
        elif opcao == "5":
            exportar_dados_organizados(respostas)
        elif opcao == "6":
            print("👋 Saindo do analisador...")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
