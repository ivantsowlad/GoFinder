from django.shortcuts import render, redirect
from .forms import SearchForm
import requests
from bs4 import BeautifulSoup
import pandas as pd
from django.http import HttpResponse


GOOGLE_URL = "https://www.google.com/search?q="
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def index(request):
    return render(request, 'main/index.html', {'title': 'Domovská'})


def project(request):
    error = ''
    pos = 0
    all_data = []
    art_dict = {}
    found_list = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Get the cleaned data from the form
            entered = form.cleaned_data['search']
            to_search = entered.replace(' ', '+')
            
            try:
                response = requests.get(url=(GOOGLE_URL + to_search), headers=HEADERS, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Try multiple selectors as Google changes its HTML structure frequently
                found_all = soup.find_all("div", {"class": "g"})
                
                # If no results with old selector, try newer ones
                if not found_all:
                    found_all = soup.find_all("div", {"class": "Gx5Zad"})
                
                for art in found_all:
                    link_tag = art.find('a')
                    if link_tag is None:
                        continue
                        
                    link = link_tag.get('href')
                    if link is not None:
                        if link.startswith('http') and 'aclk' not in link and '/search?' not in link:
                            pos = pos + 1
                            art_dict["link"] = link
                            
                            # Try multiple title selectors
                            try:
                                title_tag = art.find('h3')
                                art_dict["title"] = title_tag.text if title_tag else "No title"
                            except Exception as e:
                                art_dict["title"] = "No title"
                            
                            # Try multiple description selectors
                            try:
                                desc_tag = art.find("div", {"class": "VwiC3b"})
                                if not desc_tag:
                                    desc_tag = art.find("div", {"class": "IsZvec"})
                                if not desc_tag:
                                    # Try to find any span or div with text content
                                    desc_tag = art.find("span", {"class": "aCOpRe"})
                                art_dict["description"] = desc_tag.text if desc_tag else "No description"
                            except Exception as e:
                                art_dict["description"] = "No description"
                            
                            all_data.append(art_dict.copy())
                            art_dict = {}
            except Exception as e:
                error = f"Error fetching results: {str(e)}"
                form = SearchForm()
                data = {
                    'title': 'Projekt',
                    'to_search': [],
                    'form': form,
                    'error': error
                }
                return render(request, 'main/project.html', data)
            
            if all_data:
                df = pd.DataFrame(all_data)
                headers = ["Link", "Title", "Description"]
                df.columns = headers
                df.to_csv('google.csv', index=False, encoding='utf-8')
                for ind, row in df.iterrows():
                    found_list.append(list((row['Link'], row['Title'], row['Description'])))
            
            data = {
                'title': 'Hledání',
                'data': found_list,
                'search_term': entered,
                'results_count': len(found_list)
            }
            return render(request, 'main/search.html', data)
        else:
            error = 'Form was not correct.'
    form = SearchForm()
    data = {
        'title': 'Projekt',
        'to_search': found_list,
        'form': form,
        'error': error
    }
    return render(request, 'main/project.html', data)


def download_file(request):
    try:
        with open('./google.csv', 'r', encoding='utf-8') as f:
            file_content = f.read()
        response = HttpResponse(file_content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename=google.csv'
        return response
    except FileNotFoundError:
        return redirect('home')

