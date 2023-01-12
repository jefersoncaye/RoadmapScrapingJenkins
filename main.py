import requests
import  re
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

htmlPorAba = {}
dicionarioAbas = {}

def buscaPagina(url, usuario='', senha=''):
    html = requests.get(url, auth=HTTPBasicAuth(usuario, senha)).content
    return html

def buscaAbas(html):
    soup = BeautifulSoup(html, 'html5lib')
    barraAbas = soup.find(id="projectstatus-tabBar")
    for aba in barraAbas.find_all('a'):
        dicionarioAbas[aba.getText()] = aba.get('href')
"""        listaAbasLink.append(aba.get('href'))
        listaAbas.append(aba.getText())"""

def formataHTML(html):
    soup = BeautifulSoup(html, 'html5lib')
    for link in soup.find_all('a',
                              attrs={'href': re.compile("^http://")}):
        print(link.get('href'))

def buscaHtmlPorAba(dicionarioAbas):
    for link in dicionarioAbas.items():
        htmlPorAba[link[0]] = buscaPagina(f'http://cit/{link[1]}', 'testcomplete', '12345')


html = buscaPagina('http://cit/view/Empresarial/job/Empresarial%20-%20SQL%20Server/', 'testcomplete', '12345')
buscaAbas(html)
buscaHtmlPorAba(dicionarioAbas)
print(htmlPorAba.keys())

