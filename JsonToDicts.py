import re

#Find all script json
list_script = soup.find_all('script',{'type':'application/ld+json'})

print(list_script)

#pattern will remove the tag SCRIPT in json
pattern = r'[^<\sscript type=\"application/ld+json\">](.*)[^</script>]'

# Convert nontype to string to modify
a = str(products[1])
#print(re.find(pattern, a))

# Find all string that match with pattern and store it to variable abc
abc = re.findall(pattern,a)
print(type(abc)) #check type of abc
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
for key,value in d.items():
    print(f'{key} : {value}')

#Test type
print(type(d))
