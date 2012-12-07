"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core import mail


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)




class EmailTest(TestCase):
    def test_send_email(self):
        msg = "> ORDER:\n"
        msg = msg + '------------------------------------------------------\n'
        msg = msg + '>> Frakt och Hantering: 40 SEK \n'
        msg = msg + '------------------------------------------------------\n'
        msg = msg + '>>> Totalpris: 10000 SEK \n'
        to=['palle.torsson@gmail.com']
        mail.send_mail('Din order med Vamlingbolaget: ',u'%s' %msg, '23ctest@gmail.com', to,  fail_silently=False,)

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Din order med Vamlingbolaget: ')