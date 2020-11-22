import requests
import time

from bs4 import BeautifulSoup

page_number = 1

data = []

len_a = 48
check = True
x= 0
while(page_number<2):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    r = requests.get(f'https://tiki.vn/laptop-may-vi-tinh/c1846?page={page_number}', headers=headers)

    # r.text is a HTML file so we will use html.parser
    soup = BeautifulSoup(r.text, 'html.parser')
    
    products = soup.find_all('div', {'class':'product-item'})

    for product in products:

        # Each product is dictionary containing the required information
        d = {'product_id':'', 'seller_id':'', 'title':'', 'price':'', 'image_url':'', 'tiki-now':'', 'freeship':'', 'number-review':'', 'badge-under-price':'', 'discount-percentage':'', 'shocking-price':'', 'installment':'' }

        # We use the try-except blocks to handle errors
        try:
            d['product_id'] = product['data-id']
            d['seller_id'] = product['data-seller-product-id']
            d['title'] = product['data-title']
            d['price'] = product['data-price']

            # There are some articles without img tag...
            if product.img:
                d['image_url'] = product.img['src']
            
            #URL PAGE
           
            #TIKI NOW
            if (product.find('div',{'class':'badge-service'}).img['src']):
                d['tiki-now'] = product.find('div',{'class':'badge-service'}).img['src']
          
            
            #FREE SHIP OR SHOCKING PRICE
            if product.find('p', {'class':'service-text'}):
                if product.find('p', {'class':'service-text'}).text == " Freeship ":
                    d['freeship'] = product.find('p', {'class':'service-text'}).text
                else:
                    d['shocking-price'] = product.find('p', {'class':'service-text'}).text    

            #NUMBERS OF REVIEWS
            if product.find('p', {'class':'review'}):
                d['number-review'] = product.find('p', {'class':'review'}).text
                
            #STARS/ PARCENTAGE OF STARS
            
            #BADGE UNDER PRICE
            if product.find('div', {'class':'badge-under_price'}):
                d['badge-under-price'] = 'Badge under price'
            if product.find('div', {'class':'badge-under-price'}):
                d['badge-under-price'] = 'Badge under price'
            
            #DISCOUNT PERCENTAGE
            if product.find('span', {'class':'sale-tag'}):
                d['discount-percentage'] = (product.find('span', {'class':'sale-tag'}).text)
                
            
            #INSTALLMENTS
            if product.find('p', {'class':'installment'}):
                d['installment'] = (product.find('p', {'class':'installment'}).text)
            if product.find('div', {'badge-benefits'}):
                d['installment'] = (product.find('div', {'badge-benefits'}).text)

            # Append the dictionary to data list
            data.append(d)
        except:
            # Skip if error and print error message
            print("We got one article error!")
    
    if len(data) > len_a or (len(data) == len_a and page_number == 1):
        page_number += 1
        len_a = len(data)
        x+=1
        print(x)
        print(data[-1])

    #total_data.extend(data)
    #print(len(total_data))