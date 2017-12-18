def privmsg(channel, msg):
    return bytes('PRIVMSG {0} :{1}\r\n'  .format(channel, msg), 'utf-8')

def nick(nick):
    return bytes('NICK {0}\r\n'.format(nick), 'utf-8')

def user(user, mode, unused, realname):
    return bytes('USER {0} {1} {2} :{3}\r\n'.format(user, mode, unused, realname), 'utf-8')

def join(channel):
    bytes('JOIN {0}\r\n'.format(channel), 'utf-8')

def quit():
    bytes('def QUIT\r\n', 'utf-8')

def pong(msg):
    bytes("PONG {0}\r\n".format(msg), 'utf-8')
