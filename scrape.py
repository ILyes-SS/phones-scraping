#Group members: Benmalti Ilyes, Chenine omar sifeddine
#website: https://webstar-electro.com/telephones-mobiles/?page=prix-telephones-portables-algerie&position=1&id_famille=3758
#description: extracted data about phones (brand, model, ram, storage, price, display size, display type) and saved it in output.csv file
#Ai was only used to help in correcting small mistakes in regex

import requests
import re
import csv

#global variable that will store all phones as dictionaries
phones = []

#each heading html element have some informations in it, this is an example of one a card body
phone_data_shape = """
        <div class="card-body" style="padding-top:10px;">
           <h3 class="produit_titre text-center" style="height_:auto; margin-bottom:0px;"><a target="_blank" title="Prix et Achat en Ligne Xiaomi  Poco M7 Pro 8/256GO - Algérie" href="/telephones-mobiles/?produit=achat-vente-telephones-portables-xiaomi-poco-m7-pro-8-256go-algerie&amp;item=26712933&amp;id_famille=3758&amp;id_fiche=0">Xiaomi  Poco M7 Pro 8/256GO</a></h3> <h3 class="text-center prix libelle-prix produit_prix"><span class="prix">Prix</span> 51 000 Da </h3> 
                    <h4 class="libelle-marque text-center ">
                    <a class="hub_link" title="Prix et Achat Téléphones Portables Xiaomi  en Algérie" href="/telephones-mobiles/?page=prix-telephones-portables-xiaomi-algerie&amp;id_marque=41820&amp;position=3&amp;id_famille=3758">Xiaomi </a>
                    </h4> 
                <h4 class="libelle-marque text-center "> <a title="Prix et Achat Téléphones Portables  6 Pouces - Algérie" href="/telephones-mobiles/?page=prix-telephones-portables-ecran-6-pouces-algerie&amp;dep1=520&amp;val1=3879&amp;position=20&amp;id_famille=3758"> 6.7 Pouces</a>&nbsp;&nbsp;<a title="Prix et Achat Téléphones Portables  AMOLED - Algérie" href="/telephones-mobiles/?page=prix-telephones-portables-qualite-ecran-amoled-algerie&amp;dep1=694&amp;val1=4071898&amp;position=20&amp;id_famille=3758"> AMOLED</a></h4>
                <h4 class="libelle-marque text-center "> <a title="Prix et Achat Téléphones Portables Ram 8 Go - Algérie" href="/telephones-mobiles/?page=prix-telephones-portables-memoire-8-go-algerie&amp;dep1=697&amp;val1=43435&amp;position=20&amp;id_famille=3758">8 Go Ram</a>&nbsp;&nbsp;<a title="Prix et Achat Téléphones Portables Disque 256 Go - Algérie" href="/telephones-mobiles/?page=prix-telephones-portables-disque-256-go-algerie&amp;dep1=768&amp;val1=20280&amp;position=20&amp;id_famille=3758">256 Go Disque</a></h4>
                //... more unecessary data ..
        </div>
"""


#get all the cards of the phones in the html content
def getShapes(html_content):
    #returns a tuple of length 1 of the captured group between() and added ? for non greedy, and added re.DOTALL so that . would match newline character
    shapes = re.findall(r'class="card-body"(?:.*?)>(.*?)</div>',html_content,re.DOTALL)
    return shapes

def getPrice(data_shape):
    #"""Extract price in Dinars from the card HTML by searching for 'Prix ... Da' pattern and capturing the number in between"""
    match = re.search(r'Prix(?:.*?)(\d{1,3}(?: \d{3})*)\s*Da', data_shape, re.DOTALL)
    price = None if not match else int(match.group(1).replace(' ', ''))
    return price


def getPhoneName(data_shape):
    """Extract the full phone name from the <a> tag in produit_titre"""
    # Primary: <h3 class="produit_titre ..."><a>NAME</a></h3>
    match = re.search(r'<h3[^>]*class="produit_titre[^"]*"[^>]*>\s*<a[^>]*>([^<]+)</a>', data_shape, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback: any phone link anchor with a title inside the card
    match = re.search(r'<a[^>]*title="[^"]*"[^>]*href="[^"]*telephones-mobiles[^"]*"[^>]*>([^<]+)</a>', data_shape, re.DOTALL)
    return match.group(1).strip() if match else None

def getBrand(phone_name):
    """Extract brand from phone name (first word before space)"""
    if not phone_name:
        return None
    # Extract first word (brand name) from phone name
    match = re.search(r'^([A-Za-z]+)', phone_name.strip())
    return match.group(1) if match else None

def getRAM(phone_name):
    """Extract RAM from phone name (number before /)"""
    if not phone_name:
        return None
    # Match pattern like "12/256GB" or "8/256GO" - extract number before /
    match = re.search(r'(\d+)\s*/\s*\d+\s*(?:GB|GO|Go)', phone_name, re.IGNORECASE)
    return match.group(1) if match else None
    
def getStorage(phone_name):
    """Extract storage from phone name (number and unit after /)"""
    if not phone_name:
        return None
    # Match pattern like "12/256GB" or "8/256GO" - extract number after /
    match = re.search(r'\d+\s*/\s*(\d+)\s*(?:GB|GO|Go)', phone_name, re.IGNORECASE)
    return match.group(1) if match else None

def getModelName(phone_name, brand):
    """Extract model name by removing brand and RAM/Storage info"""
    if not phone_name or not brand:
        return None
    # Remove brand from beginning
    model = re.sub(rf'^{re.escape(brand)}\s*', '', phone_name, flags=re.IGNORECASE)
    # Remove RAM/Storage pattern from end
    model = re.sub(r'\s*\d+\s*/\s*\d+\s*(?:GB|GO|Go)\s*$', '', model, flags=re.IGNORECASE)
    return model.strip() if model.strip() else None


def getDisplaySize(data_shape):
    """Extract display size text (e.g., '6.7 Pouces') from the card HTML"""
    if not data_shape:
        return None
    match = re.search(r'>\s*([\d.,]+)\s*Pouces\s*<', data_shape, re.IGNORECASE)
    if match:
        size = match.group(1).replace(',', '.').strip()
        return size
    return None


def getDisplayType(data_shape):
    """Extract display type text (e.g., 'AMOLED') from the card HTML"""
    if not data_shape:
        return None
    # First, try to find 'qualite-ecran-...' link
    match = re.search(r'qualite-ecran-[^"\s]*"[^>]*>\s*([^<]+?)\s*<', data_shape, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    display_keywords = [
        'AMOLED', 'OLED', 'LCD', 'IPS', 'TFT', 'Retina', 'Infinity', 'LTPO', 'LTPS',
        'Super AMOLED', 'Dynamic AMOLED', 'Fluid AMOLED', 'Super Retina', 'P-OLED',
        'ProMotion', 'Super LCD', 'PLS LCD'
    ]
    # Fallback: search all <a> tags for known display type keywords
    anchors = re.findall(r'<a[^>]*>([^<]+)</a>', data_shape, re.IGNORECASE)
    for anchor_text in anchors:
        text = anchor_text.strip()
        lowered = text.lower()
        if any(keyword.lower() in lowered for keyword in display_keywords):
            return text

    return None


def populate_phones(shapes):
    for shape in shapes:
        price = getPrice(shape)
        name = getPhoneName(shape)
        brand = getBrand(name)
        model = getModelName(name, brand)
        ram = getRAM(name)
        storage = getStorage(name)
        display_size = getDisplaySize(shape)
        display_type = getDisplayType(shape)
        if price and name and brand and model and ram and storage:
            phones.append({
                'brand': brand,
                'model': model,
                'ram': ram,
                'storage': storage,
                'price': price,
                'display_size': display_size,
                'display_type': display_type
            })
    
def create_csv():
    fields = ['brand', 'model', 'ram', 'storage', 'price', 'display_size', 'display_type']
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(phones)

for i in range(10): 
    #the website has pagination for the phones display (10 pages) visible in the url
    
    params = {'page_group': i}
    response = requests.get("https://webstar-electro.com/telephones-mobiles/?page=prix-telephones-portables-algerie&position=1&id_famille=3758",params=params,timeout=10) # maximum time for waiting


    # we check if our request did not fail (status code other than 200)
    try:
        if response.status_code == 200: 
            content = response.text
            shapes = getShapes(content)
            populate_phones(shapes)
            
        else:
            print(f"Error: status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    

create_csv()
