from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import pandas as pd
import itertools 

url = "https://www.beeradvocate.com/beer/styles/"

# Deal with empty cells
def replaceBlank(x):
  if x == '':
    return 0
  else:
    return x

# create a new Chrome session
driver = webdriver.Chrome('/Users/evangrandfield/Desktop/BeerMe/chromedriver') 
driver.implicitly_wait(30)
driver.get(url)


# get every beer style and every beer style's link to its specific starting page
html_list = driver.find_element_by_id("ba-content")
items = html_list.find_elements_by_tag_name("li")
base_links = html_list.find_elements_by_tag_name("a")
urls = [base_link.get_attribute("href")for base_link in base_links]
styles = [item.text for item in items]

# for each style and respective link go to each starting page by clicking the link
for i in range(0, len(urls) - 1):
	driver.get(urls[i])
	style_type = str(styles[i])
	base_url = str(driver.current_url)
	Name = []
	Brewery =  []
	ABV = []
	Ratings = []
	Score = []
	Style = []
	d = {'Name': Name, 'Brewery': Brewery, 'ABV': ABV, 'Ratings': Ratings, 'Score': Score, 'Style': Style}
	# once on the starting page, go to each next page, until there is not a next page (blank table), and then exit inner loop
	for j in range(0, 40000, 50):
		next_url = base_url[0:len(base_url)-1] + '?sort=revsD&start={0}'.format(j)
		driver.get(next_url)
		html = driver.page_source
		page_soup = soup(html, 'lxml')
		table = page_soup.find('table')
		rows = table.find_all('tr')
		iterrows = iter(rows)
		print(rows)
		next(iterrows)
		next(iterrows)
		next(iterrows)
		if len(rows) > 4:
			for row in iterrows:
				print(row)
				print('-'*20)
				columns = row.find_all('td')
				if len(columns) >= 4:
					Name.append(replaceBlank(columns[0].text))
					Brewery.append(replaceBlank(columns[1].text))
					ABV.append(replaceBlank(columns[2].text))
					Ratings.append(replaceBlank(columns[3].text))
					Score.append(replaceBlank(columns[4].text))
					Style.append(style_type)
		else:
			ratings = pd.DataFrame(d)
			path = '/Users/evangrandfield/Desktop/BeerMe/beers{0}.csv'.format(i)
			ratings.to_csv(path)
			break

