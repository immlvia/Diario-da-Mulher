from datetime import datetime

def formatar_data_atual():
    """Retorna a data atual formatada para exibição no diário"""
    data_atual = datetime.now()
    dia = data_atual.day
    mes = MESES[data_atual.month]
    ano = data_atual.year
    return f"{dia} de {mes} de {ano}"

# Lista de meses em português para formatação de datas
MESES = {
    1: 'janeiro',
    2: 'fevereiro',
    3: 'março',
    4: 'abril',
    5: 'maio',
    6: 'junho',
    7: 'julho',
    8: 'agosto',
    9: 'setembro',
    10: 'outubro',
    11: 'novembro',
    12: 'dezembro'
}

def formatar_data_personalizada(data):
    """Formata uma data para exibição no diário"""
    try:
        dia = data.day
        mes = MESES[data.month]
        ano = data.year
        return f"{dia} de {mes} de {ano}"
    except (AttributeError, KeyError):
        return formatar_data_atual()
