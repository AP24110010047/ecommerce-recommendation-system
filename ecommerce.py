import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

data = {
    'Product': [
        'Laptop', 'Mobile', 'Shoes', 'Watch', 'Headphones',
        'Tablet', 'Camera', 'Backpack', 'SmartTV', 'Keyboard'
    ],
    'User1': [5, 3, 0, 1, 4, 2, 0, 3, 5, 4],
    'User2': [4, 0, 0, 1, 5, 3, 4, 0, 4, 5],
    'User3': [1, 1, 0, 5, 4, 4, 5, 2, 0, 3],
    'User4': [0, 0, 5, 4, 0, 1, 0, 5, 4, 0],
    'User5': [5, 4, 0, 2, 5, 3, 4, 1, 5, 4]
}

product_details = {
    'Laptop': {'price': 60000, 'category': 'Electronics'},
    'Mobile': {'price': 20000, 'category': 'Electronics'},
    'Shoes': {'price': 3000, 'category': 'Fashion'},
    'Watch': {'price': 5000, 'category': 'Accessories'},
    'Headphones': {'price': 2500, 'category': 'Electronics'},
    'Tablet': {'price': 30000, 'category': 'Electronics'},
    'Camera': {'price': 45000, 'category': 'Electronics'},
    'Backpack': {'price': 1500, 'category': 'Fashion'},
    'SmartTV': {'price': 70000, 'category': 'Electronics'},
    'Keyboard': {'price': 2000, 'category': 'Accessories'}
}

df = pd.DataFrame(data)
df.set_index('Product', inplace=True)

print("USER-PRODUCT RATING MATRIX:\n")
print(df)

similarity = cosine_similarity(df)
similarity_df = pd.DataFrame(similarity, index=df.index, columns=df.index)

print("\nPRODUCT SIMILARITY MATRIX:\n")
print(similarity_df)

def recommend_products(product_name, top_n=3):
    scores = similarity_df[product_name].sort_values(ascending=False)
    scores = scores.drop(product_name)
    return scores.head(top_n)

print("\nRECOMMENDATIONS:\n")

for product in df.index:
    print("\nProduct:", product)

    recs = recommend_products(product)

    for item, score in recs.items():
        print(" ", item, "| Score:", round(score, 2),
              "| Price:", product_details[item]['price'])

df['Average Rating'] = df.mean(axis=1)

print("\nAVERAGE RATINGS:\n")
for product, rating in df['Average Rating'].items():
    print(product, ":", round(rating, 2))

print("\nTOP 5 TRENDING PRODUCTS:\n")

top_products = df['Average Rating'].sort_values(ascending=False).head(5)

for product, rating in top_products.items():
    print(product, "| Rating:", round(rating, 2))

print("\nMOST SIMILAR PRODUCT PAIR:\n")

max_score = 0
pair = ("", "")

for i in similarity_df.index:
    for j in similarity_df.columns:
        if i != j and similarity_df.loc[i, j] > max_score:
            max_score = similarity_df.loc[i, j]
            pair = (i, j)

print(pair[0], "<->", pair[1], "| Score:", round(max_score, 2))

print("\nCATEGORY-WISE PRODUCTS:\n")

category_products = {}

# Group products by category
for product, details in product_details.items():
    cat = details['category']
    category_products.setdefault(cat, []).append(product)

# Display
for cat, items in category_products.items():
    print(cat, ":", ", ".join(items))

print("\nCATEGORY-WISE AVERAGE PRICE:\n")

category_prices = {}

for product, details in product_details.items():
    cat = details['category']
    category_prices.setdefault(cat, []).append(details['price'])

for cat, prices in category_prices.items():
    avg_price = sum(prices) / len(prices)
    print(cat, "| Avg Price:", round(avg_price, 2))

print("\nHIGH RATED PRODUCTS (Avg > 4):\n")

for product, rating in df['Average Rating'].items():
    if rating > 4:
        print(product, "| Rating:", round(rating, 2))

print("\nSystem executed successfully!")

