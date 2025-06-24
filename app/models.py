from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(usuario_id)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    data_inicio = db.Column(db.DateTime, default=datetime.now)
    diarios = db.relationship('Diario', backref='usuario', lazy=True)

class Diario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data = db.Column(db.DateTime, default=datetime.now)

    #Emoções - Como me senti hoje
    feliz = db.Column(db.Boolean, default=False)
    triste = db.Column(db.Boolean, default=False)
    alteracao_humor = db.Column(db.Boolean, default=False) #sem pontuação
    sensivel = db.Column(db.Boolean, default=False)
    raiva = db.Column(db.Boolean, default=False)
    irritavel = db.Column(db.Boolean, default=False)
    ansiosa = db.Column(db.Boolean, default=False)
    falta_controle = db.Column(db.Boolean, default=False) #sem pontuação
    indiferenca = db.Column(db.Boolean, default=False) #sem pontuação

    #Mente - Como minha mente estava hoje?
    mente_confusa = db.Column(db.Boolean, default=False) #sem pontuação
    calma = db.Column(db.Boolean, default=False) #sem pontuação
    estresse = db.Column(db.Boolean, default=False)
    motivacao = db.Column(db.Boolean, default=False)
    criatividade = db.Column(db.Boolean, default=False) #sem pontuação
    bom_rendimento = db.Column(db.Boolean, default=False)
    preguica_desanimo = db.Column(db.Boolean, default=False) #sem pontuação

    #Sociabilidade
    sociavel = db.Column(db.Boolean, default=False) #sem pontuação
    introvertida = db.Column(db.Boolean, default=False) #sem pontuação  
    compreensiva = db.Column(db.Boolean, default=False) #sem pontuação
    amorosa = db.Column(db.Boolean, default=False) #sem pontuação
    conflituosa = db.Column(db.Boolean, default=False) #sem pontuação

    #lazer
    ferias = db.Column(db.Boolean, default=False) #sem pontuação  
    encontros = db.Column(db.Boolean, default=False) #sem pontuação
    ressaca = db.Column(db.Boolean, default=False) #sem pontuação
    alcool = db.Column(db.Boolean, default=False) #sem pontuação
    cigarro = db.Column(db.Boolean, default=False) #sem pontuação

    # Sintomas físicos
    dor_cabeca = db.Column(db.Boolean, default=False)
    tensao_corporal = db.Column(db.Boolean, default=False)
    dor_corporal = db.Column(db.Boolean, default=False)
    insonia = db.Column(db.Boolean, default=False)
    queda_cabelo = db.Column(db.Boolean, default=False)
    taquicardia = db.Column(db.Boolean, default=False)
    #sintomas fisicos sem pontuação:
    surto_acne = db.Column(db.Boolean, default=False) #sem pontuação  
    sem_apetite = db.Column(db.Boolean, default=False) #sem pontuação
    alergia_dermatite = db.Column(db.Boolean, default=False) #sem pontuação
    gripe = db.Column(db.Boolean, default=False) #sem pontuação
    alteracao_hormonal = db.Column(db.Boolean, default=False) #sem pontuação
    problemas_digestivos = db.Column(db.Boolean, default=False) #sem pontuação

    # Ações do parceiro
    piadas_ofensivas = db.Column(db.Boolean, default=False)
    chantagem = db.Column(db.Boolean, default=False)
    mentira = db.Column(db.Boolean, default=False)
    dar_gelo = db.Column(db.Boolean, default=False)
    ciumes = db.Column(db.Boolean, default=False)
    culpar = db.Column(db.Boolean, default=False)
    desqualificar = db.Column(db.Boolean, default=False)
    palavras_carinho = db.Column(db.Boolean, default=False)
    humilhar = db.Column(db.Boolean, default=False)
    xingamentos = db.Column(db.Boolean, default=False)
    ameacar = db.Column(db.Boolean, default=False)
    proibir = db.Column(db.Boolean, default=False)
    destruir_bens = db.Column(db.Boolean, default=False)
    apertar = db.Column(db.Boolean, default=False)
    brincar_bater = db.Column(db.Boolean, default=False)
    beliscar = db.Column(db.Boolean, default=False)
    empurrar = db.Column(db.Boolean, default=False)
    bater = db.Column(db.Boolean, default=False)
    chutar = db.Column(db.Boolean, default=False)
    confinar = db.Column(db.Boolean, default=False)
    ameacar_objetos = db.Column(db.Boolean, default=False)
    ameacar_armas = db.Column(db.Boolean, default=False)
    ameacar_morte = db.Column(db.Boolean, default=False)
    obrigou_relacao_sexual = db.Column(db.Boolean, default=False)
    abuso_sexual = db.Column(db.Boolean, default=False)
    sufocar = db.Column(db.Boolean, default=False)
    feriu_animal = db.Column(db.Boolean, default=False)
    tentou_se_matar = db.Column(db.Boolean, default=False)

    pontuacao_total = db.Column(db.Integer)

    def validar_emoções(self):
        #Para que não seja selecionado emoções opostas (Ele vai tirar a selenção das emoções conflitantes com "feliz") Arrumar depois
        if self.feliz:
            self.triste = False
            self.irritavel = False
            self.raiva = False
            self.indiferenca = False
            
    def calcular_pontuacao(self):
        
        self.validar_emoções()
        total = 0
        
        # Sintomas emocionais
        if self.feliz: total -= 2
        if self.triste: total += 2
        if self.alteracao_humor: total += 0 #sem pontuação
        if self.sensivel: total += 1
        if self.raiva: total += 1
        if self.irritavel: total += 1
        if self.ansiosa: total += 2
        if self.falta_controle: total += 0  #sem pontuação
        if self.indiferenca: total += 0  #sem pontuação
        if self.estresse: total += 1
        if self.motivacao: total -= 1
        if self.bom_rendimento: total -= 1
        if self.preguica_desanimo: total += 0 #sem pontuação
        
        #Lazer (SEM PONTUAÇÃO)
        if self.ferias: total += 0 #sem pontuação
        if self.encontros: total += 0 #sem pontuação
        if self.ressaca: total +=0 #sem pontuação
        if self.alcool: total += 0 #sem pontuação
        if self.cigarro: total += 0 #sem pontuação

        # Sintomas físicos
        if self.dor_cabeca: total += 2
        if self.tensao_corporal and not self.gripe: total += 2
        if self.dor_corporal and not self.gripe: total += 2
        if self.insonia: total += 1
        if self.queda_cabelo: total += 1
        if self.taquicardia: total += 1
        #sintomas fisicos sem pontuação
        if self.surto_acne: total += 0 #sem pontuação
        if self.sem_apetite: total += 0 #sem pontuação
        if self.alergia_dermatite: total += 0 #sem pontuação
        if self.gripe: total += 0 #sem pontuação
        if self.alteracao_hormonal: total += 0 #sem pontuação
        if self.problemas_digestivos: total += 0 #sem pontuação
        
        # Ações do parceiro
        if self.palavras_carinho: total -= 5
        if self.piadas_ofensivas: total += 10
        if self.chantagem: total += 15
        if self.mentira: total += 10
        if self.dar_gelo: total += 25
        if self.ciumes: total += 30
        if self.culpar: total += 35
        if self.desqualificar: total += 40
        if self.humilhar: total +=45
        if self.xingamentos: total += 45
        if self.ameacar: total += 50
        if self.proibir: total += 55
        if self.destruir_bens: total +=60
        if self.apertar: total += 70
        if self.brincar_bater: total += 75
        if self.beliscar: total += 80
        if self.empurrar: total += 85
        if self.bater: total += 90
        if self.chutar: total += 95
        if self.confinar: total += 100
        if self.ameacar_objetos: total += 105
        if self.ameacar_armas: total += 110
        if self.ameacar_morte: total += 115
        if self.obrigou_relacao_sexual: total += 120
        if self.abuso_sexual: total += 125
        if self.sufocar: total += 130
        if self.feriu_animal: total +=60
        if self.tentou_se_matar: total += 60
        
        self.pontuacao_total = total
        
        return total

#Fazer código para que emoções opostas não possam ser escolhidas mais tarde