from bs4 import BeautifulSoup
import requests
import os

if __name__ == "__main__":
    while True:
        search = input("Enter Name: ")
        search = search.replace(' ', '+')
        try:
            url = requests.get(f"http://worldsubtitle.info/?s={search}")
        except requests.ConnectionError:
            print('Please check your internet connection')
            continue
        soap = BeautifulSoup(url.text, 'html.parser')
        soap = soap.find_all('div', {'class': 'cat-post-titel'})
        if soap:
            break
        else:
            print("Found Nothing.")
    num = 0
    print('Select from following list: ')
    for page in soap:
        num += 1
        print(f'{num}. {page.a["title"]}')
    link = []
    for page in soap:
        link.append(page.a['href'])
    while True:
        search = input()
        if search.isnumeric():
            search = int(search)
            if len(soap) >= search > 0:
                url = link[search - 1]
                soap = BeautifulSoup(requests.get(url).text, 'html.parser')
                break
            else:
                print("Wrong input")
        else:
            print('Wrong input')
    page = soap.find_all('div', {'class': 'new-link-1'})
    num = 0
    print('Select option to download:')
    for link in page:
        num += 1
        print(f"{num}. {link.string.strip()}")
    soap = soap.find_all('div', {'class': 'new-link-3'})
    url = []
    for link in soap:
        url.append(link.a['href'])
    while True:
        search = input()
        if search.isnumeric():
            search = int(search)
            if len(soap) >= search > 0:
                url = url[search - 1]
                break
            else:
                print('Wrong input')
        else:
            print('Wrong input')
    print('save location: ')
    print('1. Downloads')
    print('2. Desktop')
    print('3. Custom location')
    while True:
        path = input()
        if path == '1':
            path = os.path.join(os.environ["HOMEPATH"], "Downloads")
            break
        elif path == '2':
            path = os.path.join(os.environ["HOMEPATH"], "Desktop")
            break
        elif path == '3':
            path = input('Custom location: ')
            break
        else:
            print('Invalid input')
    r = requests.get(url, allow_redirects=True)
    name = url.split('/')[-1]
    with open(path + '/' + name, 'wb') as f:
        f.write(r.content)
        print('Download Complete')
