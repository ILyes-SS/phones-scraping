import requests
import re


#the website has pagination for the phones display (10 pages) visible in the url
params = {'page_group': 0}
response = requests.get("https://webstar-electro.com/telephones-mobiles/?page=prix-telephones-portables-algerie&position=1&id_famille=3758",params=params,timeout=10) # maximum time for waiting


# we check if our request did not fail (status code other than 200)
try:
    if response.status_code == 200: 
        content = response.text
        print("Successfully fetched the page")
    else:
        print(f"Error: status code {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
 
print(content)