## Website(s) used

- Webstar Electro — https://webstar-electro.com/telephones-mobiles/?page=prix-telephones-portables-algerie&position=1&id_famille=3758

The scraper paginates through the site using the `page_group` parameter in the requests.

## What data was collected

The scraper extracts the following fields for each phone and writes them to `output.csv`:

- brand: Manufacturer
- model: Model name
- ram: RAM size in GB
- storage: Storage size in GB
- price: Price in Algerian Dinars (integer)
- display_size: Screen diagonal in inches
- display_type: Display technology (e.g., AMOLED, LCD)

## Explanation of the regular expressions used

The regexes are described below.

- getShapes(html_content)

  - Regex: `r'class="card-body"(?:.*?)>(.*?)</div>'` with `re.DOTALL`
  - Purpose: find each phone card's inner HTML. It looks for the opening marker `class="card-body"`, then captures everything until the first `</div>` following that, using DOTALL so newlines are included. The `(?:.*?)>` portion skips attribute text up to the close of the opening tag.

- getPrice(data_shape)

  - Regex: `r'Prix(?:.*?)(\d{1,3}(?: \d{3})*)\s*Da'` with `re.DOTALL`
  - Purpose: find the price labeled by the word "Prix" and followed by a number and the currency `Da`. The numeric capture supports thousands separated by spaces (e.g., `51 000`) and converts the captured group to an integer after removing spaces.

- getPhoneName(data_shape)

  - Primary regex: `r'<h3[^>]*class="produit_titre[^\"]*"[^>]*>\s*<a[^>]*>([^<]+)</a>'` with `re.DOTALL`
  - Fallback regex: `r'<a[^>]*title="[^"]*"[^>]*href="[^"]*telephones-mobiles[^"]*"[^>]*>([^<]+)</a>'`
  - Purpose: extract the visible phone name from the anchor inside the `produit_titre` heading. The fallback looks for any anchor with a `title` attribute that links to the phones section.

- getBrand(phone_name)

  - Regex: `r'^([A-Za-z]+)'`
  - Purpose: grab the first alphabetical token from the phone name as the brand. This is a simple heuristic and may fail for brands with spaces or non-Latin characters.

- getRAM(phone_name)

  - Regex: `r'(\d+)\s*/\s*\d+\s*(?:GB|GO|Go)'`, case-insensitive
  - Purpose: extract the number before the `/` in names that use the `RAM/Storage` notation (e.g., `8/256GO`), returning the RAM amount.

- getStorage(phone_name)

  - Regex: `r'\d+\s*/\s*(\d+)\s*(?:GB|GO|Go)'`, case-insensitive
  - Purpose: extract the storage number after the `/` in `RAM/Storage` notation.

- getModelName(phone_name, brand)

  - Uses Python `re.sub` to remove the brand at the start and the `RAM/Storage` pattern at the end: `r'\s*\d+\s*/\s*\d+\s*(?:GB|GO|Go)\s*$'`
  - Purpose: return the remaining text as the model name.

- getDisplaySize(data_shape)

  - Regex: `r'>\s*([\d.,]+)\s*Pouces\s*<'`, case-insensitive
  - Purpose: capture the numeric display size (like `6.7`) from anchor/label elements that include the word `Pouces` (French for "inches"). Commas are normalized to dots.

- getDisplayType(data_shape)
  - First attempt looks for links with `qualite-ecran-...` in the href and captures its anchor text.
  - Fallback scans all `<a>` anchors and compares anchor text to a keyword list (AMOLED, OLED, LCD, IPS, etc.).
  - Purpose: heuristically identify a display technology string.
