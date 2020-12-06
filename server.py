import socket
from _thread import *
import sys

server = "192.168.0.163"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # тип подключенпия и как передаем информацию

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

s.listen(2)  # лимит подключения
print("Waiting for a connection, Server Started")


def read_pos(str):
    str = str.split(',')
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])


pos = [(6, 7), (8, 7)]


def threaded_client(conn, player):
    global currentPlayer
    conn.send(str.encode(make_pos(pos[player])))
    reply = ''
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data
            # reply = data.decode('utf-8')

            if not data:
                print('Disconnected')
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print('Recived: ', data)
                print('Sendig: ',  reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print('Lost connection')
    currentPlayer -= 1
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
    print(currentPlayer)

