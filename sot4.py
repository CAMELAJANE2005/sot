import requests
from bs4 import BeautifulSoup

def get_html_content(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def extract_article_title(soup):
    title = soup.find('h1', id='firstHeading').text
    return title

def extract_article_text(soup):
    article_text = {}
    paragraphs = soup.find_all('p')
    
    current_heading = None
    current_paragraphs = []
    
    for paragraph in paragraphs:
        if paragraph.find('span', class_='mw-headline'):
            if current_heading is not None:
                article_text[current_heading] = ' '.join(current_paragraphs)
                current_paragraphs = []
            
            current_heading = paragraph.find('span', class_='mw-headline').text
        
        current_paragraphs.append(paragraph.text)
    
    if current_heading is not None:
        article_text[current_heading] = ' '.join(current_paragraphs)
    
    return article_text

def collect_redirect_links(soup):
    redirect_links = []
    links = soup.find_all('a', href=True)
    
    for link in links:
        href = link['href']
        if href.startswith('/wiki/') and ':' not in href:
            redirect_links.append(href)
    
    return redirect_links


def process_wikipedia_page(url):
    soup = get_html_content(url)
    title = extract_article_title(soup)
    article_text = extract_article_text(soup)
    redirect_links = collect_redirect_links(soup)
    
    result = {
        'title': title,
        'article_text': article_text,
        'redirect_links': redirect_links
    }
    
    return result

url = 'https://en.wikipedia.org/wiki/Artificial_intelligence'
result = process_wikipedia_page(url)

print("Title:", result['title'])
print("Article Text:")
for heading, paragraph in result['article_text'].items():
    print(heading)
    print(paragraph)
    print()

print("Redirect Links:", result['redirect_links'])