import unittest

from email.utils import make_msgid

from mailer import Message

class MessageTestCase(unittest.TestCase):
    def test_message_as_string(self):
        msg = Message(
            To='foo@test.com',
            From='bar@test.com',
            Subject='Test Message',
            Text='This is just a test message.',
            Html='<body><p>This is just a test message.</p></body>',
        )
        msg.header('Message-ID', make_msgid())
        s = msg.as_string()
        assert type(s) == str

if __name__ == '__main__':
	unittest.main()
