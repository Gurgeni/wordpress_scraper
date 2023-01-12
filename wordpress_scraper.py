import requests
import json
import csv

url ='https://www.thebrokebackpacker.com/wp-json/wp/v2/posts?categories=226'
http_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

asd = ''
def GetCategoryUrl(url):
    return f'https://{url}/wp-json/wp/v2/categories'

def GetPostUrl(url,id):
    return f'https://{url}/wp-json/wp/v2/posts?categories={id}'

def SaveCsv(type,title,category,link):
    data = [type,title,category,link]
    with open('Database.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

class Category:
    def __init__(self, id,name):
        self.id=id
        self.name = name

def GetAllCategories(website):
    baseUrl = GetCategoryUrl(website)
    categories=[]
    page  =1
    while 1:
        url = baseUrl+f'?page={page}'
        resp = session.get(url,headers=http_headers)
        if resp.status_code >= 400:
            raise Exception(f'something went wrong fetching category\r\nStatus Code:{resp.status_code}\r\nUrl:{url}')
        jsonData = json.loads(resp.text)
        if len(jsonData) ==0:
            break
        for item in jsonData:
            id = item['id']
            name = item['name']
            print(f'Category Id:{id}, Name:{name}')
            categories.append(Category(id,name))
        page+=1
    return categories


def GetPosts(website,Id,category):
    baseUrl = GetPostUrl(website,Id)
    page = 1
    while 1:
        url = baseUrl+f'&page={page}'
        resp = session.get(url,headers=http_headers)
        if resp.status_code > 400:
            raise Exception(f'something went wrong fetching posts\r\nStatus Code:{resp.status_code}\r\nUrl:{url}')
        jsonData = json.loads(resp.text)
        if len(jsonData) ==0:
            break
        try:
            code = jsonData['code']
            break
        except:
            pass
        for item in jsonData:
            type = item['type']
            link = item['link']
            title = item['title']
            SaveCsv(type,title,category,link)
            print(f'Post Type:{type},Title:{title},Category:{category},Link:{link}')
        page+=1


def main():
    print('Print Exit to stop process')
    global session
    while 1:
        try:
            url = input('Enter Url: ')
            if url == 'Exit' or url == 'exit':
                return
            session = requests.Session()
            categories = GetAllCategories(url)
            for category in categories:
                GetPosts(url,category.id,category.name)
        except Exception as e:
            print('Exception:')
            print(str(e))
        finally:
            session.close()


if __name__ == "__main__":
    main()
