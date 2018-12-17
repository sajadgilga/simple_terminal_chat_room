import json
import subprocess

import sys
from io import TextIOWrapper
from threading import Thread

PORT = '8090'

server_cmd = ['netcat', '-l', '-p', PORT]
client_cmd = ['netcat', 'localhost', PORT]


def log(logger, message, sender):
    logger.write(sender + ": " + message + '\n')
    logger.flush()


def exit(process, file):
    file.close()
    process.terminate()
    sys.exit()


def input_handler(process, logger: TextIOWrapper):
    while True:
        inp = input()
        message = {
            'name': name,
            'msg': inp
        }
        if inp == 'quit':
            print('are you sure?')
            ans = input()
            if ans.lower() == 'yes':
                exit(process, logger)

        message = json.dumps(message) + '\n'
        process.stdin.write(bytes(message, 'utf8'))
        process.stdin.flush()
        log(logger, inp, '_me')


def output_handler(process, logger: TextIOWrapper):
    while True:
        output = process.stdout.readline().decode()
        if output == '':
            exit(process, logger)
        try:
            message = json.loads(output)
        except:
            message = {'name': 'anonymous', 'msg': output}
        sender_name = message['name']
        recieved_msg = message['msg']
        print(sender_name + ' said: ' + recieved_msg)
        log(logger, recieved_msg, '+' + sender_name)


def connection_maker(command, side_name):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    print('welcome to chat room, ', name)
    logger = open(side_name + '-logger.txt', "w+")

    input_thread = Thread(target=input_handler, args=[process, logger])
    output_thread = Thread(target=output_handler, args=[process, logger])
    input_thread.start()
    output_thread.start()


if __name__ == "__main__":
    print('This program is written and maintained by AI infra team 2019.\nAll credits go to rezvanian group.'
          '\nTo chat as a server enter [server <your '
          'name>] as a command, if not enter [client <your name>.'
          '\n remember to quit you just need to write it down:)')
    arg = input().split()
    type = arg[0]
    name = arg[1]

    if type == 'server':
        connection_maker(server_cmd, 'server')
    else:
        connection_maker(client_cmd, 'client')
