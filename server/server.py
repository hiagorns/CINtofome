import sys
sys.path.append('../')

from socket import *
from common import *

# Configurações do Servidor
serverName = ''

nextAck = 1
nextRcvACK = -1
lastPktRcvd = None

simularPerda = 3

serverSocket = socket(AF_INET, SOCK_DGRAM) # Cria socket
serverSocket.bind((serverName, serverPort)) # Associa o socket a porta serverPort
print("Server is ready to receive")

filename = ''

#loop para receber o primeiro pacote não corrompido
while True:
    pkt, (clientName, clientPort) = serverSocket.recvfrom(BUFFER_SIZE) # recebe o nome do arquivo
    pktObj = pickle.loads(pkt) # remonta os bytes recebidos no objeto pacote
    if((not corrupt(pktObj)) and is_ACK(pktObj, nextRcvACK)): # verifica se o pacote recebido está corrompido e se recebeu o ACK corret (no primeiro pacote recebido, o ACK esperado é definido pelo ACK recebido)
        fileName = pktObj['data']
        nextRcvACK = 1 if pktObj['head']['ack'] == 0 else 0 # troca o ACK esperado
        lastPktRcvd = pkt # guarda ultimo pacote recebido para reenvio em caso de ACK recebido errado
        serverSocket.sendto(lastPktRcvd, (clientName, clientPort)) # envia o ultimo pacote recebido com o mesmo ACK para confirmação
        break
        
# com o nome do arquivo recebido, cria o arquivo para escrita
path = './' + fileName
f = open(path, mode='wb') # Cria e abre para escrita de bytes o arquivo que está sendo recebido

print(f'Receiving {fileName}')
# loop para receber todos os dados do arquivo
while True :
    pkt, (clientName, clientPort) = serverSocket.recvfrom(BUFFER_SIZE) #recebe o pacote com dados do arquivo
    if(simularPerda < 1):
        pktObj = pickle.loads(pkt) #remonta o pacote recebido no objeto pacote
        
        if((not corrupt(pktObj)) and is_ACK(pktObj, nextRcvACK)): # verifica se os checksums batem e se foi recebido o ACK correto
            nextRcvACK = 1 if nextRcvACK == 0 else 0 # troca o ACK esperado
            lastPktRcvd = pkt # guarda ultimo pacote recebido para reenvio em caso de ACK recebido errado
            serverSocket.sendto(lastPktRcvd, (clientName, clientPort)) # envia o ultimo pacote recebido com o mesmo ACK para confirmação
            
            data = pktObj['data']
            if(not data): # se os dados chegam vazios, significa que o arquivo já foir completamente recebido
                break
            f.write(data)  # escreve no arquivo resposta os bytes recebidos
        elif (not is_ACK(pktObj, nextRcvACK)): # se foi recebido o ACK errado significa que é dulpicata
            serverSocket.sendto(lastPktRcvd, (clientName, clientPort)) # reenvia o ultimo pacote recebido com o mesmo ACK para confirmação
    else:
        print('simulando perda')
        simularPerda = simularPerda - 1

f.close() # fecha o arquivo
print("Finished")

f = open(path, "rb") # abre o arquivo para leitrura de bytes

print(f"returning {fileName}")

# Começa a devolver o arquivo recebido
while True :
    data = f.read(READ_BUFFER_SIZE) # lê os bytes do arquivo na quantidade especificada por BUFFER_SIZE
    pkt = make_pkt(data, nextAck) # Criação do pacote com dados lidos
    
    received = send_pkt(serverSocket, clientName, clientPort, pkt, nextAck, 4) #Processo de envio e reenvio do pacote

    if(not received): # se o pacote não foi recebido e todas as tentativas esgotaram, encerra o programa
        print('Ocorreu algum problema! Encerrando o programa')
        testFile.close()
        clientSocket.close() # encerra o socket
        exit()
    else: # se o pacote foi recebido, altera o próximo ACK
        nextAck = 1 if nextAck == 0 else 0
    
    if(not data): # se os bytes lidos estiverem vazios, sai o loop e para de enviar
        break

f.close() # fecha o arquivo
print("Finished")

serverSocket.close() # encerra o socket