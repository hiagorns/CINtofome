from socket import *
import rdt3

# Configurações do Servidor
server_name = ""
server_port = 12000
BUFFER_SIZE = 1024

server_socket = socket(AF_INET, SOCK_DGRAM)  # Cria socket
server_socket.bind((server_name, server_port))  # Associa o socket a porta serverPort
print("Server is ready to receive")

# Recebe o nome do arquivo
encoded_file_name, client_address = rdt3.receive_data(
    dest_socket=server_socket, buffer_size=BUFFER_SIZE
)

# Decodifica os dados que são recebidos em bytes
file_name = encoded_file_name.decode()
print(f"Receiving {file_name}...")

# Cria e abre para escrita de bytes o arquivo que está sendo recebido
path = "./" + file_name
f = open(path, mode="wb")
print(f"Receiving {file_name}...")

while True:
    # Recebe os dados enviados no tamnho do buffer definido e o endereço de quem enviou
    # data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    data, client_address = rdt3.receive_data(
        dest_socket=server_socket, buffer_size=BUFFER_SIZE
    )

    if not data:  # Se os dados recebidos estiverem vazios, sai do loop
        break

    f.write(data)  # Escreve os bytes recebidos no arquivo

f.close()  # fecha o arquivo
print("Finished")

f = open(path, "rb")  # abre o arquivo para leitura de bytes

print(f"Returning {file_name}")

# Começa a devolver o arquivo recebido
while True:
    # lê o arquivo na quantidade de bytes especificada por BUFFER_SIZE
    data = f.read(BUFFER_SIZE)

    # envia os bytes lidos do arquivo para o cliente origem
    rdt3.send_data(data=data, src_socket=server_socket, dest_address=client_address)

    if not data:  # se não houver nada para ler do arquivo, sai do loop
        break

f.close()  # fecha o arquivo
print("Finished")

server_socket.close()  # encerra o socket
