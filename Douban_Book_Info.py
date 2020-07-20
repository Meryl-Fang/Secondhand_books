

import requests
import re
import csv
from bs4 import BeautifulSoup 

s = requests.Session()

def login_douban():

	login_url = 'https://accounts.douban.com/j/mobile/login/basic'

	headers = {'user-agent':'Mozilla/5.0','Referer':'https://accounts.douban.com/passport/login_popup?login_source=anony'}

	data ={'name':,'password':,'remember':'false'} #logindata omitted

	try:
		r = s.post(login_url,headers = headers, data = data)
		r.raise_for_status()
	except:
		print("login failed: " +r.text)

	#print(r.text)

def get_html(url):

	headers = {'user-agent':'Mozilla/5.0'}

	try:
		response = s.get(url , headers = headers)
		response.raise_for_status()
		print("html successfully fetched")
		return response.text
	except requests.RequestException:
		print("html failed")
		return None

###        With the exact douban url of the book, use this function  #####
####### E.G. https://book.douban.com/subject/11508896/
def get_book_info(r):

    #delete <br> in html and replace it with a made-up tag what can i do??!!
	new_r = r.replace('<br>','<span class="temp">').replace('<br/>','<span/>')

	
	soup = BeautifulSoup(new_r,'lxml')


	#e.g. <span property="v:itemreviewed">夜航</span>
	title = soup.find('span',property = 'v:itemreviewed').get_text()
	#print(title)

	book_info = soup.body.find('div', id='info')
	book_rating = soup.body.find('div', class_='rating_self clearfix').find('strong').get_text(strip=True)
	#print(book_rating)

	author = book_info.find('a').get_text().replace(' ','').replace('\n','')
	#print(author)

	for line in book_info.find_all('span',class_='temp'):
		line.text.strip().replace(' ','')


def get_book_series_info(series_url,total_page_number):

	
	urls = [series_url+ str(i+1) for i in range(total_page_number)]
	result = []

	for i in urls:
		r=get_html(i)
		#sleep(5)
		soup = BeautifulSoup(r,'lxml')

		for tags in soup.find_all('div',class_='info'):#,class_='subject-item'):
	
			info_list=[]
			title = tags.find('a').get('title')
			#print(title)


			pub_tag = tags.find('div',class_='pub').get_text().strip()
			pub_tags = pub_tag.replace(' ','').split('/')

			#### some books have 匿名作者
			if len(pub_tags)==5:
				author_w_nationality = pub_tags[0]
				translator = pub_tags[1]
				publisher = pub_tags[2]
				date_of_1st_publishing = pub_tags[3]
				face_value = re.search(r"\d{1,4}.\d{0,2}",pub_tags[4]).group()
				#print(face_value)

			elif len(pub_tags) == 4:
				author_w_nationality = pub_tags[0]
				translator = pub_tags[0]
				publisher = pub_tags[1]
				date_of_1st_publishing = pub_tags[2]
				face_value = re.search(r"\d{1,4}.\d{0,2}",pub_tags[3]).group()

			

			if tags.find('span',class_='rating_nums')!=None:
				rating = tags.find('span',class_='rating_nums').get_text()
			else:
				rating = 'N/A'

			if tags.find('span',class_='pl')!=None:
				rating_pop = re.search(r"\d{1,11}",tags.find('span',class_='pl').get_text()).group()
			else:
				rating_pop ='< 10'
			#print(rating_pop)

			#min price by Douban (multiple sources)
			if tags.find('span',class_='buy-info')!= None:
				re_current_price = re.search(r"\d{1,4}.\d{0,2}",tags.find('span',class_='buy-info').get_text())
				current_price = re_current_price.group()
			else:
				current_price = 'N/A'
			
			#print(current_price)

			info_list.append(title)
			info_list.append(author_w_nationality)
			info_list.append(translator)
			info_list.append(date_of_1st_publishing)
			info_list.append(face_value)
			info_list.append(current_price)
			info_list.append(rating)
			info_list.append(rating_pop)
			result.append(info_list)

	return result

def save(data):
	file_csv = open('yl_mingjiawenxue.csv','w+',newline='')
	writer = csv.writer(file_csv)
	headers = ['title','author_w_nationality','translator','date_of_1st_publishing','face_value','current_price','rating','rating_pop']

	for book in data:
		try:
			writer.writerow(book)
		except:
			continue
	file_csv.close()







        
if __name__ == '__main__':
	url='https://book.douban.com/series/681?page='
	login_douban()
	save(get_book_series_info(url,2))




