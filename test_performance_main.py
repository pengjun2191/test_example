import os
from common.KT_op_remote import Paramiko_sftp,Paramiko_ssh

def transfer_file(server_configfile,cmd,local_dir,remote_dir):
    pk_sftp=Paramiko_sftp(server_configfile)
    pk_sftp.pk_connect()
    if pk_sftp.put_file(local_dir,remote_dir):
        pk_ssh=Paramiko_ssh(server_configfile)
        pk_ssh.sshop_cmd(f"cd {remote_dir};{cmd}")
        return True
    else:
        return False

def main(args):
    if args.start_type=="master":
        os.system(f"locust  --{args.start_type} -f {args.master_name}")
    else:
        if args.worker_type=="python":
            os.system(f"locust  --{args.start_type} -f {args.python_worker_name}")
        else:
            go_cmd=f"go run {args.go_worker_name}"
            server_configfile={}
            if args.worker_host !="localhost" and args.worker_host_user is not None and args.worker_host_password is not None:
                server_configfile['host']=args.worker_host
                server_configfile['username']=args.worker_host_user
                server_configfile['passwd']=args.worker_host_password
                server_configfile['port']=args.worker_port
                if transfer_file(server_configfile,go_cmd,args.worker_local_dir,args.worker_host_dir):
                    print("remote host cmd success")
            else:
                os.system(go_cmd)


if __name__=="__main__":
    from test_performance_case.locust_cli import locust_cli
    args=locust_cli()
    main(args)