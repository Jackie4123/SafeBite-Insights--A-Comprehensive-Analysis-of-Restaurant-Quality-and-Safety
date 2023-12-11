import json
import pandas as pd
import numpy as np
import csv


# Handling Missing Values
def replace_nan_value(obj):
	# if it is a dictionary
	if isinstance(obj, dict):
		return {key: replace_nan_value(value) for key, value in obj.items()}
	# if it is a list
	elif isinstance(obj, list):
		return [replace_nan_value(element) for element in obj]
	elif pd.isna(obj) or obj == 'null':
		return ''
	else:
		return obj

# Cleaning data from restaurant basic info Json file
def cleaning_restaurant_basic_info(fb):
	
	restaurant_basic_info = json.load(fb)['businesses']

	# Convert the data to a Pandas DataFrame
	df = pd.DataFrame(restaurant_basic_info)

	# Apply a function to a Dataframe elementwise
	df = df.applymap(replace_nan_value)

	# Removing Duplicates
	df = df.drop_duplicates(subset="id")

	# Converting Data into a Structured Format
	df["review_count"] = pd.to_numeric(df["review_count"])
	df["rating"] = pd.to_numeric(df["rating"])

	# Covert name to lowercase
	df["name"] = df["name"].str.lower()

	# Save the cleaned DataFrame as a JSON file
	df.to_json("../data/processed/restaurant_basic_info_cleaned.json", orient="records")
	print(f"JSON data has been successfully stored")

#cleaning_restaurant_basic_info()

# Cleaning data from restaurant reviews Json file
def cleaning_restaurant_reviews(fr):

	cleaning_restaurant_reviews = json.load(fr)

	# Convert the data to a Pandas DataFrame
	data = pd.DataFrame(cleaning_restaurant_reviews)

	# Convert the nested data to a flat list of dictionaries
	flat_data = []
	for business_id, business_data in data.items():

		for review in business_data["reviews"]:

			flat_data.append({
				"business_id": business_id,
				"review_id": review["id"],
				"url": review["url"],
				"text": review["text"],
				"rating": review["rating"],
				"time_created": review["time_created"],
				"user_id": review["user"]["id"],
				"user_profile_url": review["user"]["profile_url"],
				"user_image_url": review["user"]["image_url"],
				"user_name": review["user"]["name"],
				"total_reviews": business_data["total"],
				"possible_languages": business_data["possible_languages"]
			})

	# Convert the flat data to a Pandas DataFrame
	df = pd.DataFrame(flat_data)

	# Apply a function to a Dataframe elementwise
	df = df.applymap(replace_nan_value)

	# Removing Duplicates
	df = df.drop_duplicates(subset=["business_id", "review_id"])

	# Converting Data into a Structured Format
	df["rating"] = pd.to_numeric(df["rating"])

	# Additional Considerations
	df["user_name"] = df["user_name"].str.lower()
	df["text"] = df["text"].str.lower()

	# Save the cleaned DataFrame as a JSON file
	df.to_json("../data/processed/restaurant_reviews_cleaned.json", orient="records")
	print(f"JSON data has been successfully stored")

#cleaning_restaurant_reviews()

# Cleaning data from restaurant inspections CSV file
def cleaning_restaurant_inspections(df):
	file_rb= open("../data/processed/restaurant_basic_info_cleaned.json")
	restaurant_basic = json.load(file_rb)
	data_rb = pd.DataFrame(restaurant_basic)

	# Handle missing value
	df.fillna('', inplace=True)

	# Convert Data into a Structured Format
	df['score'] = pd.to_numeric(df['score'])

	# Convert string to lowercase
	df['service_description'] = df['service_description'].str.lower()
	df['program_name'] = df['program_name'].str.lower()

	# Additional Considerations
	df['facility_name'] = df['facility_name'].str.lower()


	# Filter the DataFrame based on whether 'facility_name' is in 'name' column of data_rb
	filtered_df = df[df['facility_name'].isin(data_rb['name'])]

	# Write JSON file directly from DataFrame
	json_file_path = "../data/processed/restaurant_inspections_cleaned.json"
	filtered_df.to_json(json_file_path, orient='records')

	print(f"JSON data has been successfully stored at {json_file_path}")

if __name__ == '__main__':

	# Open the restaurant basic info Json file
	fb = open('../data/raw/restaurant_basic_info.json')
	cleaning_restaurant_basic_info(fb)

	# Open the restaurant reviews info Json file
	fr = open('../data/raw/restaurant_reviews.json')
	cleaning_restaurant_reviews(fr)

	# Read the CSV file into a DataFrame
	df = pd.read_csv('../data/raw/Restaurant_and_Market_Health_Inspections.csv')
	cleaning_restaurant_inspections(df)
