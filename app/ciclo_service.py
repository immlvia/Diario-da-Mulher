from app.diario_service import obter_estatisticas_diario
from app.models import Diario


def calcular_dados_ciclo(usuario_id):

    entradas_diario = Diario.query.filter_by(usuario_id=usuario_id).all()
    if not entradas_diario:
            return 0

    #SOMA PONTUAÇÃO DAS ENTRADAS E CALCULA A MEDIA (ENTRADAS) DO USUARIO
    soma_total_pontos = 0
    for entrada in entradas_diario:
        if entrada.pontuacao_total is not None:
            soma_total_pontos += entrada.pontuacao_total

    total_de_entradas = len(entradas_diario)
    media_pontos = soma_total_pontos / total_de_entradas
    porcentagem = (media_pontos / 200.0) * 100

    #PORCENTAGEM NÃO PASSAR DE 100 NEM SER NEGATIVO
    if porcentagem > 100:
        porcentagem = 100
    if porcentagem < 0:
        porcentagem = 0

    return int(porcentagem)