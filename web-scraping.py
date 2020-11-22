import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

page_number = 1

data = []

len_a = 48
check = True
x= 0



def get_star(product_position):
  #Find all script json
  list_script = soup.find_all('script',{'type':'application/ld+json'})

  #pattern will remove the tag SCRIPT in json
  pattern = r'[^<\sscript type=\"application/ld+json\">](.*)[^</script>]'

  # Convert nontype to string to modify
  a = str(list_script[product_position])
  #print(re.find(pattern, a))

  # Find all string that match with pattern and store it to variable abc
  abc = re.findall(pattern,a)
  #check type of abc
  #print(abc)

  #split string where it has comma, and it will create a list 
  list_abc =abc[0].split(',')

  #Because the json structure in this web has format like dict, so we convert it to dict to get info 
  d = {}

  #We pass each element of list_abc and remove junk components by using regex
  for i in list_abc:
      component = re.sub(r'(.*{)|(}.*)|"','',i).split(':')
      d[component[0]] = component[1]
      #print(component)

  # Test the result
  return d


  


while(page_number < 5):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    r = requests.get(f'https://tiki.vn/laptop-may-vi-tinh/c1846?page={page_number}', headers=headers)

    # r.text is a HTML file so we will use html.parser
    soup = BeautifulSoup(r.text, 'html.parser')
    
    products = soup.find_all('div', {'class':'product-item'})

    product_position = 1

    for product in products:

        # Each product is dictionary containing the required information
        d = {'product_id':'', 'seller_id':'', 'title':'', 'price':'', 'image_url':'', 'product_page_url':'', 'tiki-now':'', 'freeship':'', 'number-review':'','percentage-star':'', 'badge-under-price':'', 'discount-percentage':'', 'shocking-price':'', 'installment':'' }

        # We use the try-except blocks to handle errors
        d['product_id'] = product['product-sku']
        d['seller_id'] = product['data-seller-product-id']
        d['title'] = product['data-title']
        d['price'] = product['data-price']

        # There are some articles without img tag...
        if product.img:
            d['image_url'] = product.img['src']
        
        #URL PAGE
        d['product_page_url'] = product.a['href']

        #TIKI NOW
        try:
          if (product.find('div',{'class':'badge-service'}).img['src']):
              d['tiki-now'] = product.find('div',{'class':'badge-service'}).img['src']
        except:
          d['tiki-now']='NO'
          #print(1)
        
        #FREE SHIP OR SHOCKING PRICE
        if product.find('p', {'class':'service-text'}):
            if product.find('p', {'class':'service-text'}).text == " Freeship ":
                d['freeship'] = product.find('p', {'class':'service-text'}).text
            else:
                d['shocking-price'] = product.find('p', {'class':'service-text'}).text    
        #print(2)

        #NUMBERS OF REVIEWS
        if product.find('p', {'class':'review'}):
            d['number-review'] = product.find('p', {'class':'review'}).text

        #print(3)
            
        #STARS/ PERCENTAGE OF STARS
        try:
          if  (get_star(product_position)['ratingValue']):
            d['percentage-star'] = (get_star(product_position)['ratingValue'])
            product_position +=1
        except:
          d['percentage-star'] = ''

        #print(4)
        
        #BADGE UNDER PRICE
        if product.find('div', {'class':'badge-under_price'}):
            d['badge-under-price'] = 'Badge under price'
        if product.find('div', {'class':'badge-under-price'}):
            d['badge-under-price'] = 'Badge under price'

        #print(5)
        
        #DISCOUNT PERCENTAGE 
        if product.find('span', {'class':'sale-tag'}):
            d['discount-percentage'] = (product.find('span', {'class':'sale-tag'}).text)
            
        #print(6)
        #INSTALLMENTS
        if product.find('p', {'class':'installment'}):
            d['installment'] = (product.find('p', {'class':'installment'}).text)
        if product.find('div', {'badge-benefits'}):
            d['installment'] = (product.find('div', {'badge-benefits'}).text)
        #print(7)
        # Append the dictionary to data list
        data.append(d)
        
    if len(data) > len_a or (len(data) == len_a and page_number == 1):
        page_number += 1
        len_a = len(data)
        x+=1
        print(len(data))
        print(data[-1])
    

    #total_data.extend(data)
    #print(len(total_data))

products = pd.DataFrame(data = data, columns = data[0].keys())
products.to_pickle("./result.pkl")
unpickled_result = pd.read_pickle("./result.pkl")
unpickled_result