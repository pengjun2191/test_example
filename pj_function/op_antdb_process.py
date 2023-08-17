import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.KT_op_remote import Paramiko_ssh 
from pj_function.get_config import cfg_singleton as cfg


class op_antdb_process:
    def __init__(self) -> None:
        self.antdb_server=cfg.AntDBServer
    def op_antdb_process(self,antdb_cmd):
        pk_ssh=Paramiko_ssh(self.antdb_server)
        if isinstance(antdb_cmd,list):
            result=pk_ssh.sshop_more_cmd(antdb_cmd)
        else:
            result=pk_ssh.sshop_cmd(antdb_cmd)
        return result   
    def root_op_antdb_process(self,antdb_cmd,type,passwd):
        pk_ssh=Paramiko_ssh(self.antdb_server)
        if isinstance(antdb_cmd,list):
            result=pk_ssh.sshop_more_cmd(antdb_cmd,type,passwd)
        else:
            result=pk_ssh.sshop_cmd(antdb_cmd,type,passwd)
        return result 

    def antdb_start(self):
        return self.op_antdb_process('pg_ctl -D /data02/antdb/app/antdb/data start')
    def antdb_stop(self):
        return self.op_antdb_process('pg_ctl -D /data02/antdb/app/antdb/data stop')
    def antdb_abnormal(self):
        abnormal_str="""ps -ef |grep postgre|grep -v "grep"|awk '{print $2}'|xargs -r kill -9"""
        return self.op_antdb_process(abnormal_str)
    def antdb_net_break(self):
        antdb_net_break="iptables -t nat -I OUTPUT -p tcp -o lo --dport 6655 -j REDIRECT --to-ports 1234 "
        return self.root_op_antdb_process(antdb_net_break,"root","xdjr0lxGu")
    def antdb_net_reset(self):
        antdb_net_reset="iptables -t nat -D OUTPUT -p tcp -o lo --dport 6655 -j REDIRECT --to-ports 1234 "
        return self.root_op_antdb_process(antdb_net_reset,"root","xdjr0lxGu")
    def antdb_iptables_break(self):
        antdb_iptables_break="iptables -t nat -A PREROUTING -p tcp -d 10.19.30.66 --dport 6655 -j DNAT --to-destination 10.19.30.66:1234 "
        return self.root_op_antdb_process(antdb_iptables_break,"root","xdjr0lxGu")
    def antdb_iptables_reset(self):
        antdb_iptables_reset="iptables -t nat -D PREROUTING -p tcp -d 10.19.30.66 --dport 6655 -j DNAT --to-destination 10.19.30.66:1234"
        return self.root_op_antdb_process(antdb_iptables_reset,"root","xdjr0lxGu")
    def antdb_firewall_break(self):
        firewall_reload="firewall-cmd --reload"
        firewall_port_forward="firewall-cmd --add-forward-port=port=6655:proto=tcp:toport=1234 --zone=public --permanent"
        firewall_port_forward_local="firewall-cmd --permanent --direct --add-rule ipv4 nat OUTPUT 0 -p tcp -o lo --dport 6655 -j REDIRECT --to-ports 1234"
        firewall_ip_forward="firewall-cmd --add-forward-port=port=6655:proto=tcp:toport=1234:toaddr=10.19.30.66 --zone=public --permanent"
        firewall_forward=[firewall_port_forward,firewall_port_forward_local,firewall_ip_forward,firewall_reload]
        return self.root_op_antdb_process(firewall_forward,"root","xdjr0lxGu")
    
    def antdb_firewall_reset(self):
        firewall_reload="firewall-cmd --reload"
        firewall_port_forward="firewall-cmd --remove-forward-port=port=6655:proto=tcp:toport=1234 --zone=public --permanent"
        firewall_port_forward_local="firewall-cmd --permanent --direct --remove-rule ipv4 nat OUTPUT 0 -p tcp -o lo --dport 6655 -j REDIRECT --to-ports 1234"
        firewall_ip_forward="firewall-cmd --remove-forward-port=port=6655:proto=tcp:toport=1234:toaddr=10.19.30.66 --zone=public --permanent"
        firewall_forward=[firewall_port_forward,firewall_port_forward_local,firewall_ip_forward,firewall_reload]
        return self.root_op_antdb_process(firewall_forward,"root","xdjr0lxGu")


if __name__=="__main__":
    op_antdb=op_antdb_process()
    #op_antdb.antdb_net_break()
    #op_antdb.antdb_iptables_break()
    #op_antdb.antdb_firewall_break()
    #op_antdb.root_op_antdb_process("iptables -t nat -L","root","xdjr0lxGu")
    op_antdb.antdb_net_reset()
    op_antdb.antdb_iptables_reset()
    op_antdb.antdb_firewall_reset()