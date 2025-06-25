from app.diario_service import obter_estatisticas_diario
from app.models import Diario


def calcular_dados_ciclo(usuario_id):

    entradas_diario = Diario.query.filter_by(usuario_id=usuario_id).all()
    if not entradas_diario:
            return 0

    # 2. Soma a pontuação de todas as entradas
    soma_total_pontos = 0
    for entrada in entradas_diario:
        if entrada.pontuacao_total is not None:
            soma_total_pontos += entrada.pontuacao_total

    # 3. Calcula a média de pontos por entrada
    total_de_entradas = len(entradas_diario)
    media_pontos = soma_total_pontos / total_de_entradas

    # 4. Converte a média para uma porcentagem (onde 160 é o máximo, ou seja, 100%)
    porcentagem = (media_pontos / 160.0) * 100

    # Garante que a porcentagem não passe de 100
    if porcentagem > 100:
        porcentagem = 100
    # Garante que a porcentagem não seja negativa
    if porcentagem < 0:
        porcentagem = 0

    return int(porcentagem)