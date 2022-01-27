from specart_com import Player, Com
import socket
import threading

soc = socket.socket()

class CON_Com(Com):
    def CON_fresh(self, content):
        command_handle(cmd)

def command_handle(cmd):
    '''
    cmd:指令字符串按空格分割后的指令列表
    '''
    
    global initGoods
    global initMoney
    global beginTime
    global myself

    global selling
    global buying

    try:
        core_cmd = cmd[0]
        
        #私人指令
        if core_cmd == 'nameok':                                        #nameok (name)
            print('Server Instruction: '+' '.join(cmd))

        elif core_cmd == 'money':                                 #money (initMoney)
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
        elif core_cmd == 'sell':                                        #sell (num) (price)
            if not (cmd[2] in selling):
                selling[cmd[2]] = int(cmd[1])
            else:
                selling[cmd[2]] += int(cmd[1])
        elif core_cmd == 'buy':                                         #buy (num) (price)
            if not (cmd[2] in buying):
                buying[cmd[2]] = int(cmd[1])
            else:
                buying[cmd[2]] += int(cmd[1])            
        elif core_cmd == 'backsell':                                    #backsell (num) (price)
            selling[cmd[2]] -= int(cmd[1])
            if selling[cmd[2]] == 0:
                del selling[cmd[2]]
        elif core_cmd == 'backbuy':                                     #backbuy (num) (price)
            buying[cmd[2]] -= int(cmd[1])
            if buying [cmd[2]] == 0:
                del buying[cmd[2]]
        elif core_cmd == 'dealsell':                                    #dealsell (num) (price) (dealtime)
            print('News: '+' '.join(cmd))
            #处理买盘
            buying[cmd[2]] -= int(cmd[1])
            if buying[cmd[2]] == 0:
                del buying[cmd[2]]
            #处理卖盘
            S_min_price = Ssort(selling)['S1'][0]
            selling[S_min_price] -= int(cmd[1])
            if selling[S_min_price] == 0:
                del selling[S_min_price]
        elif core_cmd == 'dealbuy':                                     #dealbuy (num) (price) (dealtime)
            print('News: '+' '.join(cmd))
            #处理卖盘
            selling[cmd[2]] -= int(cmd[1])
            if selling[cmd[2]] == 0:
                del selling[cmd[2]]
            #处理买盘
            B_max_price = Bsort(buying)['B1'][0]
            buying[B_max_price] -= int(cmd[1])
            if buying[B_max_price] == 0:
                del buying[B_max_price]
        elif core_cmd == 'name':                                        #name (IP):(port) (name)
            print(f'Players: {cmd[2]} {cmd[1]}')
        elif core_cmd == 'begin':                                       #begin (time)
            beginTime = cmd[1]
            print('GAME START!')

            
    except IndexError:
        print('void cmd')

def Bsort(B):
    '''
    将买盘按价格降序排列后返回
    B:买盘字典
    返回:字典，形如{'B1':(price, num), 'B2':(price, num)...}
    '''

    B_lst = list(B.items())
    B_lst.sort(key=lambda tpl:int(tpl[0]), reverse=True)
    
    length = len(B_lst)
    if length <= 5:
        n = length + 1
    else:
        n = 6
    ret = {}
    for i in range(1, n):
        ret[f'B{i}'] = B_lst[i-1]
    
    return ret

def Ssort(S):
    '''
    将卖盘按价格升序排列后返回
    S:卖盘字典
    返回:字典，形如{'S1':(price, num), 'S2':(price, num)...}
    '''

    S_lst = list(S.items())
    S_lst.sort(key=lambda tpl:int(tpl[0]), reverse=False)

    length = len(S_lst)
    if length <= 5:
        n = length + 1
    else:
        n = 6
    ret = {}
    for i in range(1, n):
        ret[f'S{i}'] = S_lst[i-1]
    
    return ret

def Myaccount(player:Player):
    '''
    查看个人账户
    '''

    print(f'Current Money:{player.money}\nCurrent Goods:{player.goods}')

def Mytransaction(player:Player):
    '''
    查看个人在途交易
    self.transaction的values是指令按空格切分后的列表
    '''
    
    print(tuple(map(' '.join, player.transaction.values())))

if __name__ == '__main__':
    username = input('Hey! What\'s your name? ')
    host = input('host: ')

    initGoods = None        #初始化
    initMoney = None        #初始化
    beginTime = None        #初始化
    myself = Player(username, initGoods, initMoney, soc)
    com = Com(0, myself)
    com.connect(host)

    buying = {}             #买盘，key为价格value为该价格挂单总数量
    selling = {}            #卖盘，key为价格value为该价格挂单总数量

    while initGoods == None or initMoney == None or beginTime == None:  #等待从服务器读取数据再继续主线程
        pass

    print('''\nrules:
    sell (num) (price)
    buy (num) (price)
    backsell (num) (price) (time)
    backbuy (num) (price) (time)
    transaction
    account
    selling
    buying\n''')       #提示操作指令

    while True:
        try:
            cmd = input().split()
            if cmd[0] == 'transaction':
                Mytransaction()
            elif cmd[0] == 'account':
                Myaccount()
            elif cmd[0] == 'selling':
                print(Ssort(selling))
            elif cmd[0] == 'buying':
                print(Bsort(buying))
            else:
                print('invalid command')
        except Exception as e:
            print(e)

