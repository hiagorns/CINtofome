from socket import *
import rdt3

# configurações do servidor com que o cliente irá se comunicar
server_name = "localhost"
server_port = 12000
BUFFER_SIZE = 1024

client_socket = socket(AF_INET, SOCK_DGRAM)  # cria o socket

file_name = "testFile.txt"
path = "./" + file_name

# Abre o arquivo que será enviado no modo de leitura de bytes
try:
    test_file = open(path, mode="rb")
except OSError as error_msg:
    print(f"Error while opening file: {error_msg}")

print(f"File {file_name} opened successfully!")

# Envia o nome do arquivo para que ele seja criado no servidor
# client_socket.sendto(file_name.encode(), (server_name, server_port))
rdt3.send_data(
    data=file_name.encode(),
    src_socket=client_socket,
    address=(server_name, server_port),
)
print(f"Sending {file_name}...")

while True:
    # lê os bytes do arquivo na quantidade especificada por BUFFER_SIZE
    data = test_file.read(BUFFER_SIZE)

    # envia os bytes lidos
    rdt3.send_data(
        data=data, src_socket=client_socket, address=(server_name, server_port)
    )

    if not data:  # se os bytes lidos estiverem vazios, sai o loop e para de enviar
        break

test_file.close()
print("Finished")

# abre o arquivo resposta para escrita de bytes
response_file = open("response_" + file_name, mode="wb")

print("Waiting Response")

# recebe o primeiro pacote de bytes
data, server_address = rdt3.receive_data(dest_socket=client_socket, buffer_size=BUFFER_SIZE)

response_file.write(data)  # escreve no arquivo resposta os bytes recebidos
print(f"Receiving response file...")

while True:
    # continua recebendo os pacotes restantes
    data, server_address = rdt3.receive_data(dest_socket=client_socket, buffer_size=BUFFER_SIZE)

    # se os dados recebidos estiverem vazios, significa que o arquivo já foi recebido por completo, então sai do loop
    if not data:
        break
    response_file.write(data)  # escreve no arquivo resposta os bytes recebidos

response_file.close()  # fecha o arquivo resposta
print("Finished")

client_socket.close()  # encerra o socket
