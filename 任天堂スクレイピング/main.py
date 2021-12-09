from bs4 import BeautifulSoup
import requests 
def main():
    url = 'https://www.yahoo.co.jp/'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find_all(class_="nc3-c-softCard__name")
    print(title)
if __name__ == '__main__':
    main()
