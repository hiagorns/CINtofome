from socket import *

#configurações do servidor com que o cliente irá se comunicar
serverName = 'localhost'
serverPort = 12000
BUFFER_SIZE = 1024

clientSocket = socket(AF_INET, SOCK_DGRAM) # cria o socket

fileName = 'testFile.txt'
path = './' + fileName

testFile = open(path, mode="rb") # Abre o arquivo que será enviado no modo de leitura de bytes

clientSocket.sendto(fileName.encode(), (serverName, serverPort)) # Envia o nome do arquivo para que ele seja criado no servidor

print(f'sending {fileName}')

while True :
    data = testFile.read(BUFFER_SIZE) # lê os bytes do arquivo na quantidade especificada por BUFFER_SIZE
    
    clientSocket.sendto(data, (serverName, serverPort)) # envia os bytes lidos
    
    if(not data): # se os bytes lidos estiverem vazios, sai o loop e para de enviar
        break
    
testFile.close()
print('Finished')

responseFile = open('responseFile.txt', mode='wb') # abre o arquivo resposta para escrita de bytes

print('Waiting Response')

data, serverAddress = clientSocket.recvfrom(BUFFER_SIZE) # recebe o primeiro pacote de bytes
responseFile.write(data)  # escreve no arquivo resposta os bytes recebidos
print(f'Receiving response file')
while True :
    data, serverAddress = clientSocket.recvfrom(BUFFER_SIZE) # continua recebendo os pacotes restantes
    if( not data) : # se os dados recebidos estiverem vazios, significa que o arquivo já foi recebido por completo, então sai do loop
        break
    responseFile.write(data) # escreve no arquivo resposta os bytes recebidos

responseFile.close() # fecha o arquivo resposta
print('Finished')

clientSocket.close() # encerra o socket

