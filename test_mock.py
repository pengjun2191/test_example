from mock import http_server,socket_server,soap_server,mail_server
def main(args):
    if args.protocol =="http":
        http_server(server_address=(args.host, args.port),mock_data_file=args.mock_data_file)
    elif args.protocol=="socket":
        socket_server(server_address=(args.host, args.port),mock_data_file=args.mock_data_file)
    elif args.protocol=="soap":
        soap_server(server_address=(args.host, args.port),mock_data_file=args.mock_data_file)
    elif args.protocol=="mail":
        mail_server(server_address=(args.host,args.port))
    else:
        print("has no protocol")
    

if __name__=="__main__":
    from mock.mock_cli import mock_cli
    args=mock_cli()
    main(args)