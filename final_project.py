##### Name: Skye Tian
##### Uniqname: ziqint
##### SI507 Final Project


# import packages
import json
import secrets
import requests
from bs4 import BeautifulSoup
import webbrowser
import matplotlib.pyplot as plt
import yaml
import pandas

baseurl_yelp = 'https://api.yelp.com/v3/businesses/search'
wiki_url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
wiki_baseurl = "https://en.wikipedia.org/wiki/"
KEY = secrets.API_KEY

# to get data from api
def getData():
    global where
    global data
    # global result_aggregate

    header = {'authorization': "Bearer " + KEY}
    print("========================================================================================")
    print("=============================== Restaurants ============================================")
    print("========================================================================================")
    where = str(input('Which city do you wanna know more about restaurants? (example: New_York)\n'))
    baseurl = "https://api.yelp.com/v3/businesses/search?location=" + where
    response = requests.get(baseurl, headers=header)
    data = response.json()

    with open ('yelp_' + where + '.json','w') as fp:
        json.dump(data,fp)
    return data

# to build data into a tree
def buildTree(data):
    restaurant_tree = []
    dic = {}
    for restaurant in data["businesses"]:
        dic = {"name":restaurant["name"], "attributes":{}}
        dic["attributes"]["url"] = restaurant["url"]
        dic["attributes"]["transactions"] = restaurant["transactions"]
        if 'price' in restaurant.keys():
            dic["attributes"]["price"] = restaurant["price"]
        else:
            dic["attributes"]["price"] = None
        if "rating" in restaurant.keys():
            dic["attributes"]["rating"] = restaurant["rating"]
        else:
            dic["attributes"]["rating"] = None
        restaurant_tree.append(dic)
    return restaurant_tree

# to get the names of restaurants
def getName():
    name = []
    restaurants = data["businesses"]
    for r in restaurants:
        name.append(r['name'])
    return name

def priceTree(restaurant_tree):
    price_tree = {'$': [], '$$': [], '$$$': [], '$$$$': []}
    for restaurant in restaurant_tree:
        price = restaurant["attributes"]["price"]
        name = restaurant['name']
        if price == '$':
            price_tree["$"].append(name)
        elif price == '$$':
            price_tree["$$"].append(name)
        elif price == '$$$':
            price_tree["$$$"].append(name)
        elif price == '$$$$':
            price_tree["$$$$"].append(name)
    return price_tree

def getCategories_city():
    global data
    cat_uniq = []
    for restaurant in data["businesses"]:
        for category in restaurant["categories"]:
            alias = category["alias"]
            if alias not in cat_uniq:
                cat_uniq.append(alias)
    return cat_uniq


def getCategories():
    global data
    global category_list

    category_list= []
    restaurants = data["businesses"]

    for restaurant in restaurants:
        name = restaurant["name"]
        cat_dic = {"name": name, "categories":[]}
        categories = restaurant["categories"]

        for category in categories:
            alias = category["alias"]
            cat_dic["categories"].append(alias)

        category_list.append(cat_dic)

    return category_list

def countCategory():
    unique_list = []
    count_dic = {}

    for restaurant in getCategories():
        category = restaurant["categories"]
        for category in category:
            if category in unique_list:
                count_dic[category] += 1
            else:
                unique_list.append(category)
                count_dic[category] = 1
    return count_dic

def drawRating(result):
    unique_list = []
    rate_dic = {}

    for tree in buildTree(result):
        rating = tree['attributes']['rating']
        if rating in unique_list:
            rate_dic[tree['attributes']['rating']] += 1
        else:
            unique_list.append(tree['attributes']['rating'])
            rate_dic[tree['attributes']['rating']] = 1
    return rate_dic

def cityInfo():
    city_dic = []
    response = requests.get('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population')
    content = BeautifulSoup(response.text, 'html.parser')
    table = content.find('table', class_='wikitable sortable')
    list = table.find('tbody').find_all('tr')[1:]
    for item in list:
        td = item.find_all('td')
        th = item.find_all('th')
         # to get the rank of the city
        number = th[0].text.strip()
        rank = int(number)
        # to get the name of the city
        get_city = td[0].find('a').text.strip()
        city = str(get_city)
        # to get the name of the state
        try:
            state = str(td[1].find('a').text.strip())
        except:
            state = td[1].text.strip()
        # to get the population of the city as an integer
        get_population = td[2].text.strip()
        population = int(get_population.replace(',', ''))
        # to get the land area of the city as a float (km)
        get_land = td[6].text.strip().split('\xa0')[0]
        land_area = float(get_land.replace(',', ''))
        # the dictionary of a single city
        city = {"rank": rank,
                "city":city,
                "state":state,
                "population": population,
                "land_area(km)":land_area}

        city_dic.append(city)
    return city_dic

def openPage():
    while True:
        yes = ['yes', 'ya', 'yeah', 'yas', 'y', 'yy', 'sure', 'ye']
        no = ['no', "n", "nah", "not"]
        print("==================================================================================================================")

        city = input("Which city do you want to know more? (example: New York) ")
        answer = input("Do you want to open the unsplash page of the city? (yes/no, answer no to move to next step) ")
        if answer.lower() in yes:
            city_url = "https://unsplash.com/s/photos/" + city
            webbrowser.open(city_url, new = 0)
        elif answer.lower() in no:
            buildTree(getData())
            break
        else:
            print("Try another city plzzz. \n")
            break

def openRestaurant(web,result):
    restaurants = buildTree(result)
    for restaurant in restaurants:
        if restaurant['name'] == web:
            webbrowser.open(restaurant["attributes"]["url"], new = 0)


## Main ##
if __name__=='__main__':
    print("==================================================================================================================")
    print("==================================================================================================================")
    print("================================== Welcome to the yelp explorer! =================================================")
    print("==================================================================================================================")
    print()
    print("=============================== Top 15 cities which have most population =========================================")
    print("==================================================================================================================")
    df = pandas.DataFrame(data = cityInfo())
    print(df.head(15))
    # ask to open unsplash to see more photos
    openPage()
    yelp = open('yelp_' + where + '.json')
    info = json.load(yelp)

    # get the restaurant name of the city
    print("==================================================================================================================")
    print("======================================= Restaurants in the city ==================================================")
    print("==================================================================================================================")

    print(yaml.dump(buildTree(data), default_flow_style=False))
    print(getName())

    # the pie chart of restaurant categories in the city
    city_categories = countCategory()
    my_labels = list(city_categories.keys())
    sizes = list(city_categories.values())
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=my_labels, autopct='%1.2f%%')
    plt.show()


    # the bar plot of numbers of restaurants of each rating
    data = drawRating(data)
    rating = list(data.keys())
    count = list(data.values())
    fig = plt.figure(figsize = (10, 5))
    plt.bar(rating, count, color ='#82A284')
    plt.title("Numbers of restaurants for each score of rating")
    plt.xlabel("Rating(s)")
    plt.ylabel("Numbers of restaurants")
    plt.show()

    print("================================================================================================================")
    print("==================================== Thank you for using =======================================================")
    print("==================================== See you next time! ========================================================")
    print("================================================================================================================")

