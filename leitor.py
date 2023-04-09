from pypdf import PdfReader
import os
import re

def buscarnome(texto):
    nome = texto.find('CNPJ:') #Variável chamando "nome", devido a uma especificidade do boleto, para achar o nome, era preciso encontrar o CNPJ 

    if nome:
        parameters = texto[max(0, nome-100):nome].split()
        if len(parameters) >= 4:
            resultadofinal = ' '.join(parameters[-10:])
            replace = re.sub(r'[,\s/]|\(=\s*Valor\s+Cobrado\)|\s*Cobrado|\s*Acréscimos|\(\+\)', '', resultadofinal)
        
        file = open('prontos.txt', 'a')
        file.write(f'\n{replace} ') #Registro em um log
        file.close()

        return replace

pasta = "C:/Users/Daniel Goldoni/Desktop/Python/leitorplan/demo" #Caminho da pasta raiz onde ele fará todas as ações
contador = 0

for caminho, subpastas, arquivos in os.walk(pasta): #É realizado a entrada nos diretórios
    for arquivo in arquivos: #Realizando as ações em todos os arquivos de todos os diretórios da variável "pasta"
        if arquivo.endswith('.pdf'): #Reconhecimento do arquivo pdf
            caminho_completo = os.path.join(caminho, arquivo)
            
            with open(caminho_completo, 'rb') as pdf_file:
                reader = PdfReader(pdf_file) #Leitura do PDF
                number_of_pages = len(reader.pages)
                page = reader.pages[0]
                text = page.extract_text() #Extração de texto do PDF
            
            resultado = buscarnome(text)
            novo_nome = resultado + ".pdf" if resultado else "arquivo_sem_nome.pdf"
            novo_caminho_completo = os.path.join(caminho, novo_nome)
            
            while True:
                try:
                    os.rename(caminho_completo, novo_caminho_completo) #Renomeção do arquivo
                    print(f"Arquivo {arquivo} renomeado para {novo_nome}")
                    break
                except FileExistsError: #Se o arquivo já existir o contador adiciona o numero no final
                    contador += 1
                    novo_nome = resultado + "_" + str(contador) + ".pdf" if resultado else "arquivo_sem_nome_" + str(contador) + ".pdf"
                    novo_caminho_completo = os.path.join(caminho, novo_nome)
        else:
            print('O arquivo não é suportado')


