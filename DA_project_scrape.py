import urllib2
from BeautifulSoup import BeautifulSoup
from selenium import webdriver
import re
import csv
import time
import random

search_prefix = 'http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords='
keyword = 'desk'

search_key = search_prefix + keyword
driver = webdriver.Chrome()
driver.get(search_key)
text = driver.page_source
text = text.encode('utf-8')
soup = BeautifulSoup(text)

# first page
results = soup.find('ul', attrs={'id': 's-results-list-atf'}).findAll('li', attrs={'class': 's-result-item celwidget'})
# remove sponsored items (ads)
results = results[:len(results)-2]
titles = []
ratings = []
prices = []
num_reviews = []
for i in range(len(results)):
    title = results[i].find('a', attrs={'class': 'a-link-normal s-access-detail-page  a-text-normal'})['title']
    titles.append(title)
    rating = results[i].find('div',attrs={'class':'a-column a-span5 a-span-last'}).find('span', attrs={'class': 'a-icon-alt'}).text
    ratings.append(rating)
    price = results[i].find('span',attrs={'class':re.compile('a-size-base a-color-price')}).text
    prices.append(price)
    num_review = results[i].find('div',attrs={'class':'a-column a-span5 a-span-last'}).find('a', attrs={'class': 'a-size-small a-link-normal a-text-normal'}).text
    num_reviews.append(num_review)

# next page and so on
while True:
    try:
        next_page = 'http://www.amazon.com' + soup.find('a',attrs={'title':'Next Page'})['href']
        driver.get(next_page)
        text = driver.page_source
        text = text.encode('utf-8')
        soup = BeautifulSoup(text)

        # add results
        results = soup.find('ul', attrs={'id': 's-results-list-atf'}).findAll('li', attrs={'class': 's-result-item celwidget'})
        # remove sponsored items (ads)
        results = results[:len(results)-2]
        for i in range(len(results)):
            title = results[i].find('a', attrs={'class': 'a-link-normal s-access-detail-page  a-text-normal'})['title']
            titles.append(title)
            if results[i].find('div',attrs={'class':'a-column a-span5 a-span-last'}).find('span', attrs={'class': 'a-icon-alt'}) is None:
                rating = None
            else:
                rating = results[i].find('div',attrs={'class':'a-column a-span5 a-span-last'}).find('span', attrs={'class': 'a-icon-alt'}).text
            ratings.append(rating)
            if results[i].find('span',attrs={'class':re.compile('a-size-base a-color-price')}) is None:
                price = None
            else:
                price = results[i].find('span',attrs={'class':re.compile('a-size-base a-color-price')}).text
            prices.append(price)
            if results[i].find('div',attrs={'class':'a-column a-span5 a-span-last'}).find('a', attrs={'class': 'a-size-small a-link-normal a-text-normal'}) is None:
                num_review = None
            else:
                num_review = results[i].find('div',attrs={'class':'a-column a-span5 a-span-last'}).find('a', attrs={'class': 'a-size-small a-link-normal a-text-normal'}).text
            num_reviews.append(num_review)

    except TypeError:
        # no more next pages found
        break

# store first table in csv
titles = [s.encode('utf-8') if s is not None else None for s in titles]
ratings = [s.encode('utf-8') if s is not None else None for s in ratings]
prices = [s.encode('utf-8') if s is not None else None for s in prices]
num_reviews = [s.encode('utf-8') if s is not None else None for s in num_reviews]

search_result = zip(titles,ratings,prices,num_reviews)
with open('search_ranking_all.csv','wb') as file:
    writer = csv.writer(file, delimiter=',' )
    writer.writerow(('item','average rating','price','number of review'))
    for row in search_result:
        writer.writerow(row)

# for specific items, find their reviews
table2_reviews = []
table2_ratings = []
table2_titles = []
table2_items = []
for i in range(len(results)):
    url = results[i].find('a', attrs = {'class': 'a-link-normal s-access-detail-page  a-text-normal'})['href']
    #page = urllib2.urlopen(url).read()
    #driver = webdriver.Chrome()
    driver.get(url)
    page = driver.page_source
    page = page.encode('utf-8')
    soup = BeautifulSoup(page)
    reviews = soup.find('div',attrs={'id':'revMHRL'}).findAll('div',attrs={'class':'a-section'})
    reviews = [review.text for review in reviews]
    ratings = soup.find('div',attrs={'id':'revMHRL'}).findAll('i', attrs={'class':re.compile('a-icon a-icon-star')})
    ratings = [rating['class'][-1] for rating in ratings]
    review_titles = soup.find('div',attrs={'id':'revMHRL'}).findAll('span', attrs={'class':'a-size-base a-text-bold'})
    review_titles = [review_title.text for review_title in review_titles]
    item = soup.find('span',attrs={'id':'productTitle'}).text
    items = [item]*len(reviews)
    # add to global variables
    table2_items.extend(items)
    table2_titles.extend(review_titles)
    table2_ratings.extend(ratings)
    table2_reviews.extend(reviews)
    wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
    time.sleep(wait_time)

# next page and so on
for j in range(4):
    try:
        next_page = 'http://www.amazon.com' + soup1.find('a',attrs={'title':'Next Page'})['href']
        driver.get(next_page)
        text = driver.page_source
        text = text.encode('utf-8')
        soup1 = BeautifulSoup(text)

        # add results
        results = soup1.find('ul', attrs={'id': 's-results-list-atf'}).findAll('li', attrs={'class': 's-result-item celwidget'})
        # remove sponsored items (ads)
        results = results[:len(results)-2]
        for i in range(3,len(results)):
            url = results[i].find('a', attrs = {'class': 'a-link-normal s-access-detail-page  a-text-normal'})['href']
            #page = urllib2.urlopen(url).read()
            #driver = webdriver.Chrome()
            driver.get(url)
            page = driver.page_source
            page = page.encode('utf-8')
            soup = BeautifulSoup(page)
            reviews = soup.find('div',attrs={'id':'revMHRL'}).findAll('div',attrs={'class':'a-section'})
            reviews = [review.text for review in reviews]
            ratings = soup.find('div',attrs={'id':'revMHRL'}).findAll('i', attrs={'class':re.compile('a-icon a-icon-star')})
            ratings = [rating['class'][-1] for rating in ratings]
            review_titles = soup.find('div',attrs={'id':'revMHRL'}).findAll('span', attrs={'class':'a-size-base a-text-bold'})
            review_titles = [review_title.text for review_title in review_titles]
            item = soup.find('span',attrs={'id':'productTitle'}).text
            items = [item]*len(reviews)
            # add to global variables
            table2_items.extend(items)
            table2_titles.extend(review_titles)
            table2_ratings.extend(ratings)
            table2_reviews.extend(reviews)
            wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
            time.sleep(wait_time)

    except TypeError:
        # no more next pages found
        break


table2_items = [s.encode('utf-8') for s in table2_items]
table2_titles = [s.encode('utf-8') for s in table2_titles]
table2_ratings = [s.encode('utf-8') for s in table2_ratings]
table2_reviews = [s.encode('utf-8') for s in table2_reviews]

table2_items_add = table2_items[564:656]
table2_titles_add = table2_titles[564:656]
table2_ratings_add = table2_ratings[564:656]
table2_reviews_add = table2_reviews[564:656]

table2_items_add = [s.encode('utf-8') for s in table2_items_add]
table2_titles_add = [s.encode('utf-8') for s in table2_titles_add]
table2_ratings_add = [s.encode('utf-8') for s in table2_ratings_add]
table2_reviews_add = [s.encode('utf-8') for s in table2_reviews_add]


# write reviews to csv
reviews_sixpage_add = zip(table2_items_add, table2_titles_add, table2_ratings_add, table2_reviews_add)
with open('reviews_sixpage_add.csv','wb') as file:
    writer = csv.writer(file, delimiter=',' )
    writer.writerow(('item','title','rating','review'))
    for row in reviews_sixpage_add:
        writer.writerow(row)

# for specific items, find also bought items
table3_items = []
table3_also_bought = []
for i in range(len(results)):
    url = results[i].find('a', attrs = {'class': 'a-link-normal s-access-detail-page  a-text-normal'})['href']
    #page = urllib2.urlopen(url).read()
    driver.get(url)
    page = driver.page_source
    page = page.encode('utf-8')
    soup = BeautifulSoup(page)
    also_bought = soup.find('div',attrs={'class':'a-carousel-viewport'}).findAll('a',attrs={'class':'a-size-small a-link-normal'})
    also_bought = [s.findPrevious('a',attrs={'class':'a-link-normal'}).findPrevious('a',attrs={'class':'a-link-normal'}) for s in also_bought]
    also_bought = ['http://www.amazon.com'+s['href'] for s in also_bought]
    item = soup.find('span',attrs={'id':'productTitle'}).text
    items = [item]*len(also_bought)
    table3_items.extend(items)
    table3_also_bought.extend(also_bought)
    wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
    time.sleep(wait_time)

table3_items = [s.encode('utf-8') for s in table3_items]
table3_also_bought = [s.encode('utf-8') for s in table3_also_bought]

# write reviews to csv
also_bought_link = zip(table3_items, table3_also_bought)
with open('also_bought_link.csv','wb') as file:
    writer = csv.writer(file, delimiter=',' )
    writer.writerow(('item','also_bought_link'))
    for row in also_bought_link:
        writer.writerow(row)

# for the also bought items, find their basic attributes
table4_items = []
table4_ratings = []
table4_prices = []
table4_num_reviews = []

for url in table3_also_bought:
    driver.get(url)
    page = driver.page_source
    page = page.encode('utf-8')
    soup = BeautifulSoup(page)
    item = soup.find('span',attrs={'id':'productTitle'}).text
    table4_items.append(item)
    rating = soup.find('span',attrs={'id':'acrPopover'})['title']
    table4_ratings.append(rating)
    price = soup.find('span',attrs={'id':'priceblock_ourprice'}).text
    table4_prices.append(price)
    num_reviews = soup.find('span',attrs={'id':'acrCustomerReviewText'}).text
    table4_num_reviews.append(num_reviews)
    wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
    time.sleep(wait_time)

# write related items to csv
table4_items = [s.encode('utf-8') for s in table4_items]
table4_ratings = [s.encode('utf-8') for s in table4_ratings]
table4_prices = [s.encode('utf-8') for s in table4_prices]
table4_num_reviews = [s.encode('utf-8') for s in table4_num_reviews]

related_items = zip(table4_items, table4_ratings, table4_prices, table4_num_reviews)
with open('related_items.csv','wb') as file:
    writer = csv.writer(file, delimiter=',' )
    writer.writerow(('item','rating','price','num_reviews'))
    for row in related_items:
        writer.writerow(row)

# for related items, find their reviews
table5_reviews = []
table5_ratings = []
table5_titles = []
table5_items = []

for url in table3_also_bought:
    driver.get(url)
    page = driver.page_source
    page = page.encode('utf-8')
    soup = BeautifulSoup(page)
    reviews = soup.find('div',attrs={'id':'revMHRL'}).findAll('div',attrs={'class':'a-section'})
    reviews = [review.text for review in reviews]
    ratings = soup.find('div',attrs={'id':'revMHRL'}).findAll('i', attrs={'class':re.compile('a-icon a-icon-star')})
    ratings = [rating['class'][-1] for rating in ratings]
    review_titles = soup.find('div',attrs={'id':'revMHRL'}).findAll('span', attrs={'class':'a-size-base a-text-bold'})
    review_titles = [review_title.text for review_title in review_titles]
    item = soup.find('span',attrs={'id':'productTitle'}).text
    items = [item]*len(reviews)
    # add to global variables
    table5_items.extend(items)
    table5_titles.extend(review_titles)
    table5_ratings.extend(ratings)
    table5_reviews.extend(reviews)
    wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
    time.sleep(wait_time)

# write reviews of related items to csv
table5_items = [s.encode('utf-8') for s in table5_items]
table5_titles = [s.encode('utf-8') for s in table5_titles]
table5_ratings = [s.encode('utf-8') for s in table5_ratings]
table5_reviews = [s.encode('utf-8') for s in table5_reviews]

related_reviews = zip(table5_items, table5_titles, table5_ratings, table5_reviews)
with open('related_reviews.csv','w') as file:
    writer = csv.writer(file, delimiter = ',')
    writer.writerow(('item','title','rating','review'))
    for row in related_reviews:
        writer.writerow(row)


# for first 16 items, scrape their 10 positive reviews and 10 negative reviews perspectively
search_prefix = 'http://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords='
keyword = 'desk'

search_key = search_prefix + keyword
driver = webdriver.Chrome()
driver.get(search_key)
text = driver.page_source
text = text.encode('utf-8')
soup = BeautifulSoup(text)

# first page
results = soup.find('ul', attrs={'id': 's-results-list-atf'}).findAll('li', attrs={'class': 's-result-item celwidget'})
# remove sponsored items (ads)
results = results[:len(results)-2]

table6_pos_reviews = []
table6_pos_ratings = []
table6_pos_titles = []
table6_pos_items = []

table7_neg_reviews = []
table7_neg_ratings = []
table7_neg_titles = []
table7_neg_items = []

for i in range(len(results)):
    url = results[i].find('a', attrs = {'class': 'a-link-normal s-access-detail-page  a-text-normal'})['href']
    #page = urllib2.urlopen(url).read()
    #driver = webdriver.Chrome()
    driver.get(url)
    page = driver.page_source
    page = page.encode('utf-8')
    soup1 = BeautifulSoup(page)
    # find the reviews page
    url1 = soup1.find('a', attrs={'class':'a-link-emphasis a-text-bold'})['href']
    url1 = re.sub('sortBy=bySubmissionDateDescending','sortBy=helpful',url1)
    driver.get(url1)
    page1 = driver.page_source
    page1 = page1.encode('utf-8')
    soup2 = BeautifulSoup(page1)
    pos_review_section = soup2.findAll('div',attrs={'class':'a-section review'})
    pos_review_section = pos_review_section[:10]
    pos_ratings = [i.find('span',attrs={'class':'a-icon-alt'}).text for i in pos_review_section]
    pos_titles = [i.find('a',attrs={'class':re.compile('a-size-base a-link-normal')}).text for i in pos_review_section]
    pos_reviews = [i.find('span',attrs={'class':'a-size-base review-text'}).text for i in pos_review_section]
    pos_items = [soup1.find('span',attrs={'id':'productTitle'}).text]*len(pos_ratings)
    table6_pos_reviews.extend(pos_reviews)
    table6_pos_ratings.extend(pos_ratings)
    table6_pos_titles.extend(pos_titles)
    table6_pos_items.extend(pos_items)

    # negative page
    url2 = 'http://www.amazon.com' + soup2.find('a', attrs={'data-reftag':'cm_cr_pr_viewpnt_rgt'})['href']
    url2 = re.sub('sortBy=bySubmissionDateDescending','sortBy=helpful',url2)
    driver.get(url2)
    page2 = driver.page_source
    page2 = page2.encode('utf-8')
    soup3 = BeautifulSoup(page2)
    neg_review_section = soup3.findAll('div',attrs={'class':'a-section review'})
    neg_review_section = neg_review_section[:10]
    neg_ratings = [i.find('span',attrs={'class':'a-icon-alt'}).text for i in neg_review_section]
    neg_titles = [i.find('a',attrs={'class':re.compile('a-size-base a-link-normal')}).text for i in neg_review_section]
    neg_reviews = [i.find('span',attrs={'class':'a-size-base review-text'}).text for i in neg_review_section]
    neg_items = [soup1.find('span',attrs={'id':'productTitle'}).text]*len(neg_ratings)
    table7_neg_reviews.extend(neg_reviews)
    table7_neg_ratings.extend(neg_ratings)
    table7_neg_titles.extend(neg_titles)
    table7_neg_items.extend(neg_items)

    wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
    time.sleep(wait_time)

# write reviews of related items to csv
table6_pos_items = [s.encode('utf-8') for s in table6_pos_items]
table6_pos_titles = [s.encode('utf-8') for s in table6_pos_titles]
table6_pos_ratings = [s.encode('utf-8') for s in table6_pos_ratings]
table6_pos_reviews = [s.encode('utf-8') for s in table6_pos_reviews]

all_pos_reviews = zip(table6_pos_items, table6_pos_titles, table6_pos_ratings, table6_pos_reviews)
with open('all_pos_reviews.csv','w') as file:
    writer = csv.writer(file, delimiter = ',')
    writer.writerow(('item','title','rating','review'))
    for row in all_pos_reviews:
        writer.writerow(row)

table7_neg_items = [s.encode('utf-8') for s in table7_neg_items]
table7_neg_titles = [s.encode('utf-8') for s in table7_neg_titles]
table7_neg_ratings = [s.encode('utf-8') for s in table7_neg_ratings]
table7_neg_reviews = [s.encode('utf-8') for s in table7_neg_reviews]

all_neg_reviews = zip(table7_neg_items, table7_neg_titles, table7_neg_ratings, table7_neg_reviews)
with open('all_neg_reviews.csv','w') as file:
    writer = csv.writer(file, delimiter = ',')
    writer.writerow(('item','title','rating','review'))
    for row in all_neg_reviews:
        writer.writerow(row)

# use regular expression to change the format of attribute csv files
item = []
rating = []
price = []
num_reviews = []
with open('related_items.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        item.append(row[0])
        rating.append(row[1])
        price.append(row[2])
        num_reviews.append(row[3])
item.pop(0)
rating.pop(0)
price.pop(0)
num_reviews.pop(0)

rating = [re.match(r'(\d\.?\d?)\s',s).group(1) for s in rating]
price = [re.match(r'\$(.+)',s).group(1) for s in price]
num_reviews = [re.match(r'(\d+,?\d*)\s',s).group(1) for s in num_reviews]

reg_related = zip(item, rating, price, num_reviews)
with open('reg_related.csv','w') as file:
    writer = csv.writer(file, delimiter = ',')
    writer.writerow(('item','rating','price','num_reviews'))
    for row in reg_related:
        writer.writerow(row)

item = []
rating = []
price = []
num_reviews = []
with open('search_ranking_all.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        item.append(row[0])
        rating.append(row[1])
        price.append(row[2])
        num_reviews.append(row[3])
item.pop(0)
rating.pop(0)
price.pop(0)
num_reviews.pop(0)

rating = ['' if s == '' else re.match(r'(\d\.?\d?)\s',s).group(1) for s in rating]
reg_search = zip(item, rating, price, num_reviews)
with open('reg_search.csv','w') as file:
    writer = csv.writer(file, delimiter = ',')
    writer.writerow(('item','rating','price','num_reviews'))
    for row in reg_search:
        writer.writerow(row)
