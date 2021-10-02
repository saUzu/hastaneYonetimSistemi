import wx
import wx.adv
import cx_Oracle
import os
from datetime import date
from dateutil.relativedelta import relativedelta

def veriTabaniBaglantisi(kullanici, sifre):
    dsnTns = cx_Oracle.makedsn('DESKTOP-37KKSF2', 1521, 'XE')
    baglanti = None
    try:
        baglanti = cx_Oracle.connect(user=kullanici, password=sifre, dsn=dsnTns)
        print('Oracle Database Sürümü : ' + str(baglanti.version))
        return baglanti
    except cx_Oracle.Error as hata:
        print(hata)


""" class hastaGoruntule(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)
        self.tumAGor = wx.Button(self, label='Tüm Hastaları Görüntüle', pos=(85, 7))
        self.tumAGor.Bind(wx.EVT_BUTTON, lambda olay: self.hepsiniGor(olay, baglanti))
        self.tcNoGir = wx.TextCtrl(self, pos=(7, 35))
        self.tcNoGir.SetHint('TC No giriniz ')
        self.tcAra = wx.Button(self, label="TC No'ya göre ara", pos=(123, 35))
        self.tcAra.Bind(wx.EVT_BUTTON, lambda olay: self.tcyeGoreAra(olay, baglanti))
        self.adGir = wx.TextCtrl(self, pos=(7, 63))
        self.adGir.SetHint('Ad Giriniz ')
        self.soyadGir = wx.TextCtrl(self, pos=(124, 63))
        self.soyadGir.SetHint('Soyad Giriniz ')
        self.adAra = wx.Button(self, label="Ada göre ara", pos=(7, 91))
        self.adAra.Bind(wx.EVT_BUTTON, lambda olay: self.adaGoreAra(olay, baglanti))
        self.soyadAra = wx.Button(self, label="Soyada göre ara", pos=(123, 91))
        self.soyadAra.Bind(wx.EVT_BUTTON, lambda olay: self.soyadaGoreAra(olay, baglanti))
        self.adSoyadAra = wx.Button(self, label="Ad ve Soyada göre ara", pos=(232, 91))
        self.adSoyadAra.Bind(wx.EVT_BUTTON, lambda olay: self.adVeSoyadaGoreAra(olay, baglanti))
        self.veriListe = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(7, 120), size=(950, 300))
        self.veriListe.InsertColumn(0, 'Hasta TC No', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(1, 'Hasta Ad', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(2, 'Hasta Soyad', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(3, 'Doğum Tarihi', wx.LIST_FORMAT_CENTRE, width=100)
        
        #self.ver = wx.StaticText(self, label="Oracle Sürüm: " + baglanti.version, pos=(500, 100))

    def gizle(self, olay):
        self.Hide()
    
    def hepsiniGor(self, olay, bag):
        #print("asd")
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute(
                "select * from yonetici.muayene inner join yonetici.hasta on yonetici.muayene.hastasira=yonetici.hasta.hastaSira where yonetici.muayene.hekimsira=12")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()

    def tcyeGoreAra(self, olay, bag):
        #print("asd")
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.muayene inner join yonetici.hasta on yonetici.muayene.hastasira=yonetici.hasta.hastaSira where yonetici.muayene.hekimsira=12 and yonetici.hasta.hastatc='" + str(self.tcNoGir.GetValue()) + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            if len(str(self.tcNoGir.GetValue())) != 11:
                raise wx.MessageDialog(
                    None, 'Yanlış TC Numarası!!', 'TC HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                self.sayac = 0
                for satir in imlec.fetchall():
                    self.veriListe.InsertItem(self.sayac, str(satir[5]))
                    self.veriListe.SetItem(self.sayac, 1, str(satir[6]))
                    self.veriListe.SetItem(self.sayac, 2, str(satir[7]))
                    self.veriListe.SetItem(self.sayac, 3, str(satir[8]))
                    self.sayac = self.sayac + 1
                    #print(satir)
                self.veriListe.Show()

    def adaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.muayene inner join yonetici.hasta on yonetici.muayene.hastasira=yonetici.hasta.hastaSira where yonetici.muayene.hekimsira=12 and yonetici.hasta.hastaad='" + self.adGir.GetValue() + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()

    def soyadaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.muayene inner join yonetici.hasta on yonetici.muayene.hastasira=yonetici.hasta.hastaSira where yonetici.muayene.hekimsira=12 and yonetici.hasta.hastasoyad='" + self.soyadGir.GetValue() + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()

    def adVeSoyadaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.muayene inner join yonetici.hasta on yonetici.muayene.hastasira=yonetici.hasta.hastaSira where yonetici.muayene.hekimsira=12 and yonetici.hasta.hastaad='" +
                          str(self.adGir.GetValue()) + "' and yonetici.hasta.hastasoyad='" + str(self.soyadGir.GetValue()) + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()
 """

class muayeneGoruntule(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)
        self.tumAGor = wx.Button(self, label='Tüm Muayeneleri Görüntüle', pos=(85, 7))
        self.tumAGor.Bind(wx.EVT_BUTTON, lambda olay: self.hepsiniGor(olay, baglanti))
        self.tcNoGir = wx.TextCtrl(self, pos=(7, 35))
        self.tcNoGir.SetHint('TC No giriniz ')
        self.tcAra = wx.Button(self, label="TC No'ya göre ara", pos=(123, 35))
        self.tcAra.Bind(wx.EVT_BUTTON, lambda olay: self.tcyeGoreAra(olay, baglanti))
        self.adGir = wx.TextCtrl(self, pos=(7, 63))
        self.adGir.SetHint('Ad Giriniz ')
        self.soyadGir = wx.TextCtrl(self, pos=(124, 63))
        self.soyadGir.SetHint('Soyad Giriniz ')
        self.adAra = wx.Button(self, label="Ada göre ara", pos=(7, 91))
        self.adAra.Bind(wx.EVT_BUTTON, lambda olay: self.adaGoreAra(olay, baglanti))
        self.soyadAra = wx.Button(self, label="Soyada göre ara", pos=(123, 91))
        self.soyadAra.Bind(wx.EVT_BUTTON, lambda olay: self.soyadaGoreAra(olay, baglanti))
        self.adSoyadAra = wx.Button(self, label="Ad ve Soyada göre ara", pos=(232, 91))
        self.adSoyadAra.Bind(wx.EVT_BUTTON, lambda olay: self.adVeSoyadaGoreAra(olay, baglanti))
        self.veriListe = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(7, 120), size=(950, 300))
        self.veriListe.InsertColumn(0, 'Hasta Sırası', wx.LIST_FORMAT_RIGHT, width=100)
        self.veriListe.InsertColumn(1, 'Hekim Sırası', wx.LIST_FORMAT_RIGHT, width=100)
        self.veriListe.InsertColumn(2, 'Muayene Tarihi', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(3, 'Hasta TC No', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(4, 'Hasta Ad', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(5, 'Hasta Soyad', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(6, 'Doğum Tarihi', wx.LIST_FORMAT_CENTRE, width=100)



        #self.ver = wx.StaticText(self, label="Oracle Sürüm: " + baglanti.version, pos=(505, 100))

    def gizle(self, olay):
        self.Hide()
    
    def hepsiniGor(self, olay, bag):
        #print("asd")
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.muayene inner join yonetici.hasta on yonetici.muayene.hastasira=yonetici.hasta.hastaSira where yonetici.muayene.hekimsira=12")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.sayac = self.sayac + 1
                print(satir)
            self.veriListe.Show()

    def tcyeGoreAra(self, olay, bag):
        #print("asd")
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.muayene inner join yonetici.hasta on yonetici.muayene.hastasira=yonetici.hasta.hastaSira where yonetici.muayene.hekimsira=12 and yonetici.hasta.hastatc='" + str(self.tcNoGir.GetValue()) + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            if len(str(self.tcNoGir.GetValue())) != 11:
                raise wx.MessageDialog(
                    None, 'Yanlış TC Numarası!!', 'TC HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                self.sayac = 0
                for satir in imlec.fetchall():
                    self.veriListe.InsertItem(self.sayac, str(satir[1]))
                    self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                    self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                    self.veriListe.SetItem(self.sayac, 3, str(satir[5]))
                    self.veriListe.SetItem(self.sayac, 4, str(satir[6]))
                    self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                    self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                    self.sayac = self.sayac + 1
                    #print(satir)
                self.veriListe.Show()

    def adaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.muayene inner join yonetici.hasta on yonetici.muayene.hastasira=yonetici.hasta.hastaSira where yonetici.muayene.hekimsira=12 and yonetici.hasta.hastaad='" + self.adGir.GetValue() + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()

    def soyadaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.muayene inner join yonetici.hasta on yonetici.muayene.hastasira=yonetici.hasta.hastaSira where yonetici.muayene.hekimsira=12 and yonetici.hasta.hastasoyad='" + self.soyadGir.GetValue() + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()

    def adVeSoyadaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.muayene inner join yonetici.hasta on yonetici.muayene.hastasira=yonetici.hasta.hastaSira where yonetici.muayene.hekimsira=12 and yonetici.hasta.hastaad='" + str(self.adGir.GetValue()) + "' and yonetici.hasta.hastasoyad='" + str(self.soyadGir.GetValue()) + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()
        
class ameliyatGoruntule(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)
        self.tumAGor = wx.Button(self, label='Tüm Ameliyatları Görüntüle', pos=(85, 7))
        self.tumAGor.Bind(wx.EVT_BUTTON, lambda olay: self.hepsiniGor(olay, baglanti))
        self.tcNoGir = wx.TextCtrl(self, pos=(7, 35))
        self.tcNoGir.SetHint('TC No giriniz ')
        self.tcAra = wx.Button(self, label="TC No'ya göre ara", pos=(123, 35))
        self.tcAra.Bind(wx.EVT_BUTTON, lambda olay: self.tcyeGoreAra(olay, baglanti))
        self.adGir = wx.TextCtrl(self, pos=(7, 63))
        self.adGir.SetHint('Ad Giriniz ')
        self.soyadGir = wx.TextCtrl(self, pos=(124, 63))
        self.soyadGir.SetHint('Soyad Giriniz ')
        self.adAra = wx.Button(self, label="Ada göre ara", pos=(7, 91))
        self.adAra.Bind(wx.EVT_BUTTON, lambda olay: self.adaGoreAra(olay, baglanti))
        self.soyadAra = wx.Button(self, label="Soyada göre ara", pos=(123, 91))
        self.soyadAra.Bind(wx.EVT_BUTTON, lambda olay: self.soyadaGoreAra(olay, baglanti))
        self.adSoyadAra = wx.Button(self, label="Ad ve Soyada göre ara", pos=(232, 91))
        self.adSoyadAra.Bind(wx.EVT_BUTTON, lambda olay: self.adVeSoyadaGoreAra(olay, baglanti))
        self.veriListe = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(7, 120), size=(950, 300))
        self.veriListe.InsertColumn(0, 'Hasta Sırası', wx.LIST_FORMAT_RIGHT, width=100)
        self.veriListe.InsertColumn(1, 'Hekim Sırası', wx.LIST_FORMAT_RIGHT, width=100)
        self.veriListe.InsertColumn(2, 'Ameliyat Tarihi', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(3, 'Hasta TC No', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(4, 'Hasta Ad', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(5, 'Hasta Soyad', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(6, 'Doğum Tarihi', wx.LIST_FORMAT_CENTRE, width=100)
        #self.veriListe.Hide()

        #self.ver = wx.StaticText(self, label="Oracle Sürüm: " + baglanti.version, pos=(510, 100))

    def gizle(self, olay):
        self.Hide()
    
    def hepsiniGor(self, olay, bag):
        #print("asd")
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute(
                "select * from yonetici.ameliyat inner join yonetici.hasta on yonetici.ameliyat.hastasira=yonetici.hasta.hastaSira where yonetici.ameliyat.hekimsira=12")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()

    def tcyeGoreAra(self, olay, bag):
        #print("asd")
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.ameliyat inner join yonetici.hasta on yonetici.ameliyat.hastasira=yonetici.hasta.hastaSira where yonetici.ameliyat.hekimsira=12 and yonetici.hasta.hastatc='" + str(self.tcNoGir.GetValue()) + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            if len(str(self.tcNoGir.GetValue())) != 11:
                raise wx.MessageDialog(
                    None, 'Yanlış TC Numarası!!', 'TC HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                self.sayac = 0
                for satir in imlec.fetchall():
                    self.veriListe.InsertItem(self.sayac, str(satir[1]))
                    self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                    self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                    self.veriListe.SetItem(self.sayac, 3, str(satir[5]))
                    self.veriListe.SetItem(self.sayac, 4, str(satir[6]))
                    self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                    self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                    self.sayac = self.sayac + 1
                    #print(satir)
                self.veriListe.Show()

    def adaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.ameliyat inner join yonetici.hasta on yonetici.ameliyat.hastasira=yonetici.hasta.hastaSira where yonetici.ameliyat.hekimsira=12 and yonetici.hasta.hastaad='" + self.adGir.GetValue() + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()

    def soyadaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.ameliyat inner join yonetici.hasta on yonetici.ameliyat.hastasira=yonetici.hasta.hastaSira where yonetici.ameliyat.hekimsira=12 and yonetici.hasta.hastasoyad='" + self.soyadGir.GetValue() + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()

    def adVeSoyadaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.ameliyat inner join yonetici.hasta on yonetici.ameliyat.hastasira=yonetici.hasta.hastaSira where yonetici.ameliyat.hekimsira=12 and yonetici.hasta.hastaad='" + str(self.adGir.GetValue()) + "' and yonetici.hasta.hastasoyad='" + str(self.soyadGir.GetValue()) + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[6]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()
        
class receteGoruntule(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)
        self.tumAGor = wx.Button(self, label='Tüm Reçeteleri Görüntüle', pos=(85, 7))
        self.tumAGor.Bind(wx.EVT_BUTTON, lambda olay : self.hepsiniGor(olay, baglanti))

        self.tcNoGir = wx.TextCtrl(self, pos=(7, 35))
        self.tcNoGir.SetHint('TC No giriniz ')
        self.tcAra = wx.Button(self, label="TC No'ya göre ara", pos=(123, 35))
        self.tcAra.Bind(wx.EVT_BUTTON, lambda olay: self.tcyeGoreAra(olay, baglanti))

        self.adGir = wx.TextCtrl(self, pos=(7, 63))
        self.adGir.SetHint('Ad Giriniz ')
        self.soyadGir = wx.TextCtrl(self, pos=(124, 63))
        self.soyadGir.SetHint('Soyad Giriniz ')
        self.adAra = wx.Button(self, label="Ada göre ara", pos=(7, 91))
        self.adAra.Bind(wx.EVT_BUTTON, lambda olay: self.adaGoreAra(olay, baglanti))
        self.soyadAra = wx.Button(self, label="Soyada göre ara", pos=(123, 91))
        self.soyadAra.Bind(wx.EVT_BUTTON, lambda olay: self.soyadaGoreAra(olay, baglanti))
        self.adSoyadAra = wx.Button(self, label="Ad ve Soyada göre ara", pos=(232, 91))
        self.adSoyadAra.Bind(wx.EVT_BUTTON, lambda olay: self.adVeSoyadaGoreAra(olay, baglanti))

        self.veriListe = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(7, 120), size=(950, 300))
        self.veriListe.InsertColumn(0, 'Hasta Sırası', wx.LIST_FORMAT_RIGHT, width=100)
        self.veriListe.InsertColumn(1, 'Hekim Sırası', wx.LIST_FORMAT_RIGHT, width=100)
        self.veriListe.InsertColumn(2, 'İlaçları', wx.LIST_FORMAT_LEFT, width=100)
        self.veriListe.InsertColumn(3, 'Son Kullanım Tarihi', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(4, 'Verilen Tarih', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(5, 'Hasta TC No', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(6, 'Hasta Ad', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(7, 'Hasta Soyad', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.InsertColumn(8, 'Doğum Tarihi', wx.LIST_FORMAT_CENTRE, width=100)
        self.veriListe.Hide()

        #self.ver = wx.StaticText(self, label="Oracle Sürüm: " + str(baglanti.version), pos=(515, 100))

    def gizle(self, olay):
        self.Hide()

    def hepsiniGor(self, olay, bag):
        #print("asd")
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute(
                "select * from yonetici.recete inner join yonetici.hasta on yonetici.recete.hastasira=yonetici.hasta.hastaSira where yonetici.recete.hekimsira=12")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[4]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.veriListe.SetItem(self.sayac, 7, str(satir[9]))
                self.veriListe.SetItem(self.sayac, 8, str(satir[10]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()
        
    def tcyeGoreAra(self, olay, bag):
        #print("asd")
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute(("select * from yonetici.recete inner join yonetici.hasta on yonetici.recete.hastasira=yonetici.hasta.hastaSira where yonetici.recete.hekimsira=12 and yonetici.hasta.hastatc='" + str(self.tcNoGir.GetValue()) + "'"))
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            if len(str(self.tcNoGir.GetValue())) != 11:
                raise wx.MessageDialog(None, 'Yanlış TC Numarası!!', 'TC HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                self.sayac = 0
                for satir in imlec.fetchall():
                    self.veriListe.InsertItem(self.sayac, str(satir[1]))
                    self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                    self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                    self.veriListe.SetItem(self.sayac, 3, str(satir[4]))
                    self.veriListe.SetItem(self.sayac, 4, str(satir[5]))
                    self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                    self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                    self.veriListe.SetItem(self.sayac, 7, str(satir[9]))
                    self.veriListe.SetItem(self.sayac, 8, str(satir[10]))
                    self.sayac = self.sayac + 1
                    #print(satir)
                self.veriListe.Show()
        
    def adaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute(("select * from yonetici.recete inner join yonetici.hasta on yonetici.recete.hastasira=yonetici.hasta.hastaSira where yonetici.recete.hekimsira=12 and yonetici.hasta.hastaad='" + self.adGir.GetValue() + "'"))
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[4]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.veriListe.SetItem(self.sayac, 7, str(satir[9]))
                self.veriListe.SetItem(self.sayac, 8, str(satir[10]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()
                
    def soyadaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute(("select * from yonetici.recete inner join yonetici.hasta on yonetici.recete.hastasira=yonetici.hasta.hastaSira where yonetici.recete.hekimsira=12 and yonetici.hasta.hastasoyad='" + self.soyadGir.GetValue() + "'"))
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[4]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.veriListe.SetItem(self.sayac, 7, str(satir[9]))
                self.veriListe.SetItem(self.sayac, 8, str(satir[10]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()

    def adVeSoyadaGoreAra(self, olay, bag):
        #print(self.adGir.GetValue())
        self.veriListe.DeleteAllItems()
        try:
            imlec = bag.cursor()
            imlec.execute(
                ("select * from yonetici.recete inner join yonetici.hasta on yonetici.recete.hastasira=yonetici.hasta.hastaSira where yonetici.recete.hekimsira=12 and yonetici.hasta.hastaad='" + str(self.adGir.GetValue()) + "' and yonetici.hasta.hastasoyad='" + str(self.soyadGir.GetValue()) + "'"))
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' +
                             str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                self.veriListe.InsertItem(self.sayac, str(satir[1]))
                self.veriListe.SetItem(self.sayac, 1, str(satir[2]))
                self.veriListe.SetItem(self.sayac, 2, str(satir[3]))
                self.veriListe.SetItem(self.sayac, 3, str(satir[4]))
                self.veriListe.SetItem(self.sayac, 4, str(satir[5]))
                self.veriListe.SetItem(self.sayac, 5, str(satir[7]))
                self.veriListe.SetItem(self.sayac, 6, str(satir[8]))
                self.veriListe.SetItem(self.sayac, 7, str(satir[9]))
                self.veriListe.SetItem(self.sayac, 8, str(satir[10]))
                self.sayac = self.sayac + 1
                #print(satir)
            self.veriListe.Show()

class receteYaz(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)

        self.yaziTcNo = wx.StaticText(self, label='Hasta TC No Giriniz :  ', pos=(7, 38))
        self.girdiTcNo = wx.TextCtrl(self, pos=(123, 35))
        self.girdiTcNo.SetHint('TC No Giriniz')
        self.tcGonder = wx.Button(self, label='Bilgileri getir', pos=(240, 35))
        self.tcGonder.Bind(wx.EVT_BUTTON, lambda olay: self.tcGetir(olay, baglanti))


        self.ad = wx.StaticText(self, label=" ", pos=(7, 75))
        self.soyad = wx.StaticText(self, label=" ", pos=(65, 75))
        self.tcNo = wx.StaticText(self, label=" ", pos=(7, 89))
        self.dogumT = wx.StaticText(self, label=" ", pos=(150, 89))
        self.ilacYazi = wx.StaticText(self, label="İlaç: ", pos=(7, 110))
        self.ilac = wx.TextCtrl(self, pos=(35, 110), size=(300, 150), style=wx.TE_MULTILINE)
        self.receteE = wx.Button(self, label='Reçeteyi Yaz', pos=(300, 270))
        self.receteE.Bind(wx.EVT_BUTTON, lambda olay: self.receteEkle(olay, baglanti))
        
        self.sonKT = wx.adv.CalendarCtrl(self, pos=(400, 110))

        self.ad.Hide()
        self.soyad.Hide()
        self.tcNo.Hide()
        self.dogumT.Hide()
        self.ilacYazi.Hide()
        self.ilac.Hide()
        self.sonKT.Hide()
        self.receteE.Hide()

        #self.ver = wx.StaticText(self, label="Oracle Sürüm: " + str(baglanti.version), pos=(520, 100))
    
    def gizle(self, olay):
        self.Hide()
    def tcGetir(self, olay, bag):
        try:
            imlec = bag.cursor()
            imlec.execute("select * from yonetici.hasta where hastaTc='" + str(self.girdiTcNo.GetValue()) + "'")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!', 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            #print("asd1")
        else:
            try:
                #bag.commit()
                self.yakalanan = imlec.fetchall()
                self.ad.SetLabel(("Ad: " + str(self.yakalanan[0][2])).strip())
                self.soyad.SetLabel(("Soyad: " + str(self.yakalanan[0][3])).strip())
                self.tcNo.SetLabel(("TC Sırası: " + str(self.yakalanan[0][1])).strip())
                self.dogumT.SetLabel(("Doğum Tarihi: " + str(self.yakalanan[0][4])[0:11]).strip())
                #print(self.ad1[0])
            except IndexError:
                wx.MessageBox('TC No Yanlış Girildi', 'TC No!', wx.OK | wx.ICON_INFORMATION)
            else:
                self.ad.Show()
                self.soyad.Show()
                self.tcNo.Show()
                self.dogumT.Show()
                self.ilacYazi.Show()
                self.ilac.Show()
                self.sonKT.Show()
                self.receteE.Show()
    
    def receteEkle(self, olay,bag):
        self.ilaclar = self.ilac.GetValue()
        self.tc_ = str(self.yakalanan[0][1]).strip()
        print(self.tc_ + "a" + str(len(self.tc_)))
        print(self.ilaclar)
        self.tarih = self.sonKT.GetDate()
        self.tarih = wx.DateTime(self.tarih).FormatISODate()
        print(self.tarih)
        try:
            imlec = bag.cursor()
            imlec.execute("begin yonetici.receteekle('" + self.ilaclar + "', '" + self.tc_ + "', to_date('" + self.tarih + "', 'YY-mm-dd')); end;")
        except cx_Oracle.Error as hata:
            print(hata)
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            bag.commit()
            wx.MessageDialog(None, 'Reçete Yazıldı', 'BAŞARILI', wx.OK | wx.ICON_INFORMATION).ShowModal()
        
class hekimPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(1350, 37))
        self.kapat = wx.Button(self, label='Çıkış', pos=(7, 7))
        self.kapat.Bind(wx.EVT_BUTTON, parent.hkmTemizle)
        #self.hstGor = wx.Button(self, label='Hastaları Görüntüleme', pos=(85, 7))
        #self.hstGor.Bind(wx.EVT_BUTTON, parent.hastaGor)
        self.muaGor = wx.Button(self, label='Muayeneleri Görüntüleme', pos=(228, 7))
        self.muaGor.Bind(wx.EVT_BUTTON, parent.mynGor)
        self.amliGor = wx.Button(self, label='Ameliyatları Görüntüleme', pos=(390, 7))
        self.amliGor.Bind(wx.EVT_BUTTON, parent.amelGor)
        self.rctGor = wx.Button(self, label='Reçete Görüntüleme', pos=(552, 7))
        self.rctGor.Bind(wx.EVT_BUTTON, parent.rcteGor)
        self.rctYaz = wx.Button(self, label='Reçete Yaz', pos=(684, 7))
        self.rctYaz.Bind(wx.EVT_BUTTON, parent.rcteYaz)

####################################################

class yntReceteSil(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)
        self.tumunuGor = wx.Button(self, label='Tüm Reçeteleri Gör', pos=(7, 35))
        self.tumunuGor.Bind(wx.EVT_BUTTON, lambda olay: self.hepsiniGor(olay, baglanti))
        print(baglanti.version+" GÖKHAN")
        self.receteListesi = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(7, 120), size=(950, 300))
        self.receteListesi.InsertColumn(0, 'Reçete Sırası', wx.LIST_FORMAT_RIGHT, width=75)
        self.receteListesi.InsertColumn(1, 'Hasta Sırası', wx.LIST_FORMAT_RIGHT, width=75)
        self.receteListesi.InsertColumn(2, 'Hekim Sırası', wx.LIST_FORMAT_RIGHT, width=75)
        self.receteListesi.InsertColumn(3, 'İlaçlar', wx.LIST_FORMAT_RIGHT, width=100)
        self.receteListesi.InsertColumn(4, 'Son Kullanım Tarihi', wx.LIST_FORMAT_RIGHT, width=150)
        self.receteListesi.InsertColumn(5, 'Verilen Tarih', wx.LIST_FORMAT_RIGHT, width=150)
        self.receteListesi.InsertColumn(6, 'TC No', wx.LIST_FORMAT_RIGHT, width=100)
        self.receteListesi.InsertColumn(7, 'Ad', wx.LIST_FORMAT_RIGHT, width=100)
        self.receteListesi.InsertColumn(8, 'Soyad', wx.LIST_FORMAT_RIGHT, width=100)
        self.receteListesi.Hide()

        self.uyari = wx.StaticText(self, label='NOT: Silinirken "Reçete Sırası" göz önüne alınarak siliniyor.\nLütfen dikkatlice silme işlemini gerçekleştiriniz.', pos=(7, 80))
        self.uyari.Hide()
        self.silDugmesi = wx.Button(self, label='Sil', pos=(7, 420), size=(100, 30))
        self.silDugmesi.Bind(wx.EVT_BUTTON, lambda olay: self.receteSil(olay, baglanti))
        self.silDugmesi.Hide()
        

        self.rctKydt = wx.Button(self, label='Reçeteleri Kaydet', pos=(110, 420), size=(120, 30))
        self.rctKydt.Bind(wx.EVT_BUTTON, lambda olay: self.receteKaydet(olay, baglanti))
        self.rctKydt.Hide()
        
    def gizle(self, olay):
        self.Hide()
    def hepsiniGor(self, olay, bag):
        self.receteListesi.DeleteAllItems()
        print(bag.version)
        try:
            imlec = bag.cursor()
            imlec.execute('select * from yonetici.recete join yonetici.hasta on yonetici.recete.hastasira=yonetici.hasta.hastasira')
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                #print(satir)
                self.receteListesi.InsertItem(self.sayac, str(satir[0]))
                self.receteListesi.SetItem(self.sayac, 1, str(satir[1]))
                self.receteListesi.SetItem(self.sayac, 2, str(satir[2]))
                self.receteListesi.SetItem(self.sayac, 3, str(satir[3]))
                self.receteListesi.SetItem(self.sayac, 4, str(satir[4]))
                self.receteListesi.SetItem(self.sayac, 5, str(satir[5]))
                self.receteListesi.SetItem(self.sayac, 6, str(satir[7]))
                self.receteListesi.SetItem(self.sayac, 7, str(satir[8]))
                self.receteListesi.SetItem(self.sayac, 8, str(satir[9]))
                self.sayac = self.sayac + 1
            self.receteListesi.Show()
            self.silDugmesi.Show()
            self.rctKydt.Show()
            self.uyari.Show()
        #print('hepsi')
    def receteSil(self, olay, bag):
        #print(self.receteListesi.GetItem(itemIdx=self.receteListesi.GetFocusedItem(), col=0).GetText())
        try:
            imlec = bag.cursor()
            imlec.execute("begin yonetici.recetesil("+ self.receteListesi.GetItem(itemIdx=self.receteListesi.GetFocusedItem(), col=0).GetText() +"); end;")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            wx.MessageDialog(None, 'Başarı ile silindi!', 'BAŞARILI!', wx.OK | wx.ICON_INFORMATION).ShowModal()
            bag.commit()
            self.hepsiniGor(olay,bag)
    def receteKaydet(self, olay, bag):
        try:
            imlec = bag.cursor()
            imlec.execute("select * from ayrintiliReceteler")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!', 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            try:
                dosya = open('Reçeteler.xlsx', 'w', encoding='utf-16')
                dosya.write('TC No\tHastanın Adı\tHastanın Soyadı\tİlaçlar\tSon Kullanma Tarihi\t')
                dosya.write('Veriliş Tarihi\tDoktorun Adı\tDoktorun Soyadı\tTıp Bölümü\n')
            except Exception as hata:
                wx.MessageDialog(None, 'Beklenmedik bir hata oluştu!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
                print(hata)
            else:
                for k in imlec.fetchall():
                    ilac = str(k[4])
                    ilac=ilac.replace(',',' ')
                    #print(ilac)
                    dosya.write(str(k[7]) + '\t' + str(k[8]) + '\t' + str(k[9]) + '\t' + ilac + '\t' + str(k[5]) + '\t' + str(k[6]) + '\t' + str(k[11]) + '\t' + str(k[12]) + '\t' + str(k[13]) + '\n')
                wx.MessageDialog(None, 'Dosya baraşılı bir şekilde kaydedildi..!', 'OLDU!!', wx.OK | wx.ICON_INFORMATION).ShowModal()
                dosya.close()

class hstaSilEkle(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)
        self.hstE = wx.Button(self, label='Hasta Ekle', pos=(7, 35))
        self.hstE.Bind(wx.EVT_BUTTON, lambda olay: self.hastaEkle(olay, baglanti))
        self.hstS = wx.Button(self, label='Hasta Çıkar', pos=(85, 35))
        self.hstS.Bind(wx.EVT_BUTTON, lambda olay: self.hastaCikar(olay, baglanti))

    def gizle(self, olay):
        self.Hide()
    
    def hastaEkle(self, olay, bag):
        dosyaSec = wx.FileDialog(self, 'Hastaların bilgileri olan dosyayı seçin', wildcard="TXT Dosyaları (*.txt)|*.txt", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_CHANGE_DIR)
        if dosyaSec.ShowModal() == wx.ID_OK:
            print(dosyaSec.GetPath())
        
        try:
            imlec = bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Bağlantı kurulamadı!', 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            try:
                dosya = open(dosyaSec.GetPath(), 'r')
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Dosya açılmadı', 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                okunan = dosya.read()
                gecici = []
                geciciY = ''
                for k in okunan:
                    #print(k)
                    p = str(k).strip()
                    if p == ' ':
                        print('BOŞ')
                    if p != ',':
                        if p != ';':
                            if p != '\n':
                                if p != '':
                                    geciciY = geciciY + p
                        else:
                            gecici.append(geciciY)
                            #print(gecici)
                            self.tc = str(gecici[0]).strip()
                            self.ad = str(gecici[1]).strip()
                            self.soyad = str(gecici[2]).strip()
                            self.tarih = str(gecici[3]).strip()
                            print(self.tc+' '+self.ad+' '+self.soyad+' '+self.tarih)
                            try:
                                print("1")
                                imlec.execute("begin yonetici.hastaekle('" + self.ad + "', '" + self.soyad + "', to_date('" + self.tarih + "', 'dd/mm/yyyy'), '" + self.tc + "'); end;")
                                print("2")
                            except cx_Oracle.Error as hata:
                                wx.MessageDialog(None, 'Procedure çalıştırılamadı!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
                            except IndexError as index:
                                wx.MessageDialog(None, 'indexte hata oluştu' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
                            except TypeError as tip:
                                wx.MessageDialog(None, 'Type Hatası\n' + str(tip), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
                            else:
                                bag.commit()
                                #print(gecici)
                                #print(self.tc+' '+self.ad+' '+self.soyad+' '+self.tarih)
                            geciciY = ''
                            gecici.clear()
                    else:
                        gecici.append(geciciY)
                        geciciY = ''
                #print(gecici)
                dosya.close()
            imlec.close()

    def hastaCikar(self, olay, bag):
        #print("Hasta Çıktı")
        try:
            imlec = bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Bağlantı kurulamadı!\n'+str(hata), 'Oracle HATASI!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            dosyaSec = wx.FileDialog(self, 'Hastaların bilgileri olan dosyayı seçin', wildcard="Txt Dosyaları (*.txt)|*.txt", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, defaultFile='hastaBilgileri')
            if dosyaSec.ShowModal() == wx.ID_OK:
                print(dosyaSec.GetPath())
                print(dosyaSec.GetFilename())
                try:
                    imlec.execute('select * from yonetici.hasta')
                except cx_Oracle.Error as hata:
                    wx.MessageDialog(None, 'SQL komutu çalışmadı!\n'+str(hata), 'SQL HATASI!', wx.OK | wx.ICON_ERROR).ShowModal()
                else:
                    try:
                        dosya = open(dosyaSec.GetPath(), 'w',encoding='utf-16')
                    except Exception as hata:
                        wx.MessageDialog(None, 'Dosya oluşturulurken hata verdi\n' + hata, 'Dosya HATASI!', wx.OK | wx.ICON_ERROR).ShowModal()
                    else:
                        for satir in imlec.fetchall():
                            print(satir)
                            self.tarih = str(satir[4]).strip().replace('-','/')
                            dosya.write(str(satir[1]).strip()+','+str(satir[2]).strip()+','+str(satir[3]).strip()+','+self.tarih[:10]+';')
                            dosya.write('\n')
                        dosya.close()
                        wx.MessageDialog(None, 'Hasta bilgileri başarılı bir şekilde çıkarıldı.', 'OLDU', wx.OK | wx.ICON_INFORMATION).ShowModal()
            dosyaSec.Close()
            
class ydkAlDon(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        baglanti.close()
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)
        self.hstE = wx.Button(self, label='Yedek Al', pos=(7, 35))
        self.hstE.Bind(wx.EVT_BUTTON, self.yedekAl)
        self.hstS = wx.Button(self, label='Yedekten Dön', pos=(85, 35))
        self.hstS.Bind(wx.EVT_BUTTON, self.yedektenDon)
        

    def gizle(self, olay):
        self.Hide()

    def yedekAl(self, olay):
        print("Yedek Alındı!")
        os.system('cmd /c "python --version"')
        try:
            dosyaSec = wx.DirDialog(self, "Yedeğin yükleneceği dosyayı seçiniz: ", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        except Exception as hata:
            wx.MessageDialog(None, 'Dosya açılamadı!\n' + str(hata), 'Olmadı!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            dosyaSec.ShowModal()
            print(dosyaSec.GetPath())
            try:
                dsnTns = cx_Oracle.makedsn('DESKTOP-37KKSF2', 1521, 'XE')
                sistemBaglanti = cx_Oracle.connect(user='system', password='0r4ckL3!', dsn=dsnTns)
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Sistem olarak bağlanılamadı!\n' + str(hata), 'Hata!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                print("Bağlandı")
                try:
                    imlec=sistemBaglanti.cursor()
                except cx_Oracle.Error as hata:
                    wx.MessageDialog(None, 'İmlec çalışmadı!\n' + str(hata), 'İmlec Hatası!', wx.OK | wx.ICON_ERROR).ShowModal()
                else:
                    try:
                        imlec.execute("CREATE OR REPLACE DIRECTORY yol AS '"+ dosyaSec.GetPath() +"'")
                    except cx_Oracle.Error as hata:
                        wx.MessageDialog(None, 'Yol oluşturulamadı!\n' + str(hata), 'Yol Hatası!', wx.OK | wx.ICON_ERROR).ShowModal()
                    else:
                        print("oldu")
                        os.system('cmd /c "expdp yonetici/yonet schemas=yonetici directory=yol dumpfile=vtOdevDMP.dmp logfile=vtOdevLOG.log"')
                sistemBaglanti.close()
  
    def yedektenDon(self, olay):
        print("asd1")
        os.system('cmd /c "python --version"')
        try:
            dsnTns = cx_Oracle.makedsn('DESKTOP-37KKSF2', 1521, 'XE')
            sistemBaglanti = cx_Oracle.connect(user='system', password='0r4ckL3!', dsn=dsnTns)
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Sistem olarak bağlanılamadı!\n' + str(hata), 'Hata!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            print("Bağlandı")
            try:
                dosyaSec = wx.DirDialog(self, "Yedeğin yükleneceği dosyayı seçiniz: ", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
            except Exception as hata:
                wx.MessageDialog(None, 'Dosya açılamadı!\n' + str(hata), 'Olmadı!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                dosyaSec.ShowModal()
                print(dosyaSec.GetPath())
                try:
                    imlec=sistemBaglanti.cursor()
                except cx_Oracle.Error as hata:
                    wx.MessageDialog(None, 'İmlec çalışmadı!\n' + str(hata), 'İmlec Hatası!', wx.OK | wx.ICON_ERROR).ShowModal()
                else:
                    yonListe=[]
                    try:
                        imlec.execute("SELECT SID, SERIAL# FROM V$SESSION WHERE USERNAME='YONETICI'")
                    except cx_Oracle.Error as hata:
                        wx.MessageDialog(None, 'SID SERIAL alınmadı!\n' + str(hata), 'Hata!', wx.OK | wx.ICON_ERROR).ShowModal()
                    else:
                        for satir in imlec.fetchall():
                            yonListe.append(satir)
                        #print(str(yonListe[0][0])+' '+str(yonListe[0][1]))
                        print(yonListe)
                        try:
                            #imlec.execute("ALTER SYSTEM KILL SESSION '"+str(yonListe[0][0])+", "+str(yonListe[0][1])+"'")
                            imlec.execute("drop user YONETICI cascade")
                        except cx_Oracle.Error as hata:
                            wx.MessageDialog(None, 'Yönetici silinmedi!\n' + str(hata), 'Yönetici silme Hatası!', wx.OK | wx.ICON_ERROR).ShowModal()
                        else:
                            try:
                                imlec.execute('create user yonetici identified by "yonet"')
                                imlec.execute("GRANT READ, WRITE ON DIRECTORY yol TO yonetici")
                                imlec.execute("grant connect to yonetici")
                                imlec.execute("grant create session, grant any privilege to yonetici")
                                imlec.execute("grant unlimited tablespace to yonetici")
                                imlec.execute("grant create table to yonetici")
                            except cx_Oracle.Error as hata:
                                wx.MessageDialog(None, 'Yönetici Oluşturulamadı!\n' + str(hata), 'Yönetici oluşturma Hatası!', wx.OK | wx.ICON_ERROR).ShowModal()
                            else:
                                os.system('cmd /c "impdp yonetici/yonet schemas=yonetici directory=yol dumpfile=vtOdevDMP.dmp logfile=vtOdevLOG.log"')
                        

                    
            sistemBaglanti.close()

class yoneticiPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(1350, 37))
        self.kapat = wx.Button(self, label='Çıkış', pos=(7, 7))
        self.kapat.Bind(wx.EVT_BUTTON, parent.yntTemizle)    
        self.rctSl = wx.Button(self, label='Reçete Sil', pos=(85, 7))
        self.rctSl.Bind(wx.EVT_BUTTON, parent.yntRctSil)
        self.hstEkle = wx.Button(self, label='Hasta Ekle/Kaldır', pos=(163, 7))
        self.hstEkle.Bind(wx.EVT_BUTTON, parent.hstEkleSil)
        self.ydk = wx.Button(self, label='Yedekleme İşlemleri', pos=(277, 7))
        self.ydk.Bind(wx.EVT_BUTTON, parent.ydkF)   

####################################################


class receteEkle(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)
        self.rctHstSiraY=wx.StaticText(self,label='Hastanın Tc Kimlik Numarasını Girin: ',pos=(7,35))
        self.rctHstSiraYaz=wx.TextCtrl(self, pos=(205,31))
        self.rctHstSiraB=wx.Button(self,label='Getir',pos=(320,31))
        self.rctHstSiraB.Bind(wx.EVT_BUTTON, lambda olay: self.rctEKLE(olay,baglanti))

        
    def gizle(self, olay):
        self.Hide()

    def rctEKLE(self,olay,bag):
        print('reçete eklendi')
        self.tcYazi = self.rctHstSiraYaz.GetValue()
        #print(bag.version)
        try:
            imlec = bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmleç oluşturulamadı!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal() 
        else:
            #print('imleç oluşturuldu')
            try:
                imlec.execute("select * from yonetici.hasta where hastaTc='"+self.tcYazi+"'")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'TC numarası hatası!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                hst=imlec.fetchall()
                if len(hst)>0:
                    for satir in hst:
                        #print(satir)
                        self.sira=satir[0]
                        self.tc=satir[1]
                        self.ad = satir[2].strip()
                        self.soyad = satir[3].strip()

                else:
                    wx.MessageDialog(None, 'Böyle bir tc numarası yok!!', 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        wx.StaticText(self, label="Hastanın TC'si: "+str(self.tc),pos=(7,60))
        wx.StaticText(self, label="Hastanın Adı: "+str(self.ad),pos=(7,80))
        wx.StaticText(self, label="Hastanın Soyadı: "+str(self.soyad),pos=(7,100))

        self.ilaclarYazi=wx.TextCtrl(self,size=(200,200),pos=(200,60),style=wx.TE_MULTILINE)
        self.ilacGir=wx.Button(self,label='Reçeteyi Yaz',pos=(200,270))
        self.ilacGir.Bind(wx.EVT_BUTTON,lambda olay: self.rctEkleIslev(olay,bag,self.tc))

    def rctEkleIslev(self,olay,bag,tc):
        print(bag.version+"  "+tc)
        try:
            imlec=bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmleç hatası!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            ilaclar=self.ilaclarYazi.GetValue()
            self.tarih = date.today()
            #print(self.tarih)
            self.tarih = date.today() + relativedelta(months=+3)
            #print(self.tarih)
            try:
                imlec.execute("begin yonetici.receteEkle('"+ilaclar+"','"+tc+"',to_date('"+str(self.tarih)+"','YY-mm-dd')); end;")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Reçete eklenmedi!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                bag.commit()
                wx.MessageDialog(None, 'Reçete eklendi!!', 'Oldu!', wx.OK | wx.ICON_INFORMATION).ShowModal()

class hstEkleS(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)
        wx.StaticText(self,label='TC Sırası: ',pos=(11,41))
        self.tcSiraYazi=wx.TextCtrl(self,pos=(65,37))
        wx.StaticText(self, label='Adı: ', pos=(11, 81))
        self.adYazi = wx.TextCtrl(self, pos=(65, 77))
        wx.StaticText(self, label='Soyadı: ', pos=(11, 121))
        self.soyadYazi = wx.TextCtrl(self, pos=(65, 117))
        wx.StaticText(self, label='Doğum Tarihi: ', pos=(250, 41))
        self.dogumTarihi = wx.adv.CalendarCtrl(self, pos=(1051, 59))
        
        self.ekleDugmesi=wx.Button(self,label='Hasta Ekle',pos=(200,160))
        self.ekleDugmesi.Bind(wx.EVT_BUTTON,lambda olay: self.ekleIslev(olay,baglanti))

    def gizle(self, olay):
        self.Hide()
    
    def ekleIslev(self,olay,bag):
        tarih = self.dogumTarihi.GetDate()
        tarih = wx.DateTime(tarih).FormatISODate()
        tc = self.tcSiraYazi.GetValue()
        ad = self.adYazi.GetValue()
        soyad=self.soyadYazi.GetValue()
        print(tarih)
        #print(tc)
        #print(ad)
        #print(soyad)
        try:
            imlec=bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmlec oluşturulamadı!\n' + str(hata), 'Hata!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            try:
                imlec.execute("begin yonetici.hastaekle('"+ad+"','"+soyad+"',to_date('"+tarih+"','yyyy-mm-dd'),'"+tc+"'); end;")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Eklenmedi!\n' + str(hata), 'Hata!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                bag.commit()
                wx.MessageDialog(None, 'Hasta eklendi!', 'Oldu!', wx.OK | wx.ICON_INFORMATION).ShowModal()

class hstSilS(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)

        self.tumunuGor = wx.Button(self, label='Tüm Hastaları Gör', pos=(7, 35))
        self.tumunuGor.Bind(wx.EVT_BUTTON, lambda olay: self.hepsiniGor(olay, baglanti))
        
        self.hastaListesi = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(7, 120), size=(950, 300))
        self.hastaListesi.InsertColumn(0, 'Hasta Sıra', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(1, 'Hasta TC', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(2, 'Ad', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(3, 'Soyad', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(4, 'Doğum Tarihi', wx.LIST_FORMAT_RIGHT, width=100)
        self.hastaListesi.Hide()

        self.uyari = wx.StaticText(self, label='NOT: Silinirken "Hasta Sırası" göz önüne alınarak siliniyor.\nLütfen dikkatlice silme işlemini gerçekleştiriniz.', pos=(7, 80))
        self.uyari.Hide()
        self.silDugmesi = wx.Button(self, label='Sil', pos=(7, 420), size=(100, 30))
        self.silDugmesi.Bind(wx.EVT_BUTTON, lambda olay: self.hastaSil(olay, baglanti))
        self.silDugmesi.Hide()

    def gizle(self, olay):
        self.Hide()      

    def hepsiniGor(self, olay, bag):
        self.hastaListesi.DeleteAllItems()
        print(bag.version)
        try:
            imlec = bag.cursor()
            imlec.execute(
                'select * from yonetici.hasta')
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Hasta seçme işlemi yapılamadı!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            self.sayac = 0
            for satir in imlec.fetchall():
                #print(satir)
                self.hastaListesi.InsertItem(self.sayac, str(satir[0]))
                self.hastaListesi.SetItem(self.sayac, 1, str(satir[1]))
                self.hastaListesi.SetItem(self.sayac, 2, str(satir[2]))
                self.hastaListesi.SetItem(self.sayac, 3, str(satir[3]))
                self.hastaListesi.SetItem(self.sayac, 4, str(satir[4]))
                self.sayac = self.sayac + 1
            self.hastaListesi.Show()
            self.silDugmesi.Show()
            self.uyari.Show()
    
    def hastaSil(self, olay, bag):
        #print(self.receteListesi.GetItem(itemIdx=self.receteListesi.GetFocusedItem(), col=0).GetText())
        try:
            imlec = bag.cursor()
            imlec.execute("begin yonetici.hastasil("+ self.hastaListesi.GetItem(itemIdx=self.hastaListesi.GetFocusedItem(), col=0).GetText() +"); end;")
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Hasta Silinmedi!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            wx.MessageDialog(None, 'Başarı ile silindi!', 'BAŞARILI!', wx.OK | wx.ICON_INFORMATION).ShowModal()
            bag.commit()
            self.hepsiniGor(olay,bag)

class muayeneEkleS(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)

        wx.StaticText(self,label='Hasta Listesi',pos=(30,40))
        self.hastaListesi = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(7, 59), size=(500, 300))
        self.hastaListesi.InsertColumn(0, 'Hasta Sıra', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(1, 'Hasta TC', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(2, 'Ad', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(3, 'Soyad', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(4, 'Doğum Tarihi', wx.LIST_FORMAT_RIGHT, width=100)
        #self.hastaListesi.Hide()

        wx.StaticText(self,label='Hekim Listesi',pos=(537,40))
        self.hekimListesi = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(514, 59), size=(500, 300))
        self.hekimListesi.InsertColumn(0, 'Hekim Sıra', wx.LIST_FORMAT_RIGHT, width=75)
        self.hekimListesi.InsertColumn(1, 'Bolum Ad', wx.LIST_FORMAT_RIGHT, width=75)
        self.hekimListesi.InsertColumn(2, 'Ad', wx.LIST_FORMAT_RIGHT, width=75)
        self.hekimListesi.InsertColumn(3, 'Soyad', wx.LIST_FORMAT_RIGHT, width=75)
        #self.hekimListesi.Hide()

        
        try:
            hastaImlec = baglanti.cursor()
            hekimImlec=baglanti.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmleç oluşturulamadı!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            try:
                hastaImlec.execute("select * from yonetici.hasta")
                hekimImlec.execute("select hekimSira,bolumad,hekimad,hekimsoyad from yonetici.hekimler inner join yonetici.bolumler on hekimler.bolumsira=bolumler.bolumsira")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Hekim yada Hasta seçilemedi!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                self.sayac = 0
                for satir in hastaImlec.fetchall():
                    self.hastaListesi.InsertItem(self.sayac, str(satir[0]))
                    self.hastaListesi.SetItem(self.sayac, 1, str(satir[1]))
                    self.hastaListesi.SetItem(self.sayac, 2, str(satir[2]))
                    self.hastaListesi.SetItem(self.sayac, 3, str(satir[3]))
                    self.hastaListesi.SetItem(self.sayac, 4, str(satir[4]))
                    self.sayac = self.sayac + 1
                self.sayac=0
                for satir in hekimImlec.fetchall():
                    self.hekimListesi.InsertItem(self.sayac, str(satir[0]))
                    self.hekimListesi.SetItem(self.sayac, 1, str(satir[1]))
                    self.hekimListesi.SetItem(self.sayac, 2, str(satir[2]))
                    self.hekimListesi.SetItem(self.sayac, 3, str(satir[3]))
                    self.sayac = self.sayac + 1
        wx.StaticText(self,label='Muayene Tarihi',pos=(1081,40))
        self.muaTarihi = wx.adv.CalendarCtrl(self, pos=(1051, 59))
        self.sec=wx.Button(self,label='Seç',pos=(600,375))
        self.sec.Bind(wx.EVT_BUTTON, lambda olay:self.hekimHastaSec(olay,baglanti))

    def gizle(self, olay):
        self.Hide()

    def hekimHastaSec(self,olay,bag):
        hasta = self.hastaListesi.GetItem(itemIdx=self.hastaListesi.GetFocusedItem(), col=0).GetText()
        hekim = self.hekimListesi.GetItem(itemIdx=self.hekimListesi.GetFocusedItem(), col=0).GetText()
        tarih = self.muaTarihi.GetDate()
        tarih = wx.DateTime(tarih).FormatISODate()
        #print(hasta+" "+hekim+" "+str(tarih))  
        try:
            imlec=bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmleç oluşturulamadı!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            try:
                imlec.execute("begin yonetici.muaEkle("+hekim+","+hasta+",to_date('"+str(tarih)+"', 'yyyy-mm-dd')); end;")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Muayene eklenmedi!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                bag.commit()
                wx.MessageDialog(None, 'Muayene eklendi!!', 'Oldu!', wx.OK | wx.ICON_INFORMATION).ShowModal()

class muayeneSilS(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)

        wx.StaticText(self,label='Muayene Listesi',pos=(30,40))
        self.muayeneListesi = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(7, 59), size=(750, 300))
        self.muayeneListesi.InsertColumn(0, 'Muayene Sırası', wx.LIST_FORMAT_RIGHT, width=100)
        self.muayeneListesi.InsertColumn(1, 'Doktorun Adı', wx.LIST_FORMAT_RIGHT, width=100)
        self.muayeneListesi.InsertColumn(2, 'Doktorun Soyadı', wx.LIST_FORMAT_RIGHT, width=120)
        self.muayeneListesi.InsertColumn(3, 'Hasta Adı', wx.LIST_FORMAT_RIGHT, width=100)
        self.muayeneListesi.InsertColumn(4, 'Hasta Soyadı', wx.LIST_FORMAT_RIGHT, width=120)
        self.muayeneListesi.InsertColumn(5, 'TC', wx.LIST_FORMAT_RIGHT, width=100)
        self.muayeneListesi.InsertColumn(6, 'Muayene Tarihi', wx.LIST_FORMAT_RIGHT, width=100)
        self.goruntule(baglanti)
        self.muaSilD=wx.Button(self,label='Sil',pos=(200,371))
        self.muaSilD.Bind(wx.EVT_BUTTON,lambda olay: self.muaSil(olay,baglanti))

    def gizle(self, olay):
        self.Hide()
    
    def goruntule(self,bag):
        self.muayeneListesi.DeleteAllItems()
        try:
            imlec=bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmleç oluşturulamadı!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            try:
                imlec.execute("select * from yonetici.ayrintiliMuayene")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Muayeneler Seçilemedi!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                self.sayac = 0
                for satir in imlec.fetchall():
                    #print(satir)
                    self.muayeneListesi.InsertItem(self.sayac, str(satir[0]))
                    self.muayeneListesi.SetItem(self.sayac, 1, str(satir[1]))
                    self.muayeneListesi.SetItem(self.sayac, 2, str(satir[2]))
                    self.muayeneListesi.SetItem(self.sayac, 3, str(satir[3]))
                    self.muayeneListesi.SetItem(self.sayac, 4, str(satir[4]))
                    self.muayeneListesi.SetItem(self.sayac, 5, str(satir[5]))
                    self.muayeneListesi.SetItem(self.sayac, 6, str(satir[6]))
                    self.sayac = self.sayac + 1

    def muaSil(self,olay,bag):
        try:
            imlec = bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmlec hatası!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:    
            try:
                imlec.execute("begin yonetici.muayeneSil("+ self.muayeneListesi.GetItem(itemIdx=self.muayeneListesi.GetFocusedItem(), col=0).GetText() +"); end;")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Hasta Silinmedi!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                wx.MessageDialog(None, 'Başarı ile silindi!', 'BAŞARILI!', wx.OK | wx.ICON_INFORMATION).ShowModal()
                bag.commit()
                self.goruntule(bag)

class ameliyatEkleS(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)

        wx.StaticText(self,label='Hasta Listesi',pos=(30,40))
        self.hastaListesi = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(7, 59), size=(500, 300))
        self.hastaListesi.InsertColumn(0, 'Hasta Sıra', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(1, 'Hasta TC', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(2, 'Ad', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(3, 'Soyad', wx.LIST_FORMAT_RIGHT, width=75)
        self.hastaListesi.InsertColumn(4, 'Doğum Tarihi', wx.LIST_FORMAT_RIGHT, width=100)
        #self.hastaListesi.Hide()

        wx.StaticText(self,label='Hekim Listesi',pos=(537,40))
        self.hekimListesi = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(514, 59), size=(500, 300))
        self.hekimListesi.InsertColumn(0, 'Hekim Sıra', wx.LIST_FORMAT_RIGHT, width=75)
        self.hekimListesi.InsertColumn(1, 'Bolum Ad', wx.LIST_FORMAT_RIGHT, width=75)
        self.hekimListesi.InsertColumn(2, 'Ad', wx.LIST_FORMAT_RIGHT, width=75)
        self.hekimListesi.InsertColumn(3, 'Soyad', wx.LIST_FORMAT_RIGHT, width=75)
        #self.hekimListesi.Hide()

        
        try:
            hastaImlec = baglanti.cursor()
            hekimImlec=baglanti.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmleç oluşturulamadı!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            try:
                hastaImlec.execute("select * from yonetici.hasta")
                hekimImlec.execute("select hekimSira,bolumad,hekimad,hekimsoyad from yonetici.hekimler inner join yonetici.bolumler on hekimler.bolumsira=bolumler.bolumsira")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Hekim yada Hasta seçilemedi!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                self.sayac = 0
                for satir in hastaImlec.fetchall():
                    self.hastaListesi.InsertItem(self.sayac, str(satir[0]))
                    self.hastaListesi.SetItem(self.sayac, 1, str(satir[1]))
                    self.hastaListesi.SetItem(self.sayac, 2, str(satir[2]))
                    self.hastaListesi.SetItem(self.sayac, 3, str(satir[3]))
                    self.hastaListesi.SetItem(self.sayac, 4, str(satir[4]))
                    self.sayac = self.sayac + 1
                self.sayac=0
                for satir in hekimImlec.fetchall():
                    self.hekimListesi.InsertItem(self.sayac, str(satir[0]))
                    self.hekimListesi.SetItem(self.sayac, 1, str(satir[1]))
                    self.hekimListesi.SetItem(self.sayac, 2, str(satir[2]))
                    self.hekimListesi.SetItem(self.sayac, 3, str(satir[3]))
                    self.sayac = self.sayac + 1
        wx.StaticText(self,label='Muayene Tarihi',pos=(1081,40))
        self.muaTarihi = wx.adv.CalendarCtrl(self, pos=(1051, 59))
        self.sec=wx.Button(self,label='Seç',pos=(600,375))
        self.sec.Bind(wx.EVT_BUTTON, lambda olay:self.hekimHastaSec(olay,baglanti))

    def gizle(self, olay):
        self.Hide()

    def hekimHastaSec(self,olay,bag):
        hasta = self.hastaListesi.GetItem(itemIdx=self.hastaListesi.GetFocusedItem(), col=0).GetText()
        hekim = self.hekimListesi.GetItem(itemIdx=self.hekimListesi.GetFocusedItem(), col=0).GetText()
        tarih = self.muaTarihi.GetDate()
        tarih = wx.DateTime(tarih).FormatISODate()
        #print(hasta+" "+hekim+" "+str(tarih))  
        try:
            imlec=bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmleç oluşturulamadı!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            try:
                imlec.execute("begin yonetici.amlEkle("+hekim+","+hasta+",to_date('"+str(tarih)+"', 'yyyy-mm-dd')); end;")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Ameliyat eklenemedi!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                bag.commit()
                wx.MessageDialog(None, 'Ameliyat eklendi!!', 'Oldu!', wx.OK | wx.ICON_INFORMATION).ShowModal()

class ameliyatSilS(wx.Panel):
    def __init__(self, parent, baglanti):
        wx.Panel.__init__(self, parent=parent, pos=(0, 50), size=(1350, 600))
        self.geri = wx.Button(self, label='Geri', pos=(7, 7))
        self.geri.Bind(wx.EVT_BUTTON, self.gizle)

        wx.StaticText(self,label='Ameliyat Listesi',pos=(30,40))
        self.ameliyatListesi = wx.ListCtrl(self, style=wx.LC_REPORT, pos=(7, 59), size=(750, 300))
        self.ameliyatListesi.InsertColumn(0, 'Ameliyat Sırası', wx.LIST_FORMAT_RIGHT, width=100)
        self.ameliyatListesi.InsertColumn(1, 'Doktorun Adı', wx.LIST_FORMAT_RIGHT, width=100)
        self.ameliyatListesi.InsertColumn(2, 'Doktorun Soyadı', wx.LIST_FORMAT_RIGHT, width=120)
        self.ameliyatListesi.InsertColumn(3, 'Hasta Adı', wx.LIST_FORMAT_RIGHT, width=100)
        self.ameliyatListesi.InsertColumn(4, 'Hasta Soyadı', wx.LIST_FORMAT_RIGHT, width=120)
        self.ameliyatListesi.InsertColumn(5, 'TC', wx.LIST_FORMAT_RIGHT, width=100)
        self.ameliyatListesi.InsertColumn(6, 'Ameliyat Tarihi', wx.LIST_FORMAT_RIGHT, width=100)
        self.goruntule(baglanti)
        self.muaSilD=wx.Button(self,label='Sil',pos=(200,371))
        self.muaSilD.Bind(wx.EVT_BUTTON,lambda olay: self.amlSil(olay,baglanti))

    def gizle(self, olay):
        self.Hide()
    
    def goruntule(self,bag):
        self.ameliyatListesi.DeleteAllItems()
        try:
            imlec=bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmleç oluşturulamadı!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            try:
                imlec.execute("select * from yonetici.ayrintiliAmeliyat")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Muayeneler Seçilemedi!!\n' + str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                self.sayac = 0
                for satir in imlec.fetchall():
                    #print(satir)
                    self.ameliyatListesi.InsertItem(self.sayac, str(satir[0]))
                    self.ameliyatListesi.SetItem(self.sayac, 1, str(satir[1]))
                    self.ameliyatListesi.SetItem(self.sayac, 2, str(satir[2]))
                    self.ameliyatListesi.SetItem(self.sayac, 3, str(satir[3]))
                    self.ameliyatListesi.SetItem(self.sayac, 4, str(satir[4]))
                    self.ameliyatListesi.SetItem(self.sayac, 5, str(satir[5]))
                    self.ameliyatListesi.SetItem(self.sayac, 6, str(satir[6]))
                    self.sayac = self.sayac + 1

    def amlSil(self,olay,bag):
        try:
            imlec = bag.cursor()
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'İmlec hatası!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:    
            try:
                imlec.execute("begin yonetici.amlSil("+ self.ameliyatListesi.GetItem(itemIdx=self.ameliyatListesi.GetFocusedItem(), col=0).GetText() +"); end;")
            except cx_Oracle.Error as hata:
                wx.MessageDialog(None, 'Hasta Silinmedi!!\n'+str(hata), 'HATA!', wx.OK | wx.ICON_ERROR).ShowModal()
            else:
                wx.MessageDialog(None, 'Başarı ile silindi!', 'BAŞARILI!', wx.OK | wx.ICON_INFORMATION).ShowModal()
                bag.commit()
                self.goruntule(bag)

class hizmetliPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(1350, 37))
        self.kapat = wx.Button(self, label='Çıkış', pos=(7, 7))
        self.kapat.Bind(wx.EVT_BUTTON, parent.hizmetliEkraniTemizle)
        self.rctSl = wx.Button(self, label='Reçete Sil', pos=(85, 7))
        self.rctSl.Bind(wx.EVT_BUTTON, parent.rctSilEkle)
        self.rctEk = wx.Button(self, label='Reçete Ekle', pos=(163, 7))
        self.rctEk.Bind(wx.EVT_BUTTON, parent.rctEkle)
        self.hstEK = wx.Button(self, label='Hasta Ekle', pos=(246, 7))
        self.hstEK.Bind(wx.EVT_BUTTON, parent.hstEkleI)
        self.hstSl = wx.Button(self, label='Hasta Sil', pos=(325, 7))
        self.hstSl.Bind(wx.EVT_BUTTON, parent.hstSilI)
        self.muaEkle = wx.Button(self, label='Muayene Ekle', pos=(403, 7))
        self.muaEkle.Bind(wx.EVT_BUTTON, parent.muaEkleI)
        self.muaSil = wx.Button(self, label='Muayene Sil', pos=(500, 7))
        self.muaSil.Bind(wx.EVT_BUTTON, parent.muaSilI)
        self.amlEkle = wx.Button(self, label='Ameliyat Ekle', pos=(588, 7))
        self.amlEkle.Bind(wx.EVT_BUTTON, parent.amlEkleI)
        self.amlSil = wx.Button(self, label='Ameliyat Sil', pos=(683, 7))
        self.amlSil.Bind(wx.EVT_BUTTON, parent.amlSilI)
        self.hstaTxt = wx.Button(self, label='Yazı olarak Hasta Çıkar/Ekle', pos=(768, 7))
        self.hstaTxt.Bind(wx.EVT_BUTTON, parent.hizHstES)



####################################################

class giris(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, size=(1350, 600))
        self.izgara = wx.GridBagSizer(0, 0)
        brdr = 2
        self.yaziKullaniciAdi = wx.StaticText(self,label='Kullanıcı Adı:')
        self.izgara.Add(self.yaziKullaniciAdi, pos=(0, 0), flag=wx.ALL, border=brdr)
        self.girdiKullaniciAdi = wx.TextCtrl(self)
        self.izgara.Add(self.girdiKullaniciAdi, pos=(0, 1), span=(1, 4),flag=wx.EXPAND | wx.ALL | wx.LEFT, border=brdr)

        self.yaziSifre = wx.StaticText(self, label='Şifre:')
        self.izgara.Add(self.yaziSifre, pos=(1, 0), flag=wx.ALL, border=brdr)
        self.girdiSifre = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.izgara.Add(self.girdiSifre, pos=(1, 1), span=(1, 3), flag=wx.EXPAND | wx.ALL, border=brdr)

        self.kapat = wx.Button(self, label='Kapat')
        self.kapat.Bind(wx.EVT_BUTTON, parent.uygKapat)
        self.izgara.Add(self.kapat, pos=(2, 3), span=(1, 2), flag=wx.ALL | wx.BOTTOM | wx.LEFT, border=brdr)
        self.kapat = wx.Button(self, label='Bağlan')
        self.kapat.Bind(wx.EVT_BUTTON, parent.gir)
        self.izgara.Add(self.kapat, pos=(2, 5), span=(1, 2), flag=wx.ALL | wx.BOTTOM | wx.LEFT, border=brdr)
        parent.SetSizer(self.izgara)

class kullaniciGirisi(wx.Frame):
    def __init__(self, miras, baslik, genislik, yukseklik):
        super().__init__(parent=miras, title=baslik, size=(genislik, yukseklik))
        self.InitUI()
        self.baglanti = None
        self.Centre()
        self.Show()

    def InitUI(self):
        #self.hkmPanel = hekimPanel(self)
        #self.hkmPanel.Hide()

        self.kllPanel = giris(self)
        #self.ver = wx.StaticText(self)
        #self.ver.Hide()
        
    def uygKapat(self,olay):
        self.Destroy()

    def gir(self,olay):
        self.kuAd = self.kllPanel.girdiKullaniciAdi.GetValue()
        self.sfre = self.kllPanel.girdiSifre.GetValue()
        try:
            self.baglanti = veriTabaniBaglantisi(self.kuAd, self.sfre)
            self.ver = wx.StaticText(self, label="Oracle Sürüm: " + str(self.baglanti.version), pos=(1100, 700))
        except cx_Oracle.Error as hata:
            wx.MessageDialog(None, 'Sistem olarak bağlanılamadı!\n' + str(hata), 'Hata!', wx.OK | wx.ICON_ERROR).ShowModal()
        else:
            if self.baglanti != None and self.kuAd == 'hekim':
                self.hkmPanel = hekimPanel(self)
                self.muaGor = muayeneGoruntule(self, self.baglanti)
                self.muaGor.Hide()
                """ self.hstGor = hastaGoruntule(self, self.baglanti)
                self.hstGor.Hide() """
                self.amlGor = ameliyatGoruntule(self, self.baglanti)
                self.amlGor.Hide()
                self.rctGor = receteGoruntule(self, self.baglanti)
                self.rctGor.Hide()
                self.rctYaz = receteYaz(self, self.baglanti)
                self.rctYaz.Hide()
                self.kllPanel.Hide()
                self.SetTitle('Hekim Kullanıcı Arayüzü')
                self.kllPanel.girdiKullaniciAdi.SetValue("")
                self.kllPanel.girdiSifre.SetValue("")
            elif self.baglanti != None and self.kuAd == 'yonetici':
                print(self.kuAd + " bağlandı.")
                self.yntPanel = yoneticiPanel(self)
                self.yntRctSl = yntReceteSil(self, self.baglanti)
                self.yntRctSl.Hide()
                self.hstES = hstaSilEkle(self, self.baglanti)
                self.hstES.Hide()
                self.ydk = ydkAlDon(self, self.baglanti)
                self.ydk.Hide()
                self.kllPanel.Hide()
                self.SetTitle('Yönetici Kullanıcı Arayüzü')
                self.kllPanel.girdiKullaniciAdi.SetValue("")
                self.kllPanel.girdiSifre.SetValue("")
            elif self.baglanti != None and self.kuAd == 'hizmetli':
                print(self.kuAd + " bağlandı.")
                self.hzmtliPnl = hizmetliPanel(self)
                self.hstES = hstaSilEkle(self, self.baglanti)
                self.hstES.Hide()
                self.yntRctSl = yntReceteSil(self, self.baglanti)
                self.yntRctSl.Hide()
                self.rctEkle2 = receteEkle(self, self.baglanti)
                self.rctEkle2.Hide()
                self.hstEkle2=hstEkleS(self,self.baglanti)
                self.hstEkle2.Hide()
                self.hstSil2 = hstSilS(self, self.baglanti)
                self.hstSil2.Hide()
                self.muaEkle2=muayeneEkleS(self,self.baglanti)
                self.muaEkle2.Hide()
                self.muaSil2=muayeneSilS(self,self.baglanti)
                self.muaSil2.Hide()
                self.amlEkle2=ameliyatEkleS(self,self.baglanti)
                self.amlEkle2.Hide()
                self.amlSil2=ameliyatSilS(self,self.baglanti)
                self.amlSil2.Hide()
                #self.hstYazi=hstaSilEkle(self,)
                self.SetTitle('Danışman İşlemleri')
                self.kllPanel.Hide()
                self.kllPanel.girdiKullaniciAdi.SetValue("")
                self.kllPanel.girdiSifre.SetValue("")

        

    def hizmetliEkraniTemizle(self,olay):
        self.SetTitle('Kullanıcı Girişi')
        self.ver.Destroy()
        self.hstES.Hide()
        self.yntRctSl.Hide()
        self.rctEkle2.Hide()
        self.hstEkle2.Hide()
        self.hstSil2.Hide()
        self.muaEkle2.Hide()
        self.muaSil2.Hide()
        self.amlEkle2.Hide()
        self.amlSil2.Hide()
        self.hzmtliPnl.Destroy()
        self.kllPanel.Show()
    
    def hizHstES(self, olay):
        self.yntRctSl.Hide()
        self.rctEkle2.Hide()
        self.hstEkle2.Hide()
        self.hstSil2.Hide()
        self.muaEkle2.Hide()
        self.muaSil2.Hide()
        self.amlEkle2.Hide()
        self.amlSil2.Hide()
        self.hstES.Show()

    def rctSilEkle(self,olay):
        self.hstES.Hide()
        self.rctEkle2.Hide()
        self.hstEkle2.Hide()
        self.hstSil2.Hide()
        self.muaEkle2.Hide()
        self.muaSil2.Hide()
        self.amlEkle2.Hide()
        self.amlSil2.Hide()
        self.yntRctSl.Show()

    def rctEkle(self, olay):
        self.hstES.Hide()
        self.yntRctSl.Hide()
        self.hstEkle2.Hide()
        self.hstSil2.Hide()
        self.muaEkle2.Hide()
        self.muaSil2.Hide()
        self.amlEkle2.Hide()
        self.amlSil2.Hide()
        self.rctEkle2.Show()
    
    def hstEkleI(self,olay):
        self.hstES.Hide()
        self.yntRctSl.Hide()
        self.rctEkle2.Hide()
        self.hstSil2.Hide()
        self.muaEkle2.Hide()
        self.muaSil2.Hide()
        self.amlEkle2.Hide()
        self.amlSil2.Hide()
        self.hstEkle2.Show()
    
    def hstSilI(self,olay):
        self.hstES.Hide()
        self.yntRctSl.Hide()
        self.rctEkle2.Hide()
        self.hstEkle2.Hide()
        self.muaEkle2.Hide()
        self.muaSil2.Hide()
        self.amlEkle2.Hide()
        self.amlSil2.Hide()
        self.hstSil2.Show()
    
    def muaEkleI(self,olay):
        self.hstES.Hide()
        self.yntRctSl.Hide()
        self.rctEkle2.Hide()
        self.hstEkle2.Hide()
        self.hstSil2.Hide()
        self.muaSil2.Hide()
        self.amlEkle2.Hide()
        self.amlSil2.Hide()
        self.muaEkle2.Show()

    def muaSilI(self,olay):
        self.hstES.Hide()
        self.yntRctSl.Hide()
        self.rctEkle2.Hide()
        self.hstEkle2.Hide()
        self.hstSil2.Hide()
        self.muaEkle2.Hide()
        self.amlEkle2.Hide()
        self.amlSil2.Hide()
        self.muaSil2.Show()

    def amlEkleI(self, olay):
        self.hstES.Hide()
        self.yntRctSl.Hide()
        self.rctEkle2.Hide()
        self.hstEkle2.Hide()
        self.hstSil2.Hide()
        self.muaSil2.Hide()
        self.muaEkle2.Hide()
        self.amlSil2.Hide()
        self.amlEkle2.Show()

    def amlSilI(self, olay):
        self.hstES.Hide()
        self.yntRctSl.Hide()
        self.rctEkle2.Hide()
        self.hstEkle2.Hide()
        self.hstSil2.Hide()
        self.muaSil2.Hide()
        self.muaEkle2.Hide()
        self.amlEkle2.Hide()
        self.amlSil2.Show()



##############################################################
    def yntTemizle(self, olay):
        self.SetTitle('Kullanıcı Girişi')
        self.yntRctSl.Destroy()
        self.hstES.Destroy()
        self.ydk.Destroy()
        self.ver.Destroy()
        self.yntPanel.Destroy()
        self.kllPanel.Show()

    def hstEkleSil(self, olay):
        self.yntRctSl.Hide()
        self.ydk.Hide()
        self.hstES.Show()
        
    def yntRctSil(self, olay):
        self.hstES.Hide()
        self.ydk.Hide()
        self.yntRctSl.Show()

    def ydkF(self, olay):
        self.hstES.Hide()
        self.yntRctSl.Hide()
        self.ydk.Show()
##############################################################
    def hkmTemizle(self, olay):
        self.SetTitle('Kullanıcı Girişi')
        self.ver.Destroy()
        #self.hstGor.Destroy()
        self.rctGor.Destroy()
        self.rctYaz.Destroy()
        self.muaGor.Destroy()
        self.amlGor.Destroy()
        self.hkmPanel.Destroy()
        self.kllPanel.Show()

    """ def hastaGor(self, olay):
        self.muaGor.Hide()
        self.amlGor.Hide()
        self.rctGor.Hide()
        self.rctYaz.Hide()
        self.hstGor.Show() """
        
    def mynGor(self, olay):
        #self.hstGor.Hide()
        self.amlGor.Hide()
        self.rctGor.Hide()
        self.rctYaz.Hide()
        self.muaGor.Show()

    def amelGor(self, olay):
        #self.hstGor.Hide()
        self.muaGor.Hide()
        self.rctGor.Hide()
        self.rctYaz.Hide()
        self.amlGor.Show()
    
    def rcteGor(self, olay):
        #self.hstGor.Hide()
        self.muaGor.Hide()
        self.amlGor.Hide()
        self.rctYaz.Hide()
        self.rctGor.Show()

    def rcteYaz(self, olay):
        #self.hstGor.Hide()
        self.muaGor.Hide()
        self.amlGor.Hide()
        self.rctGor.Hide()
        self.rctYaz.Show()
        
        



if __name__ == "__main__":
    uyg = wx.App()
    kGirisi = kullaniciGirisi(None, 'Kullanıcı Girişi', 1366, 764)
    uyg.MainLoop()
    kGirisi.Destroy()
    uyg.Destroy()