from io import SEEK_SET
import struct
import os
def main(numeroDivisoes,caminho):
    
    size_file = os.stat(caminho).st_size
    registroCEP = struct.Struct("72s72s72s72s2s8s2s")
    tamanhoDaLinha = registroCEP.size
    numeroDelinhas = size_file // registroCEP.size 
    qtdLinhaPorDivisao = numeroDelinhas // numeroDivisoes 
    versao = 0
    with open(caminho,"rb") as f: #lendo arquivo
        for divisaoAtual in range(1, numeroDivisoes+1):
            listaTemp= []
            f.seek((divisaoAtual-1) * qtdLinhaPorDivisao * tamanhoDaLinha, SEEK_SET) #faz o deslocamento do ponteiro do arquivo para a divisao pertinente
            line = f.readline(tamanhoDaLinha)
            
            i = 1
            while(i <= qtdLinhaPorDivisao) and len(line)>0:
                endereco = registroCEP.unpack(line) #Gera tuplas com base na struct definida
                listaTemp.append(endereco) # adicicona o endereco a lista
                line = f.read(tamanhoDaLinha)
                i += 1
            
            listaTemp.sort(key=lambda e: e[5]) #ordena o arquivo gerado
            with open("parte_ordenada{}_{}.dat".format(versao, divisaoAtual),"wb") as file:
                for endereco in listaTemp: 
                    file.write(registroCEP.pack(*endereco))

