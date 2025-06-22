#!/usr/bin/env python3

"""
Script para consultar registros do diário no banco de dados
Uso: python development_tools/consultar_diario.py
"""

import sys
import os
# Adiciona o diretório raiz ao path para poder importar o app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Usuario, Diario
from app.utils import formatar_data_personalizada

def consultar_diarios():
    """
    Consulta e exibe todos os registros de diário no banco de dados
    """
    with app.app_context():
        # Consulta todos os diários
        diarios = Diario.query.all()
        
        if not diarios:
            print("\n🔍 Nenhum registro de diário encontrado no banco de dados.")
            return
        
        print(f"\n🔍 Encontrados {len(diarios)} registros de diário:")
        
        # Exibe informações de cada diário
        for diario in diarios:
            usuario = Usuario.query.filter_by(id=diario.usuario_id).first()
            usuario_nome = usuario.nome if usuario else "Usuário não encontrado"
            
            print("\n" + "="*50)
            print(f"ID: {diario.id}")
            print(f"Usuário: {usuario_nome} (ID: {diario.usuario_id})")
            
            data_formatada = formatar_data_personalizada(diario.data) if diario.data else "Data não disponível"
            print(f"Data: {data_formatada}")
            
            print(f"Pontuação Total: {diario.pontuacao_total}")
            
            # Exibe emoções selecionadas
            emocoes = []
            if diario.feliz: emocoes.append("Feliz")
            if diario.triste: emocoes.append("Triste")
            if diario.alteracao_humor: emocoes.append("Alteração de humor")
            if diario.sensivel: emocoes.append("Sensível")
            if diario.raiva: emocoes.append("Raiva")
            if diario.irritavel: emocoes.append("Irritável")
            if diario.ansiosa: emocoes.append("Ansiosa")
            if diario.falta_controle: emocoes.append("Falta de controle")
            if diario.indiferenca: emocoes.append("Indiferença")
            
            print(f"Emoções: {', '.join(emocoes) if emocoes else 'Nenhuma emoção registrada'}")
            
            # Exibe estado mental selecionado
            mente = []
            if diario.mente_confusa: mente.append("Mente confusa")
            if diario.calma: mente.append("Calma")
            if diario.estresse: mente.append("Estresse")
            if diario.motivacao: mente.append("Motivação")
            if diario.criatividade: mente.append("Criatividade")
            if diario.bom_rendimento: mente.append("Bom rendimento")
            if diario.preguica_desanimo: mente.append("Preguiça ou desânimo")
            
            print(f"Estado Mental: {', '.join(mente) if mente else 'Nenhum estado mental registrado'}")

def consultar_por_usuario(usuario_id):
    """
    Consulta e exibe os registros de diário de um usuário específico
    """
    with app.app_context():
        usuario = Usuario.query.filter_by(id=usuario_id).first()
        
        if not usuario:
            print(f"\n❌ Usuário com ID {usuario_id} não encontrado.")
            return
        
        diarios = Diario.query.filter_by(usuario_id=usuario_id).all()
        
        if not diarios:
            print(f"\n🔍 Nenhum registro de diário encontrado para o usuário {usuario.nome}.")
            return
        
        print(f"\n🔍 Encontrados {len(diarios)} registros de diário para o usuário {usuario.nome}:")
        
        for diario in diarios:
            print("\n" + "-"*40)
            data_formatada = formatar_data_personalizada(diario.data) if diario.data else "Data não disponível"
            print(f"Data: {data_formatada}")
            print(f"Pontuação: {diario.pontuacao_total}")

if __name__ == "__main__":
    # Consulta todos os diários
    consultar_diarios()
    
    # Você pode descomentar esta linha e modificar o ID do usuário para consultar diários de um usuário específico
    # consultar_por_usuario(1)  # Substitua 1 pelo ID do usuário desejado

consultar_diarios()
