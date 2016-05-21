# coding=UTF-8

'''
   Simulação de acesso a memória cache com mapeamento direto.

   Desenvolvido em python3.5.1, por Guilherme Zaleski e Tcharles Clunk

'''


import sys

'''-------------Definicoes---------'''
# Define tamanho de endereçamento da memória cache
class defCache(object):
    tamEndereco = 32
    tamByte = 2
    tamOffSet = 2
    tamIndex = 4
    tamTag = 24

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

#função para abertura de arquivo, com tratamento de erros na abertura
# recece como parametros os argumentos e retrorna o arquivo
def abrirArquivo(param):
    try:

        #param2 recebe caminho do arquivo a ser aberto
        param2 = param[1]

    except Exception:

        print('\n   --Erro, informe o caminho do arquivo\n')
        sys.exit(1)

    try:

        #Abre  o arquivo em modo de leitura em codificacao utf8
        arq = open(param[1], 'r', encoding="utf8")

    except Exception:
        print('\n   --Erro, não foi possivel abrir o arquivo\n')
        sys.exit(1)

    # retorna arquivo
    return arq

#funcao para fechar o arquivo
def fecharArquivo(arqvTxt):

    arqvTxt.close()

#função ler conteudo do arquivo, com tratamento de erros na leitura do arquivo
#recebe o arquivo para ser lido e retorna uma lista com os endereços
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
#recebe como argumento as listas cache e valichache, os tamanhos  e hit miss
def tabelaCache(cache, valiCache, defCache, hit, miss):

    tamWrdHex = int((defCache.tamTag + defCache.tamIndex + defCache.tamOffSet )/4) #armazena o tamanho da palavra
    tamTag = ' '
    tamWrdHexAux = ' '
    traco = '='
    qntBlocos = ''

    #Configura o espaco da tag no cabecalho para imprimir
    for y in range(int(defCache.tamTag/4)-4):
        tamTag = tamTag + ' '

    #Configura o espaco da palavra no cabecalho para imprimir
    for y in range(tamWrdHex-2):
        tamWrdHexAux = tamWrdHexAux + ' '

    #Configura e adiciona no cabecalho o espaco e a palavra Data
    for y in range(2**defCache.tamOffSet):
        qntBlocos = qntBlocos + ' | Data' + tamWrdHexAux

    #Configura tamnho do traco abaixo do cabecalho
    for y in range(15+int(defCache.tamTag/4)+((6+tamWrdHex)*(2**defCache.tamOffSet))):
        traco = traco + '='

    #Imprime cabecalho
    print('\n'
          '| Idx | V | Tag ',tamTag + qntBlocos + ' |' '\n' + traco)

    #realiza o loop  conforme quantidades de linhas na cache, a cada loop eh realizada a impressao de uma linha
    for x in range(2**defCache.tamIndex):

        endrCache = cache[x]
        linha = hex(x)

        #verifica o bit de validade, se valido imprime conteudo
        if valiCache[x] == 1:
            tag = testaTamEndr(hex(int(endrCache[0:defCache.tamTag], 2)), int(defCache.tamTag/4))#extrai tag do endereco

            #extrair word do endereço
            word = testaTamEndr(hex(int(endrCache, 2)), int(defCache.tamEndereco/4))
            word = word[:tamWrdHex+2]

            #Concatena word para impressao
            data = ' '
            for y in range(2**defCache.tamOffSet):
                data = data + word[:tamWrdHex+2]+'X | '

            print( '|',linha,'|',valiCache[x],'|',
                   tag+' |'+ data)

        #Se bit de validade for nulo ou invalido, imprime em branco
        else:
            print('|', linha, '|', valiCache[x], '|')

    print(traco)
    print('    HITS:', hit, '    MISSES:', miss)

#busca tag do endereco lido do arquivo
#recebe os endereco em binario e as definicções de tamanho
#retorna a tag do endereço
def buscaTag(endrBin, defCache):

    tag = endrBin[2:defCache.tamTag+2]

    return tag

#busca index do endereco lido do arquivo
#recebe os endereco em binario e as definicções de tamanho
#retorna a index do endereço
def buscaIdx(endrBin, defCache):

    idx = endrBin[defCache.tamTag + 2:defCache.tamIndex + defCache.tamTag + 2]

    return idx

#busca offset do endereco lido do arquivo
#recebe os endereco em binario e as definicções de tamanho
#retorna a offset do endereço
def buscaOffset(endrBin, defCache):

    offset = endrBin[defCache.tamTag + defCache.tamIndex + 2 :
                        defCache.tamTag + defCache.tamIndex + defCache.tamOffSet + 2]

    return offset

#busca byte do endereco lido do arquivo
#recebe os endereco em binario e as definicções de tamanho
#retorna a byte do endereço
def buscaByte(endrBin,defCache):

    byte = endrBin[defCache.tamTag + defCache.tamIndex + defCache.tamOffSet + 2:
                    defCache.tamTag + defCache.tamIndex + defCache.tamOffSet + defCache.tamByte + 2]

    return byte

#testa e complementa com zero a quantidade de bits pedidos
#recebe um endereço em hexa ou bin e o tamnhanho desejado
def testaTamEndr(endr, tamEndereco):

    tam = len(endr) - 2
    aux = ''

    if not tamEndereco <= tam:
        comp = tamEndereco - tam #diferença do tamanho requisitado
        for x in range(comp):
            aux = aux + '0'
        endr = endr[0:2] + str(aux) + endr[2:] #concatena os zeros com o endereço informado

    return endr



'''
#####################################################################
#-----------------------------  MAIN  ------------------------------#
#####################################################################
'''

#-------------busca e tratamento de argumentos
#atribuicao dos parametro
argv = sys.argv

#inicializacao de variaveis

hit = 0
miss = 0

#controle para execucao do passo a passo
passo = False
passoCabecalho = False
cont = len(argv)

#testa se o segundo argumento passado e valido
if cont == 3:
    if not argv[2] == '-p':
        print('\n   --Erro, argumentos não conhecidos\n')
        help()
    elif argv[2] == '-p':
        #Se o segundo paramentro for -p ele paaso recebe True, assim executando passo a passo
        passo = True
        passoCabecalho = True

#testa se os argumentos sao validos ou chamada de help, senao chama o help
if cont == 2:
    try:
        if argv[1] == '/?' or argv[1] == 'help':
            print('\n   --Erro, argumentos não conhecidos\n')
            help()
    except:
        if not argv[1] == '/?' or argv[1] == 'help':
            print('\n   --Erro, argumentos não conhecidos\n')
            help()

#chama funcao para abrir
arqvTxt = abrirArquivo(argv)

#retorna o conteudo do arquivo, cada linha em uma posicao da lista
enderecosHexa = lerArquivo(arqvTxt)

#fecha o arquivo
fecharArquivo(arqvTxt)

#inicializa a lista Cache com zeros de acordo com o tamanho de index
cache = [0 for x in range(2**defCache.tamIndex)]

#inicializa a lista do Bit de validade com zeros de acordo com o tamanho de index
valiCache = [0 for x in range(2**defCache.tamIndex)]



#a cada loop recebe um endereco para trabalhar
for endr in enderecosHexa:

    # verifica se ira imprimir a tabela a cada leitura de endereco, imprimindo a cache vazia
    if passo == True and passoCabecalho == True:

        print('\n\nEstado Inicial:')

        #imprime a tabela cache
        tabelaCache(cache, valiCache, defCache, hit, miss)
        passoCabecalho = False
        input() #aguarda comando do usuario para continuar

    try:
        endrBin = bin(int(endr, 16)) #converte de hexadecimal para binario
        endrBin = testaTamEndr(endrBin, defCache.tamEndereco)#complementa o tamanho requerido

        tag =    buscaTag    (endrBin, defCache) #busca a tag
        idx =    buscaIdx    (endrBin, defCache) #busca o index
        offset = buscaOffset (endrBin, defCache) #busca o offset
        byte =   buscaByte   (endrBin, defCache) #busca o byte

    except Exception:
        print('-Erro, endereço inválido', endr)
        continue

    #verifica se o bit de validade na posicao é valido(1) ou nao(0)
    if valiCache[int(idx,2)] == 0:

        miss += 1 #contador de miss
        valiCache[int(idx, 2)] = 1 #muda a o bit para valido
        cache[int(idx, 2)] = tag + idx + offset + byte #grava na posicao

    elif valiCache[int(idx,2)] == 1:

        endrCache = cache[int(idx, 2)] #recebe o conteudo da linha da cache

        #verifica de a tag eh igual a solicitada
        if tag == endrCache[0:defCache.tamTag]:
            hit += 1 #contador de hit
        else:
            miss += 1 #contador de miss
            cache[int(idx, 2)] = tag + idx + offset + byte #grava na posicao

    # verifica se ira imprimir a tabela a cada leitura de endereco
    if passo == True:

        print('\n\nLeitura do endereço: 0x'+ endr)

        #imprime a tabela cache
        tabelaCache(cache, valiCache, defCache, hit, miss)
        input()#aguarda comando do usuario para continuar


#imprime a tabela cache ao final da execucao, se não imprimiu passo a passo
if not passo == True:
    tabelaCache(cache, valiCache, defCache, hit, miss)


#fim do codigo