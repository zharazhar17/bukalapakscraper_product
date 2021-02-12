import sqlite3, time, os, json, sys, datetime, requests, string, re
from random import randint

# from bs4 import BeautifulSoup

import config as cfg
import urllib.request
from urllib.parse import urlencode

import pandas as pd 
from base64 import b64encode
# import MySQLdb as mdb
# import xlwt 
# from xlwt import Workbook

#=========FIGLET========
import sys

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format
#======== FIGLET=======
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException, \
    UnexpectedAlertPresentException, ElementNotVisibleException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from sqlite3 import Error
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
timeout = 30
isLoggedIn = False
# url = sys.argv[1]
username = "test"

def copyright_apply(input_image_path,
                   outputname):

    original_image = Image.open(cfg.app['dataPath']+input_image_path)
    watermark = Image.open(cfg.app['dataPath']+'gratisongkir.png')

    watermark_width, watermark_height = watermark.size

    x, y = original_image.size
    margin = 40

    # left top
    position = (x - margin - watermark_width, y - margin - watermark_height)

    image_with_watermark = Image.new('RGBA', (x, y), (0, 0, 0, 0))
    image_with_watermark.paste(original_image, (0, 0))
    image_with_watermark.paste(watermark, position, mask=watermark)
    # image_with_watermark.show()
    image_with_watermark.save(cfg.app['dataPath']+'afterwatermark/'+outputname)



    client_id = '9a605c106a0db6f'

    headers = {"Authorization": "Client-ID 9a605c106a0db6f"}

    api_key = 'c66f2796f93a241e4e75dfbe23d7a2b2cd55d96a'

    url = "https://api.imgur.com/3/upload.json"

    j1 = requests.post(
        url, 
        headers = headers,
        data = {
            'key': api_key, 
            'image': b64encode(open(cfg.app['dataPath']+"afterwatermark/"+outputname, 'rb').read()),
            'type': 'base64',
            'name': '1.jpg',
            'title': 'Picture no. 1'
        }
    )

    parse = json.loads(j1.text)
    print("DONE SUKSES UPLOAD IMGURl GET LINK "+str(parse['data']['link']))
    return str(parse['data']['link'])
def official(typenya,urltoko, limit_getscrap,filenamenya):
    
    driverPath = cfg.app['driverPath']
    dataPath = cfg.app['dataPath']+'profile/'+username
    print(dataPath)
    ch_options = webdriver.ChromeOptions()
    #ch_options.add_argument("user-data-dir=" + dataPath)
    # #ch_options.add_argument("--user-data-dir="+dataPath+"")
    ch_options.add_argument("--disable-dev-shm-usage")
    if cfg.app['headless']:
        ch_options.add_argument('headless')

    if cfg.app['no-sandbox']:
        ch_options.add_argument('no-sandbox')

    agent = cfg.agent[randint(0, len(cfg.agent)-1)]
    print(agent)
    ch_options.add_argument(
        'user-agent='+agent)
    driver = webdriver.Chrome(executable_path=driverPath, chrome_options=ch_options)

    
    if typenyanih == "toko":
        print("TOKO")
        driver.get(str(urltoko))
        time.sleep(2)
        link_list_prod = []
        limit_item = limit_getscrap
        nom = 0

        nama_product = []
        deskripsi_product = []
        kategory_code = []
        berat_arr = []
        minimum_pemesanan = []
        nomor_etalase = []
        waktu_proses = []
        kondisi = []
        gambar_1 = []
        gambar_2 = []
        gambar_3 = []
        gambar_4 = []
        gambar_5 = []
        url_video1 = []
        url_video2 = []
        url_video3 = []
        sku_name = []

        status_arr = []
        jumlah_stok = []
        harga_arr = []
        asuransi_arr = []

        try:
            products = driver.find_elements_by_css_selector('a[class="c-product-card__name js-track-ab-hide-review js-tracker-product-link"]')
            for prd in products:
                link_list_prod.append(prd.get_attribute('href'))
            print("Selanjutnya")
        except NoSuchElementException:
            print("Failed get product url list")

        for datanya in link_list_prod:
            nom = nom + 1
            print("NOMER NYA => "+str(nom))

            if nom == int(limit_item):
                break
            else:
                # eksekusi(driver, datanya, "TEST")
                namefolder = "TEST"
                print(str(datanya))
                driver.get(datanya)
                time.sleep(2)
                if not os.path.exists(cfg.app['dataPath']+""+namefolder):
                            os.makedirs(cfg.app['dataPath']+""+namefolder)
                print("======================= START DATA ================")
                while True:
                    time.sleep(2)
                    minimum_pemesanan.append("1")
                    nomor_etalase.append("-")
                    waktu_proses.append("Tidak ada PreOrder")
                    asuransi_arr.append("ya")
                    status_arr.append("1")
                    kategory_code.append("-")
                    gambar_2.append("-")
                    gambar_3.append("-")
                    gambar_4.append("-")
                    gambar_5.append("-")
                    url_video1.append("-")
                    url_video2.append("-")
                    url_video3.append("-")
                    sku_name.append("SKU NYA TIDAK ADA DUMMY")

                    try:
                        name_product = driver.find_element_by_css_selector('h1[class="c-main-product__title u-txt--large"]').text
                        nama_product.append(str(name_product))
                        print(str(name_product))
                        pass
                    except NoSuchElementException:
                        nama_product.append("-")
                        print("Failed Get Name Product")
                        pass
                    
                    time.sleep(2)
                    try:
                        harga = driver.find_element_by_css_selector('div[class="c-product-price -original -main"]').text
                        harga_arr.append(str(harga))
                        print("HARGA NORMAL => "+str(harga))
                        pass
                    except NoSuchElementException:
                        print("No Harga Normal")
                        pass
                    time.sleep(2)
                    try:
                        harga = driver.find_element_by_css_selector('div[class="c-product-price -discounted -main"]').text
                        harga_arr.append(str(harga))                       
                        print("HARGA DISKON =>"+str(harga))
                        pass
                    except NoSuchElementException:
                        print("Failed get diskon harga")
                        pass
                    time.sleep(2)
                    try:
                        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                        # driver.execute_script("window.scrollTo(10,20, document.body.scrollHeight)")
                        # driver.execute_script("document.body.style.zoom='50%'")
                        # time.sleep(2)
                        
                        description = driver.find_element_by_css_selector('div[class="c-information__description-txt"]').text
                        deskripsi_product.append(str(description))
                        print("DESKRIPSI => "+str(description))
                        pass
                    except NoSuchElementException:
                        deskripsi_product.append("-")
                        print("Faield Get Description Product")
                        pass
                    
                    
                    time.sleep(2)
                    try:
                        #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                        kategory = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[1]/td[2]/a')
                        
                        print("KATEGORY => "+str(kategory.text))
                        pass
                    except NoSuchElementException:
                        print("Failed get kategory Name")
                        pass

                    try:
                        #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                        berat = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[2]/td[2]')
                        berat_arr.append(str(berat.text))
                        print("BERAT => "+str(berat.text))
                        pass
                    except NoSuchElementException:
                        berat_arr.append("-")
                        print("Failed get berat barang")
                        pass
                    
                    try:
                        stoknya = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[4]').text
                        if stoknya == "Tersedia > 10 stok barang":
                            jumlah_stok.append(">10")
                        else:
                            jumlah_stok.append(">50")
                    except:
                        jumlah_stok.append("-")
                        print("Failed get stok")
                    try:
                        #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                        asal = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[3]/td[2]')
                        print("Asal Barang => "+str(asal.text))
                        pass
                    except NoSuchElementException:
                        print("Failed get asal barang")


                    try:
                        kondi = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div').text
                        print("Kondisi =>"+str(kondi))
                        if str(kondi) == "BARU":
                            kondisi.append(str(kondi))
                        else:
                            kondisi.append("-")
                    except:
                        kondisi.append("-")
                        print("Failed get kondisi barang")
                    try:
                        terjual = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[1]/div[1]/div/span').text
                        print("TERJUAL => "+str(terjual))
                        pass
                    except NoSuchElementException:
                        print("Faield get data terjual")
                        pass

                    try:
                        #driver.execute_script("document.body.style.zoom='100%'")
                        image = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/section[1]/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/picture/img')
                        gambar_1.append(str(image.get_attribute('src')))

                        print(str("IMAGE 1 => "+image.get_attribute('src')))
                        urllib.request.urlretrieve(str(image.get_attribute('src')), cfg.app['dataPath']+""+str(namefolder)+"/"+str(randint(3, 9999))+".png")
                        time.sleep(2)
                        break
                    except NoSuchElementException:
                        gambar_1.append("-")
                        print("Failed get images url")
                        break
                    
                print("======================= END DATA ================")

        print("TOTAL LINK => "+str(len(link_list_prod)))

        df = pd.DataFrame({
                        
                        'Nama Product': nama_product,
                        'Deskripsi Product': deskripsi_product,
                        'Kategory Kode': kategory_code,
                        'Berat *(Gram)': berat_arr,
                        'Minimum Pemesanan': minimum_pemesanan,
                        'Nomor Etalase': nomor_etalase,
                        'Waktu Proses Preorder': waktu_proses,

                        'Kondisi': kondisi,
                        'Gambar 1': gambar_1,
                        'Gambar 2': gambar_2,
                        'Gambar 3': gambar_3,
                        'Gambar 4': gambar_4,
                        'URL Video Produk 1': url_video1,
                        'URL Video Produk 2': url_video2,
                        'URL Video Produk 3': url_video3,
                        'SKU Name': sku_name,
                        
                        'Status': status_arr,
                        'Jumlah Stok': jumlah_stok,
                        'Harga': harga_arr,
                        'Asuransi Pengiriman': asuransi_arr})
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(str(filenamenya)+'.xlsx', engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Hasil', index=False)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
    else:
        typenya = sys.argv[1]
        search = sys.argv[2]
        
        limit = sys.argv[3]
        limit_item = sys.argv[4]
        driver.get("https://www.bukalapak.com/products?from=omnisearch&from_keyword_history=false&search%5Bkeywords%5D="+str(search)+"&search_source=omnisearch_keyword&source=navbar")

        list_url = []

        nama_product = []
        deskripsi_product = []
        kategory_code = []
        berat_arr = []
        minimum_pemesanan = []
        nomor_etalase = []
        waktu_proses = []
        kondisi = []
        gambar_1 = []
        gambar_2 = []
        gambar_3 = []
        gambar_4 = []
        gambar_5 = []
        url_video1 = []
        url_video2 = []
        url_video3 = []
        sku_name = []

        status_arr = []
        jumlah_stok = []
        harga_arr = []
        asuransi_arr = []


        get_paginate = driver.find_elements_by_css_selector('a[class="bl-pagination__link"]')
        last_paginate = driver.find_element_by_css_selector('#product-explorer-container > div > div > div.bl-flex-item.bl-product-list-wrapper > div > div:nth-child(2) > nav > ul > li:nth-child(9) > a').text
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        print(int(last_paginate))
        no=0
        nom =0
        finish = False
        while no < int(last_paginate):
            no = no + 1

            driver.get("https://www.bukalapak.com/products?page="+str(no)+"&search%5Bkeywords%5D="+str(search)+"")
            if no == int(limit):
                finish = True
            if finish == False:
                try:
                    get_link = driver.find_elements_by_css_selector('p[class="bl-text bl-text--body-small bl-text--ellipsis__2"]>a[class="bl-link"]')
                    for urlnya in get_link:
                        list_url.append(urlnya.get_attribute('href'))
                    time.sleep(2)
                    print("Selanjutnya")
                except NoSuchElementException:
                    print("Failed Get Product Link")
            else:
                
                if nom == int(limit_item):
                    break
                else:
                    for datanya in list_url:
                        nom = nom + 1
                        print("NOMER NYA => "+str(nom))

                        if nom == int(limit_item):
                            break
                        else:
                        # eksekusi(driver, datanya, "TEST")
                            namefolder = "TEST"
                            print(str(datanya))
                            driver.get(datanya)
                            time.sleep(2)
                            if not os.path.exists(cfg.app['dataPath']+""+namefolder):
                                        os.makedirs(cfg.app['dataPath']+""+namefolder)
                            print("======================= START DATA ================")
                            while True:
                                time.sleep(2)
                                minimum_pemesanan.append("1")
                                nomor_etalase.append("-")
                                waktu_proses.append("Tidak ada PreOrder")
                                asuransi_arr.append("ya")
                                status_arr.append("1")
                                kategory_code.append("-")
                                gambar_2.append("-")
                                gambar_3.append("-")
                                gambar_4.append("-")
                                gambar_5.append("-")
                                url_video1.append("-")
                                url_video2.append("-")
                                url_video3.append("-")
                                sku_name.append("SKU NYA TIDAK ADA DUMMY")

                                try:
                                    name_product = driver.find_element_by_css_selector('h1[class="c-main-product__title u-txt--large"]').text
                                    nama_product.append(str(name_product))
                                    print(str(name_product))
                                    pass
                                except NoSuchElementException:
                                    nama_product.append("-")
                                    print("Failed Get Name Product")
                                    pass
                                
                                time.sleep(2)
                                try:
                                    harga = driver.find_element_by_css_selector('div[class="c-product-price -original -main"]').text
                                    harga_arr.append(str(harga))
                                    print("HARGA NORMAL => "+str(harga))
                                    pass
                                except NoSuchElementException:
                                    print("No Harga Normal")
                                    pass
                                time.sleep(2)
                                try:
                                    harga = driver.find_element_by_css_selector('div[class="c-product-price -discounted -main"]').text
                                    harga_arr.append(str(harga))                       
                                    print("HARGA DISKON =>"+str(harga))
                                    pass
                                except NoSuchElementException:
                                    print("Failed get diskon harga")
                                    pass
                                time.sleep(2)
                                try:
                                    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                                    # driver.execute_script("window.scrollTo(10,20, document.body.scrollHeight)")
                                    # driver.execute_script("document.body.style.zoom='50%'")
                                    # time.sleep(2)
                                    
                                    description = driver.find_element_by_css_selector('div[class="c-information__description-txt"]').text
                                    deskripsi_product.append(str(description))
                                    print("DESKRIPSI => "+str(description))
                                    pass
                                except NoSuchElementException:
                                    deskripsi_product.append("-")
                                    print("Faield Get Description Product")
                                    pass
                                
                                
                                time.sleep(2)
                                try:
                                    #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                                    kategory = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[1]/td[2]/a')
                                    
                                    print("KATEGORY => "+str(kategory.text))
                                    pass
                                except NoSuchElementException:
                                    print("Failed get kategory Name")
                                    pass

                                try:
                                    #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                                    berat = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[2]/td[2]')
                                    berat_arr.append(str(berat.text))
                                    print("BERAT => "+str(berat.text))
                                    pass
                                except NoSuchElementException:
                                    berat_arr.append("-")
                                    print("Failed get berat barang")
                                    pass
                                
                                try:
                                    stoknya = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[4]').text
                                    if stoknya == "Tersedia > 10 stok barang":
                                        jumlah_stok.append(">10")
                                    else:
                                        jumlah_stok.append(">50")
                                except:
                                    jumlah_stok.append("-")
                                    print("Failed get stok")
                                try:
                                    #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                                    asal = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[3]/td[2]')
                                    print("Asal Barang => "+str(asal.text))
                                    pass
                                except NoSuchElementException:
                                    print("Failed get asal barang")


                                try:
                                    kondi = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div').text
                                    print("Kondisi =>"+str(kondi))
                                    if str(kondi) == "BARU":
                                        kondisi.append(str(kondi))
                                    else:
                                        kondisi.append("-")
                                except:
                                    kondisi.append("-")
                                    print("Failed get kondisi barang")
                                try:
                                    terjual = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[1]/div[1]/div/span').text
                                    print("TERJUAL => "+str(terjual))
                                    pass
                                except NoSuchElementException:
                                    print("Faield get data terjual")
                                    pass

                                try:
                                    #driver.execute_script("document.body.style.zoom='100%'")
                                    image = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/section[1]/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/picture/img')
                                    gambar_1.append(str(image.get_attribute('src')))

                                    print(str("IMAGE 1 => "+image.get_attribute('src')))
                                    urllib.request.urlretrieve(str(image.get_attribute('src')), cfg.app['dataPath']+""+str(namefolder)+"/"+str(randint(3, 9999))+".png")
                                    time.sleep(2)
                                    break
                                except NoSuchElementException:
                                    gambar_1.append("-")
                                    print("Failed get images url")
                                    break
                                
                            print("======================= END DATA ================")
            
        
        
        print("TOTAL LINK => "+str(len(list_url)))

        df = pd.DataFrame({
                        
                        'Nama Product': nama_product,
                        'Deskripsi Product': deskripsi_product,
                        'Kategory Kode': kategory_code,
                        'Berat *(Gram)': berat_arr,
                        'Minimum Pemesanan': minimum_pemesanan,
                        'Nomor Etalase': nomor_etalase,
                        'Waktu Proses Preorder': waktu_proses,

                        'Kondisi': kondisi,
                        'Gambar 1': gambar_1,
                        'Gambar 2': gambar_2,
                        'Gambar 3': gambar_3,
                        'Gambar 4': gambar_4,
                        'URL Video Produk 1': url_video1,
                        'URL Video Produk 2': url_video2,
                        'URL Video Produk 3': url_video3,
                        'SKU Name': sku_name,
                        
                        'Status': status_arr,
                        'Jumlah Stok': jumlah_stok,
                        'Harga': harga_arr,
                        'Asuransi Pengiriman': asuransi_arr})
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(str(sys.argv[5])+'.xlsx', engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Hasil', index=False)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
# Function to insert row in the dataframe 

def toko(username, limit_paginate, filenamenya, kode_kategory):

    driverPath = cfg.app['driverPath']
    dataPath = cfg.app['dataPath']+'profile/'+username
    print(dataPath)
    ch_options = webdriver.ChromeOptions()
    #ch_options.add_argument("user-data-dir=" + dataPath)
    #ch_options.add_argument("--user-data-dir="+dataPath+"")
    ch_options.add_argument("--disable-dev-shm-usage")
    if cfg.app['headless']:
        ch_options.add_argument('headless')

    if cfg.app['no-sandbox']:
        ch_options.add_argument('no-sandbox')

    agent = cfg.agent[randint(0, len(cfg.agent)-1)]
    print(agent)
    ch_options.add_argument(
        'user-agent='+agent)
    driver = webdriver.Chrome(executable_path=driverPath, chrome_options=ch_options)
    
    limit = limit_paginate
    
    

    list_url = []

    nama_product = []
    deskripsi_product = []
    kategory_code = []
    berat_arr = []
    minimum_pemesanan = []
    nomor_etalase = []
    waktu_proses = []
    kondisi = []
    gambar_1 = []
    gambar_2 = []
    gambar_3 = []
    gambar_4 = []
    gambar_5 = []
    url_video1 = []
    url_video2 = []
    url_video3 = []
    sku_name = []

    status_arr = []
    jumlah_stok = []
    harga_arr = []
    asuransi_arr = []


    nom = 0
    nooom = 0
    while nom < int(limit):
        nom = nom + 1
        print("=========================== INFO PAGE =====================================")
        print(str("https://www.bukalapak.com/u/"+str(username)+"?keywords=&price_range=&sort=bestselling&deal=&condition=&rating=&installment=&free_shipping_provinces=&wholesale=&page="+str(nom)))
        print("=========================== END OF SITE ====================================")
        driver.get("https://www.bukalapak.com/u/"+str(username)+"?keywords=&price_range=&sort=bestselling&deal=&condition=&rating=&installment=&free_shipping_provinces=&wholesale=&page="+str(nom))
        time.sleep(2)
        
        
        try:
            link_list_product = driver.find_elements_by_css_selector('a[class="c-product-card__name js-tracker-product-link u-mrgn-top--2 u-mrgn-bottom--1 c-product-card__ellipsis c-product-card__ellipsis-2"]')
            for llp in link_list_product:
                list_url.append(llp.get_attribute('href'))
            print("Item di Page "+str(nom)+" Ada "+str(len(link_list_product))+" Product")
            print("Selanjutnya")
        except NoSuchElementException:
            print("Tidak Ada Product")
        print("PAGE KE => "+str(nom))
        noo = 0
        time.sleep(2)
    limit_scraptitem = input("LIMIT PRODUCT DI SCRAP [1-"+str(len(list_url))+"]: ")
    limit_item = limit_scraptitem
    noo = 0
    time.sleep(2)
    for datanya in list_url:
        noo = noo + 1
        
        if noo > int(limit_item):
            break
        else:
            print("PRODUCT SCRAP YG KE => "+str(noo))
            print("MENUJU URL PRODUCT => "+str(datanya))
            # eksekusi(driver, datanya, "TEST")
            namefolder = username
            driver.get(datanya)
            time.sleep(2)
            if not os.path.exists(cfg.app['dataPath']+""+namefolder):
                        os.makedirs(cfg.app['dataPath']+""+namefolder)
            print("======================= START DATA ================")
            while True:
                time.sleep(2)
                minimum_pemesanan.append("1")
                nomor_etalase.append("-")
                waktu_proses.append("Tidak ada PreOrder")
                asuransi_arr.append("ya")
                status_arr.append("1")
                
                gambar_2.append("-")
                gambar_3.append("-")
                gambar_4.append("-")
                gambar_5.append("-")
                url_video1.append("-")
                url_video2.append("-")
                url_video3.append("-")
                sku_name.append("SKU NYA TIDAK ADA DUMMY")

                try:
                    name_product = driver.find_element_by_css_selector('h1[class="c-main-product__title u-txt--large"]').text
                    nama_product.append(str(name_product))
                    print(str(name_product))
                    pass
                except NoSuchElementException:
                    nama_product.append("-")
                    print("Failed Get Name Product")
                    pass
                
                time.sleep(2)
                try:
                    harga = driver.find_element_by_css_selector('div[class="c-product-price -original -main"]').text
                    hargainteger = re.sub("[^0-9]", "", str(harga))
                    harga_arr.append(str(hargainteger))
                    print("HARGA NORMAL => "+str(harga))
                    pass
                except NoSuchElementException:
                    print("No Harga Normal")
                    pass
                time.sleep(2)
                try:
                    harga = driver.find_element_by_css_selector('div[class="c-product-price -discounted -main"]').text
                    hargainteger = re.sub("[^0-9]", "", str(harga))
                    harga_arr.append(str(hargainteger))                     
                    print("HARGA DISKON =>"+str(harga))
                    pass
                except NoSuchElementException:
                    print("Failed get diskon harga")
                    pass
                time.sleep(2)
                try:
                    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    # driver.execute_script("window.scrollTo(10,20, document.body.scrollHeight)")
                    # driver.execute_script("document.body.style.zoom='50%'")
                    # time.sleep(2)
                    
                    description = driver.find_element_by_css_selector('div[class="c-information__description-txt"]').text
                    deskripsi_product.append(str(description))
                    print("DESKRIPSI => "+str(description))
                    pass
                except NoSuchElementException:
                    deskripsi_product.append("-")
                    print("Faield Get Description Product")
                    pass
                
                
                time.sleep(2)
                try:
                    #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                    kategory = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[1]/td[2]/a')
                    kategory_code.append(str(kode_kategory))
                    print("KATEGORY => "+str(kategory.text))
                    pass
                except NoSuchElementException:
                    # kategory_code.append("-")
                    kategory_code.append(str(kode_kategory))
                    print("Failed get kategory Name")
                    pass

                try:
                    #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                    berat = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[2]/td[2]')
                    berat_arr.append(str(berat.text))
                    print("BERAT => "+str(berat.text))
                    pass
                except NoSuchElementException:
                    berat_arr.append("-")
                    print("Failed get berat barang")
                    pass
                
                try:
                    stoknya = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[4]').text
                    if stoknya == "Tersedia > 10 stok barang":
                        jumlah_stok.append(">10")
                    else:
                        jumlah_stok.append(">50")
                except:
                    jumlah_stok.append("-")
                    print("Failed get stok")
                try:
                    #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                    asal = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[3]/td[2]')
                    print("Asal Barang => "+str(asal.text))
                    pass
                except NoSuchElementException:
                    print("Failed get asal barang")


                try:
                    kondi = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div').text
                    print("Kondisi =>"+str(kondi))
                    if str(kondi) == "BARU":
                        kondisi.append(str(kondi))
                    else:
                        kondisi.append("-")
                except:
                    kondisi.append("-")
                    print("Failed get kondisi barang")
                try:
                    terjual = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[1]/div[1]/div/span').text
                    print("TERJUAL => "+str(terjual))
                    pass
                except NoSuchElementException:
                    print("Faield get data terjual")
                    pass

                try:
                    #driver.execute_script("document.body.style.zoom='100%'")
                    image = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/section[1]/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/picture/img')
                    #gambar_1.append(str(image.get_attribute('src')))

                    print(str("IMAGE 1 => "+image.get_attribute('src')))
                    randomnya = randint(3, 9999)
                    urllib.request.urlretrieve(str(image.get_attribute('src')), cfg.app['dataPath']+""+str(namefolder)+"/"+str(randomnya)+".png")
                    uploadnya = copyright_apply(str(namefolder)+"/"+str(randomnya)+".png", str(randomnya)+'.png')
                    gambar_1.append(str(uploadnya))
                    time.sleep(2)
                    break
                except NoSuchElementException:
                    gambar_1.append("-")
                    print("Failed get images url")
                    break
                
            print("======================= END DATA ================")

    print("TOTAL LINK => "+str(len(list_url))+ " Link Yang Di GET hanya "+str(limit_item))

    df = pd.DataFrame({
                    
                    'Nama Product': nama_product,
                    'Deskripsi Product': deskripsi_product,
                    'Kategory Kode': kategory_code,
                    'Berat *(Gram)': berat_arr,
                    'Minimum Pemesanan': minimum_pemesanan,
                    'Nomor Etalase': nomor_etalase,
                    'Waktu Proses Preorder': waktu_proses,

                    'Kondisi': kondisi,
                    'Gambar 1': gambar_1,
                    'Gambar 2': gambar_2,
                    'Gambar 3': gambar_3,
                    'Gambar 4': gambar_4,
                    'URL Video Produk 1': url_video1,
                    'URL Video Produk 2': url_video2,
                    'URL Video Produk 3': url_video3,
                    'SKU Name': sku_name,
                    
                    'Status': status_arr,
                    'Jumlah Stok': jumlah_stok,
                    'Harga': harga_arr,
                    'Asuransi Pengiriman': asuransi_arr})
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(str(filenamenya)+'.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Hasil', index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

def bykeyword(keyword, limit_paginate, limit_getscrap, filenamenya):

    driverPath = cfg.app['driverPath']
    dataPath = cfg.app['dataPath']+'profile/'+username
    print(dataPath)
    ch_options = webdriver.ChromeOptions()
    #ch_options.add_argument("user-data-dir=" + dataPath)
    #ch_options.add_argument("--user-data-dir="+dataPath+"")
    ch_options.add_argument("--disable-dev-shm-usage")
    if cfg.app['headless']:
        ch_options.add_argument('headless')

    if cfg.app['no-sandbox']:
        ch_options.add_argument('no-sandbox')

    agent = cfg.agent[randint(0, len(cfg.agent)-1)]
    print(agent)
    ch_options.add_argument(
        'user-agent='+agent)
    driver = webdriver.Chrome(executable_path=driverPath, chrome_options=ch_options)

    # typenya = sys.argv[1]
    search = keyword
    
    limit = limit_paginate
    limit_item = limit_getscrap
    driver.get("https://www.bukalapak.com/products?from=omnisearch&from_keyword_history=false&search%5Bkeywords%5D="+str(search)+"&search_source=omnisearch_keyword&source=navbar")

    list_url = []

    nama_product = []
    deskripsi_product = []
    kategory_code = []
    berat_arr = []
    minimum_pemesanan = []
    nomor_etalase = []
    waktu_proses = []
    kondisi = []
    gambar_1 = []
    gambar_2 = []
    gambar_3 = []
    gambar_4 = []
    gambar_5 = []
    url_video1 = []
    url_video2 = []
    url_video3 = []
    sku_name = []

    status_arr = []
    jumlah_stok = []
    harga_arr = []
    asuransi_arr = []


    get_paginate = driver.find_elements_by_css_selector('a[class="bl-pagination__link"]')
    last_paginate = driver.find_element_by_css_selector('#product-explorer-container > div > div > div.bl-flex-item.bl-product-list-wrapper > div > div:nth-child(2) > nav > ul > li:nth-child(9) > a').text
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    print(int(last_paginate))
    no=0
    nom =0
    finish = False
    while no < int(last_paginate):
        no = no + 1

        driver.get("https://www.bukalapak.com/products?page="+str(no)+"&search%5Bkeywords%5D="+str(search)+"")
        if no == int(limit):
            finish = True
        if finish == False:
            try:
                get_link = driver.find_elements_by_css_selector('p[class="bl-text bl-text--body-small bl-text--ellipsis__2"]>a[class="bl-link"]')
                for urlnya in get_link:
                    list_url.append(urlnya.get_attribute('href'))
                time.sleep(2)
                print("Selanjutnya")
            except NoSuchElementException:
                print("Failed Get Product Link")
        else:
            
            if nom == int(limit_item):
                break
            else:
                for datanya in list_url:
                    nom = nom + 1
                    print("NOMER NYA => "+str(nom))

                    if nom == int(limit_item):
                        break
                    else:
                    # eksekusi(driver, datanya, "TEST")
                        namefolder = "TEST"
                        print(str(datanya))
                        driver.get(datanya)
                        time.sleep(2)
                        if not os.path.exists(cfg.app['dataPath']+""+namefolder):
                                    os.makedirs(cfg.app['dataPath']+""+namefolder)
                        print("======================= START DATA ================")
                        while True:
                            time.sleep(2)
                            minimum_pemesanan.append("1")
                            nomor_etalase.append("-")
                            waktu_proses.append("Tidak ada PreOrder")
                            asuransi_arr.append("ya")
                            status_arr.append("1")
                            kategory_code.append("-")
                            gambar_2.append("-")
                            gambar_3.append("-")
                            gambar_4.append("-")
                            gambar_5.append("-")
                            url_video1.append("-")
                            url_video2.append("-")
                            url_video3.append("-")
                            sku_name.append("SKU NYA TIDAK ADA DUMMY")

                            try:
                                name_product = driver.find_element_by_css_selector('h1[class="c-main-product__title u-txt--large"]').text
                                nama_product.append(str(name_product))
                                print(str(name_product))
                                pass
                            except NoSuchElementException:
                                nama_product.append("-")
                                print("Failed Get Name Product")
                                pass
                            
                            time.sleep(2)
                            try:
                                harga = driver.find_element_by_css_selector('div[class="c-product-price -original -main"]').text
                                harga_arr.append(str(harga))
                                print("HARGA NORMAL => "+str(harga))
                                pass
                            except NoSuchElementException:
                                print("No Harga Normal")
                                pass
                            time.sleep(2)
                            try:
                                harga = driver.find_element_by_css_selector('div[class="c-product-price -discounted -main"]').text
                                harga_arr.append(str(harga))                       
                                print("HARGA DISKON =>"+str(harga))
                                pass
                            except NoSuchElementException:
                                print("Failed get diskon harga")
                                pass
                            time.sleep(2)
                            try:
                                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                                # driver.execute_script("window.scrollTo(10,20, document.body.scrollHeight)")
                                # driver.execute_script("document.body.style.zoom='50%'")
                                # time.sleep(2)
                                
                                description = driver.find_element_by_css_selector('div[class="c-information__description-txt"]').text
                                deskripsi_product.append(str(description))
                                print("DESKRIPSI => "+str(description))
                                pass
                            except NoSuchElementException:
                                deskripsi_product.append("-")
                                print("Faield Get Description Product")
                                pass
                            
                            
                            time.sleep(2)
                            try:
                                #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                                kategory = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[1]/td[2]/a')
                                
                                print("KATEGORY => "+str(kategory.text))
                                pass
                            except NoSuchElementException:
                                print("Failed get kategory Name")
                                pass

                            try:
                                #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                                berat = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[2]/td[2]')
                                berat_arr.append(str(berat.text))
                                print("BERAT => "+str(berat.text))
                                pass
                            except NoSuchElementException:
                                berat_arr.append("-")
                                print("Failed get berat barang")
                                pass
                            
                            try:
                                stoknya = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[4]').text
                                if stoknya == "Tersedia > 10 stok barang":
                                    jumlah_stok.append(">10")
                                else:
                                    jumlah_stok.append(">50")
                            except:
                                jumlah_stok.append("-")
                                print("Failed get stok")
                            try:
                                #kategory = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div[2]/div[7]').text
                                asal = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div/div/table/tbody/tr[3]/td[2]')
                                print("Asal Barang => "+str(asal.text))
                                pass
                            except NoSuchElementException:
                                print("Failed get asal barang")


                            try:
                                kondi = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[2]/div').text
                                print("Kondisi =>"+str(kondi))
                                if str(kondi) == "BARU":
                                    kondisi.append(str(kondi))
                                else:
                                    kondisi.append("-")
                            except:
                                kondisi.append("-")
                                print("Failed get kondisi barang")
                            try:
                                terjual = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[1]/div[1]/div/span').text
                                print("TERJUAL => "+str(terjual))
                                pass
                            except NoSuchElementException:
                                print("Faield get data terjual")
                                pass

                            try:
                                #driver.execute_script("document.body.style.zoom='100%'")
                                image = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/section[1]/div[2]/div[1]/div/div[1]/div/div/div/div/div/div/picture/img')
                                gambar_1.append(str(image.get_attribute('src')))

                                print(str("IMAGE 1 => "+image.get_attribute('src')))
                                urllib.request.urlretrieve(str(image.get_attribute('src')), cfg.app['dataPath']+""+str(namefolder)+"/"+str(randint(3, 9999))+".png")
                                
                                time.sleep(2)
                                break
                            except NoSuchElementException:
                                gambar_1.append("-")
                                print("Failed get images url")
                                break
                            
                        print("======================= END DATA ================")
        
    
    
    print("TOTAL LINK => "+str(len(list_url)))

    df = pd.DataFrame({
                    
                    'Nama Product': nama_product,
                    'Deskripsi Product': deskripsi_product,
                    'Kategory Kode': kategory_code,
                    'Berat *(Gram)': berat_arr,
                    'Minimum Pemesanan': minimum_pemesanan,
                    'Nomor Etalase': nomor_etalase,
                    'Waktu Proses Preorder': waktu_proses,

                    'Kondisi': kondisi,
                    'Gambar 1': gambar_1,
                    'Gambar 2': gambar_2,
                    'Gambar 3': gambar_3,
                    'Gambar 4': gambar_4,
                    'URL Video Produk 1': url_video1,
                    'URL Video Produk 2': url_video2,
                    'URL Video Produk 3': url_video3,
                    'SKU Name': sku_name,
                    
                    'Status': status_arr,
                    'Jumlah Stok': jumlah_stok,
                    'Harga': harga_arr,
                    'Asuransi Pengiriman': asuransi_arr})
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(str(filenamenya)+'.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Hasil', index=False)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

def Insert_row_(row_number, df, row_value): 
    # Slice the upper half of the dataframe 
    df1 = df[0:row_number] 
   
    # Store the result of lower half of the dataframe 
    df2 = df[row_number:] 
   
    # Inser the row in the upper half dataframe 
    df1.loc[row_number]=row_value 
   
    # Concat the two dataframes 
    df_result = pd.concat([df1, df2]) 
   
    # Reassign the index labels 
    df_result.index = [*range(df_result.shape[0])] 
   
    # Return the updated dataframe 
    return df_result 

# def eksekusi(driver,url,namefolder):


if __name__ == "__main__":
    cprint(figlet_format('Scrap', font='starwars'),
       'yellow', 'on_red', attrs=['bold'])
    cprint(figlet_format('BL- Zhar', font='starwars'),
       'yellow', 'on_red', attrs=['bold'])
    
    typenyanih = input("Type [official,toko,keyword] : ")
    if typenyanih == "official":
        url_toko = input("URL OFFICIAL : ")
        limit_scraptitem = input("LIMIT PRODUCT DI SCRAP [1-99] : ")
        filenamenya = input("FileName Hasil Scrap [tanpa extenstion]: ")
        official(typenyanih,url_toko,limit_scraptitem,filenamenya)
    elif typenyanih == "toko":
        usernamenya = input("USERNAME TOKO [lexchannel]: ")
        limit_page = input("LIMIT Page DI SCRAP [1-20]: ")
        filenamenya = input("FileName Hasil Scrap [tanpa extenstion]: ")
        kategorynyakode = input("Kode Kategory : ")
        toko(usernamenya, limit_page,filenamenya, kategorynyakode)
    else:
        keywordnya = input("Input Kata Kunci [ex:baju]: ")
        limit_page = input("Input Limit Page Di Scrap [1-20]: ")
        limit_scraptitem = input("LIMIT PRODUCT DI SCRAP [1-99]: ")
        filenamenya = input("FileName Hasil Scrap [tanpa extenstion]: ")
        bykeyword(keywordnya,limit_page,limit_scraptitem,filenamenya)
