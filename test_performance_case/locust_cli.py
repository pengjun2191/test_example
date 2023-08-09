import argparse
def locust_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-st','--start_type', dest='start_type',  default="master",choices=["master","worker"],
                        help='choice start_type master/worker,default:master')
    parser.add_argument('-mn','--master_name', dest='master_name', default="./test_performance_case/prometheus_exporter.py",
                    help='input master file name,default:./test_performance_case/prometheus_exporter.py')
    parser.add_argument('-wn','--worker_name', dest='worker_name', default="test_performance_main.py",
                    help='input worker file name,default:test_performance_main.py')
    args=parser.parse_args()
    return args