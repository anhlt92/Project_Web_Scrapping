# Week_1_Project_Group3
Web Scrapping

Result : https://docs.google.com/spreadsheets/d/1BTJgfg_YCdx90ZhIJzwJ25AZr79NiZ4oGXFG-BPJzEo/edit?usp=sharing


## WEB-SCRAPING (TIKI)

Using format string with dynamic page_number increasing each loop + Using while(true) to get the next page

### PROBLEM 1 : Each time you try to request the web link it will change the tag of product-item : <a> or <div>

Because we get the info inside tag div with class = product-item, so when it load the product-item with tag a, we dont get any product information

              -> SOlUTION : When we get the length of total_data, we'll compare with the previous total_data, 
              To see whether the length increasing or not, if it inscreases, I go to the next page, but if it's not I request this page again 
+ Use for loop inside to get product infomation in tag div with class name is product-item:
### PROBLEM 2 : Almost infomation is found in this tag, but the percentage of star. Finally, we found it from the script json:

        To get the information inside json, we have 2 options : 
          + No1 : use regex to get the only one infomation of star rating
          + No2 : We saw this seems like the type dictionary, so we can convert it to dictionary
              -> Choose No2: Although the first way is faster than the last one, 
              but we noticed that there're many information inside json script, and we will get it easy if we use dictionary, just get required value through key
                  + We create one function to convert json to dicts, not using library here, b'c it'll take more memory
                    Step 1 : We use regex remove tag script (remember convert it to string first, because it is an NoneType object before)
                    Step 2 : We split it at each comma
                    Step 3 : We split each key and value at each ":"
                    -> When we get all infomations we need including key and value, we store it into dicts  
