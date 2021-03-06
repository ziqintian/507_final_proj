## SI 507 Final Project

### Project code

- Here's the link to the GitHub repository to the project checkpoint [SI507 Final Project GitHub](https://github.com/ziqintian/507_final_proj).

- Required Python packages:
  - json
  - secrets
  - requests
  - yaml
  - pandas
  - from bs4 import BeautifulSoup
  - webbrowser
  - import matplotlib.pyplot as plt

### Data sources

#### 1. Wikipedia
- List of United States cities by population
List of United States cities by population
[Wikipedia-population](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population).
Data of each city is scraped from this page to give a background information about cities. "rank" "city", "state", "population", and "land area" are shown in the table.

- Challenge score: 4

#### 2. Unsplash [Link to Unsplash photos page](https://unsplash.com/)
- The photos of each city can be accessed based on users request.

#### 3. Yelp Fushion [Link to Yelp Fushion](https://api.yelp.com/v3/businesses/search)
- I use private API to access restaurant information. "Restaurant name", "url", "transactions", "price" and "rating" are included in restaurant information shown to the users.

- Challenge score: 4

### Data Structure

- Tree structure with dictionary to add information for each restaurant
- Price Tree: the tree for restaurants in each price level.

- Structure of Data

![image of tree structure](Documentation/tree.png)

### Interaction and Presentation Plans
- Interacting with users by asking questions. Data visualization based on the answers offered by users.
- List top 15 cities which have most population
- Open the Unsplash website to view more images of the city.
- List the restaurants in a city based on users answer.
- Pie chart: restaurant categories for city input by the user.
- Bar chart: Numbers of restaurants for each score of rating.

### Demo Video
Click here to open the demo video:

[Demo Video](https://youtu.be/5hbyh7wd-oU)

### Get Started
##### 1. Import libraries

  import json

  import secrets

  import requests

  from bs4 import BeautifulSoup

  import webbrowser

  import matplotlib.pyplot as plt

  import yaml

  import pandas

##### 2. Access your own API key from [Yelp](https://www.yelp.com/developers/documentation/v3/get_started)

##### 3. Replace API_KEY by your own in secrets.py

##### 4. Run final_project.py to play with it
