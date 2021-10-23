import requests, bs4

def download_file(url, filename=''):
    req = requests.get(url)
    try:
        if filename:
            filename = str(filename)+req.url[url.rfind('.'):]            
        else:
            filename = req.url[url.rfind('/')+1:]

        with requests.get(url) as req:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=10240):
                    if chunk:
                        f.write(chunk)
            return filename
    except Exception as e:
        print(e)
        return None

body = True
while body:
    #print()
    #domain = str(input("Choose a domain (rs/is/st): "))
    #print("[In case of exception, close & run again with a different domain]")

    print()
    print("[In case of exception or if it is taking a long time, close & run again]")
    isbn = str(input("Enter the ISBN: "))
    try:
        req = requests.get('https://libgen.rs/search.php?req='+str(isbn)+'&open=0&res=25&view=simple&phrase=1&column=def')
    except Exception:
        try:
            req = requests.get('https://libgen.is/search.php?req='+str(isbn)+'&open=0&res=25&view=simple&phrase=1&column=def')
        except Exception:
            req = requests.get('https://libgen.st/search.php?req='+str(isbn)+'&open=0&res=25&view=simple&phrase=1&column=def')
        
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    mirror = ["this mirror", "Libgen.lc"] #"Z-Library", "Libgen.pw", "BookFI.net"
    #linkNum = int(input("Choose a download link (1/2/3/4/5): "))
    #print("[P.S. In case of exception, close & run again with a different download link]")

    i = 0
    run = True
    while run:
        try:
            linkElements = soup.find_all('a', {'title':mirror[i]})
            if len(linkElements)==0:
                print()
                print("ISBN either invalid or not found") 
            run = False
        except Exception as e:
            if i<2:
                i += 1
            else:
                print(e)
                run = False

    try:
        res = requests.get(linkElements[0].get('href'))
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        linkElements = soup.find_all('a', string="GET")

        if i==0:
            title = soup.find('h1').contents[0]
        elif i==1:
            title = soup.find('h2').contents[0]
    
        attributes = soup.find_all('p')
        print()
        print("Downloading ", title, " by ", attributes[0].contents[0])
        print(attributes[1].contents[0])
        print(attributes[2].contents[0])

        #print(linkElements[0].get('href'))
        download_file(linkElements[0].get('href'), title)
        print()
        print("Downloaded!")
    except Exception as e:
        #print(e)
        pass

    reply = str(input("Do you have another book to download?(y/n) "))
    if reply == 'y' or reply == 'Y':
        body = True
        print("______________________________________________________________________")
    else:
        body = False
