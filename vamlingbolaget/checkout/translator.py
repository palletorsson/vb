#-*-coding:utf-8-*-

def toEnglish(ordermessage): 
    ordermessage = ordermessage.replace(u"Din", u"Your")
    ordermessage = ordermessage.replace(u"från ", u"from ")
    ordermessage = ordermessage.replace(u"till ", u"to ")
    ordermessage = ordermessage.replace(u"Storlek", u"Size")
    ordermessage = ordermessage.replace(u"Pris per produkt", u"Price per product")
    ordermessage = ordermessage.replace(u"Frakt och hantering", u"Shipping and handling")
    ordermessage = ordermessage.replace(u"Totalpris", u"Total price")
    ordermessage = ordermessage.replace(u"Ditt telefonnummer", u"Your Phone number")
    ordermessage = ordermessage.replace(u"En order to Vamlingbolaget tar ca 3 veckor eftersom vi syr upp dina plagg", u"An order to Vamlingbo Team takes about 3 weeks since we sew your garments")
    return ordermessage