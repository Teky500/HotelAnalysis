import pandas as pd

import fitz

class CustomerCheck:
    def __init__(self, Name, InDate, OutDate, CN, IN, IND, HSTN, Unit, Country):
        self.name = Name
        self.InDate = InDate
        self.OutDate = OutDate
        self.CN = CN
        self.IN = IN
        self.IND = IND
        self.HSTN = HSTN
        self.Unit = Unit
        self.Country = Country
    def get_country(self):
        return self.Country
    def __str__(self):
        return (f"Name: {self.name}\n InDate: {self.InDate}\n OutDate: {self.OutDate}\n Unit: {self.Unit}\n Country: {self.Country}")

# DOC

doc = fitz.open('CheckOutPDF.pdf')

PersonList = []
NameList = []
InDateList = []
OutDateList = []
PUnitList = []
PCountry = []

for l in range(1, len(doc)):
    othertext = doc[l].get_text()
    splittext = othertext.split("Date", 1)
    firsttext = splittext[0].split('\n')
    Name = firsttext[2]
    InDate = firsttext[4]
    OutDate = firsttext[6]
    CN = firsttext[8]
    IN = firsttext[10]
    ID = firsttext[12]
    HSTN = firsttext[14]
    Unit = firsttext[16]
    Country = firsttext[len(firsttext)-2]
    Person = CustomerCheck(Name, InDate, OutDate, CN, IN, ID, HSTN, Unit, Country)
    PersonList.append(Person)
    NameList.append(Name)
    InDateList.append(InDate)
    OutDateList.append(OutDate)
    PUnitList.append(Unit)
    PCountry.append(Country)
for i in PersonList:
    print(i)
DATA = pd.DataFrame(dict(Name = NameList, InDate = InDateList, OutDate = OutDateList, Unit = PUnitList, Country = PCountry))
print(DATA)
