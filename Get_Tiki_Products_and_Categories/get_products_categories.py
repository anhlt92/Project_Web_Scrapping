from bs4 import BeautifulSoup
import requests
import sqlite3
import pandas as pd
import re


TIKI_URL = 'https://tiki.vn'

from google.colab import drive
drive.mount('/content/gdrive')

PATH_TO_DB = '/content/gdrive/MyDrive/'

conn = sqlite3.connect(PATH_TO_DB+'tiki.db')
cur = conn.cursor()

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

# cur.execute('DROP TABLE IF EXISTS categories;')

conn.commit()

"""### Function to get HTML response from given URL"""

# Get the HTML content get_url()
def get_url(url):
    try:
        response = requests.get(url,headers = HEADERS).text
        soup = BeautifulSoup(response, 'html.parser')
        return soup
    except Exception as err:
        print('ERROR BY REQUEST:', err)

"""### Function to do CRUD (create/ read/ update/ delete) on database

# CREATE CATEGORIES TABLE
"""

# Create table categories in the database using a function
def create_categories_table():
    query = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url TEXT, 
            parent_id INTEGER, 
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        cur.execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

# # drop the whole table to clean things up
# cur.execute('DROP TABLE IF EXISTS categories;')
# conn.commit()

# # re-create our category table again
# create_categories_table()

"""# CREATE PRODUCTS TABLE"""

# Create table products in the database using a function
def create_products_table():
    query = """
        CREATE TABLE IF NOT EXISTS products (
            ProductID INTEGER PRIMARY KEY,
            CategoryID INTEGER,
            ProductName VARCHAR(255),
            Price TEXT,
            ProductUrl TEXT,
            TikiNow TEXT,
            FreeShip TEXT,
            NumberReview TEXT,
            BadgeUnderPrice TEXT,
            Discount TEXT,
            Installment TEXT,
            FreeGift TEXT,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        cur.execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

# # drop the whole table to clean things up
# cur.execute('DROP TABLE IF EXISTS products;')
# conn.commit()

# # re-create our category table again
# create_products_table()

"""### OOP to do CRUD (create/ read/ update/ delete) on database"""

# Instead of using a function to do CRUD on database,
# creating a class Category is preferred
# attributes: name, url, parent_id
# instance method: save_into_db()
class Category:
    def __init__(self, name, url, parent_id=None, cat_id=None):
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.parent_id = parent_id

    def __repr__(self):
        return f"ID: {self.cat_id}, Name: {self.name}, URL: {self.url}, Parent: {self.parent_id}"

    def save_into_db(self):
        query = """
            INSERT INTO categories (name, url, parent_id)
            VALUES (?, ?, ?);
        """
        val = (self.name, self.url, self.parent_id)
        try:
            cur.execute(query, val)
            self.cat_id = cur.lastrowid
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)

class Product:
    def __init__(self, ProductID, CategoryID, ProductName, Price, ProductUrl=None, TikiNow=None, FreeShip=None, NumberReview=None, BadgeUnderPrice=None, Discount=None, Installment=None, FreeGift=None):
        self.ProductID = ProductID
        self.CategoryID = CategoryID 
        self.ProductName = ProductName
        self.Price = Price
        self.ProductUrl = ProductUrl
        self.TikiNow = TikiNow
        self.FreeShip = FreeShip
        self.NumberReview = NumberReview
        self.BadgeUnderPrice = BadgeUnderPrice
        self.Discount = Discount
        self.Installment = Installment
        self.FreeGift = FreeGift
        
    def __repr__(self):
        return f"ID: {self.ProductID}, Cat_ID: {self.CategoryID}, Name : {self.ProductName}, URL: {self.ProductUrl}"

    def save_into_db(self):
        query = """
            INSERT INTO products (ProductID, CategoryID, ProductName, Price, ProductUrl, TikiNow, FreeShip, NumberReview, BadgeUnderPrice, Discount, Installment, FreeGift)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        val = (self.ProductID, self.CategoryID, self.ProductName, self.Price, self.ProductUrl, self.TikiNow, self.FreeShip, self.NumberReview, self.BadgeUnderPrice, self.Discount, self.Installment, self.FreeGift)
        try:
            cur.execute(query, val)
            #self.cat_id = cur.lastrowid
            conn.commit()
        except Exception as err:
            print('ERROR BY INSERT:', err)

"""### Get main categories """

CATEGORY_SET = set()
def can_add_to_cat_set(cat_name,save=False):
  if cat_name not in CATEGORY_SET:
    if save:
      CATEGORY_SET.add(cat_name)
      print(f'Added "{cat_name}" to CATEGORY_SET')
    return True
  return False

def get_main_categories(save_db=False):
    soup = get_url(TIKI_URL)

    result = []
    for a in soup.find_all('a', {'class': 'menu-link'}):
        name = a.find('span', {'class': 'text'}).text.strip()
        
        _=can_add_to_cat_set(name,save_db)

        url = a['href']
        main_cat = Category(name, url) # object from class Category

        if save_db:
            main_cat.save_into_db()
        result.append(main_cat)
    return result

# main_categories = get_main_categories(save_db=False)
main_categories = get_main_categories(save_db=True)

print(len(main_categories))
main_categories

"""### Get sub categories"""

import re

# get_sub_categories() given a parent category
def get_sub_categories(parent_category, save_db=False):
    parent_url = parent_category.url
    result = []

    try:
        soup = get_url(parent_url)
        for a in soup.find_all('a', {'class':'item item--category '}):
            name = a.text.strip()
            if can_add_to_cat_set(name,save_db): 
              sub_url = a['href']
              cat = Category(name, sub_url, parent_category.cat_id) # we now have parent_id, which is cat_id of parent category
              if save_db:
                  cat.save_into_db()
              result.append(cat)
    except Exception as err:
        print('ERROR IN GETTING SUB CATEGORIES:', err)
    return result

"""### Get all categories

**Now we can start getting all the possible categories in Tiki**
"""

# get_all_categories() given a list of main categories (This is a recursion function)

list_lowest_sub_cat = {}
def get_all_categories(categories,save_db):
    # if I reach the last possible category, I need to stop
    if len(categories) == 0:
        return      
    for cat in categories:
        print(f'Getting {cat} sub-categories...')
        sub_categories = get_sub_categories(cat, save_db=save_db)
        print(f'Finished! {cat.name} has {len(sub_categories)} sub-categories')
        #dict with the key is cat_id, and value is the rest
        if len(sub_categories) == 0:
          list_lowest_sub_cat[cat.cat_id] = [cat.name,cat.url,cat.parent_id] 
        get_all_categories(sub_categories,save_db=save_db) # make sure to switch on (or off) save_db here

# # drop the whole table to clean things up
# cur.execute('DROP TABLE IF EXISTS categories;')
# conn.commit()

# # re-create our category table again
# create_categories_table()

type(main_categories)

get_all_categories(main_categories,save_db=True)



print(len(list_lowest_sub_cat))

list_lowest_sub_cat

# data = pd.read_sql_query('Select * From categories', conn)
# data



PRODUCT_SET = set()
def can_add_to_pro_set(pro_name,save=False):
  if pro_name not in PRODUCT_SET:
    if save:
      PRODUCT_SET.add(pro_name)
      print(f'Added "{pro_name}" to PRODUCT_SET')
    return True
  return False


def get_product_info(list_lowest_sub_cat, save_db = False):
  
  data = []
  list_product_id = []
  for key in list_lowest_sub_cat:
    # if key == 2:
    #   break
    
    url = list_lowest_sub_cat[key][1]
    page_number = 1
    
    while(page_number < 3):
      soup = get_url(f'{url}?page={page_number}')
      # try:
      #   r = requests.get(f'{url}?page={page_number}', headers=headers)
      # except:
      #   break
      #soup = BeautifulSoup(r.text, 'html.parser')
      products = soup.find_all('a', {'class':'product-item'})
     
      check = True
      for product in products:       
        d = {'product_id':'', 'name':'', 'price':'', 'product_page_url':'', 'tiki-now':'', 'freeship':'', 'number-review':'', 'badge-under-price':'', 'discount-percentage':'', 'installment':'' , 'free-gift':''}

        p = re.compile(r'\w*p(\d+)[^html]')
        a = p.findall(str(product['href']))
        #print(type(a[len(a)-1]))
        # 1. Product ID
        d['product_id'] = a[-1]
        #print(d['product_id'])
        if d['product_id'] in list_product_id:
          #print(f"Total = {max(1,page_number-1)} page(s)")
          print('*'*20)
          check = False
          break
        
        list_product_id.append(d['product_id'])
        # 2. Product Name
        d['name'] = product.find('div', {'class':'name'}).text 
        #print(d['name'])
        name = d['name']
        _=can_add_to_pro_set(name,save_db)

        # 3. Price
        d['price'] = product.find('div', {'class':'price-discount__price'}).text
        #print(d['price'])
        
        # 4. Product Url
        d['product_page_url'] = f"https://tiki.vn{product['href']}"
        #print(d['product_page_url'])
        
        # 5. Tikinow
        try:
            if (product.find('div',{'class':'badge-service'}).img['src']):
                d['tiki-now'] = 'Tikinow'
                #print(f"{d['tiki-now']} : {product.find('div',{'class':'badge-service'}).img['src']}")
        except:
            d['tiki-now']=''
                #print(1)
        
        
        # 6. Freeship
        try:
          if product.img:
              d['freeship'] = product.find('div', {'class':'item top'}).text
              #d['freeship'] = 'Freeship'
              #print(f"{d['freeship']} : {product.img['src']}")
        except:
          d['freeship'] = ''
        
        # 7. Number of reviews
        if product.find('div', {'class':'review'}):
            d['number-review'] = product.find('div', {'class':'review'}).text
            #print(d['number-review'])
            
        # 8. Badge under price
        try:
            if product.find('div', {'class':'badge-under-price'}).img['src']:
                d['badge-under-price'] = 'Badge under price'
                #print(f"{d['badge-under-price']} : {(product.find('div', {'class':'badge-under-price'})).img['src']}")
        except:
            d['badge-under-price']=''
            
        # 9. Discount percentage
        try:
          if product.find('div', {'class':'price-discount__discount'}):
              d['discount-percentage'] = (product.find('div', {'class':'price-discount__discount'}).text)
              #print(d['discount-percentage'])
        except:
          d['discount-percentage'] = ''

        #print(6)
        # 10. INSTALLMENTS
        try :
          if product.find('p', {'class':'installment'}):
              d['installment'] = (product.find('p', {'class':'installment'}).text)
          elif product.find('div', {'badge-benefits'}):
              d['installment'] = (product.find('div', {'badge-benefits'}).text)
        except:
          d['installment'] = ''
        #print(7)
        
        # 11. Freegift
        try:
          if product.find('div',{'class':'freegift-list'}):
              d['free-gift'] = product.find('div',{'class':'gift-image-list'}).img['src']
              #print(f"{product.find('div',{'class':'freegift-list'}).text} : {d['free-gift']}")
        except:
          d['free-gift'] = ''
        
        sub_pro =  Product(d['product_id'], key, d['name'], d['price'], d['product_page_url'], d['tiki-now'], d['freeship'], d['number-review'], d['badge-under-price'], d['discount-percentage'], d['installment'], d['free-gift'])

        print(f'Getting ID: {sub_pro}')
        if save_db:
            sub_pro.save_into_db()          

        data.append(sub_pro)
      #if(check):
        #print(f'Page : {page_number}')
      page_number+=1
  return data

# # drop the whole table to clean things up
# cur.execute('DROP TABLE IF EXISTS products;')
# conn.commit()

# # re-create our category table again
# create_products_table()

# products_info = get_product_info(list_lowest_sub_cat, save_db = True)

# data = pd.read_sql_query('Select * From products', conn)
# data

print(len(list_lowest_sub_cat))

cat = pd.read_sql_query('SELECT * FROM categories', conn)
cat

"""Query to get category name of each product by join 2 table (categories and products)"""

pd.read_sql_query("""
SELECT p.ProductName, p.ProductUrl, c.name as CategoryName
FROM products as p
  JOIN categories as c
where p.CategoryID = c.id
LIMIT 5
""", conn)

products = pd.DataFrame(data = data, columns = data.keys())
products.to_csv("./result.csv", index=False)
