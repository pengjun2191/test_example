import argparse
def locust_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-st','--start_type', dest='start_type',  default="master",choices=["master","worker"],
                        help='choice start_type master/worker,default:master')
    parser.add_argument('-mn','--master_name', dest='master_name', default="./test_performance_case/prometheus_exporter.py",
                    help='input master file name,default:./test_performance_case/prometheus_exporter.py')
    parser.add_argument('-wt','--worker_type', dest='worker_type', default="python",choices=["go","python"],
                    help='input worker file type,default:python')
    parser.add_argument('-pwn','--python_worker_name', dest='python_worker_name', default="./test_performance_case/locust_client_main.py",
                    help='input python worker file name,default:./test_performance_case/locust_client_main.py')
    parser.add_argument('-gwn','--go_worker_name', dest='go_worker_name', default="main.go",
                    help='input go worker file name,default: main.go')
    parser.add_argument('-wh','--worker_host', dest='worker_host', default="localhost",
                    help='input worker machine host for useing sftp put worker file,default:localhost')
    parser.add_argument('-wp','--worker_port', dest='worker_port', default="22",
                    help='input worker machine port for useing sftp put worker file,default:22')
    parser.add_argument('-whu','--worker_host_user', dest='worker_host_user', 
                    help='input worker machine host user for useing sftp put worker file')
    parser.add_argument('-whp','--worker_host_password', dest='worker_host_password', 
                    help='input worker machine host password for useing sftp put worker file')
    parser.add_argument('-wld','--worker_local_dir', dest='worker_local_dir', default="./go_performance_case",
                    help='input worker local dir for useing sftp put worker file')
    parser.add_argument('-whd','--worker_host_dir', dest='worker_host_dir', default="./go_performance_case",
                    help='input worker host dir for useing sftp put worker file')
    args=parser.parse_args()
    return args