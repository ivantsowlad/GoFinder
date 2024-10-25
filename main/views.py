from django.shortcuts import render, redirect
from .forms import SearchForm
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.http import HttpResponse


GOOGLE_URL = "https://www.google.com/search?q="
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def index(request):
    return render(request, 'main/index.html', {'title': 'Vítám Vás na mé stránce s projektem.'})


def project(request):
    error = ''
    pos = 0
    all_data = []
    art_dict = {}
    found_list = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            entered = (form['search'].as_text().replace('<input type="text" name="search" value="', '')
                                               .replace('" required id="id_search">', ''))
            to_search = entered.replace(' ', '+')
            response = requests.get(url=(GOOGLE_URL + to_search), headers=HEADERS).text
            soup = BeautifulSoup(response, "html.parser")
            found_all = soup.find_all("div", {"class": "g"})
            for art in range(0, len(found_all)):
                link = found_all[art].find('a').get('href')
                if link is not None:
                    if link.find('https') != -1 and link.find('http') == 0 and link.find('aclk') == -1:
                        pos = pos + 1
                        art_dict["link"] = link
                        try:
                            art_dict["title"] = found_all[art].find('h3', {"class": "DKV0Md"}).text
                        except:
                            art_dict["title"] = None
                        try:
                            art_dict["description"] = found_all[art].find("div", {"class": "VwiC3b"}).text
                        except:
                            art_dict["description"] = None
                        all_data.append(art_dict)
                        art_dict = {}
                    else:
                        continue
                else:
                    continue
            df = pd.DataFrame(all_data)
            headers = ["Link", "Title", "Description"]
            df.columns = headers
            df.to_csv('google.csv', index=False, encoding='utf-8')
            for ind, row in df.iterrows():
                found_list.append(list((row['Link'], row['Title'], row['Description'])))
            data = {
                'title': 'Výsledky hledání',
                'data': found_list
            }
            return render(request, 'main/search.html', data)
        else:
            error = 'Form was not correct.'
    form = SearchForm()
    data = {
        'title': 'Pro vyhledání napíšte do pole a klikněte tlačítko',
        'to_search': found_list,
        'form': form,
        'error': error
    }
    return render(request, 'main/project.html', data)


def download_file(request):
    for i in range(0, 1):
        f = open('../GoFinder/google.csv', 'r').read()
        response = HttpResponse(f)
        response['Content-Disposition'] = 'attachment;filename=google.csv'
        return response
    redirect('home')

