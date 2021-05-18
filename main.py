from flask import Flask, render_template, request # importuojam klases, flask yra pagrindinis frameworkas,
# kuris leidzia dirbti su web, gauta python info perkelti i html. render_template sugeneruoja mum html koda.
from selenium import webdriver # webdriveris gauna komandas (pvz paimti teksta) ir vygdo tas komandas svetaineje
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException  
import pyrebase
PATH = "C:\webdrivers\chromedriver.exe" # vieta kur randasi chrome narsykles driveris
options = webdriver.ChromeOptions() # chrome driverio nustatymai
options.add_argument("--disable-web-security") # kad leistu be jokiu kluciu imti informacija is svetaines
options.add_argument("--disable-site-isolation-trials")
options.headless = True # padaro, kad svetaine butu paleidziama fone (jos nesimato)

app = Flask(__name__) # sukuriamas flask kintamanasis

firebaseConfig = {'apiKey': "AIzaSyDWmSRRcsbpXOp2SgaO2lS8R6dKsoNzv9o",
    'authDomain': "python-f5bc6.firebaseapp.com",
    'projectId': "python-f5bc6",
    'storageBucket': "python-f5bc6.appspot.com",
    'messagingSenderId': "408299245563",
    'appId': "1:408299245563:web:04887a8c9369f02a1dc55e",
    "databaseURL": "https://python-f5bc6-default-rtdb.europe-west1.firebasedatabase.app/",}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
db.remove()

@app.route('/updateData', methods=['POST'])
def updateData(): # metodas, kuris grazina musu sugeneruota teksta
    
    inputVal = request.form.get("inputVal") # gauna irasyta teksta is HTML input laukelio
    shops = [
        {
        'url': 'https://www.mobili.lt/lt/greita_paieska.html?searc=',
        'product': '//*[@id="body_inner"]/table/tbody/tr/td[2]/div/div[2]/div[2]/table/tbody/tr/td[1]/a',
        'name': '//*[@id="tlf_info_modelis"]',
        'price': '//*[@id="phone_price2"]/div[1]/span',
        'img': '//*[@id="ti_img_kaina"]/img',
        'logo': '//*[@id="head_container"]/div[1]/a/img'
        },
        {
        'url': 'https://www.mp.lt/paieska/?search=',
        'product': '//*[@id="product_items"]/div/div[1]/a',
        'name': '//*[@id="products_detailed"]/div[1]/div/div[2]/h1',
        'price': '//*[@id="products_add2cart"]/form/div[3]/div[1]/div',
        'img': '//*[@id="slider"]/div/div/div[2]/a/img',
        'logo': '//*[@id="logo"]/a/img'
        },
    ]
    length = len(shops)
    name = []
    href = []
    price = []
    img = []
    logo = []

    for x in range(length):
        URL = shops[x]['url'] + inputVal # pilnas URL

        driver = webdriver.Chrome(PATH, options=options) # nustatom chrome narsykles nustatymus
        driver.get(URL) # paleidziame svetaine su savo norimu URL ir nustatymais
        driver.find_element_by_xpath(shops[x]['product']).click()
        name.append(driver.find_element_by_xpath(shops[x]['name']).text) # paima is DOM elemento teksta
        price.append(driver.find_element_by_xpath(shops[x]['price']).text)
        href.append(driver.current_url)
        img.append(str(driver.find_element_by_xpath(shops[x]['img']).get_attribute("src")))
        logo.append(str(driver.find_element_by_xpath(shops[x]['logo']).get_attribute("src")))
        data = {'name': name[x], 'price': price[x], 'img': img[x], 'logo': logo[x], 'href': href[x]}
        db.push(data)
        driver.close()

    name = []
    href = []
    price = []
    img = []
    logo = []

    phones = db.get()
    for phone in phones.each():
        name.append(phone.val()['name'])
        price.append(phone.val()['price'])
        href.append(phone.val()['href'])
        img.append(phone.val()['img'])
        logo.append(phone.val()['logo'])
    
    return render_template('data.html',name=name, href=href, price=price, img=img, logo=logo, length=length)
@app.route('/')
def hello_world(): # pagrinidis metodas
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True) # iskvieciame python scripta, paleidziame programa