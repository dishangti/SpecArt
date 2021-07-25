from Player import Player
import socket
import threading

soc = socket.socket()

def recv():
    while True:
        buff = soc.recv(1024).decode('utf8')
        command = buff.split('#')
        for i in command[:]:                    #去除空指令
            if not i:
                command.remove(i)
        for item in command:
            out = item.strip().split()
            command_handle(out)

def command_handle(cmd):
    '''
    cmd:指令字符串按空格分割后的指令列表
    '''
    
    global initGoods
    global initMoney
    global beginTime
    global myself

    try:
        core_cmd = cmd[0]
        
        #私人指令
        if core_cmd == 'nameok':                                        #nameok (name)
            print('Server Instruction: '+' '.join(cmd))

        elif core_cmd == 'money':                                       #money (initMoney)
            myself.money = initMoney = int(cmd[1])
            print('initial money: ', cmd[1], sep='')

        elif core_cmd == 'goods':                                       #goods (initGoods)
            myself.goods = initGoods = int(cmd[1])
            print('initial goods: ', cmd[1], sep='')

        elif core_cmd == 'sellok':                                      #sellok (num) (price) (time)
            print('Server Instruction: '+' '.join(cmd))
            cmd[0] = 'sell'
            myself.transaction[cmd[3]] = cmd
            myself.goods -= int(cmd[1])

        elif core_cmd == 'buyok':                                       #buyok (num) (price) (time)
            print('Server Instruction: '+' '.join(cmd))
            cmd[0] = 'buy'
            myself.transaction[cmd[3]] = cmd
            myself.money -= int(cmd[1])*int(cmd[2])

        elif core_cmd == 'backsellok':                                  #backsellok (num) (price) (time)
            myself.goods += int(myself.transaction[cmd[3]][1])
            del myself.transaction[cmd[3]]
            print('Server Instruction: '+' '.join(cmd))

        elif core_cmd == 'backbuyok':                                   #backbuyok (num) (price) (time)
            myself.money += int(myself.transaction[cmd[3]][1])*int(myself.transaction[cmd[3]][2])
            del myself.transaction[cmd[3]]
            print('Server Instruction: '+' '.join(cmd))

        elif core_cmd == 'buydealok':                                   #buydealok (num) (price) (time)
            #处理余额
            if cmd[2] == myself.transaction[cmd[3]][2]:
                pass
            elif int(cmd[2]) < int(myself.transaction[cmd[3]][2]):
                myself.money += (int(myself.transaction[cmd[3]][2]) - int(cmd[2])) * int(cmd[1])
            else:
                myself.money -= (int(cmd[2]) - int(myself.transaction[cmd[3]][2])) * int(cmd[1])
            
            #处理物资
            myself.goods += int(cmd[1])
            num_ordered = int(myself.transaction[cmd[3]][1])
            num_ordered -= int(cmd[1])
            if num_ordered == 0:
                del myself.transaction[cmd[3]]
            else:
                myself.transaction[cmd[3]][1] = str(num_ordered)
            
            print('Server Instruction: '+' '.join(cmd))
            
        elif core_cmd == 'selldealok':                                  #selldealok (num) (price) (time)
            #处理余额
            myself.money += int(cmd[2]) * int(cmd[1])
            
            #处理物资
            num_ordered = int(myself.transaction[cmd[3]][1])
            num_ordered -= int(cmd[1])
            if num_ordered == 0:
                del myself.transaction[cmd[3]]
            else:
                myself.transaction[cmd[3]][1] = str(num_ordered)
            
            print('Server Instruction: '+' '.join(cmd))
        
        
        #广播指令
        elif core_cmd == 'dealsell':
            print('News: '+' '.join(cmd))
        elif core_cmd == 'dealbuy':
            print('News: '+' '.join(cmd))
        elif core_cmd == 'name':
            print('Players: '+' '.join(cmd))
        elif core_cmd == 'begin':                                       #begin (time)
            beginTime = cmd[1]
            print('GAME START!')

            
    except IndexError:
        print('void cmd')

username = input('Hey! What\'s your name? ')
host = input('host: ')
port = 7733#int(input('port: '))

soc.connect((host, port))

soc.sendall(f'name {username}#'.encode('utf8'))

initGoods = None        #初始化
initMoney = None        #初始化
beginTime = None        #初始化
myself = Player(username, initGoods, initMoney, soc)

thread = threading.Thread(target=recv, name='recvThread')
thread.start()

while initGoods == None or initMoney == None or beginTime == None:  #等待从服务器读取数据再继续主线程
    pass

print('''\nrules:
sell (num) (price)
buy (num) (price)
backsell (num) (price) (time)
backbuy (num) (price) (time)
transaction
account\n''')       #提示操作指令

while True:
    try:
        cmd = input().split()
        if cmd[0] == 'sell':
            myself.sell(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == 'buy':
            myself.buy(int(cmd[1]), int(cmd[2]))
        elif cmd[0] == 'backsell':
            myself.backsell(cmd[1], cmd[2], cmd[3])
        elif cmd[0] == 'backbuy':
            myself.backbuy(cmd[1], cmd[2], cmd[3])
        elif cmd[0] == 'transaction':
            myself.Mytransaction()
        elif cmd[0] == 'account':
            myself.Myaccount()
        else:
            print('invalid command')
    except Exception as e:
        print(e)

