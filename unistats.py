from lxml import html
from bs4 import BeautifulSoup
import urllib.request

def extractScores(html):
    races = ['SAP', 'TIT', 'KHR']
    soup = BeautifulSoup(html, 'html.parser')

    rows = soup.find('table',
                     {'class': 'shade max_width_minus_margin', 'align': 'center', 'border': '0', 'cellpadding': '0',
                      'cellspacing': '0'}).find_all('tr')

    result = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 8:
            if cols[0].text != 'Pos.':
#               result.append([cols[1].img.get('src').split('/')[-1].split('.')[0], cols[2].text[1:], cols[3].text,
# TODO: Fix russian encoding issue and return back player name (optional)
               result.append([cols[1].img.get('src').split('/')[-1].split('.')[0], cols[3].text,
               races[int(cols[4].img.get('src').split('/')[-1].split('.')[0][-1])-1], cols[5].text,
               cols[6].text, cols[7].text])
    return result



#####################################
# Retrieveing HTML from website
#####################################

result = []
output = open('output.txt', 'w')
for page in range(1, 51):
    url = 'http://www.uniwar.com/ladder.page?leaderboard=0&page=' + str(page)
    print('Requesting URL: ', url)
    response = urllib.request.urlopen(url)

    for row in extractScores(response.read()):
        result.append(row)
        line = str(row)[1:-1].encode('utf-8')
        output.write(str(row)[1:-1] + '\n')

output.close()

print('Total number of records: ', len(result))

