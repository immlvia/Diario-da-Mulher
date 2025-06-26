from app import db
from app.models import Diario
from datetime import datetime

mapeamento_campos = {
    #EMOÇÕES
    'emocoes': {
        'feliz': 'feliz',
        'triste': 'triste',
        'alteracao-humor': 'alteracao_humor',
        'sensivel': 'sensivel',
        'raiva': 'raiva',
        'irritavel': 'irritavel',
        'ansiosa': 'ansiosa',
        'falta-controle': 'falta_controle',
        'indiferenca': 'indiferenca'
    },
    #MENTE
    'mente': {
        'mente-confusa': 'mente_confusa',
        'calma': 'calma',
        'estresse': 'estresse',
        'motivacao': 'motivacao',
        'criatividade': 'criatividade',
        'bom-rendimento': 'bom_rendimento',
        'preguica-desanimo': 'preguica_desanimo'
    },
    #SOCIABILIDADE
    'sociabilidade': {
        'sociavel': 'sociavel',
        'introvertida': 'introvertida',
        'compreensiva': 'compreensiva',
        'amorosa': 'amorosa',
        'conflituosa': 'conflituosa'
    },
    #LAZER
    'lazer': {
        'ferias': 'ferias',
        'encontro': 'encontros',
        'ressaca': 'ressaca',
        'alcool': 'alcool',
        'cigarro': 'cigarro'
    },
    #SINTOMAS FÍSICOS
    'sintomas': {
        'dor-cabeca': 'dor_cabeca',
        'tensao-corporal': 'tensao_corporal',
        'dor-muscular': 'dor_corporal',
        'insonia': 'insonia',
        'queda-cabelo': 'queda_cabelo',
        'taquicardia': 'taquicardia',
        'surto-acne': 'surto_acne',
        'sem-apetite': 'sem_apetite',
        'alergia-dermatite': 'alergia_dermatite',
        'gripe-doenca': 'gripe',
        'alteracoes-hormonais': 'alteracao_hormonal',
        'problema-digestivo': 'problemas_digestivos'
    },
    #AÇÕES DO PARCEIRO
    'conversa': {
        'piadas-ofensivas': 'piadas_ofensivas',
        'chantagear': 'chantagem',
        'mentiras': 'mentira',
        'dar-gelo': 'dar_gelo',
        'ciumes': 'ciumes',
        'culpar': 'culpar',
        'desqualificar': 'desqualificar',
        'palavras-carinhosas': 'palavras_carinho',
        'presentes': 'presentes',
        'humilhar': 'humilhar',
        'xingamentos': 'xingamentos',
        'ameacar': 'ameacar',
        'proibir': 'proibir'
    },
    'comportamentos': {
        'destruir-bens': 'destruir_bens',
        'apertar': 'apertar',
        'brincar-bater': 'brincar_bater',
        'beliscar-arranhar': 'beliscar',
        'empurrar': 'empurrar',
        'bater': 'bater',
        'chutar': 'chutar',
        'confinar-prender': 'confinar',
        'obrigou_relacao_sexual': 'obrigou_relacao_sexual',
        'abuso-sexual': 'abuso_sexual',
        'sufocar-estrangular': 'sufocar'
    },
    'socializacao': {
        'matou-feriu-animal': 'feriu_animal',
        'tentou-se-matou': 'tentou_se_matar',
        'ameacar': 'ameacar',
        'empurrar-outros': 'empurrar_outro',
        'beliscar-arranhar-outros' : 'beliscar_outro',
        'chutar-outros' : 'chutar_outro',
        'bater-outros' : 'bater_outro',
        'apertar-outros' : 'apertar_outro'
    }
}


def registrar_diario(usuario_id, dados_form):
    """
    Registra uma nova entrada no diário com base nos dados do formulário
    Args:
        usuario_id: ID do usuário atual
        dados_form: Dados do formulário do diário
    Returns:
        Objeto Diario salvo
    """
    dia_de_hoje = Diario(usuario_id=usuario_id)

    #PROCESSAMENTO DOS CAMPOS DO FÓRMULARIO
    for categoria, campos in mapeamento_campos.items():
        valores_selecionados = dados_form.getlist(categoria)
        for valor in valores_selecionados:
            if valor in campos:
                setattr(dia_de_hoje, campos[valor], True)
            else:
                print(
                    f"Aviso: Valor '{valor}' na categoria '{categoria}' não encontrado no mapeamento")
        
    #AJUSTE DE "PRESENTES" E "PALAVRAS CARINHOSAS"    
    pontuacao_base_dia = dia_de_hoje.calcular_pontuacao()
    pontuacao_final_dia = pontuacao_base_dia
    historico_diario = Diario.query.filter_by(usuario_id=usuario_id).all()

    if historico_diario:
        soma_historico = sum(entrada.pontuacao_total for entrada in historico_diario if entrada.pontuacao_total is not None)
        total_historico = len(historico_diario)
        media_historico = soma_historico / total_historico if total_historico > 0 else 0
        
        limite_alerta = 80

        if media_historico >= limite_alerta:
            if dia_de_hoje.palavras_carinho:
                pontuacao_final_dia += 10
            if dia_de_hoje.presentes:
                pontuacao_final_dia += 10

    dia_de_hoje.pontuacao_total = pontuacao_final_dia

    #CÁLCULO DA PONTUAÇÃO
    dia_de_hoje.pontuacao_total = dia_de_hoje.calcular_pontuacao()

    # SALVA PONTUAÇÃO NO BANCO DE DADOS
    db.session.add(dia_de_hoje)
    db.session.commit()

    return dia_de_hoje


def obter_historico_diario(usuario_id):
    """
    Obtém o histórico do diário de um usuário
    Args:
        usuario_id: ID do usuário
    Returns:
        Lista de entradas do diário ordenadas por data
    """
    return Diario.query.filter_by(usuario_id=usuario_id).order_by(Diario.data.desc()).all()


def obter_estatisticas_diario(usuario_id):
    """
    Calcula estatísticas do diário de um usuário
    Args:
        usuario_id: ID do usuário
    Returns:
        Dicionário com estatísticas
    """
    entradas = obter_historico_diario(usuario_id)

    if not entradas:
        return {
            'total_entradas': 0,
            'media_pontuacao': 0,
            'emocoes_comuns': [],
            'sintomas_comuns': []
        }

    # Contadores
    emocoes = {}
    sintomas = {}
    total_pontos = 0

    for entrada in entradas:
        total_pontos += entrada.pontuacao_total if entrada.pontuacao_total else 0

        #CONTAGEM DE EMOÇÃO
        for emocao in ['feliz', 'triste', 'alteracao_humor', 'sensivel', 'raiva',
                       'irritavel', 'ansiosa', 'falta_controle', 'indiferenca']:
            if getattr(entrada, emocao):
                emocoes[emocao] = emocoes.get(emocao, 0) + 1

        #CONTAGEM DE SINTOMA
        for sintoma in ['dor_cabeca', 'tensao_corporal', 'dor_corporal', 'insonia',
                        'queda_cabelo', 'taquicardia', 'surto_acne', 'sem_apetite',
                        'alergia_dermatite', 'gripe', 'alteracao_hormonal', 'problemas_digestivos']:
            if getattr(entrada, sintoma):
                sintomas[sintoma] = sintomas.get(sintoma, 0) + 1

    #ORDENAR POR FREQUÊNCIA
    emocoes_ordenadas = sorted(
        emocoes.items(), key=lambda x: x[1], reverse=True)
    sintomas_ordenados = sorted(
        sintomas.items(), key=lambda x: x[1], reverse=True)

    return {
        'total_entradas': len(entradas),
        'media_pontuacao': total_pontos / len(entradas) if entradas else 0,
        'emocoes_comuns': [{'nome': nome.replace('_', ' ').title(), 'contagem': contagem}
                           for nome, contagem in emocoes_ordenadas[:5]],
        'sintomas_comuns': [{'nome': nome.replace('_', ' ').title(), 'contagem': contagem}
                            for nome, contagem in sintomas_ordenados[:5]]
    }
