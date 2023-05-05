import sys
sys.path.append('../')

from socket import *
from common import *

#configurações do servidor com que o cliente irá se comunicar
serverName = 'localhost'
serverPort = 12000

#Definição do ACK inicial
nextAck = 0
nextRcvACK = -1

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
else:
    nextAck = 1 if nextAck == 0 else 0 

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

responseFile = open(f'responseFile-{fileName}', mode='wb') # abre o arquivo resposta para escrita de bytes

print('Waiting Response')

while True :
    pkt, (serverName, serverPort) = clientSocket.recvfrom(BUFFER_SIZE) #recebe o pacote com dados do arquivo
    
    pktObj = pickle.loads(pkt) #remonta o pacote recebido no objeto pacote
    
    if((not corrupt(pktObj)) and is_ACK(pktObj, nextRcvACK)): # verifica se os checksums batem e se foi recebido o ACK correto
        if(nextRcvACK == -1):
            nextRcvACK = pktObj['head']['ack']
        nextRcvACK = 1 if nextRcvACK == 0 else 0 # troca o ACK esperado
        lastPktRcvd = pkt # guarda ultimo pacote recebido para reenvio em caso de ACK recebido errado
        clientSocket.sendto(lastPktRcvd, (serverName, serverPort)) # envia o ultimo pacote recebido com o mesmo ACK para confirmação
        
        data = pktObj['data']
        if(not data): # se os dados chegam vazios, significa que o arquivo já foir completamente recebido
            break
        responseFile.write(data)  # escreve no arquivo resposta os bytes recebidos
    elif (not is_ACK(pktObj, nextRcvACK)): # se foi recebido o ACK errado significa que é dulpicata
        clientSocket.sendto(lastPktRcvd, (serverName, serverPort)) # reenvia o ultimo pacote recebido com o mesmo ACK para confirmação
    
responseFile.close() # fecha o arquivo resposta
print('Finished')

clientSocket.close() # encerra o socket