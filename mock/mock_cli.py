import argparse
def mock_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--host', dest='host',  default="localhost",
                        help='This is IP/host,default:localhost ')
    parser.add_argument('-p','--port', dest='port', type=int,default=7777,
                    help='This is port,default:7777')
    parser.add_argument('-md','--mock_data', dest='mock_data_file', default="./mock/mock_data/mock_response.xls",
                    help='This is mock_data_file,default:./mock/mock_data/mock_response.xls ')
    parser.add_argument('-pl','--protocol', dest='protocol', default="http",choices=["http","socket","soap","mail"],
                    help='choice portocol http/socket/soap/mail,default:http')
    args=parser.parse_args()
    return args