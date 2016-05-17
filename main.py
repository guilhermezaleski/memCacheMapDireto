# coding=UTF-8
import sys

#-------------Definicoes---------
# Define tamanho de endereçamento da memória cache

tamEndereco = 32
tamByte = 2
tamOffSet = 2
tamIndex = 4
tamTag = 24
#--------------------------------

# funcao para impressao do HELP
def help():
    print('\n\n'
          "python main.py  [\caminho arquivo txt] [-p]\n\n"
          "[-p]                      Executa passo a passo\n"
          "[\caminho arquivo txt]    Informe o caminho completo onde se encontra o arquivo "
          "                          txt com enderecos\n"
          "                          Ex: c:\proj\endr.txt\n"
          "\n"
          "                          Obs: o arquivo de conter apenas os enderecos de 32bits"
          "                          em hexadecimal\n\n")
    sys.exit(1)

#função para abertura de arquivo
def abrirArquivo():
    try:

        #param2 recebe caminho do arquivo a ser aberto
        param2 = param[1]

    except Exception:

        print('\n   --Erro, informe o caminho do arquivo\n')
        sys.exit(1)

    try:

        #somente no modo leitura em codificação utf8
        arq = open(param[1], 'r', encoding="utf8")

    except Exception:
        print('\n   --Erro, não foi possivel abrir o arquivo\n')
        sys.exit(1)

    # retorna arquivo
    return arq

#funcao para fechar o arquivo
def fecharArquivo(arqvTxt):

    arqvTxt.close()

#função ler conteudo do arquivo
def lerArquivo(arqv):
    txt = []
    try:
        for linha in arqv.readlines(): #le cada linha do arquivo
            aux = linha.replace('\n','') #exclui enter
            txt.append(aux) #sequencia as linhas

    except Exception:
        print('\n   --Erro, não foi possivel ler o arquivo\n')
        sys.exit(1)

    return txt

#função de print da estrutura visual e conteudo da cache
def tabelaCache(cache, valiCache, tamTag, tamIndex, tamOffSet, hit, miss):

    idx = len(cache) #retorna qtde de linhas do cache

    print('\n'
        '| Idx | V | Tag      |    data    |    data    |    data    |    data    |\n'
        '-------------------------------------------------------------------------')

    for x in range(idx): #realiza for conforme linhas da cache

        endrCache = cache[x]
        linha = hex(x)

        if valiCache[x] == 1: #verifica o bit de validade
            tag = testaTamEndr(hex(int(endrCache[0:tamTag], 2)), int(tamTag/4)) #extrair tag do endereco
            tamWrdHex = int((tamTag + tamIndex + tamOffSet)/4) #armazena o tamanho da palavra
            word = testaTamEndr(hex(int(endrCache, 2)),tamWrdHex) #extrair word do endereço

            print( '|',linha,'|',valiCache[x],'|',
                    tag,'|',
                    word[0:tamWrdHex+2]+'X','|',
                    word[0:tamWrdHex+2]+'X','|',
                    word[0:tamWrdHex+2]+'X','|',
                    word[0:tamWrdHex+2]+'X','|')
        else:
            print('|', linha, '|', valiCache[x], '|')
    print('--------------------------------------------------------------------------')
    print('hit:', hit, '  miss:', miss)

#busca tag do endereco lido do arquivo
def buscaTag(endrBin, tamTag):

    tag = endrBin[2:tamTag+2]

    return tag

#busca index do endereco lido do arquivo
def buscaIdx(endrBin, tamTag, tamIndex):

    idx = endrBin[tamTag + 2:tamIndex + tamTag + 2]

    return idx

#busca offset do endereco lido do arquivo
def buscaOffset(endrBin, tamTag, tamIndex, tamOffSet):

    offset = endrBin[tamTag + tamIndex + 2:tamTag + tamIndex + tamOffSet + 2]

    return offset

#busca byte do endereco lido do arquivo
def buscaByte(endrBin,tamTag, tamIndex, tamOffSet, tamByte):

    byte = endrBin[tamTag + tamIndex + tamOffSet + 2:tamTag + tamIndex + tamOffSet + tamByte + 2]

    return byte

#testa e complementa a quantidade de bits pedidos
def testaTamEndr(endr, tamEndereco):

    tam = len(endr) - 2
    aux = ''

    if not tamEndereco == tam:
        comp = tamEndereco - tam #diferença do tamanho requisitado
        for x in range(comp):
            aux = aux + '0'
        endr = endr[0:2] + str(aux) + endr[2:] #concatena os zeros com o endereço informado

    return endr





#####################################################################
#-------------------------------MAIN---------------------------------
#####################################################################


#-------------busca e tratamento de argumentos

param = sys.argv  #atribuicao dos parametro

cont = len(param)
passo = False #controle para execucao do passo a passo

#testa se o segundo argumento passado e valido
if cont == 3:
    if not param[2] == '-p':
        print('\n   --Erro, argumentos não conhecidos\n')
        help()
    elif param[2] == '-p':
        passo = True

#testa se os argumentos sao validos, se nao chama o help
if cont == 2:
    try:
        if param[1] == '/?' or param[1] == 'help':
            print('\n   --Erro, argumentos não conhecidos\n')
            help()
    except:
        if not param[1] == '/?' or param[1] == 'help':
            print('\n   --Erro, argumentos não conhecidos\n')
            help()

#-------------------------------------------------------

arqvTxt = abrirArquivo() #chama funcao para abrir
enderecosHexa = lerArquivo(arqvTxt) #retorna o conteudo do arquivo, cada linha em uma posicao da lista
fecharArquivo(arqvTxt) #fecha o arquivo


cache = [0 for x in range(2**tamIndex)] #inicializa a lista Cache com zeros de acordo com o tamanho de index
valiCache = [0 for x in range(2**tamIndex)] #inicializa a lista do Bit de validade com zeros de
                                            # acordo com o tamanho de index
hit = 0
miss = 0

for endr in enderecosHexa: #a cada loop recebe um endereco para trabalhar

    endrBin = bin(int(endr, 16)) #converte de hexadecimal para binario
    endrBin = testaTamEndr(endrBin, tamEndereco)#complementa o tamanho do by

    try:
        tag =    buscaTag    (endrBin, tamTag) #busca a tag
        idx =    buscaIdx    (endrBin, tamTag, tamIndex) #busca o index
        offset = buscaOffset (endrBin, tamTag, tamIndex, tamOffSet) #busca o offset
        byte =   buscaByte   (endrBin, tamTag, tamIndex, tamOffSet, tamByte) #busca o byte
    except Exception:
        print('-Erro, endereço inválido', endr)
        continue

    #verifica se o bit de validade na posicao é valido(1) ou nao(0)
    if valiCache[int(idx,2)] == 0:

        miss += 1 #contador de miss
        valiCache[int(idx, 2)] = 1 #muda a o bit para valido
        cache[int(idx, 2)] = tag + idx + offset + byte #grava na posicao

    elif valiCache[int(idx,2)] == 1:
        endrCache = cache[int(idx, 2)]

        #verifica de a tag eh igual a solicitada
        if tag == endrCache[0:tamTag]:
            hit += 1 #contador de hit
        else:
            miss += 1
            cache[int(idx, 2)] = tag + idx + offset + byte

    # verifica se ira imprimir a tabela a cada leitura de endereco
    if passo == True:
        print('\n\nLeitura do endereço:', endr)
        tabelaCache(cache, valiCache, tamTag, tamIndex, tamOffSet, hit, miss) #imprime a tabela cache
        input()

#imprime a tabela cache ao final da execucao, se não imprimir passo a passo
if not passo == True:
    tabelaCache(cache, valiCache, tamTag, tamIndex, tamOffSet, hit, miss)


#fim do codigo