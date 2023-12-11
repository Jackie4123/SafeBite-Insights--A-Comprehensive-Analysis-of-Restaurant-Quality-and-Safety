import json
import pandas as pd
import csv
import numpy as np
from textblob import TextBlob
from wordcloud import WordCloud,STOPWORDS
from sklearn.linear_model import LinearRegression
from pandas import json_normalize
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter


# Data Normalization function
def min_max_scaling(scores):
	min_val = min(scores)
	max_val = max(scores)
	return [(x - min_val) / (max_val - min_val) for x in scores]

# Sentiment Analysis 
def Sentiment_analysis(data_fr):

	# Getting reviews' text and analyze their sentiment score 
	sentiment_scores = []
	numerical_scores = []
	positive_count = 0
	negative_count = 0
	neutral_count = 0
	all_reviews_text = ""
	inspection_description = ""

	for i in range(len(data_fr)):

		numerical_score = data_fr[i]['rating']
		numerical_scores.append(numerical_score)

		reviews_text = data_fr[i]['text']
		analysis = TextBlob(reviews_text)
		sentiment_score = analysis.sentiment.polarity

		# Append sentiment score to the list
		sentiment_scores.append(sentiment_score)

		# Positive
		if sentiment_score > 0:
			positive_count+=1
		# Negative  
		elif sentiment_score < 0:
			negative_count+=1
		# Neutral   
		else:
			neutral_count+=1

		# Combine all reviews text into a single string
		the_reviews_text = " ".join(reviews_text.split())
		all_reviews_text += the_reviews_text

	normalize_numerical_scores = min_max_scaling(numerical_scores)
	normalize_sentiment_scores = min_max_scaling(sentiment_scores)
	
	return all_reviews_text,normalize_numerical_scores,normalize_sentiment_scores

def Linear_Regression_analysis(normalize_numerical_scores,normalize_sentiment_scores):

	# Plot for sentiment score vs numerical score and their linear regression line
	normalize_numerical_scores = np.array(normalize_numerical_scores)
	normalize_sentiment_scores = np.array(normalize_sentiment_scores)
	# Reshape x to a column vector
	normalize_numerical_scores = normalize_numerical_scores.reshape(-1, 1)
	# Create a linear regression model and fit it to the data
	model = LinearRegression()
	model.fit(normalize_numerical_scores, normalize_sentiment_scores)

	# Predict normalize_sentiment_scores values based on the linear regression model
	ns_pred = model.predict(normalize_numerical_scores)
	
	return normalize_numerical_scores,normalize_sentiment_scores,ns_pred


# Correlation analysis for inspection score and restaurant rating score
def Correlation_analysis(data_fb,data_fi):
	
	# Create a dictionary to store the score data for each matching name
	matching_scores = {}
	restaurant_score = []
	inspeciton_score = []
	inspection_description = ""

	# Get inspection score
	for json_item in data_fb:
		json_name = json_item.get('name')

		# Find matching rows in JSON data
		matching_rows = [row for row in data_fi if row['facility_name'] == json_name]
		
		if matching_rows:
			# Match found, extract the score data
			i_scores = [float(row['score']) for row in matching_rows]
			i_de = [row['pe_description'] for row in matching_rows]
			
			matching_scores[json_name] = i_scores[0], i_de[0]
			inspeciton_score.append(i_scores[0])
			inspection_description += i_de[0]


	for fi_name in matching_scores:

		for fb_name in data_fb:
			if fb_name.get('name') == fi_name:
				restaurant_score.append(fb_name.get('rating'))

	# Do the min max scaling to normalize the data
	inspeciton_score_normalized = min_max_scaling(inspeciton_score)
	restaurant_score_normalized = min_max_scaling(restaurant_score)

	return restaurant_score_normalized,inspeciton_score_normalized,inspection_description

def Language_distribution_analysis(data_fr):
	# Restaurant possible language distribution analysis
	possible_languages = []

	for restaurant in data_fr:
		possible_languages.extend(restaurant.get('possible_languages', []))

	# Count occurrences of each language
	language_counts = Counter(lang for lang in possible_languages)

	# Generate shades of pink colors
	pink_colors = sns.color_palette("pink", n_colors=len(language_counts))

	return language_counts,pink_colors

def Comprehensive_analysis_data(data_fb,data_fi):
	# Parse JSON data
	json_df = json_normalize(data_fb)
	json_di = json_normalize(data_fi)

	# Merge the two DataFrames based on a common key (facility_name)
	merged_df = pd.merge(json_di, json_df, left_on='facility_name', right_on='name', how='inner')

	# Convert 'location.zip_code' to numeric (assuming it contains numeric values)
	merged_df['location.zip_code'] = pd.to_numeric(merged_df['location.zip_code'], errors='coerce')

	numerical_columns = ['score', 'location.zip_code','rating']
	numerical_data = merged_df[numerical_columns]

	return numerical_data

