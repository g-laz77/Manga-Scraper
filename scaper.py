import requests
import os
import sys
import webbrowser,bs4
os.makedirs(sys.argv[1],0755)
add="http://www.mangareader.net"
i=1
while i<len(sys.argv):
    try:
        int(sys.argv[i])
        break
    except ValueError:
        i+=1

address='-'.join(sys.argv[1:i])
url=add+'/'+address+'/'+str(sys.argv[i])
print(url)
i=1
while 1:
     res = requests.get(url)
     res.raise_for_status()
     soup = bs4.BeautifulSoup(res.text)
     comicElem=soup.select('.episode-table #imgholder a img')
     if comicElem==[]:
         print("Done")
         break
     else:
         try:
             comicUrl=comicElem[0].get('src')
             print('Downloading image %s...' % (comicUrl))
             res = requests.get(comicUrl)
             res.raise_for_status()
         except requests.exceptions.MissingSchema:
             # skip this comic
             url=add+comicElem[0].get('href')
             continue
     imageFile = open(os.path.join(sys.argv[1], os.path.basename(comicUrl)), 'wb')
     for chunk in res.iter_content(100000):
         imageFile.write(chunk)
     imageFile.close()
     k=soup.select('#imgholder a')
     url=add+k[0].get('href')

#webbrowser.open(add+address)
