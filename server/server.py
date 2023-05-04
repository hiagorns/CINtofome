import sys
sys.path.append('../')

from socket import *
from common import *

# Configurações do Servidor
serverName = ''

nextAck = 1

serverSocket = socket(AF_INET, SOCK_DGRAM) # Cria socket
serverSocket.bind((serverName, serverPort)) # Associa o socket a porta serverPort
print("Server is ready to receive")


filename = ''

pkt, (clientName, clientPort) = serverSocket.recvfrom(BUFFER_SIZE) # recebe o primeiro pacote de bytes

if(not corrupt(pkt)):
    pktObj = pickle.loads(pkt)
    fileName = pktObj['data']
    send_pkt(serverSocket, clientName, clientPort, pkt, pktObj['head']['ack'], 4)

path = './' + fileName
f = open(path, mode='wb') # Cria e abre para escrita de bytes o arquivo que está sendo recebido

print(f'Receiving {fileName}')

data = ''
while True :
    pkt, (clientName, clientPort) = serverSocket.recvfrom(BUFFER_SIZE)
    if(not corrupt(pkt)):
        data = pickle.loads(pkt)['data']
        f.write(data)  # escreve no arquivo resposta os bytes recebidos
    if(not data):
        break

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