import sys
sys.path.append('../')

from socket import *
from common import *

#configurações do servidor com que o cliente irá se comunicar
serverName = 'localhost'
serverPort = 12000
READ_BUFFER_SIZE = 963 # Como o cabeçalho está acrescentando 61 bytes ao pacote, o buffer de leitura foi reduzido para cumprir a restrição do projeto

#Definição do ACK inicial
nextAck = 0

clientSocket = socket(AF_INET, SOCK_DGRAM) # cria o socket

fileName = 'testFile.txt'
path = './' + fileName

testFile = open(path, mode="rb") # Abre o arquivo que será enviado no modo de leitura de bytes

pkt = make_pkt(fileName, nextAck) #criação do pacote com o nome do arquivo

received = send_pkt(clientSocket, serverName, serverPort, pkt, nextAck, 4) #Processo de envio e reenvio do pacote

if(not received): # se o pacote não foi recebido e todas as tentativas esgotaram, encerra o programa
    print('Ocorreu algum problema! Encerrando o programa')
    testFile.close()
    clientSocket.close() # encerra o socket
    exit()

print(f'sending {fileName}')

while True :
    data = testFile.read(READ_BUFFER_SIZE) # lê os bytes do arquivo na quantidade especificada por BUFFER_SIZE
    pkt = make_pkt(data, nextAck) # Criação do pacote com dados lidos
    
    received = send_pkt(clientSocket, serverName, serverPort, pkt, nextAck, 4) #Processo de envio e reenvio do pacote

    if(not received): # se o pacote não foi recebido e todas as tentativas esgotaram, encerra o programa
        print('Ocorreu algum problema! Encerrando o programa')
        testFile.close()
        clientSocket.close() # encerra o socket
        exit()
    else: # se o pacote foi recebido, altera o próximo ACK
        nextAck = 1 if nextAck == 0 else 0
    
    if(not data): # se os bytes lidos estiverem vazios, sai o loop e para de enviar
        break
    
testFile.close()
print('Finished')

responseFile = open('responseFile.txt', mode='wb') # abre o arquivo resposta para escrita de bytes

print('Waiting Response')

data =''
pkt, serverAddress = clientSocket.recvfrom(BUFFER_SIZE) # recebe o primeiro pacote de bytes
if(not corrupt(pkt)):
    data = pickle.loads(pkt)['data']
    responseFile.write(data)  # escreve no arquivo resposta os bytes recebidos

print(f'Receiving response file')
while True :
    pkt, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
    if(not corrupt(pkt)):
        data = pickle.loads(pkt)['data']
        responseFile.write(data)  # escreve no arquivo resposta os bytes recebidos
    if(not data):
        break

responseFile.close() # fecha o arquivo resposta
print('Finished')

clientSocket.close() # encerra o socket