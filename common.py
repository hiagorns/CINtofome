import pickle
import time

#configurações do servidor e dos buffers
serverName = 'localhost'
serverPort = 12000
BUFFER_SIZE = 1024
READ_BUFFER_SIZE = 962 # Como o cabeçalho está acrescentando 61 bytes ao pacote, o buffer de leitura foi reduzido para cumprir a restrição do projeto

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(data):
    s = 0
    if(isinstance(data, bytes)):
        for i in range(0, len(data), 2):
            if i + 1 == len(data):
                w = data[i]
            else:
                w = data[i] + (data[i + 1] << 8)
            s = carry_around_add(s, w)
    else:
        for i in range(0, len(data), 2):
            if i + 1 == len(data):
                w = ord(data[i])
            else:
                w = ord(data[i]) + (ord(data[i + 1]) << 8)
            s = carry_around_add(s, w)
    return ~s & 0xffff


def make_pkt(data, nextAck):
    pkt = {
        "head": {
            "ack" : nextAck,
            "checksum": checksum(data)
            },
        "data": data
    }

    return pickle.dumps(pkt)

def ACKConfimation(sock, currentACK):
    received = False #flag que irá informar se a confimação foi recebida

    start = time.time() #marca o inicio do temporizador para que seja possível reconfigurar o temporizador com o tempo restante em caso de ack errado
    
    sock.settimeout(1) #inicia o temporizador
    
    while True:
        try:
            reply, senderAddress = sock.recvfrom(BUFFER_SIZE)
            reply = pickle.loads(reply)
            
            if reply["head"]["ack"] == currentACK: 
                received = True
            else:
                print("ack incorreto!") #se o ack foi incorreto, reconfigura o timeout para o tempo restante
                print(f"tempo restante: {sock.gettimeout() - (time.time() - start)}")
                sock.settimeout(sock.gettimeout() - (time.time() - start))
        except Exception as e: # Se ocorrer a exceção de timeout, sai do loop
            print(f"Estouro do temporizador")
            break
    
    sock.settimeout(None) # para o
    return received

def send_pkt(sock, destName, destPort, pkt, currentACK, attempts):
    received = False

    while(attempts >= 0):
        sock.sendto(pkt, (destName, destPort)) # envia o pacote
        received = ACKConfimation(sock, currentACK)
        if(not received): # Se estourou o temporizador e a confirmação não foi recebida
            print(f'Tentativas restantes: {attempts}')
            attempts = attempts - 1 # reduz o número e tentativas
        else:
            print("Confirmação recebida")
            break
    return received

def corrupt(pkt): ## verifica se o pacote não está corrompido
    return not pkt['head']['checksum'] == checksum(pkt['data'])

def is_ACK(pkt, ACK):
    if (ACK == -1):
        ACK = pkt['head']['ack']
    return pkt['head']['ack'] == ACK
        
