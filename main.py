import argparse
import whois
import unicodedata
import random
import json

import constants
import tlds

parser = argparse.ArgumentParser(description="tldwatch", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--no-search", "-s", default=False, help="Don't look up domain availability", action='store_true')

args = parser.parse_args()
config = vars(args)

def asciify(string):
    return unicodedata.normalize('NFD', string).encode('ascii', 'ignore').decode()

try:
    f = open('tlds.json')
    tlds_file = json.load(f)
except:
    print(f"{constants.colors.FAIL}[!] {constants.colors.ENDC}Can't open TLDs database or it is corrupt (tlds.json)!\nPlease use one of the scrapers or use the \"--no-search\" launch argument")
    exit()

tlds_list = tlds.list

for i in range(len(tlds_list)):
    tlds_list[i] = tlds_list[i].lower()

for tld in tlds_file['result']:
    tld = tld['tld']
    if(tld not in tlds_list):
        tlds_list.append(tld)

running = True

while running:
    print("="*32)
    inp = input("🔎 Search: ")
    inp = " ".join(inp.lower().split())

    if(inp == ""): 
        running = False
        continue

    if("." in inp):
        continue

    inp = asciify(inp)

    found = False
    results = []

    for tld in tlds_list:
        parts = [(inp[:-len(tld)]), ""]
        if(inp.endswith(tld)):
            found = True
            tld_item = None
            for tld_file in tlds_file['result']:
                if(tld_file['tld'] == tld):
                    tld_item = tld_file
            parts = [parts[0], tld]
            result = ".".join(parts)
            if(not config['no_search']):
                print(f"{constants.colors.OKCYAN}[i] {constants.colors.ENDC}Searching {result}...", end="\r")
                try:
                    w = whois.whois(result.lower()) # aawdhaiwhdawdicom
                except:
                    w = {'domain_name': None}
                if(w['domain_name'] is None):
                    price = None
                    print(f"{constants.colors.OKGREEN}[✓] {constants.colors.ENDC}{result} is available")
                    if(tld_item is not None):
                        price = tld_item['register']
                    results.append([result, price])
                else:
                    print(f"{constants.colors.FAIL}[!] {constants.colors.ENDC}{result} is already registered")
            else:
                results.append(result)
    
    if(not found):
        print(f"{constants.colors.FAIL}[!] {constants.colors.ENDC}TLD not found")
    if(len(results) > 0):
        print(f"Results:")
        for result in results:
            print(f"\t{constants.colors.OKCYAN + '['+str(result[1])+']' if result[1] is not None else constants.colors.WARNING + '[NP]'} {constants.colors.ENDC}{result[0]}")

    print("="*32)

if(not config['no_search']):
    f.close()