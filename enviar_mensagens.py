import pywhatkit
import time
from datetime import datetime, timedelta

# Estrutura de dados com alunos, responsáveis e faltas
alunos = {
    "turma1": [
        {
            "nome": "João Gabriel",
            "responsavel": "Camila",
            "telefone": "+55 82 9305-5741",
            "faltas": ["26/07"],
            "enviar_para": "responsavel"
        },
        {
            "nome": "Guilherme Alves Silva",
            "telefone": "+55 82 9840-6032",
            "faltas": ["19/07", "26/07"],
            "enviar_para": "aluno"
        },
        {
            "nome": "Josefa Marcia Lima",
            "telefone": "+55 82 8220-3748",
            "faltas": ["12/07", "26/07"],
            "enviar_para": "aluno"
        },
        {
            "nome": "Josivan",
            "telefone": "+55 82 9944-1016",
            "faltas": ["26/07", "09/08"],
            "enviar_para": "aluno"
        },
        {
            "nome": "Kira Fireman",
            "telefone": "+55 82 9925-3233",
            "faltas": ["26/07", "02/08"],
            "enviar_para": "aluno"
        },
        {
            "nome": "Mirilane Vieira",
            "telefone": "+55 82 8222-5814",
            "faltas": ["12/07", "19/07", "26/07", "09/08"],
            "enviar_para": "aluno"
        },
        {
            "nome": "Cleyton",
            "responsavel": "Suênia",
            "telefone": "+55 82 9308-2313",
            "faltas": ["26/07", "02/08"],
            "enviar_para": "responsavel"
        }
    ],
    "turma2": [
        {
            "nome": "Gabrielly Vitória",
            "telefone": "+55 82 9172-0074",
            "faltas": [],
            "enviar_para": "aluno"
        },
        {
            "nome": "Genielson Ramos",
            "telefone": "+55 41 9538-0181",
            "faltas": ["12/07", "19/07", "26/07", "02/08", "09/08"],
            "enviar_para": "aluno"
        },
        {
            "nome": "Isabella Caroline",
            "telefone": "+55 82 9912-6099",
            "faltas": ["19/07", "26/07"],
            "enviar_para": "aluno"
        },
        {
            "nome": "Esvaldo",
            "responsavel": "Marcia",
            "telefone": "+55 82 9927-4985",
            "faltas": ["12/07", "19/07", "26/07"],
            "enviar_para": "responsavel"
        },
        {
            "nome": "Ian Pietro",
            "responsavel": "Maria Elisangela",
            "telefone": "+55 67 8444-5189",
            "faltas": ["19/07", "26/07"],
            "enviar_para": "responsavel"
        },
        {
            "nome": "Pedro Jhefyte",
            "telefone": "+55 82 8138-7661",
            "faltas": ["12/07", "19/07", "26/07"],
            "enviar_para": "aluno"
        },
        {
            "nome": "Maria Fernanda",
            "responsavel": "Poliana",
            "telefone": "+55 82 9639-0908",
            "faltas": ["19/07", "26/07"],
            "enviar_para": "responsavel"
        },
        {
            "nome": "Taisa Fernanda",
            "telefone": "+55 82 8161-1334",
            "faltas": ["12/07", "19/07", "26/07"],
            "enviar_para": "aluno"
        }
    ]
}

def gerar_mensagem(aluno):
    # Definir destinatário da mensagem
    if aluno["enviar_para"] == "responsavel":
        destinatario = f"Olá! Tudo bem? 😊\nO(A) {aluno['nome']}"
    else:
        destinatario = f"Olá, {aluno['nome']}! Tudo bem? 😊\nVocê"

    # Se não tem faltas
    if not aluno["faltas"]:
        return f"{destinatario} esteve presente em todas as aulas, não há reposições pendentes. 🙌\n— Erick Oliveira | Você+ Digital"

    # Se tem apenas uma falta
    if len(aluno["faltas"]) == 1:
        return f"{destinatario} tem aula pendente no dia {aluno['faltas'][0]}.\nMe passe os dias e horários disponíveis para reposição.\nAguardo seu retorno!\n— Erick Oliveira | Você+ Digital"

    # Se tem múltiplas faltas
    faltas_texto = ", ".join(aluno["faltas"])
    return f"{destinatario} tem aulas pendentes nas datas: {faltas_texto}.\nMe envie os dias e horários disponíveis para reposição.\nAguardo seu retorno!\n— Erick Oliveira | Você+ Digital"

def enviar_mensagens():
    # Horário inicial para começar os envios
    agora = datetime.now()
    hora_envio = agora.hour
    minuto_envio = agora.minute + 1  # Começar um minuto depois

    for turma in alunos.values():
        for aluno in turma:
            # Formata o número removendo espaços e traços
            numero = aluno["telefone"].replace(" ", "").replace("-", "")
            
            mensagem = gerar_mensagem(aluno)
            
            try:
                # Envia a mensagem
                pywhatkit.sendwhatmsg(numero, mensagem, hora_envio, minuto_envio)
                
                # Incrementa 1 minuto para o próximo envio
                minuto_envio += 1
                if minuto_envio >= 60:
                    minuto_envio = 0
                    hora_envio += 1
                
                # Espera 15 segundos entre cada envio
                time.sleep(15)
                
            except Exception as e:
                print(f"Erro ao enviar mensagem para {aluno['nome']}: {str(e)}")

if __name__ == "__main__":
    print("Iniciando envio de mensagens...")
    enviar_mensagens()
    print("Processo de envio finalizado!")
