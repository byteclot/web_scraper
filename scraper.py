import string
from bs4 import BeautifulSoup
import requests
import os


# url = input("Input the URL:\n")

# movie_dictionary = {}
#try:
#    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
#    if r.status_code == 200:
#        soup = BeautifulSoup(r.content, 'html.parser')
#        title_tag = soup.find('title')
#        tag = soup.find('meta', {'name': 'description'})
#        text = tag.text
#        title_split = title_tag.text.split(" (")
#        if len(title_split) < 2:
#            print("Invalid movie page!")
#        else:
#            movie_dictionary['title'] = title_split[0]
#            movie_dictionary['description'] = tag.get('content') #.split(".")[-1].strip()
#            print(movie_dictionary)
#    else:
#        print("Invalid movie page!")
# except:
#    print("Invalid movie page!")

# r = requests.get(url)
# status = r.status_code
# print(status)
# if status == 200:
#    page_content = r.content
#    saved_file = open('source.html', 'wb')
#    saved_file.write(page_content)
#    saved_file.close()
#    print("Content saved.")
# else:
#    print(f'The URL returned {status}!')


saved_articles = []

num_of_pages = int(input())
desired_type = input()

for i in range(num_of_pages):

    url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i + 1}'
    folder_name = f'Page_{i + 1}'
    os.makedirs(folder_name, exist_ok=True)
    # print(url)
    # print(folder_name)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.find_all('article')

    links_list = []

    for article in articles:
        a_t = article.find('span', {'class': 'c-meta__type'})
        if a_t.text.lower() == desired_type.lower():
            h_l = article.find('a', {'data-track-action': 'view article'})
            links_list.append((h_l.get('href')))

    # print(links_list)
    for article_link in links_list:
        article_url = f'https://www.nature.com{article_link}'
        r = requests.get(article_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        article_body = soup.find('div', {'class': 'c-article-body'})
        article_body_text = article_body.text
        article_title = soup.find('h1').text
        # print()
        translator = str.maketrans('', '', string.punctuation + '—’')
        article_title = article_title.translate(translator).rstrip()
        file_name = article_title.replace(' ', '_') + '.txt'
        my_file = open(os.path.join(folder_name, file_name), 'wb')
        my_file.write(article_body_text.rstrip().encode())
        my_file.close()
        saved_articles.append(file_name)

print("Saved all articles.")
# print("Saved articles:")
# print(saved_articles)

