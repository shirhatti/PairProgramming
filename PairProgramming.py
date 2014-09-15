import os
import socket
import sublime
import sublime_plugin
import subprocess
import sys
import threading
import asynchat
import asyncore
import socket

debug_flag = True
enable_send = True
enable_receive = True

server_subprocesses = []
sever_portnumber = []
# class SocketConnection(threading.Thread):
#     def __init__(self,timeout):
#         self.port_number = 0
#         self.timeout = timeout
#         self.result = None
#         threading.Thread.__init__(self)

#     def run(self):
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         server_name = 'localhost'
#         self.port_number = _available_port()
#         server_address = (server_name, self.port_number)
#         debug(sys.stderr, 'PairProgramming\t::::\tStarting up on %s:%s' % server_address)
#         sock.bind(server_address)
#         sock.listen(1)
#         repeat = True
#         while repeat:
#             print (sys.stderr, 'PairProgramming\t::::\tWaiting for a connection')
#             connection, client_address = sock.accept()
#             try:
#                 print (sys.stderr, 'client connected:', client_address)
#                 while True:
#                     data = connection.recv(16)
#                     print (sys.stderr, 'received "%s"' % data)
#                     if data == b'end\r\n':
#                         repeat = False
#                         debug('received end command')
#                         break
#                     if data == b'disconnect\r\n':
#                         break
#                     if data:
#                         connection.sendall(data)
#                     else:
#                         break
#             finally:
#                 connection.close()

#         sock.close()
#         debug('PairProgramming\t::::\tSocket closed')
   
def debug(*args, **kwargs):
    if debug_flag == True:
        print(*args, **kwargs)

def _available_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

class ChatClient(asynchat.async_chat):
 
    def __init__(self, host, port, view):
        self.view = view
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
 
        self.set_terminator(b'\0')
        self.buffer = []
 
    def collect_incoming_data(self, data):
        self.buffer.append(data)
 
    def found_terminator(self):
        msg = b''.join(self.buffer)
        print ('Receivved:', msg)
        self.view.run_command('run_macro_file', {"file": "Packages/PairProgramming/Clear.sublime-macro"})
        self.view.run_command("insert", {"characters": msg.decode('utf-8')})

        self.buffer = []

class ChatClientRunner(threading.Thread):
    def __init__(self, host, port, view):
        self.host = host
        self.port = port
        self.view = view
        threading.Thread.__init__(self)

    def run(self):
        self.client = ChatClient(self.host, self.port, self.view)
        asyncore.loop()

# def communicate_server(target_process, dummy):
#     stdin_data, stderr_data = target_process.communicate()
#     if stderr_data:
#         for stderr_line in stderr_data.splitlines():
#             debug('error:%s' % stderr_line)
#     else:
#         debug('exit_solution_server')

# def create_subprocess():
#     if len(server_subprocesses) >= 1:
#         debug('Echoserver already running')
#         return
#     args = [
#         'python', 'echoserver.py', 'localhost'
#     ]
#     debug('starting debug server')
#     server_process = subprocess.Popen(args, stderr=subprocess.PIPE)
#     server_thread = threading.Thread(target=communicate_server, args=(server_process, ''))
#     server_thread.daemon = True
#     server_subprocesses.append(server_thread)
#     server_thread.start()

# def stop_subprocess():
#     try:
#         server_process = server_subprocesses.pop()
#         debug('Stopping echoserver')
#         os.system("lsof -n -i4TCP:10001 | grep LISTEN | awk '{print $2}' | xargs kill -9")
#     except IndexError as e:
#         debug('Cannot stop process. No processes are currently running')

class PairProgrammingConnectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.thread = ChatClientRunner('beta.shirhatti.com', 5051, self.view)
        self.thread.daemon = True
        debug("PairProgramming\t\tConnect")
        self.thread.start()
        # self.handle_thread(self.thread)

    # def handle_thread(self, thread, offset=0, i=0, dir=1):

    #     next_thread = None
    #     if thread.is_alive():
    #         next_thread = thread
    #     thread = next_thread

    #     if thread:
    #         # This animates a little activity indicator in the status area
    #         before = i % 8
    #         after = (7) - before
    #         if not after:
    #             dir = -1
    #         if not before:
    #             dir = 1
    #         i += dir
    #         self.view.set_status('syncing', 'Syncing [%s=%s]' % \
    #             (' ' * before, ' ' * after))
         
    #         sublime.set_timeout(lambda: self.handle_thread(thread,
    #             offset, i, dir), 100)
    #         return

class PairProgrammingDisconnectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        pass
        # try:
        #     self.thread = server_subprocesses.pop()
        #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     debug(self.thread.port_number)
        #     s.connect(('localhost', self.thread.port_number))
        #     s.send(bytes('end\r\n', 'UTF-8'))
        #     data = s.recv(16)
        #     s.close()
        #     debug(data)
        #     while(self.thread.is_alive()):
        #         pass
        #     # debug('Stopping echoserver')
        # except IndexError as e:
        #     debug('No process currently running')

class ChatClientSend(asynchat.async_chat):
 
    def __init__(self, host, port):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
 
        self.set_terminator(b'\0')
        self.buffer = []
 
    def collect_incoming_data(self, data):
        pass
 
    def found_terminator(self):
        pass

class Test(sublime_plugin.EventListener):
    def __init__(self):
        debug('Initialize EventListener')
        self.client = ChatClientSend('beta.shirhatti.com', 5051)
        self.comm = threading.Thread(target=asyncore.loop)
        self.comm.daemon = True
        self.comm.start()

    def on_modified(self,view):
        source = view.substr(sublime.Region(0, view.size()))
        self.client.push(bytearray(source + '\0', 'utf-8'))