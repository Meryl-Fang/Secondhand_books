
import requests
import re
import csv
from bs4 import BeautifulSoup 

def get_html(url):

	headers = {'user-agent':'Mozilla/5.0'}

	try:
		response = requests.get(url , headers = headers)
		#response.raise_for_status()
		print(response.text)
		return response.text
	except requests.RequestException:
		return None

def get_book_info(r):

    
	soup = BeautifulSoup(r,'lxml')


	tags = soup.find_all('div',class_='jsx-287405651 root cateogry_book_item')

	for tag in tags:
		title = tag.find('h3',class_='jsx-571581149 title').get_text()
		print(title)

        
if __name__ == '__main__':
	url='https://www.duozhuayu.com/open-collections/139770746170770544'
	get_book_info(get_html(url))

