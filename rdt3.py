from socket import *
from random import random, randint

LOSS_RATE = 0.2
CORRUPT_RATE = 0.09


def send_data(data, src_socket, dest_address):
    # Cria o pacote a partir dos dados
    send_packet = make_packet(0, data)
    print("Creating packet...")

    # Envia o packet criado
    udt_send(send_packet, src_socket, dest_address)

    # Inicia o timer

    # Aguarda até receber a resposta adequada (ACK) ou dar timeout
    received_ack = False


def receive_data(dest_socket, buffer_size):
    # data, server_address = client_socket.recvfrom(buffer_size)
    # return received data and address
    pass


def receive_packet(packet):
    # return received_packet
    pass


def udt_send(packet, src_socket, dest_address):
    # Simula a perda de pacotes no canal não confiável
    loss = random()
    if loss > LOSS_RATE:
        print("! - Pacote perdido na camada não confiável")
        return

    # Simula um pacote sendo corrompido no canal não confiável
    corrupt = random()
    if corrupt > CORRUPT_RATE:
        # Pega o índice de um bit aleatório
        bit_index = randint(0, len(packet) * 8 - 1)

        # Calcula a posição do byte e do bit dentro do byte
        byte_index = bit_index // 8
        bit_offset = bit_index % 8

        # Troca o bit no packet
        byte_value = packet[byte_index]
        bit_mask = 1 << (7 - bit_offset)
        new_byte_value = byte_value ^ bit_mask
        corrupted_packet = (
            packet[:byte_index] + bytes([new_byte_value]) + packet[byte_index + 1 :]
        )
        # Envia o pacote corrompido
        src_socket.sendto(corrupted_packet, dest_address)
        print("! - Pacote corrompido na camada não confiável")

    # Finalmente, envia o pacote não corrompido
    src_socket.sendto(packet, dest_address)


def udt_receive(dest_socket, buffer_size):
    # Foi abstraído para uma função apenas para separar as camadas
    received_data, address = dest_socket.recvfrom(buffer_size)
    return received_data, address


def make_packet(sequence_number, data):
    # Calcula o checksum dos dados
    checksum = calculate_checksum(data)

    # Cria o pacote com o sequence number, o checksum e os dados

    # Retorna o pacote


def extract(packet, data):
    # return data
    pass


def deliver_data(data):
    # return
    pass


def calculate_checksum(data):
    # divide os dados em palavras de 16 bits e soma todas
    words = [
        int.from_bytes(data[i : i + 2], byteorder="big") for i in range(0, len(data), 2)
    ]
    total_sum = sum(words)

    while total_sum >> 16:
        total_sum = (total_sum & 0xFFFF) + (total_sum >> 16)

    # faz o complemento a um da soma
    checksum = ~total_sum & 0xFFFF

    return checksum


def is_corrupt(packet):
    # return is_corrupt (bool)
    pass


def is_ack(packet, sequence_number):
    # return if that packet is an ack to the specified sequence number
    pass


def has_sequence(packet, sequence_number):
    # return packet["sequence_number"] == sequence_number
    pass


def start_timer():
    pass


def stop_timer():
    pass
