import requests
import csv
from bs4 import BeautifulSoup

MOP_COUNT = 460

def load_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    except requests.RequestException as e:
        print(f"Error loading webpage: {e}")
        return None


def dom_get_next_sibling_text(dom, id):
    label = dom.find(id=f"{id}")
    next_sibling = label.find_next_sibling()
    return next_sibling.text if next_sibling else ""

csv_file = open("mop_list-0.csv", "w", newline="")
csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
csv_writer.writerow(("lp.", "imię i nazwisko", "wykształcenie", "lista", "nr okręgu", "miasto", "głosy"))

for i in range(1, MOP_COUNT + 1):
    url = f"https://www.sejm.gov.pl/Sejm10.nsf/posel.xsp?id={str(i).zfill(3)}&type=A"
    dom = load_webpage(url)

    if dom:
        name = dom.find("h1").text
        list = dom_get_next_sibling_text(dom, "lblLista")
        district_combined = dom_get_next_sibling_text(dom, "lblOkreg").split("\xa0\xa0")
        district_no = int(district_combined[0])
        city = district_combined[1]
        votes = int(dom_get_next_sibling_text(dom, "lblGlosy"))
        education = dom_get_next_sibling_text(dom, "lblWyksztalcenie")
        print(f"{i}. {name}")
        csv_writer.writerow((i, name, education, list, district_no, city, votes))

csv_file.close()