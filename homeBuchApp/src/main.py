import sys

import pprint

from shutil import copyfile

from billsGetter import EmailGetter, FilesGetter
from db.controller import Controller

if __name__ == "__main__":
    from sqlalchemy import create_engine

    pp = pprint.PrettyPrinter(indent=4)

    # при чтении файла чека он всегда удаляется, поэтому копируем тестовый чек
    copyfile("../billsTemp/19_05_2019_08_48_404185210208576816315.json",
             "../bills/19_05_2019_08_48_404185210208576816315.json"
        )

    # EmailBillGetter = EmailGetter(login='', passwd='', imap='')
    # bills = EmailBillGetter.getBills()
    FilesGetter = FilesGetter()
    bills = FilesGetter.getBills()
    print(type(bills))
    for bill in bills:
        for attr, value in bill.__dict__.items():
            print(attr, value)
        print("======================================================================")

    db_engine = create_engine('sqlite:///homeBuch.db', echo=False, pool_recycle=3600)

    controllerInst = Controller(db_engine)

    controllerInst.parseBill(bills)

    print("whole expenses for whole time:")
    print(controllerInst.getWholeExpenses())

