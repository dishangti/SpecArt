from server import SpecArt, NetHandler, syn_lock
import time as tm
import threading as thrd

def init():
    SpecArt('0.0.0.0', 7733)

def controller():
    '''
    Control the server.
    '''
    print('Input b and press enter to begin after all the players in.')
    print('Input q and press enter to quit.')

    while True:
        cmd = input('')
        if SpecArt.stop_flag or SpecArt.win_flag:
            break
        if cmd == 'b' and SpecArt.begin_flag == False:
            SpecArt.begin_flag = True
            time = tm.time()
            begin_info = 'SpecArt Begins at ' + tm.ctime(time)
            print(begin_info)
            with syn_lock:
                NetHandler.broadcast('begin', time)
                for player in NetHandler.players.values():
                    NetHandler.broadcast('name', player.addr, player.name)

        if cmd == 'q':
            break

print('SpecArt ' + SpecArt.VERSION + '.' + '\n' + 'See https://github.com/dishangti/SpecArt' + '\n')
print("Welcome to SpecArt Server!")
server = thrd.Thread(target=init)
server.start()
print("Server is running...")
controller()
