# Reverse Shell

This Python script establishes a reverse shell, enabling remote access to a targeted machine. It comprises two scripts:

reverse-shell-server.py: Listens on an open port to receive connections, facilitating remote command execution.

reverse-shell-client.py: Initiates communication from the target machine (client) back to the attacker's machine (server), enabling remote access and control.

![image](https://github.com/IlyaKosloF/reverse-shell/assets/174350287/6a09b285-4176-4be1-9f2f-8d29f0238134)


git clone https://github.com/IlyaKosloF/reverse-shell.git

cd server

python3 server.py
