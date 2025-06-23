from app import db
from app.models import Diario
from datetime import datetime

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
    
    # Mapeamento de campos do formulário para atributos do modelo
    mapeamento_campos = {
        # Emoções
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
        # Mente
        'mente': {
            'mente-confusa': 'mente_confusa',
            'calma': 'calma',
            'estresse': 'estresse',
            'motivacao': 'motivacao',
            'criatividade': 'criatividade',
            'bom-rendimento': 'bom_rendimento',
            'preguica-desanimo': 'preguica_desanimo'
        },
        # Sociabilidade
        'sociabilidade': {
            'sociavel': 'sociavel',
            'introvertida': 'introvertida',
            'compreensiva': 'compreensiva',
            'amorosa': 'amorosa',
            'conflituosa': 'conflituosa'
        },
        # Lazer
        'lazer': {
            'ferias': 'ferias',
            'encontros': 'encontros',
            'ressaca': 'ressaca',
            'alcool': 'alcool',
            'cigarro': 'cigarro'
        },
        # Sintomas físicos
        'sintomas': {
            'dor-cabeca': 'dor_cabeca',
            'tensao-corporal': 'tensao_corporal',
            'dor-corporal': 'dor_corporal',
            'insonia': 'insonia',
            'queda-cabelo': 'queda_cabelo',
            'taquicardia': 'taquicardia',
            'surto-acne': 'surto_acne',
            'sem-apetite': 'sem_apetite',
            'alergia-dermatite': 'alergia_dermatite',
            'gripe': 'gripe',
            'alteracao-hormonal': 'alteracao_hormonal',
            'problemas-digestivos': 'problemas_digestivos'
        },
        # Ações do parceiro
        'parceiro': {
            'piadas-ofensivas': 'piadas_ofensivas',
            'chantagem': 'chantagem',
            'mentira': 'mentira',
            'dar-gelo': 'dar_gelo',
            'ciumes': 'ciumes',
            'culpar': 'culpar',
            'desqualificar': 'desqualificar',
            'palavras-carinho': 'palavras_carinho',
            'humilhar': 'humilhar',
            'xingamentos': 'xingamentos',
            'ameacar': 'ameacar',
            'proibir': 'proibir',
            'destruir-bens': 'destruir_bens',
            'apertar': 'apertar',
            'brincar-bater': 'brincar_bater',
            'beliscar': 'beliscar',
            'empurrar': 'empurrar',
            'bater': 'bater',
            'chutar': 'chutar',
            'confinar': 'confinar',
            'ameacar-objetos': 'ameacar_objetos',
            'ameacar-armas': 'ameacar_armas',
            'ameacar-morte': 'ameacar_morte',
            'obrigou-relacao-sexual': 'obrigou_relacao_sexual',
            'abuso-sexual': 'abuso_sexual',
            'sufocar': 'sufocar',
            'feriu-animal': 'feriu_animal',
            'tentou-se-matar': 'tentou_se_matar'
        }
    }
    
    # Processamento dos campos do formulário
    for categoria, campos in mapeamento_campos.items():
        valores_selecionados = dados_form.getlist(categoria)
        for valor in valores_selecionados:
            if valor in campos:
                setattr(dia_de_hoje, campos[valor], True)
    
    # Cálculo da pontuação
    dia_de_hoje.pontuacao_total = dia_de_hoje.calcular_pontuacao()
    
    # Salva no banco de dados
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
        
        # Contagem de emoções
        for emocao in ['feliz', 'triste', 'alteracao_humor', 'sensivel', 'raiva', 
                        'irritavel', 'ansiosa', 'falta_controle', 'indiferenca']:
            if getattr(entrada, emocao):
                emocoes[emocao] = emocoes.get(emocao, 0) + 1
        
        # Contagem de sintomas
        for sintoma in ['dor_cabeca', 'tensao_corporal', 'dor_corporal', 'insonia', 
                         'queda_cabelo', 'taquicardia', 'surto_acne', 'sem_apetite', 
                         'alergia_dermatite', 'gripe', 'alteracao_hormonal', 'problemas_digestivos']:
            if getattr(entrada, sintoma):
                sintomas[sintoma] = sintomas.get(sintoma, 0) + 1
    
    # Ordenar por frequência
    emocoes_ordenadas = sorted(emocoes.items(), key=lambda x: x[1], reverse=True)
    sintomas_ordenados = sorted(sintomas.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'total_entradas': len(entradas),
        'media_pontuacao': total_pontos / len(entradas) if entradas else 0,
        'emocoes_comuns': [{'nome': nome.replace('_', ' ').title(), 'contagem': contagem} 
                            for nome, contagem in emocoes_ordenadas[:5]],
        'sintomas_comuns': [{'nome': nome.replace('_', ' ').title(), 'contagem': contagem} 
                             for nome, contagem in sintomas_ordenados[:5]]
    }
