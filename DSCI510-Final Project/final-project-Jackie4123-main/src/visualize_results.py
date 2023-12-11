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
import run_analysis

def WordCloud_visualization(all_reviews_text,inspection_description):

	all_reviews_text = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(all_reviews_text)

	# Visualize word cloud
	plt.figure(figsize=(10, 5))
	plt.imshow(all_reviews_text, interpolation='bilinear')
	plt.axis('off')
	plt.title('Word Cloud of Reviews')
	plt.show()

	# Textual analysis and WordCloud visualization for inspection description
	inspection_description = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(inspection_description)

	# Visualize word cloud
	plt.figure(figsize=(10, 5))
	plt.imshow(inspection_description, interpolation='bilinear')
	plt.axis('off')
	plt.title('Word Cloud of Inspection description')
	plt.show()

def Correlation_coefficient(normalize_numerical_scores,normalize_sentiment_scores):
	# Calculate and print the correlation coefficient
	correlation_coefficient = np.corrcoef(normalize_numerical_scores, normalize_sentiment_scores)[0, 1]
	print(f'Correlation Coefficient: {correlation_coefficient}')


def Linear_Regression(normalize_numerical_scores,normalize_sentiment_scores,ns_pred):
	# Plot
	plt.figure(figsize=(8, 6))
	plt.plot(normalize_numerical_scores, ns_pred, color='red', linewidth=2, label='Linear Regression Line') # Plot the linear regression line
	plt.scatter(normalize_numerical_scores, normalize_sentiment_scores, color='blue', alpha=0.5)
	plt.title('Sentiment Score vs Numerical Score') 
	plt.xlabel('Numerical Score')
	plt.ylabel('Sentiment Score')
	plt.show()

def Correlation_inspection_restaurant(restaurant_score_normalized,inspeciton_score_normalized):
	# Regression plot
	sns.regplot(x= restaurant_score_normalized, y= inspeciton_score_normalized)
	plt.title('Regression Plot of Inspection Score vs Restaurant Score')
	plt.xlabel('Restaurant score')
	plt.ylabel('Inspeciton Score')
	plt.show()

def Language_distribution_visualization(language_counts,pink_colors):
	# Create a pie chart with labels but without percentage values
	plt.figure(figsize=(8, 8))
	pie_chart = plt.pie(language_counts.values(), labels=language_counts.keys(), startangle=90, colors=pink_colors)

	# Add a title
	plt.title('Distribution of Possible Languages Among Restaurants')

	# Create a legend with handles and labels
	legend_labels = ['{0} - {1:1.1f}%'.format(lang, (count/sum(language_counts.values()))*100) for lang, count in language_counts.items()]
	plt.legend(handles=pie_chart[0], labels=legend_labels, title='Languages', loc='center left', bbox_to_anchor=(1, 0.5))

	# Show the plot
	plt.show()

def Comprehensive_analysis_visualization(numerical_data):

	# Examine relationships between numerical variables using a pair plot
	sns.pairplot(numerical_data)

	# Show the plot
	plt.show()

	# A heatmap to explore the correlation matrix of numerical variables
	correlation_matrix = numerical_data.corr()

	# Create a heatmap
	plt.figure(figsize=(8, 6))
	sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=2)

	# Add a title
	plt.title('Correlation Matrix of Numerical Variables')

	# Show the plot
	plt.show()


if __name__ == '__main__':

	# Open restaueant basic information cleaned json
	fb = open('../data/processed/restaurant_basic_info_cleaned.json')
	# Open restaueant reviews cleaned json
	fr = open('../data/processed/restaurant_reviews_cleaned.json')
	# Data for restaueant inspection
	fi = open("../data/processed/restaurant_inspections_cleaned.json")

	# Data for restaueant basic information
	data_fb = json.load(fb)
	# Data for restaueant reviews
	data_fr = json.load(fr)
	# Data for restaueant inspection
	data_fi = json.load(fi)


	all_reviews_text = run_analysis.Sentiment_analysis(data_fr)[0]
	normalize_numerical_scores = run_analysis.Sentiment_analysis(data_fr)[1]
	normalize_sentiment_scores = run_analysis.Sentiment_analysis(data_fr)[2]
	linear_numerical_scores = run_analysis.Linear_Regression_analysis(normalize_numerical_scores,normalize_sentiment_scores)[0]
	linear_sentiment_scores = run_analysis.Linear_Regression_analysis(normalize_numerical_scores,normalize_sentiment_scores)[1]
	ns_pred = run_analysis.Linear_Regression_analysis(normalize_numerical_scores,normalize_sentiment_scores)[2]
	restaurant_score_normalized = run_analysis.Correlation_analysis(data_fb,data_fi)[0]
	inspeciton_score_normalized = run_analysis.Correlation_analysis(data_fb,data_fi)[1]
	inspection_description = run_analysis.Correlation_analysis(data_fb,data_fi)[2]
	language_counts = run_analysis.Language_distribution_analysis(data_fr)[0]
	pink_colors = run_analysis.Language_distribution_analysis(data_fr)[1]
	numerical_data = run_analysis.Comprehensive_analysis_data(data_fb,data_fi)

	# Visualization
	WordCloud_visualization(all_reviews_text,inspection_description) # WordCloud for reviews and inspection decriptions
	Correlation_coefficient(normalize_numerical_scores,normalize_sentiment_scores) # Correlation coefficient between rating and sentiment score
	Linear_Regression(normalize_numerical_scores,normalize_sentiment_scores,ns_pred) # Linear regression plot for rating and sentiment score
	Correlation_inspection_restaurant(restaurant_score_normalized,inspeciton_score_normalized) # Correlation between rating and inspection score
	Correlation_coefficient(restaurant_score_normalized,inspeciton_score_normalized) # Correlaiton coefficient between rating and inspection score
	Language_distribution_visualization(language_counts,pink_colors) # Language distribution visualization
	Comprehensive_analysis_visualization(numerical_data) # Comprehensive analysis for numeric data


	
	