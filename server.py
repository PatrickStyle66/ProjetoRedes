import socket
from _thread import *
import pickle
from game import Game

server = socket.gethostbyname(socket.gethostname())
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
s.listen(0)
print("Servidor Iniciado, aguardando conexão...")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if "*" in data:
                        index = str(data).split("*")
                        if index[1] == '1':
                            game.wins[int(index[1])] = int(index[0])

                        elif index[1] == '0':
                            game.wins[int(index[0])] = int(index[0])
                        print("jogador" + index[1] + ":" + index[0])
                    elif "/" in str(data):
                        name = str(data).strip('/')
                        game.names[p] = name
                    elif data == "reset":
                        game.resetWent()
                    elif data != "get" and '/' not in str(data) and '*' not in str(data):
                        game.play(p, data)
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Conexão Perdida")
    try:
        del games[gameId]
        print("Fechando Jogo", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Conectado a:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Criando novo jogo...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))