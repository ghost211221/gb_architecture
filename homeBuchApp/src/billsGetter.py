from abc import ABC, abstractmethod
import json
import re
import sys
import os

import imaplib
import email

from meta.singleton import Singleton
from bill import Bill

class AbstractBillGetter(ABC):

    @abstractmethod
    def getBills(self):
        pass

class EmailGetter(AbstractBillGetter):
    __metaclass__ = Singleton
    def __init__(self, login=None, passwd=None, imap=None) -> None:
        print(login, passwd, imap)
        self.__login = None
        self.__passwd = None
        self.__imap = imap
        self.__mail = None
        if self.__checkIfEmail(login):
            self.__login = login
            self.__passwd = passwd
        else:
            print(f"wrong email ipaddress {login}")
            sys.exit(1)


    def __checkIfEmail(self, login=None) -> bool:
        email_re = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(email_re, login):  
            return True
        else:  
            return False

    def __emailLogIn(self):
        try:
            print(self.__login, self.__passwd, self.__imap)
            self.__mail = imaplib.IMAP4_SSL(self.__imap)
            self.__mail.login(self.__login, self.__passwd)
        except Exception as e:
            print(f"loggin in error: {str(e)}")
            sys.exit(1)

    def __emailLogOut(self):
        try:
            self.__mail.logout()
        except Exception as e:
            print(f"loggin out error: {str(e)}")
            sys.exit(1)

    def __getFromUnseen(self):
        """ читаем заранее созанную папку bills в почте,
            скачиваем непрочитанные письма """
        self.__mail.select("bills")
        result, data = self.__mail.uid('search', None, '(UNSEEN)')
        billsList = []
        for i in data[0].split():
            result, data = self.__mail.uid('fetch', i, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_string(str(raw_email, "utf-8"))
            if email_message.get_content_maintype() == 'multipart': #multipart messages only
                for part in email_message.walk():
                    #find the attachment part
                    if part.get_content_maintype() == 'multipart': continue
                    if part.get('Content-Disposition') is None: continue
                    # написать функцию создания чекатмм
                    billsList.append(Bill((json.loads(part.get_payload(decode=True)))))
        return billsList



    def getBills(self):
        self.__emailLogIn()
        bills = self.__getFromUnseen()
        self.__emailLogOut()

        return bills

class FilesGetter(AbstractBillGetter):

    def __scanDir(self):
        return os.listdir(path = "../bills")

    def __getFromFiles(self, files):
        billsList = []
        for file in files:
            fileName = f"../bills/{file}"
            with open(fileName, encoding="utf8") as i_f:
                billsList.append(Bill(json.load(i_f)))
            os.remove(fileName)

        return billsList

    def getBills(self):
        files = self.__scanDir()
        bills = self.__getFromFiles(files)        

        return bills

if __name__ == "__main__":
    import pprint

    from shutil import copyfile

    pp = pprint.PrettyPrinter(indent=4)

    # почту светить не буду, работает, возващает список объектов
    EmailBillGetter = EmailGetter('', '', '')
    bills = EmailBillGetter.getBills()

    pp.pprint(bills)
    
    copyfile("../billsTemp/19_05_2019_08_48_404185210208576816315.json",
             "../bills/19_05_2019_08_48_404185210208576816315.json"
        )

    FilesGetter = FilesGetter()
    bills = FilesGetter.getBills()
    pp.pprint(bills)

