import time
import re
import os
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

link = 'http://cit/view/Empresarial/job/Empresarial%20-%20SQL%20Server/'

# 'http://cit/view/Empresarial/job/Empresarial%20-%20SQL%20Server/'

def buscaPagina(url, usuario='', senha=''):
    html = requests.get(url, auth=HTTPBasicAuth(usuario, senha)).content
    return html

def buscaAbas(html):
    dicionarioAbas = {}
    soup = BeautifulSoup(html, 'html5lib')
    barraAbas = soup.find(id="projectstatus-tabBar")
    for aba in barraAbas.find_all('a'):
        dicionarioAbas[aba.getText()] = aba.get('href')
    return dicionarioAbas

def buscaLinks(dicionario):
    dicionarioNovo = {}
    for i in dicionario.items():
        listaTestes = []
        soup = BeautifulSoup(i[1], 'html5lib')
        for link in soup.find_all('a',
                                  attrs={"class":"jenkins-table__link model-link inside"}):
            listaTestes.append(link.get('href'))
        dicionarioNovo[i[0]] = listaTestes
    return dicionarioNovo

def buscaHtmlPorAba(dicionarioAbas):
    htmlPorAba = {}
    for link in dicionarioAbas.items():
        htmlPorAba[link[0]] = buscaPagina(f'http://cit/{link[1]}', 'testcomplete', '12345')
    return htmlPorAba

def buscaProjeto(link):
    projeto = []
    html = buscaPagina(link, 'testcomplete', '12345')
    soup = BeautifulSoup(html, 'html5lib')
    for cofiguracoes in soup.find_all('input', attrs={"name": "_.suite"}):
        projeto.append(cofiguracoes.get('value'))
    for cofiguracoes in soup.find_all('input', attrs={"name": "_.project"}):
        projeto.append(cofiguracoes.get('value'))
    projeto = list(filter(len, projeto))
    if len(projeto) == 2:
        return projeto
    else: return ['', '']


def buscaKeywordsProjeto(listaDiretorioProjeto):
    caminho = listaDiretorioProjeto[0]
    caminho = caminho.replace('\\', '==').replace('/', '==')
    caminho = caminho.split('==')
    novoCaminho = ''
    for i in caminho[:-1]:
        novoCaminho = novoCaminho + '\\' + i
    listaKeywords = []
    novoCaminho = f'D:\workspace\Empresarial.TC{novoCaminho}\\{listaDiretorioProjeto[1]}\KeywordTests\KeywordTests.tcKDT'
    #novoCaminho = f'D:\\workspace\\testesweb{novoCaminho}\\{listaDiretorioProjeto[1]}\KeywordTests\KeywordTests.tcKDT'
    if os.path.exists(novoCaminho):
        arquivo = open(novoCaminho, 'r')
        for linha in arquivo:
            if 'child name=' in linha:
                teste = linha.replace('{', '').replace('}', '').replace('key=', '').replace('<child name=', '').replace(
                    '/>', '')
                teste = re.sub(r'"\w\w\w\w\w\w\w\w-\w\w\w\w-\w\w\w\w-\w\w\w\w-\w\w\w\w\w\w\w\w\w\w\w\w"', '', teste)
                listaKeywords.append(teste.strip())
    return listaKeywords

def criaTXTModeloRoadmap(dicionarioTestesPorAba):
    with open("documentacaoRoadmap.txt", "w") as txt:
        txt.write('h1. Listagem de Testes')
        cont = 1
        for item in dicionarioTestesPorAba.items():
            if item[0].lower() == 'jobs':
                continue
            txt.write('\n\n-----------\n\n')
            txt.write(f'h2. {cont} - {item[0]}')
            txt.write('\n\n-----------\n')
            cont += 1
            cont2 = 1
            for teste in item[1]:
                linkTeste = link + '/' + teste
                txt.write(f'\nh3. {cont2} - "{teste.replace("job/","").replace("/",(""))}":{linkTeste}')
                txt.write(f'\n\nObjetivo: ')
                time.sleep(3)
                projetos = buscaProjeto(f"{linkTeste}/configure")
                txt.write(f'\n\n*Project Suite:* {projetos[0]}'
                          f'\n*Project:* {projetos[1]}')
                txt.write('\n')
                cont2 += 1
                txt.write(f'\n\n*Keywords:*')
                for linha in buscaKeywordsProjeto(projetos):
                    txt.write('\n')
                    txt.write(f'- {linha}')

                txt.write('\n\nTeste implementado na tarefa:')
                txt.write(f'\n\nLink do teste no Jenkins: {linkTeste}')
                txt.write('\n\n-----------\n')
        txt.close()



def criaTXTModeloFuncionalidade(dicionarioTestesPorAba):
    with open("documentacaoFuncionalidade.txt", "w", encoding='utf-8') as txt:
        txt.write('h1. Testes Empresarial, mapeamento por funcionalidades e rotinas')
        cont = 1
        for item in dicionarioTestesPorAba.items():
            if item[0].lower() == 'jobs':
                continue
            txt.write('\n\n-----------\n\n')
            txt.write(f'h2. {cont} - {item[0]}')
            txt.write('\n\n-----------\n')
            cont += 1
            cont2 = 1
            for teste in item[1]:
                linkTeste = link + teste
                txt.write(f'\nh3. {cont2} - Documentação do Teste: {teste.replace("job/","").replace("/",(""))}')
                txt.write('\n\n* *Categoria / Rotina do teste:*')
                txt.write('\n\n* *Subcategoria:*')
                txt.write('\n\n* *Objetivo:*')
                txt.write('\n\n* *Cenário de teste:*')
                txt.write('\n\nTarefa de implementação do teste:')
                txt.write(f'\n\nLink do teste: {linkTeste}')
                txt.write('\n')
                txt.write('\n-----------\n')
                cont2 += 1
        txt.close()

html = buscaPagina(link, 'testcomplete', '12345')
dicionarioAbas = buscaAbas(html)
htmlPorAba = buscaHtmlPorAba(dicionarioAbas)
dicionarioTestesPorAba = buscaLinks(htmlPorAba)
criaTXTModeloRoadmap(dicionarioTestesPorAba)
