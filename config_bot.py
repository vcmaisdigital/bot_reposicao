# -*- coding: utf-8 -*-
"""
Arquivo de configuração para o Bot de Reposição de Aulas
Personalize aqui as mensagens, horários e configurações
"""

# ============================================================================
# CONFIGURAÇÕES GERAIS
# ============================================================================

# Nome e assinatura do professor
PROFESSOR_NOME = "Erick Oliveira"
PROFESSOR_EMPRESA = "Você+ Digital"

# Intervalo entre mensagens (em segundos) - evita bloqueios
INTERVALO_ENTRE_MENSAGENS = 3

# Intervalo entre verificações de resposta (em segundos)
INTERVALO_VERIFICACAO = 2

# Número máximo de tentativas para envio
MAX_TENTATIVAS_ENVIO = 3

# Tempo de espera para carregamento das páginas
TEMPO_ESPERA_CARREGAMENTO = 45

# ============================================================================
# CONFIGURAÇÃO DOS HORÁRIOS DE REPOSIÇÃO
# ============================================================================

# Período de reposição
PERIODO_REPOSICAO = "18 a 22 de agosto"

# Horários disponíveis por dia
HORARIOS_DISPONIVEIS = {
    "Segunda-feira": [
        "08:00 às 09:50",
        "10:00 às 11:50",
        "14:00 às 15:50",
        "16:00 às 17:50"
    ],
    "Terça-feira": [
        "08:00 às 09:50",
        "10:00 às 11:50",
        "19:00 às 20:50"
    ],
    "Quarta-feira": [
        "08:00 às 09:50",
        "10:00 às 11:50",
        "14:00 às 15:50",
        "16:00 às 17:50"
    ]
}

# ============================================================================
# CONFIGURAÇÃO DAS MENSAGENS
# ============================================================================

# Padrões para identificar horários nas respostas dos alunos
PADROES_HORARIOS = {
    "dias": [
        ("segunda", "Segunda-feira"),
        ("terça", "Terça-feira"),
        ("quarta", "Quarta-feira")
    ],
    "periodos": [
        ("manhã", "Manhã"),
        ("tarde", "Tarde"),
        ("noite", "Noite")
    ],
    "horarios_especificos": [
        ("08:00", "08:00 às 09:50"),
        ("10:00", "10:00 às 11:50"),
        ("14:00", "14:00 às 15:50"),
        ("16:00", "16:00 às 17:50"),
        ("19:00", "19:00 às 20:50")
    ]
}

# ============================================================================
# CONFIGURAÇÃO DO NAVEGADOR
# ============================================================================

# Opções do Chrome para melhor performance
CHROME_OPTIONS = [
    "--start-maximized",
    "--disable-notifications",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled"
]

# ============================================================================
# FUNÇÕES DE CONFIGURAÇÃO
# ============================================================================

def gerar_texto_horarios():
    """Gera o texto dos horários disponíveis para as mensagens"""
    texto = f"Horários disponíveis para reposição ({PERIODO_REPOSICAO}):\n\n"
    
    for dia, horarios in HORARIOS_DISPONIVEIS.items():
        texto += f"{dia}:\n"
        for horario in horarios:
            texto += f"• {horario}\n"
        texto += "\n"
    
    return texto.strip()

def gerar_assinatura():
    """Gera a assinatura padrão das mensagens"""
    return f"— {PROFESSOR_NOME} | {PROFESSOR_EMPRESA}"

def obter_configuracao_completa():
    """Retorna todas as configurações em um dicionário"""
    return {
        "professor": {
            "nome": PROFESSOR_NOME,
            "empresa": PROFESSOR_EMPRESA
        },
        "horarios": HORARIOS_DISPONIVEIS,
        "periodo": PERIODO_REPOSICAO,
        "padroes": PADROES_HORARIOS,
        "intervalos": {
            "mensagens": INTERVALO_ENTRE_MENSAGENS,
            "verificacao": INTERVALO_VERIFICACAO
        },
        "tentativas": MAX_TENTATIVAS_ENVIO,
        "tempo_espera": TEMPO_ESPERA_CARREGAMENTO,
        "chrome_options": CHROME_OPTIONS
    }

# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    print("🔧 CONFIGURAÇÕES DO BOT DE REPOSIÇÃO")
    print("="*50)
    
    config = obter_configuracao_completa()
    
    print(f"👨‍🏫 Professor: {config['professor']['nome']}")
    print(f"🏢 Empresa: {config['professor']['empresa']}")
    print(f"📅 Período: {config['periodo']}")
    print(f"⏰ Horários configurados: {len(config['horarios'])} dias")
    print(f"🔄 Tentativas de envio: {config['tentativas']}")
    print(f"⏱️ Intervalo entre mensagens: {config['intervalos']['mensagens']}s")
    
    print("\n📋 Horários disponíveis:")
    for dia, horarios in config['horarios'].items():
        print(f"   {dia}: {len(horarios)} opções")
    
    print("\n✅ Configurações carregadas com sucesso!")
