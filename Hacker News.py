import requests
from bs4 import BeautifulSoup
import pprint
import os


def sort_by_votes(hn):
    return sorted(hn, key=lambda k: k['votes'], reverse=True)


def create_the_list(links, subtext):
    my_list = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = vote[0].getText().replace(
                ' point', '').replace('s', '')
            points = int(points)
            if points > 100:
                my_list.append({'title': title, 'link': href, 'votes': points})

    return my_list


def get_votes_list(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.storylink')
    subtext = soup.select('.subtext')
    return create_the_list(links, subtext)


def get_number_of_pages():
    while True:
        try:
            number_of_pages = int(input("Please enter the number of pages "))
            if number_of_pages <= 0:
                print("Please enter number greater than 0")
                continue
        except ValueError:
            print("Please enter only numbers  ")
        else:
            return number_of_pages


def main():
    number_of_pages = get_number_of_pages()
    final_votes_list = []
    for i in range(1, number_of_pages+1):
        final_votes_list += get_votes_list(
            f'https://news.ycombinator.com/news?p={i}')

    final_votes_list = sort_by_votes(final_votes_list)
    pprint.pprint(final_votes_list)


if __name__ == "__main__":
    main()
    os.system("pause")
