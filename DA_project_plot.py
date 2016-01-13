import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import step, legend, xlim, ylim, show
import collections
import wordcloud
from wordcloud import WordCloud, STOPWORDS
from scipy import stats
from collections import Counter
import re
import string


con = psycopg2.connect(dbname='postgres', user='congqing', host = 'localhost')
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
dbname = "amazon"
cur = con.cursor()

# define a function to convert raw text to wordlist
def words(d):
    # first replace punctuations with space
    replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    d = d.translate(replace_punctuation)
    # replace numbers
    d = re.sub('[0-9]', ' ', d)
    # replace tab, carriage return, newline
    d = re.sub('\t|\r|\n', ' ', d)
    word = d.split()
    # remove words with length < 3
    wordlist = [i.lower() for i in word if len(i)>=3]
    # remove all the stopwords
    wordlist = [i for i in wordlist if i not in stopWords]
    return wordlist

def words_count_list(docs): # get term frequency for each document and documents term count
    df = Counter()
    alltext = []
    for d in docs:
        words1 = words(d) # name the variable words1 to avoid conflicting with the function name
        tf = Counter(words1)
        alltext = alltext + words1
        for t in tf:
            df[t] += 1
    return (alltext, df)

# plot rating against ranking
cur.execute("SELECT * FROM (SELECT item_ID, item_name, rating, price, number_of_reviews FROM amazon.item_info) LHS\
INNER JOIN (SELECT item_ID, search_rank FROM amazon.item_rank) RHS USING(item_ID) WHERE item_name ILIKE '%desk%';")
test = cur.fetchall()

# 204/305 items include 'desk' in their names

ranking = []
rating = []
price1 = []
num_reviews1 = []

for i in range(len(test)):
    if test[i][1] != None:
        ranking.append(test[i][0])
        rating.append(test[i][1])
        price1.append(test[i][2])
        num_reviews1.append(test[i][3])

plt.scatter(ranking,rating)
xlim(-10,350)
plt.xlabel('Rank')
plt.ylabel('Rating')
plt.title('Rating vs Rank')
plt.savefig('Rating vs Rank.png')

plt.scatter(ranking,price1)
xlim(-10,350)
plt.xlabel('Rank')
plt.ylabel('Price')
plt.title('Price vs Rank')
plt.savefig('Price vs Rank.png')

plt.scatter(ranking,num_reviews1)
xlim(-10,350)
plt.xlabel('Rank')
plt.ylabel('Number of reviews')
plt.title('Number of reviews vs Rank')
plt.savefig('Number of reviews vs Rank.png')


plt.scatter(price1,ranking)
ylim(-10,350)

# ranking against reviews
plt.scatter(ranking, np.array(num_reviews1)/np.array(num_reviews1).mean()*np.array(rating)/np.array(rating).mean())
xlim(-10,350)
plt.xlabel('Rank')
plt.ylabel('Rating/ mean(Rating)* Num_reviews/ mean(Num_reviews)')
plt.title('Rating * Number of reviews vs Rank')
plt.savefig('Rating * Number of reviews vs Rank.png')

# np.log(np.array(price1))

# ranking without rating histogram
cur.execute('SELECT search_rank FROM\
(SELECT item_ID, rating, price, number_of_reviews FROM amazon.item_info) LHS\
INNER JOIN\
(SELECT item_ID, search_rank FROM amazon.item_rank) RHS\
USING(item_ID)\
WHERE rating IS NULL;')
test4 = cur.fetchall()
null_ranking = []
for i in range(len(test4)):
    null_ranking.append(test4[i][0])
plt.hist(null_ranking)
plt.xlabel('Rank')
plt.ylabel('Count')
plt.title('Histogram of search rank of items without rating')
plt.savefig('Histogram of search rank of items without rating.png')

# for each rating, average ranking
cur.execute('SELECT item_ID, rating, price, assoc_avg_rating, assoc_avg_price FROM amazon.item_info;')
test2 = cur.fetchall()
avg_rating = []
avg_ranking = []
for i in range(len(test2)):
    avg_rating.append(test2[i][0])
    avg_ranking.append(test2[i][1])

plt.scatter(avg_rating, avg_ranking)

price = []
num_reviews = []
ranking1 = []
for i in range(len(test)):
    ranking1.append(test[i][0])
    price.append(test[i][2])
    num_reviews.append(test[i][3])
plt.scatter(price,ranking1)
ylim(-10,350)
xlim(-10,500)
plt.scatter(ranking1,num_reviews)
xlim(-10,350)
ylim(-10,2000)

ratings_dict = collections.Counter(rating)
fig = plt.figure()
# Get the Axes object within figure
ax = fig.add_subplot(111)
# Plot ratings on X axis and counts on Y axis
ax.bar(ratings_dict.keys(), ratings_dict.values(), align = 'center', color = 'c', width = 0.1)
plt.title("Rating Histogram", fontsize = 16, fontweight = 'bold')
plt.xlabel('Rating', fontsize = 14)
plt.ylabel('Count', fontsize = 14)


# b Order posts by reverse chronological order
cur.execute('SELECT * FROM amazon.original_items AS a INNER JOIN amazon.original_related AS b \
  ON a.item = b.original LEFT JOIN amazon.related_items AS c ON b.related = c.item;')
test1 = cur.fetchall()

origin_rating = []
origin_price = []
origin_num_reviews = []
related_rating = []
related_price = []
related_num_reviews = []
for i in range(len(test1)):
    origin_rating.append(test1[i][2])
    origin_price.append(test1[i][3])
    origin_num_reviews.append(test1[i][4])
    related_rating.append(test1[i][9])
    related_price.append(test1[i][10])
    related_num_reviews.append(test1[i][11])

plt.scatter(origin_rating, related_rating)
plt.scatter(origin_price, related_price)
plt.scatter(origin_num_reviews, related_num_reviews)

# average rating
or_rating = []
re_rating = []
cur.execute('SELECT LHS.item_ID, avg(price) AS avg_price FROM\
(SELECT item_ID, associated_ID FROM amazon.item_association_map) LHS\
INNER JOIN\
(SELECT item_ID, price FROM amazon.item_info) RHS\
ON LHS.associated_ID=RHS.item_ID\
GROUP BY LHS.item_ID) AS inner_q\
WHERE t.item_ID=inner_q.LHS.item_ID;')
test3 = cur.fetchall()
for i in range(len(test3)):
    or_rating.append(test3[i][0])
    re_rating.append(test3[i][1])

x = np.arange(3.43,4.7,0.05)
y = x*0.04295352565318112 + 3.7727249734392574

plt.scatter(or_rating, re_rating)
plt.plot(x, y, color = 'r')
plt.xlabel('Original items rating')
plt.ylabel('Related items average rating')
plt.title('Related vs Original Rating')
plt.savefig('Related vs Original Rating.png')

stats.linregress(or_rating, re_rating)

# average price
or_price = []
re_price = []
cur.execute('SELECT LHS.item_ID, avg(price) AS avg_price FROM\
(SELECT item_ID, associated_ID FROM amazon.item_association_map) LHS\
INNER JOIN\
(SELECT item_ID, price FROM amazon.item_info) RHS\
ON LHS.associated_ID=RHS.item_ID\
GROUP BY LHS.item_ID) AS inner_q\
WHERE t.item_ID=inner_q.LHS.item_ID;')
test7 = cur.fetchall()
for i in range(len(test7)):
    or_price.append(test7[i][0])
    re_price.append(test7[i][1])
plt.scatter(or_price, re_price)
plt.plot(x, y, color = 'r')
plt.xlabel('Original items price')
plt.ylabel('Related items average price')
plt.title('Related vs Original Price')
plt.savefig('Related vs Original Price.png')
x = np.arange(10,280)
y = x*0.33806979306815194 + 32.906640823615376

stats.linregress(or_price, re_price)

cur.close()
con.close()
##

# words frequency
# get all item names
cur.execute('SELECT item_name FROM amazon.item_info;')
test4 = cur.fetchall()
item_names = []
for i in range(len(test4)):
    item_names.append(test4[i][0])

(a, df) = words_count_list(item_names)
plot_items = df.most_common(10)
x = [i[0] for i in plot_items]
x1 = range(len(x))
y = [i[1] for i in plot_items]
y[0] = y[0] + 13
fig = plt.figure()
# Get the Axes object within figure
ax = fig.add_subplot(111)
# Plot ratings on X axis and counts on Y axis
# ax.bar(df.keys(), df.values(), align = 'center', color = 'c', width = 0.1)

ax.bar(x1, y, align='center')
ax.set_xticks(x1)
ax.set_xticklabels(x)

plt.title("Frequent words of original items", fontsize = 16, fontweight = 'bold')
plt.xlabel('Words', fontsize = 14)
plt.ylabel('Count', fontsize = 14)
plt.savefig('Frequent words of original items.png')

# update the table
cur.execute('UPDATE amazon.item_info t SET assoc_avg_price= inner_q.avg_price FROM\
(SELECT LHS.item_ID, avg(price) AS avg_price FROM\
(SELECT item_ID, associated_ID FROM amazon.item_association_map) LHS\
INNER JOIN\
(SELECT item_ID, price FROM amazon.item_info) RHS\
ON LHS.associated_ID=RHS.item_ID\
GROUP BY LHS.item_ID) AS inner_q\
WHERE t.item_ID=inner_q.LHS.item_ID;')


str_item_names = item_names[0]
for i in range(1,len(item_names)):
    str_item_names = str_item_names + ' ' + item_names[i]
wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color='white',
                          width=1200,
                          height=1000
                         ).generate(str_item_names)


plt.imshow(wordcloud)
plt.axis('off')
plt.title('Frequent words of original items')
plt.show()
plt.savefig('Frequent words of original items.png')


cur.execute("SELECT review_text FROM amazon.review_positivity WHERE positive_or_negative='pos';")
pos_reviews = cur.fetchall()
pos_reviews = [i[0] for i in pos_reviews]
# bar chart
(a, df4) = words_count_list(pos_reviews)
plot_not_items = df4.most_common(10)
x = [i[0] for i in plot_not_items]
x1 = range(len(x))
y = [i[1] for i in plot_not_items]
fig = plt.figure()
# Get the Axes object within figure
ax = fig.add_subplot(111)
# Plot ratings on X axis and counts on Y axis
# ax.bar(df.keys(), df.values(), align = 'center', color = 'c', width = 0.1)

ax.bar(x1, y, align='center')
ax.set_xticks(x1)
ax.set_xticklabels(x)

plt.title("Frequent words in positive reviews", fontsize = 16, fontweight = 'bold')
plt.xlabel('Words', fontsize = 14)
plt.ylabel('Count', fontsize = 14)
plt.savefig('Frequent words in positive reviews.png')

# word cloud
str_pos_reviews = pos_reviews[0]
for i in range(1,len(pos_reviews)):
    str_pos_reviews = str_pos_reviews + ' ' + pos_reviews[i]
wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color='white',
                          width=1200,
                          height=1000
                         ).generate(str_pos_reviews)


plt.imshow(wordcloud)
plt.axis('off')
plt.title('Frequent words in positive reviews')
plt.show()
plt.savefig('Frequent words in positive reviews wc.png')

# negative reviews
cur.execute("SELECT review_text FROM amazon.review_positivity WHERE positive_or_negative='neg';")
neg_reviews = cur.fetchall()
neg_reviews = [i[0] for i in neg_reviews]
# bar chart
(a, df4) = words_count_list(neg_reviews)
plot_not_items = df4.most_common(10)
x = [i[0] for i in plot_not_items]
x1 = range(len(x))
y = [i[1] for i in plot_not_items]
fig = plt.figure()
# Get the Axes object within figure
ax = fig.add_subplot(111)
# Plot ratings on X axis and counts on Y axis
# ax.bar(df.keys(), df.values(), align = 'center', color = 'c', width = 0.1)

ax.bar(x1, y, align='center')
ax.set_xticks(x1)
ax.set_xticklabels(x)

plt.title("Frequent words in negative reviews", fontsize = 16, fontweight = 'bold')
plt.xlabel('Words', fontsize = 14)
plt.ylabel('Count', fontsize = 14)
plt.savefig('Frequent words in negative reviews.png')

# word cloud
def unlist_string(l):
    result = l[0]
    for i in range(1,len(l)):
        result = result + ' ' + l[i]
    return result

str_neg_reviews = neg_reviews[0]
for i in range(1,len(neg_reviews)):
    str_neg_reviews = str_neg_reviews + ' ' + neg_reviews[i]
wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color='white',
                          width=1200,
                          height=1000
                         ).generate(str_neg_reviews)

plt.imshow(wordcloud)
plt.axis('off')
plt.title('Frequent words in negative reviews')
plt.show()
plt.savefig('Frequent words in negative reviews wc.png')

# plot histograms of price,
cur.execute('SELECT item, rating, price, num_reviews FROM amazon.item_info;')
items = cur.fetchall()

ratings = []
prices = []
num_reviews = []

for item in items:
    if item[1] is not None:
        ratings.append(item[1])
        prices.append(item[2])
        num_reviews.append(item[3])

plt.hist(ratings)
plt.title("Rating Histogram", fontsize = 16, fontweight = 'bold')
plt.xlabel('Rating', fontsize = 14)
plt.ylabel('Count', fontsize = 14)
plt.savefig('Rating Histogram.png')
