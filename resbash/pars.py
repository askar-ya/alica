# -*- coding: utf-8 -*-
import requests
import json
import re
import time
import api
from random import randint
from bs4 import BeautifulSoup

def main():

	###################
	# парсинг новостей#
	###################

	url = 'https://resbash.ru'
	r = requests.get(url+'/news')
	soup = BeautifulSoup(r.text, 'lxml')

	#заголовки 
	news = soup.findAll('div', class_='page-news__name')
	titel_news=[]  
	for i in range(15):
		if news[i].find('a') is not None:
		    titel_news.append(str(news[i].text))

	#сылки на новости
	a = soup.findAll('a', class_='page-news__img')
	link_news=[]
	for i in range(15):
		link_news.append(url+str(a[i].get('href')))

	#ссылки на фото
	img = soup.findAll('a', class_='page-news__img')
	img_news=[]
	for i in range(15):
		img_news.append(url + '/' + str(img[i].find('img').get('src')))

	##сохранение фото
	for i in range(15):
		p = requests.get(str(img_news[i]))
		out = open('img-news/' + str(i) + "news.jpg", "wb")
		out.write(p.content)
		out.close()

	##подключение к api
	yandex = api.YandexImages()
	yandex.set_auth_token(token = 'AgAAAAAkiWDYAAT7owzE7VLXTEEukUZVVqOY9No')
	yandex.skills = '8e21efac-5e57-4c0a-8379-c8014f97147e'

	##удаление старых фото
	yandex.deleteAllImage()

	##добавление новых фото новостей
	for i in range(15):
		yandex.downloadImageFile('img-news/' +  str(i) + "news.jpg")

	##получение масива фото новостей
	imgId_news = []
	load_img = yandex.getLoadedImages()
	load_img = load_img[::-1]
	for i in range(15):
		imgId_news.append(str(load_img[i]['id']))

	##запись новостей
	news = {'news-titel':titel_news, 'news-link':link_news, 'news-imgId':imgId_news}


	###################
	# парсинг статей  #
	###################

	url = 'https://resbash.ru'
	r = requests.get(url+'/last-number/')
	soup = BeautifulSoup(r.text, 'lxml')

	#заголовки 
	stat = soup.findAll('div', class_='page-news__name')
	titel_stat=[]  
	for i in range(len(stat)):
		if stat[i].find('a') is not None:
		    titel_stat.append(str(stat[i].text))
	print(titel_stat)

	#лид 
	stat = soup.findAll('a', class_='page-news__anons')
	lid_stat=[]  
	for i in range(len(stat)):
		if stat[i].find('p') is not None:
		    lid_stat.append(str(stat[i].text))

	#сылки на статьи
	a = soup.findAll('a', class_='page-news__img')
	link_stat=[]
	for i in range(len(a)):
		link_stat.append(url+str(a[i].get('href')))

	#ссылки на фото
	img = soup.findAll('a', class_='page-news__img')
	img_stat=[]
	for i in range(len(a)):
		img_stat.append(url + '/' + str(img[i].find('img').get('src')))

	##сохранение фото
	for i in range(len(img_stat)):
		p = requests.get(str(img_stat[i]))
		out = open('img-stat/' + str(i) + "stat.jpg", "wb")
		out.write(p.content)
		out.close()

	##добавление новых фото статей
	for i in range(len(img_stat)):
		yandex.downloadImageFile('img-stat/' +  str(i) + "stat.jpg")

	##получение масива фото статей
	imgId_stat = []
	load_img = yandex.getLoadedImages()
	load_img = load_img[:len(img_stat)]
	load_img = load_img[::-1]

	for i in range(len(img_stat)):
		imgId_stat.append(str(load_img[i]['id']))

	##запись статей
	stat = {'stat-titel':titel_stat,'stat-lid':lid_stat, 'stat-link':link_stat, 'stat-imgId':imgId_stat}

	pars = {'news':news, 'stat':stat}
	with open('out_pars.json', 'w', encoding='utf8') as f:
		json.dump(pars, f, sort_keys=False,ensure_ascii=False,separators=(',', ': '))

main()