# WEB-SCRAPING PROJECT 
Web Scrapping

Result : https://docs.google.com/spreadsheets/d/1BTJgfg_YCdx90ZhIJzwJ25AZr79NiZ4oGXFG-BPJzEo/edit?usp=sharing


## WEB-SCRAPING (TIKI)


### CHALLENGE 1 : Each time you try to request the web link, it could be change the tag of "product-item" : \<a> or \<div>

 B'c the only tag \<div> has product information, so when it loads the product-item with tag \<a>, we dont get any product information here

              -> SOLUTION : When we get the length of total_data, we'll compare with the previous total_data, to see whether the length increasing or not, if it inscreases, we go to the next page, but if it's not (tag \<a>), I request this page again till get the information (tag \<div>), I switch to a next page.

### CHALLENGE 2 : Almost information is found in tag <\div>, but the star rating. \nFinally, we found it from the script json:

              -> SOLUTION : To get the information inside json, we have 2 options : 
                  + No1 : use regex to get the only one infomation of star rating
                  + No2 : We saw this seems like the type dict, so we can convert it to dict
                      -> We choose No2: Although the first way is faster than the last one, 
                      but we noticed that there're many information inside json script, 
                      and we will get it easy if we use dict, just get required value through key
                         + We create one function to convert json to dict, **not using** library here, b'c it'll take more memory
                            Step 1 : We use regex remove tag script (remember convert it to string first, because it is an NoneType object before)
                            Step 2 : We split it at each comma
                            Step 3 : We split each key and value at each ":"
                            -> When we get all infomation, we store it into dict, after that you can get anything just through the key.
                            -> The solution gives you the way :
                            + To get every information inside script json 
                            + Not using the librabry, it avoids wasting memory
                            + Re-use in the future. 
                             => So it's very efficient. 
