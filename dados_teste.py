ALUNOS_TESTE = [
    # Um aluno que recebe diretamente
    {
        "nome": "Gabrielly Vitória",
        "numero": "+55 82 9172-0074",
        "faltas": [],
        "enviar_para_responsavel": False,
        "turma": "Turma II"
    },
    # Um aluno com mensagem para responsável
    {
        "nome": "Maria Fernanda",
        "responsavel": "Poliana",
        "numero": "+55 82 9639-0908",
        "faltas": ["19/07", "26/07"],
        "enviar_para_responsavel": True,
        "turma": "Turma II"
    },
    # Um aluno com número alternativo
    {
        "nome": "Stefanne Soraya",
        "responsavel": "Joseane",
        "numero": "+55 82 9397-7656",  # Número da Stefanne
        "numero_responsavel": "+55 82 9955-5410",  # Número da mãe
        "faltas": ["26/07"],
        "enviar_para_responsavel": False,
        "turma": "Turma I"
    }
]
