from fileinput import filename
import whats_reader
from utils import find_pattern,multisplit

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
    message_list = whats_reader.get_messages(whats, grupo_fichas,10)
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
        #Divide os campos
        ficha_list = ficha.split("•")
        
        #Tira o header da ficha
        ficha_list.pop(0)
        
        #Cria  e popula o dicionário com as informações da ficha
        ficha_dict = {}
        
        #Para cada campo na lista...
        for f in ficha_list:
                #Divide cada campo
                f = f.split(":")
                
                #Limpa as keys
                f[0] = f[0].strip()
                f[0] =  f[0].replace("\n","")
                
                #Nao adiciona se não for par
                if len(f) < 2:          
                        print(f[0])
                        continue
                
                #Processa os campos
                if f[0] == 'Itens':
                        f[1] = f[1].replace("não inclui relíquias","")
                        f[1] = f[1].split("\n")
                        if isinstance(f[1],list):
                                f[1] = [i for i in f[1] if i != "" and i != " -"]
                elif f[0] == 'Habilidades' or f[0] == 'Magias':
                        f[1] = f[1].split("\n")
                        if isinstance(f[1],list):
                                f[1] = [i for i in f[1] if i != ""]
                else:
                        #Limpa os pulos de linha
                        f[1] =  f[1].replace("\n","")
                        #Limpa o value
                        f[1] = f[1].strip()
                
                if f[0] == 'Sanidade':
                        f[1] = f[1].replace("Campos Especiais Deixar em branco no início.","")
                elif f[0] == 'Fama':
                        f[1] = f[1].replace(" Campos Adicionais          Obrigatório!","")
                
                
                #Adiciona ao dicionário
                ficha_dict[f[0]] = f[1]
                
        return ficha_dict

#TODO: Aperfeiçoar leitura de habilidades e magias; Adicionar comentários
def process_ficha_with_lists(ficha : str) -> dict:
        special_chars = ["•","_"]
        messages_to_rmv = ["não inclui relíquias","Deixar em branco no início.","Obrigatório!","Campos Especiais","Campos Adicionais"]
        
        #Divide os campos
        ficha_list = ficha.split("\n")
        
        for i in range(6):
                ficha_list.pop(0)
        
        add_itens = False
        add_hab = False
        add_mag = False
        add_tit = False
        

        tits = ['Títulos']
        
        ficha_dict = {}
        
        for f in ficha_list:

                for c in special_chars:
                        f = f.replace(c,"")
                
                f = f.strip()
                        
                if f == '' or f in messages_to_rmv:
                        continue
                   
                f = f.split(":")
                
                if f[0] == "Itens":
                        add_itens = True
                        ficha_dict["Itens"] = []
                        continue
                elif f[0] == "Nível":
                        add_itens = False
                elif f[0] == "Habilidades":
                        add_hab = True
                        ficha_dict['Habilidades'] = []
                        continue             
                elif f[0] == "Magias":
                        add_hab = False
                        add_mag = True
                        ficha_dict["Magias"] = []
                        continue
                elif f[0] == "G$":
                        add_mag = False
                elif f[0] == "Títulos":
                        add_tit = True
                        ficha_dict["Títulos"] = []
                        continue
                elif f[0] == 'Profissão':
                        add_tit = False
                
                if add_itens or add_hab or add_mag or add_tit:
                        for h in f:                              
                                if add_itens:
                                        ficha_dict["Itens"].append(h)
                                elif add_hab:
                                        ficha_dict['Habilidades'].append(h)
                                elif add_mag:
                                        ficha_dict["Magias"].append(h)
                                elif add_tit:
                                        ficha_dict["Títulos"].append(h)
                        continue
                
                
                if len(f) > 1:
                        if len(f) > 2:
                                ficha_dict[f[0]] = [i for i in f[1:] if i != ""]
                        else:               
                                ficha_dict[f[0]] = f[1]
        
        return ficha_dict

#Recebe a ficha como string, uma string com o nome da lista que deve ser processada, e aonde essa lista precisa terminar   
def process_list_of_habs(ficha : str,to_find : str, ending : str) -> list:
        ind = find_pattern(to_find, ficha)[0]
        m_ind = find_pattern(ending, ficha)[0]
                
        if(ind < 0):
                return ["Error"]
        n_index = ind + len(to_find) - 1
        all_habs = ficha[n_index]
        l = ""
        
        if m_ind > 0:
                while n_index < m_ind:
                        all_habs += l
                        n_index += 1
                        l = ficha[n_index]
        else:
                while l != "•":
                        all_habs += l
                        n_index += 1
                        l = ficha[n_index]

        full_hab = multisplit('\n'," ",":",'\r',",", txt=all_habs)
        for h in range(len(full_hab)):
                if type(full_hab[h]) == str:
                        full_hab[h] = full_hab[h].replace("•","").replace("\\n","").replace("\\r","").replace("[","").replace("]","").replace("(","").replace(")","")
        full_hab = list(filter(None,full_hab))
                        
        return full_hab

#Abre documento com fichas de exemplo (Pra não precisar abrir o Selenium toda hora)
def fichas_sample() -> list:
        f_list = []
        with open("fichas_example.txt", "rb") as file:
                f_text = file.read().decode("utf-8",'replace')
                f_list = str(f_text).split("-----------------------------------------------------------------------------------------------")
        return f_list

if __name__ == "__main__":
        f_list = fichas_sample()
        for i in range(len(f_list)):
                h_list = process_list_of_habs(f_list[i],"Habilidades:","Magias:")
                print("Habilidades:")
                print(h_list)
                m_list = process_list_of_habs(f_list[i],"Magias:","G$:")
                print("Magias:")
                print(m_list)
                print("\n \n---------------------------- \n")
        