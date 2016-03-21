import paramiko
import os
comm = 'rm -rf /root/.ssh;ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa;'
os.popen(comm)

with open('host') as f:
    for line in f:
        info = line.split(' ')
        addr = info[0]
        username = info[1]
        password = info[2]
        #print(addr,username,password)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(addr,22,username, password)
        ssh.exec_command(comm)
        ssh.exec_command('rm -rf /tmp/id_rsa.pub')
        #print('comm end')
        t = paramiko.Transport((addr,22))
        t.connect(username = username, password = password)
        sftp = paramiko.SFTPClient.from_transport(t)
        remotepath= '/tmp/id_rsa.pub'
        localpath= '/root/.ssh/id_rsa.pub'
        sftp.put(localpath,remotepath)
        t.close()
        #print('put end')

        command = 'cat ' + remotepath + ' >> /root/.ssh/authorized_keys;chmod 600 /root/.ssh/authorized_keys'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(addr,22,username, password)
        ssh.exec_command(command)
        ssh.close()
        print('{0} copy success'.format(addr))
        #print('cat end')
       