from socket import *

# Configurações do Servidor
serverName = ''
serverPort = 12000
BUFFER_SIZE = 1024

serverSocket = socket(AF_INET, SOCK_DGRAM) # Cria socket
serverSocket.bind((serverName, serverPort)) # Associa o socket a porta serverPort
print("Server is ready to receive")

encodedFileName, clientAddress = serverSocket.recvfrom(BUFFER_SIZE) # Recebe o nome do arquivo
fileName = encodedFileName.decode() # Decodifica os dados que são recebidos em bytes
print(f" Receiving {fileName}")

path = './' + fileName
f = open(path, mode='wb') # Cria e abre para escrita de bytes o arquivo que está sendo recebido

print(f'Receiving {fileName}')

while True :
    data, clientAddress = serverSocket.recvfrom(BUFFER_SIZE) # Recebe os dados enviados no tamnho do buffer definido e o endereço de quem enviou
    
    if(not data): # Se os dados recebidos estiverem vazios, sai do loop
        break
    
    f.write(data) # Escreve os bytes recebidos no arquivo

f.close() # fecha o arquivo
print("Finished")

f = open(path, "rb") # abre o arquivo para leitrura de bytes

print(f"returning {fileName}")

# Começa a devolver o arquivo recebido
while True:
    data = f.read(BUFFER_SIZE) # lê o arquivo na quantidade de bytes especificada por BUFFER_SIZE

    serverSocket.sendto(data, clientAddress) # envia os bytes lidos do arquivo para o cliente origem

    if (not data): # se não houver nada para ler do arquivo, sai do loop
        break

f.close() # fecha o arquivo
print("Finished")

serverSocket.close() # encerra o socket