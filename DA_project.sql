-- 1)
SELECT rating, price FROM amazon.item_info;
-- Purpose: return rating and price of all items and study their distribution as an initial exploration

-- 2)
SELECT * FROM
(SELECT item_ID, rating, price, number_of_reviews FROM amazon.item_info) LHS
INNER JOIN
(SELECT item_ID, search_rank FROM amazon.item_rank) RHS
USING(item_ID);
-- Purpose: match each item’s search rank with its info by ID to study the relation between rank and info

-- 3)
SELECT item_name FROM amazon.item_info;
-- Purpose: return each item’s name to perform text analysis

-- 4)
SELECT * FROM
(SELECT item_ID, item_name, rating, price, number_of_reviews FROM amazon.item_info) LHS
INNER JOIN
(SELECT item_ID, search_rank FROM amazon.item_rank) RHS
USING(item_ID)
WHERE item_name ILIKE '%desk%';
-- Purpose: study the relation between rank and info of items containing ‘desk’

-- 5)
SELECT search_rank FROM
(SELECT item_ID, rating, price, number_of_reviews FROM amazon.item_info) LHS
INNER JOIN
(SELECT item_ID, search_rank FROM amazon.item_rank) RHS
USING(item_ID)
WHERE rating IS NULL;
-- Purpose: study the rank of items without ratings

-- 6)
SELECT item_name FROM
(SELECT associated_ID FROM amazon.item_association_map) LHS
INNER JOIN
(SELECT item_ID, item_name FROM amazon.item_info) RHS
ON LHS.associated_ID=RHS.item_ID;
-- Purpose: return associated items’ names to perform text analysis

-- 7)
ALTER TABLE amazon.item_info ADD COLUMN assoc_avg_rating FLOAT;

UPDATE amazon.item_info t SET assoc_avg_rating= inner_q.avg_rating FROM
(SELECT LHS.item_ID, avg(rating) AS avg_rating FROM
(SELECT item_ID, associated_ID FROM amazon.item_association_map) LHS
INNER JOIN
(SELECT item_ID, rating FROM amazon.item_info) RHS
ON LHS.associated_ID=RHS.item_ID
GROUP BY LHS.item_ID) AS inner_q
WHERE t.item_ID=inner_q.LHS.item_ID;
-- Purpose: calculate average ratings of associated items of each item. Add one column to item_info table and place the average ratings in it.

-- Similar action were taken to average prices of associated items as well.
ALTER TABLE amazon.item_info ADD COLUMN assoc_avg_price FLOAT;

UPDATE amazon.item_info t SET assoc_avg_price= inner_q.avg_price FROM
(SELECT LHS.item_ID, avg(price) AS avg_price FROM
(SELECT item_ID, associated_ID FROM amazon.item_association_map) LHS
INNER JOIN
(SELECT item_ID, price FROM amazon.item_info) RHS
ON LHS.associated_ID=RHS.item_ID
GROUP BY LHS.item_ID) AS inner_q
WHERE t.item_ID=inner_q.LHS.item_ID;

-- 8)
SELECT item_ID, rating, price, assoc_avg_rating, assoc_avg_price
FROM amazon.item_info;
-- Purpose: with average ratings and prices of associated items of each item added, return them with original price and rating of each item and study the relation between the associated average and the original.

-- 9)
SELECT review_text FROM amazon.review_positivity
WHERE positive_or_negative='neg';
-- Purpose: return all positive reviews and perform text analysis

-- 10)
SELECT review_text FROM amazon.review_positivity
WHERE positive_or_negative='pos';
-- Purpose: return all negative reviews and perform text analysis

