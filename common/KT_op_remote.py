import paramiko
import os

class Paramiko_sftp:
    def __init__(self,server_configfile):
        self.host = server_configfile['host']
        self.username = server_configfile['username']
        self.passwd = server_configfile['passwd']
        self.port = server_configfile['port']
        self.tt = None

    def pk_connect(self):
        self.tt = paramiko.Transport((self.host, self.port))
        self.tt.connect(username = self.username, password = self.passwd)
        try:
            return paramiko.SFTPClient.from_transport(self.tt)
        except Exception as e:
            print ('Connect error:',e)
            exit()

    def put_file(self,local_dir,remote_dir):
        sftp = self.pk_connect()
        files = os.listdir(local_dir)
        cnt = 0
        for file in files:
            sftp.put(os.path.join(local_dir, file), os.path.join(remote_dir, file))
            cnt += 1

        if cnt == len(files):
            print (str(cnt) +' files put successful')
        else:
            print ('put failure')
        self.tt.close()

    def get_file(self,local_dir,remote_dir):
        sftp = self.pk_connect()
        files = sftp.listdir(remote_dir)
        cnt = 0
        for file in files:
            sftp.get(os.path.join(remote_dir, file),os.path.join(local_dir, file))
            cnt += 1

        if cnt == len(files):
            print (str(cnt) +' files get successful')
        else :
            print ('get failure')
        self.tt.close()

class Paramiko_ssh:
    def __init__(self,server_configfile):
        self.host = server_configfile['host']
        self.username = server_configfile['username']
        self.passwd = server_configfile['passwd']
        self.port = server_configfile['port']

    def pk_ssh(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host,self.port,self.username,self.passwd,timeout=20)
        '''
        self.tt = paramiko.Transport((self.host, self.port))
        self.tt.connect(username = self.username, password = self.passwd)
        ssh._transport=self.tt
        '''
        try:
            return ssh
        except Exception as e:
            print ('Connect error:',e)
            exit()

    def chan_execute(self,channel,command,end_with="# "):
        """
        command:要执行的命令
        end_with：输出结束的标志，例如当指令执行结束后，Linux窗口会显示#
        """
        command = command + "\n"
        print("command is: %s" % command)
        channel.send(command)
        buff = ''
        while not buff.endswith(end_with):
            resp = channel.recv(9999)
            try:
                buff += resp.decode('utf-8')
            except:
                buff += resp.decode('GBK')  
        print("output is: %s" % buff)
        return buff
    
    def invoke_shell(self,ssh_client,cmd,passwd="xdjr0lxGu",end_with="# "):
        print("开始使用为终端")
        chan = ssh_client.invoke_shell()  # 使用伪终端，默认vt100创建交互式
        try:
            self.chan_execute(chan,"su -","Password: ")
            self.chan_execute(chan,passwd,end_with)
        except:
            print("Failed to switch to root by dia")
            exit(-1)
        if isinstance(cmd,list):
            s=[]
            for c in cmd:
                s.append(self.chan_execute(chan,c,end_with))
        elif isinstance(cmd,str):
            s=self.chan_execute(chan,cmd,end_with)
        return s
    
    def sshop_cmd(self,cmd="",type="user",passwd="xdjr0lxGu",end_with="# "):
        pk_ssh=self.pk_ssh()
        if type=="root":
            result=self.invoke_shell(pk_ssh,cmd,passwd,end_with)
            pk_ssh.close()
            return result
        else:
            try:
                print(cmd)
                stdin, stdout, stderr = pk_ssh.exec_command(cmd,timeout=20)
                result=stdout.read()
                print(result)
                pk_ssh.close()
                try:
                    return result.decode('utf-8')
                except:
                    return result.decode('GBK')
            except Exception as e :
                print("execute timeout,recv error",e)
                pk_ssh.close()
    
    def sshop_more_cmd(self,more_cmd=[],type="user",passwd="xdjr0lxGu",end_with="# "):
        result=[]
        pk_ssh=self.pk_ssh()
        if type=="root":
            result=self.invoke_shell(pk_ssh,more_cmd,passwd,end_with)
        else:
            for cmd in more_cmd:
                stdin, stdout, stderr = pk_ssh.exec_command(cmd)
                res=stdout.read()
                try:
                    result.append(res.decode('utf-8'))
                except UnicodeDecodeError:
                    result.append(res.decode('GBK'))
        pk_ssh.close()
        return result

if __name__=='__main__':
    pk_sftp=Paramiko_sftp()
    pk_ssh=Paramiko_ssh()
    print(pk_ssh.sshop_cmd("cd home;ls -l"))
    #print(pk_ssh.sshop_more_cmd(["cd home","ls -l"]))
