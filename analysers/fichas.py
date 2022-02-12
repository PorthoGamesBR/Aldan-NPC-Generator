import whats_reader

ficha_head = """ A L I A N Ç A 
 Ficha.
Versão 5.0"""

ficha_vazia = """ A L I A N Ç A 
 Ficha.
Versão 5.0

Campos Obrigatórios

•Nome: 
•Idade: 
•Raça: 
•Classe: 
•Sexo: 
•Itens: 
não inclui relíquias
•Nível: 0 
•Habilidades:

•Magias:

•G$: 20.000
•XP: 0
•Hp/Mp: 
•Sanidade: 100/100

Campos Especiais ⚜
Deixar em branco no início.

•Guilda: 
•Mestre:
•Aprendiz: 
•Técnicas: 
•Títulos: 

•Iniciante 

 •Profissão:
 •Casta especial
 •Relíquia:
 •Habilidades Únicas:
 •Imóveis: 
 •Fama: 0

Campos Adicionais 
        Obrigatório!

•História: 
•Personalidade:
•Objetivos: 
•Traumas: 
•Altura: mínimo 50 cm. Máximo 5m 
•Peso:"""

grupo_fichas = "⚜️Aliança : Grupo Fichas 🔰"

def get_fichas() -> list:
    #Começa o cliente do Whatsapp
    whats = whats_reader.Whatsapp()

    #Pega a lista de mensagens do grupo de fichas
    message_list = whats_reader.get_messages(whats, grupo_fichas)
    ficha_list = []

    #Processa todas as mensagens
    for msg in message_list:
        d_msg = msg.decode('utf8')
        
        #Vê se são fichas de jogadores e exclui as vazias
        if ficha_head in d_msg and d_msg != ficha_vazia:
                ficha_list.append(d_msg)
    #Fecha o cliente do whatsapp
    whats.close()
    
    return ficha_list
        
def process_ficha(ficha : str) -> dict:
        ficha =  ficha.replace("\n","")
        ficha_list = ficha.split("•")
        ficha_list.pop(0)
        ficha_dict = {}
        for f in ficha_list:
                f = f.split(":")
                f[0] = f[0].strip()
                if len(f) < 2:
                        print(f[0])
                        continue
                f[1] = f[1].strip()
                ficha_dict[f[0]] = f[1]
        print(ficha_dict)
        
f_list = get_fichas()
process_ficha(f_list[0])