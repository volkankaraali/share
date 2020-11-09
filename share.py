from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv 

browser=webdriver.Chrome() #chrome ile açmak için

shareLink='https://finans.mynet.com/borsa/canliborsa#ALL'
browser.get(shareLink)

#tüm hisseler scroll yapılınca geldiği için önce sayfa son hisse gelene kadar aşağı scroll yapılır 
for i in range(1,15):
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)") #body kadar scrol yapar.
    time.sleep(1) #her scrollda 1 saniye bekler ve 15 kere tekrar yapar.

#tüm hisseler scroll yapıldıktan sonra html kodları parse edilir
html = browser.page_source
soup = BeautifulSoup(html,'html.parser')
shares=soup.find_all('tr',{'class':'sortTR'}) #her bir hissenin tutulduğu satır. 

#csv dosya yazma
file=open('shares.csv','w',newline='',encoding='utf-8') #'w' write- veriyi excele yazmak için kullanıldı.newline ile exceldeki boşluk silindi. 
writer=csv.writer(file,delimiter=';') #delimiter ';' ile csvde sutun olarak ayırır.
#excelde satır başlıkları 
writer.writerow(['Hisse Adi','Son Fiyat','En Dusuk','En Yuksek'])

for share in shares:
    #hisselerin tutulduğu satırda istenilen verilerin classları aynı olduğundan index olarak kaçıncı değerde olduğu bulunur. 
    shareLine=share.find_all('td',{'class':'text-center static null'})
    
    shareName=shareLine[0].text.strip() 
    shareValue=shareLine[2].text.strip() 
    shareMin=shareLine[6].text.strip()
    shareMax=shareLine[7].text.strip()

    print(shareName+shareValue+shareMin+shareMax)
    writer.writerow([shareName,shareValue,shareMin,shareMax])

file.close()
#browser kapanır.
browser.close()
