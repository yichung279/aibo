# standard import
from datetime import datetime
from sys import modules
import iso8601
import json
import re
import requests
import sys

#third-party import
from bs4 import BeautifulSoup

#local import
import config

def parse(url):
    pattern = '|'.join(config.available_host)
    match = re.search(rf'{pattern}', url)
    if not match:
        return None, None, None, None

    source = match.group()
    if 'medium.com' == source:
        url += '?format=json'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    date, title, article, keywords = getattr(modules['crawler'],
                                             source.replace('.', ''))(soup)
    return date, title, article, keywords

def blocktempo(soup):
    date = datetime.strptime(soup.find(class_='jeg_meta_date').text.strip('\n'), '%Y-%m-%d')
    title = soup.find('h1').text
    article = ''
    for paragraph in soup.find(class_='content-inner').find_all(['p', 'h3']):
        period = '' if 'h2' == paragraph.name else '。'
        article += paragraph.text + period
    keywords = ''
    for tag in soup.find(class_='jeg_post_tags').find_all('a'):
        keywords += tag.text + ','
    return date, title, article, keywords.strip(',')

def bnextcom(soup):
    date = datetime.strptime(soup.select('span.item')[0].text, '%Y.%m.%d')
    title = soup.find('h1').text
    article = soup.find(class_='htmlview').find('article').text
    keywords = ''
    for tag in soup.find(class_='cate_box').find_all('a'):
        keywords += tag.text + ','
    return date, title, article, keywords.strip(',')

def buzzorange(soup):
    date = iso8601.parse_date(soup.find('time')['datetime'])
    title = soup.find('h1').text
    article = ''
    for paragraph in soup.find(class_='fb-quotable').find_all(['p', 'h2']):
        period = '' if 'h2' == paragraph.name else '。'
        article += paragraph.text + period
    keywords = ''
    for tag in soup.find(class_='post-tags').find_all('a'):
        keywords += tag.text + ','
    return date, title, article, keywords.strip(',')

def chinatimes(soup):
    date = iso8601.parse_date(soup.find('time')['datetime'])
    title = soup.find('h1').text
    article = ''
    for paragraph in soup.find(class_='article-body').find_all(['p']):
        article += paragraph.text
    keywords = ''
    for tag in soup.find(class_='article-hash-tag').find_all('a'):
        keywords += tag.text + ','
    return date, title, article, keywords.strip(',')

def cnews(soup):
    date = datetime.strptime(soup.find(class_='date').text.strip(), '%Y-%m-%d')
    title = soup.find(class_='_line').find('strong').text
    article = soup.find('article').text
    keywords = ''
    for tag in soup.find(class_='tags').find_all('a'):
        keywords += tag.text + ','
    return date, title, article, keywords.strip(',')

def ctee(soup):
    date = iso8601.parse_date(soup.find('time')['datetime'])
    title = soup.find(class_='post-title').text
    article = soup.find(class_='entry-content').text
    keywords = ''
    for tag in soup.find(class_='terms-label').find_all('a'):
        keywords += tag.text + ','
    return date, title, article, keywords.strip(',')

def ecltn(soup):
    date = datetime.strptime(soup.find(class_='time').text, '%Y/%m/%d %H:%M')
    title = soup.find('h1').text
    selects = soup.find_all(class_=['before_ir', 'after_ir', 'appE1121'])
    for select in selects:
        select.decompose()
    article = soup.find(class_='text').text.strip()
    return date, title, article, None

def fncebc(soup):
    date = re.sub(r'[^\d \:\/]', '', soup.find(class_='info').text).strip()
    date = datetime.strptime(date, '%Y/%m/%d %H:%M')
    title = soup.find('h1').text
    article = ''
    for paragraph in soup.find(id='fncNewsEditorContainer').find_all('p'):
        article += paragraph.text
    return date, title, article, None

def inside(soup):
    date = datetime.strptime(soup.find(class_='post_date').text.strip('\n'), '%Y/%m/%d')
    title = soup.find('h1').text
    article = ''
    for paragraph in soup.find('article').find_all('p'):
        article += paragraph.text
    keywords = soup.find(class_='post_meta').find_all('li')[-1].text.replace('\n', '').replace('、', ',')
    return date, title, article, keywords


def ithome(soup):
    date = datetime.strptime(soup.find(class_='created').text, '%Y-%m-%d')
    title = soup.find('h1').text
    article = soup.find(class_='content-summary').text + soup.find('article').text
    return date, title, article, None

def mediumcom(soup):
    string = re.sub(r'.*;', '', soup.text)
    data = json.loads(string)['payload']['value']
    date = datetime.fromtimestamp(data['updatedAt'] / 1000)
    title = data['title']
    article = ''
    keywords = ''

    for paragraph in data['content']['bodyModel']['paragraphs']:
        if 'text' in paragraph.keys():
            article += paragraph['text']

    for tag in data['virtuals']['tags']:
        keywords += tag['name'] + ','
    return date, title, article, keywords.strip(',')

def moneyudn(soup):
    date = datetime.strptime(soup.find(class_='shareBar__info').find('span').text, '%Y-%m-%d %H:%M')
    title = soup.find('h2').text
    article = ''
    for paragraph in soup.find(id='article_body').find_all('p'):
        article += paragraph.text
    keywords = ''
    for tag in soup.find(id='story_tags').find_all('a'):
        keywords += tag.text + ','
    return date, title, article, keywords.strip(',')

def meetbnext(soup):
    date = soup.find(class_='article_info').find_all('span')[-1].text
    date = datetime.strptime(date.replace('Date：', ''), '%m / %d / %Y')
    title = soup.find('h1').text
    article = soup.find(class_='htmlview').text
    keywords = ''
    for keyword in soup.find(class_='cates').find_all('a'):
        keywords += keyword.text + ','
    return date, title, article, keywords.strip(',')

def newsyahoo(soup):
    date = iso8601.parse_date(soup.find('time')['datetime'])
    title = soup.find('h1').text
    article = soup.find('article').text
    keywords = ''
    for a in soup.find_all('a', href=True):
        if re.search(r'\/tag\/', a['href']):
            keywords += a.text + ','
    return date, title, article, keywords.strip(',')

def stockyahoo(soup):
    date = iso8601.parse_date(soup.find('time')['datetime'])
    title = soup.find('h1').text
    article = soup.find('article').text
    return date, title, article, None

def technews(soup):
    date = re.sub(r'[\u4E00-\u9FFF\s]', '', soup.select('#main header span.body')[1].text)
    date = datetime.strptime(date, '%Y%m%d%H:%M')
    title = soup.find('h1').text
    article = ''
    for paragraph in soup.find(class_='indent').find_all('p'):
        article += paragraph.text
    keywords = ''
    for tag in soup.find(class_='entry-content').find_all('div')[-1].find_all('a'):
        keywords += tag.text + ','
    return date, title, article, keywords.strip(',')

def top10(soup):
    date = iso8601.parse_date(soup.find('time')['datetime'])
    title = soup.find('h1').text
    article = ''
    for paragraph in soup.find(class_='post-content').find_all('p', recursive=False):
        article += paragraph.text
    keywords = ''
    for tag in soup.find(class_='tagcloud').find_all('a'):
        keywords += tag.text + ','
    return date, title, article, keywords.strip(',')

def udncom(soup):
    date = datetime.strptime(soup.find(class_='authors').find('time').text, '%Y-%m-%d %H:%M')
    title = soup.find('h1').text
    article = soup.find(class_='article-content__editor').text
    keywords = ''
    for keyword in soup.find(id='keywords').find_all('a'):
        keywords += keyword.text + ','
    return date, title, article, keywords.strip(',')

def wealthcom(soup):
    date = re.sub(r'[\u4E00-\u9FFF\s\:]', '', soup.select('.entry-header p')[0].text)
    date = datetime.strptime(date, '%Y-%m-%d')
    title = soup.find('h1').text
    article = ''
    for paragraph in soup.find(id='cms-article').find_all('p'):
        article += paragraph.text
    keywords = ''
    for tag in soup.find(class_='article-tag').find_all('a'):
        keywords += tag.text + ','
    return date, title, article, keywords.strip(',')

def wealthhket(soup):
    selects = soup.find(class_='article-details-info-container_date').find_all('span')

    date = datetime.strptime(selects[0].text + ' ' + selects[1].text, '%H:%M %Y/%m/%d')
    title = soup.find('h1').text

    for table in soup.find_all('table'):
        table.decompose()
    article = soup.find(class_='article-detail-content-container').text
    keywords = soup.find(class_='article-detail_extra-info').find_all('span')[-1].text
    return date, title, article, keywords

if '__main__' == __name__:
    url = sys.argv[1]
    pattern = '|'.join(config.available_host)
    match = re.search(rf'{pattern}', url)
    if match:
        source = match.group()
        if 'medium.com' == source:
            url += '?format=json'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')

        date, title, article, keywords = getattr(modules['__main__'], source.replace('.', ''))(soup)
        print(date)
        print(title)
        print(article)
        print(keywords)


