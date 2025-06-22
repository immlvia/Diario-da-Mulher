# Ferramentas de Desenvolvimento

Esta pasta contém ferramentas úteis para o desenvolvimento e manutenção do projeto Diário da Mulher.

## Scripts Disponíveis

### consultar_diario.py
Script para consultar registros do diário no banco de dados.

**Uso:**
```bash
python development_tools/consultar_diario.py
```

**Funcionalidades:**
- Lista todos os registros de diário existentes no banco de dados
- Exibe detalhes completos de cada registro, incluindo:
  - ID do registro
  - Nome e ID do usuário
  - Data do registro
  - Pontuação total
  - Emoções selecionadas
  - Estado mental registrado

**Opções adicionais:**
Para consultar diários de um usuário específico, edite o script e descomente a linha:
```python
# consultar_por_usuario(1)  # Substitua 1 pelo ID do usuário desejado
```
