import smtpd
import asyncore
 
class CustomSMTPServer(smtpd.SMTPServer):
	def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
		print('---------- MESSAGE FOLLOWS ----------')
		if kwargs:
			if kwargs.get('mail_options'):
				print('mail options: %s' % kwargs['mail_options'])
			if kwargs.get('rcpt_options'):
				print('rcpt options: %s\n' % kwargs['rcpt_options'])
		print ('Receiving message from: ',peer)
		print ('Message addressed from: ',mailfrom)
		print ('Message addressed to  : ',rcpttos)
		print ('Message length        : ',len(data))
		print('------------ END MESSAGE ------------')
		return

def mail_server(server_address):
	try:
		server=CustomSMTPServer(server_address,None)
		print ('服务已经开启')
		print("listen at: %s:%s" %server_address)
		asyncore.loop()
	except:
		print ('服务已经结束')  
if __name__=="__main__":
    from mock_cli import mock_cli
    args=mock_cli()  
    mail_server((args.host,args.port))