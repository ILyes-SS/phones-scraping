import requests
import re

#global variable that will store all phones as dictionaries
phones = []

#each heading html element have some informations
phone_data_shape = """
        <div class="card-body" style="padding-top:10px;">
           <h3 class="produit_titre text-center" style="height_:auto; margin-bottom:0px;"><a target="_blank" title="Prix et Achat en Ligne Xiaomi  Poco M7 Pro 8/256GO - Algérie" href="/telephones-mobiles/?produit=achat-vente-telephones-portables-xiaomi-poco-m7-pro-8-256go-algerie&amp;item=26712933&amp;id_famille=3758&amp;id_fiche=0">Xiaomi  Poco M7 Pro 8/256GO</a></h3> <h3 class="text-center prix libelle-prix produit_prix"><span class="prix">Prix</span> 51 000 Da </h3> 
                    <h4 class="libelle-marque text-center ">
                    <a class="hub_link" title="Prix et Achat Téléphones Portables Xiaomi  en Algérie" href="/telephones-mobiles/?page=prix-telephones-portables-xiaomi-algerie&amp;id_marque=41820&amp;position=3&amp;id_famille=3758">Xiaomi </a>
                    </h4> 
                <h4 class="libelle-marque text-center "> <a title="Prix et Achat Téléphones Portables  6 Pouces - Algérie" href="/telephones-mobiles/?page=prix-telephones-portables-ecran-6-pouces-algerie&amp;dep1=520&amp;val1=3879&amp;position=20&amp;id_famille=3758"> 6.7 Pouces</a>&nbsp;&nbsp;<a title="Prix et Achat Téléphones Portables  AMOLED - Algérie" href="/telephones-mobiles/?page=prix-telephones-portables-qualite-ecran-amoled-algerie&amp;dep1=694&amp;val1=4071898&amp;position=20&amp;id_famille=3758"> AMOLED</a></h4>
                <h4 class="libelle-marque text-center "> <a title="Prix et Achat Téléphones Portables Ram 8 Go - Algérie" href="/telephones-mobiles/?page=prix-telephones-portables-memoire-8-go-algerie&amp;dep1=697&amp;val1=43435&amp;position=20&amp;id_famille=3758">8 Go Ram</a>&nbsp;&nbsp;<a title="Prix et Achat Téléphones Portables Disque 256 Go - Algérie" href="/telephones-mobiles/?page=prix-telephones-portables-disque-256-go-algerie&amp;dep1=768&amp;val1=20280&amp;position=20&amp;id_famille=3758">256 Go Disque</a></h4>
        </div>
"""


def getShapes(html_content):
    #returns a tuple of length 1 of the captured group between() and added ? for non greedy, and added re.DOTALL so that . would match newline character
    shapes = re.findall(r'class="card-body"(?:.*?)>(.*?)</div>',html_content,re.DOTALL)
    return shapes

def getPrice(data_shape):
    match = re.search(r"Prix(?:.*?)(\d+ \d+) Da",data_shape,re.DOTALL)  #search for the price pattern
    price = None if not match else match.group(1)  #first captured group or None if price is not mentioned
    print("the price", price)
    return price

def populate_phones(shapes):
    for shape in shapes:
        price = getPrice(shape)  #add the remaining functions
        if price:
            phones.append({"price":price})  #append a dictionary with the phone data to the global list

    


for i in range(10): 
    #the website has pagination for the phones display (10 pages) visible in the url
    params = {'page_group': i}
    response = requests.get("https://webstar-electro.com/telephones-mobiles/?page=prix-telephones-portables-algerie&position=1&id_famille=3758",params=params,timeout=10) # maximum time for waiting


    # we check if our request did not fail (status code other than 200)
    try:
        if response.status_code == 200: 
            content = response.text
            print(f'\n\n########### PAGE : {i}   ########## \n\n')
            shapes = getShapes(content)
            populate_phones(shapes)
        else:
            print(f"Error: status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
print(phones)


