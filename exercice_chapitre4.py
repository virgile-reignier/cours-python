import requests, csv
from bs4 import BeautifulSoup
url = "http://www.memoire-ardeche.com/cahiers/table.htm"
response_table = requests.get(url)
page_table = response_table.text
soup = BeautifulSoup(page_table, features="html.parser")
lines_nodes = soup.find_all('tr')
results = []
for line in lines_nodes[1:]:
    content_line = {}
    informations = line.find_all("td")
    content_line["num"] = informations[0].get_text()
    content_line["date"] = informations[1].get_text()
    content_line["title"] = informations[2].find("a").get_text()
    url_num = "http://www.memoire-ardeche.com/cahiers/" + informations[2].find("a")["href"]
    content_line["url"] = url_num
    content_line["title_page"] = BeautifulSoup(requests.get(url_num).text, features="html.parser").find('title').get_text()
    results.append(content_line)
with open('matp.csv', 'w', newline='') as csvfile:
    fieldnames = ['num', 'date', 'title', 'url', 'title_page']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for line in results:
        writer.writerow(line)