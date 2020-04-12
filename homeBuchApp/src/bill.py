from abc import ABC, abstractmethod

class AbstractItem(ABC):

    @abstractmethod
    def __init__(self):
        pass

    def setAttr(self, attrName, dictIn, key):
        if key in dictIn.keys():
            for attr, value in self.__dict__.items():
                if attr == attrName:
                    self.__dict__[attr] = dictIn[key]

class Bill(AbstractItem):
    def __init__(self, dataIn:dict={}):
        print("dataIn:")
        print(dataIn)
        print("=====================================")
        self.dateTime = None
        self.discount = None
        self.discountSum = None
        self.total = None
        self.fiscalDocNum = None
        self.fiscalDriveNum = None
        self.fiscalSign = None
        self.retailAddr = None
        self.shopName = None
        self.shopINN = None
        self.prodDataList = []

        if dataIn:
            self.setAttr("dateTime", dataIn, "dateTime")
            self.setAttr("discount", dataIn, "discount")
            self.setAttr("discountSum", dataIn, "discountSum")
            self.setAttr("total", dataIn, "totalSum")
            self.setAttr("fiscalDocNum", dataIn, "fiscalDocumentNumber")
            self.setAttr("fiscalDriveNum", dataIn, "fiscalDriveNumber")
            self.setAttr("fiscalSign", dataIn, "fiscalSign")
            self.setAttr("retailAddr", dataIn, "dateTime")
            self.setAttr("shopName", dataIn, "user")
            self.setAttr("shopINN", dataIn, "userInn")

            self.__setProductsList(dataIn["items"])

    def __setProductsList(self, dataList):
        for productDict in dataList:
            self.prodDataList.append(Product(productDict))

class Product(AbstractItem):
    def __init__(self, dataIn:dict):
        self.name = None
        self.price = None
        self.quantity = None
        self.total = None
        self.category = None
        self.subCategory = None

        if dataIn:
            self.setAttr("name", dataIn, "name")
            self.setAttr("price", dataIn, "price")
            self.setAttr("quantity", dataIn, "quantity")
            self.setAttr("total", dataIn, "sum")


if __name__ == "__main__":


    billDict = {
        'cashTotalSum': 0, 
        'dateTime': 1573288440, 
        'discount': None, 
        'discountSum': None, 
        'ecashTotalSum': 60000, 
        'fiscalDocumentNumber': 49443, 
        'fiscalDriveNumber': '9252440300030946', 
        'fiscalSign': 3980658383, 
        'items': [
            {
                'modifiers': None, 
                'name': 'GANZER 90150 LUX шланг для душа, 150см',
                'nds0': None,
                'nds10': None,
                'nds18': None,
                'ndsCalculated10': None,
                'ndsCalculated18': None,
                'ndsNo': None,
                'price': 60000,
                'quantity': 1.0,
                'sum': 60000,
                'storno': False
            },
            {
                'modifiers': None, 
                'name': 'GANZER 90155 LUX шланг для душа, 155см',
                'nds0': None,
                'nds10': None,
                'nds18': None,
                'ndsCalculated10': None,
                'ndsCalculated18': None,
                'ndsNo': None,
                'price': 65000,
                'quantity': 1.0,
                'sum': 65000,
                'storno': False
            }
        ], 
        'kktNumber': None,
        'kktRegId': '0001435350019624',
        'markup': None,
        'markupSum': None,
        'modifiers': None,
        'nds0': None,
        'nds10': None,
        'nds18': None,
        'ndsCalculated10': None,
        'ndsCalculated18': None,
        'ndsNo': 60000,
        'operationType': 1,
        'operator': 'Кассир 1',
        'requestNumber': 3,
        'retailPlaceAddress': None,
        'shiftNumber': 420,
        'stornoItems': None,
        'taxationType': 2,
        'totalSum': 60000,
        'user': 'ИП  ВОРОНОВ С.Е.',
        'userInn': '773570652261'
    }

    BillInst = Bill(billDict)