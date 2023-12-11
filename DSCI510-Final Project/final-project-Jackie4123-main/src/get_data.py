import json
import requests
import pandas as pd


# Restaurant inspection data
def Health_restaurant():
	df= pd.read_csv("../data/raw/Restaurant_and_Market_Health_Inspections.csv",encoding='unicode_escape')
	print(df)

# Restaurant data
def find_food(location: str):

	url_find_restaurant = "https://api.yelp.com/v3/businesses/search"

	headers = {
		"accept": "application/json",
		"Authorization": "Bearer pJ5bGqspPAV0ZVW5nfim6Ln5yWgw1TcPGT601sDATwyUDGLDK0FTEXaNaryQRTG7lGuRwxEvgvBR_fRMR-wZFXprsXNCTEeo1tpUUcjxFLI2XxWivCUaM2W68_VPZXYx"
	}

	params = {
		'location': location,
		'categories': 'restsurant, market',  # Set to 'food' for restaurants
		'limit': 50  # Limit the results to the 50 restaurants
	}

	response = requests.get(url_find_restaurant, headers=headers,params=params)
	
	# Download restaurant basic information
	restaurant_basic_info_json = "../data/raw/restaurant_basic_info.json"

	# Writing to a JSON file
	with open(restaurant_basic_info_json, 'w') as json_file:
		json.dump(response.json(), json_file, indent=4)

	print(f"JSON data has been stored in {restaurant_basic_info_json}")


	#Download reviews by using restaurant id 
	all_restaurant_reviews={}

	for i in range(50):
		restaurant_id=response.json()['businesses'][i]['id']
		url_restaurant_reviews = "https://api.yelp.com/v3/businesses/"+restaurant_id+"/reviews"
		response_reviews = requests.get(url_restaurant_reviews, headers=headers)
		all_restaurant_reviews[restaurant_id]= response_reviews.json()
	
	restaurant_reviews_json = "../data/raw/restaurant_reviews.json"

	# Writing to a JSON file
	with open(restaurant_reviews_json, 'w') as json_file:
		json.dump(all_restaurant_reviews, json_file, indent=4)

	print(f"JSON data has been stored in {restaurant_reviews_json}")


if __name__ == '__main__':

	# Display the downloaded restaurant inspection csv file 
	Health_restaurant()

	# Download restaurant basic and reviews data with Los Angeles as the location
	location="Los Angeles"
	find_food(location)


