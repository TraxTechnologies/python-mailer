
import asyncore
import Queue
import smtpd
import time
import threading
import unittest

import mailer

class CustomSMTPServer(smtpd.SMTPServer):

##	def handle_accept(self):
##		super(CustomSMTPServer, self).handle_accept()

	def process_message(self, peer, mailfrom, rcpttos, data):
##		print 'Receiving message from:', peer
##		print 'Message addressed from:', mailfrom
##		print 'Message addressed to  :', rcpttos
##		print 'Message length        :', len(data)
		self.queue.put((peer, mailfrom, rcpttos, data))
		return


class BasicTestCase(unittest.TestCase):

	def helper(self):
		server = CustomSMTPServer(('127.0.0.1', 1025), None)
##		server = smtpd.DebuggingServer(('127.0.0.1', 1025), None)
		server.queue = self.queue
		self.queue.put('ready')
		asyncore.loop(use_poll=True)

	def setUp(self):
		self.queue = Queue.Queue()

	def tearDown(self):
		pass

	def runTest(self):
		'''
		Tests basic functionality.
		'''
		t = threading.Thread(target=self.helper)
		t.setDaemon(True)
		t.start()
		self.assertEqual(self.queue.get(.1), 'ready')
		time.sleep(.1)

		try:
			From = "translation@ginstrom.com"
			To = ["translation@ginstrom.com", "software@ginstrom.com"]

			mailer_inst = mailer.Mailer('127.0.0.1', 1025)
			msg = mailer.Message(From=From, To=To, charset="utf-8")
			mailer_inst.send(msg)

			peer, mailfrom, rcpttos, data = self.queue.get(.1)

			self.assertEqual(mailfrom, From)
			self.assertEqual(rcpttos, To)
			print data

		finally:
			try:
				raise asyncore.ExitNow()
			except asyncore.ExitNow:
				pass

if __name__ == '__main__':
	unittest.main()
