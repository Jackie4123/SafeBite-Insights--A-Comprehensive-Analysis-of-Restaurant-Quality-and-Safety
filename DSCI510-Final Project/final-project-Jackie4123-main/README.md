# SafeBite Insights - <br/>_A Comprehensive Analysis of Restaurant Quality and Safety_
### "SafeBite Insights" is an innovative data analysis project that focuses on Los Angeles City and aims to provide a holistic understanding of restaurant quality and safety.
## Dependencies
The Python version used in this project is 3.8.1.<br/> Please ensure and check the requirements.txt, including all libraries you may want to pip install and import for the project.<br/> Below is the requirement.txt content.<br/>
<ul>
  <li>python==3.8.1</li>
  <li>pandas==2.0.3</li>
  <li>numpy==1.21.0</li>
  <li>textblob==0.17.1</li>
  <li>wordcloud==1.9.2</li>
  <li>scikit-learn==0.23.1</li>
  <li>matplotlib==3.7.4</li>
  <li>seaborn==0.13.0</li>
  <li>requests==2.31.0 </li>
</ul>

## Project Structure
#### Below is the project structure:
- data
  - raw
    - Restaurant_and_Market_Health_Inspections.csv _(The restaurant inspection data downloaded from the "County of Los Angeles Open Data")_
    - restaurant_basic_info.json _(The restaurant basic information data request from Yelp API)_
    - restaurant_reviews.json _(The restaurant reviews information data request from Yelp API)_
  - processed
    - restaurant_basic_info_cleaned.json _(The restaurant basic information cleaned data)_
    - restaurant_inspections_cleaned.json _(The restaurant inspection cleaned data)_
    - restaurant_reviews_cleaned.json _(The restaurant reviews cleaned data)_
- results
  - Final report.pdf _(The final report, with a comprehensive process description for data collection, cleaning, analysis, and visualization, provides insights into the project.)_
- src
  - get_data.py _(This python file is used to gather all data.)_
  - clean_data.py _(This python file is used to clean all data.)_
  - run_analysis.py _(This python file analyzes the data and returns values to make the visualization in visualze_results python file.)_
  - visualize_results.py _(This python file is used to get the values from the run_analysis python file and make the visualization.)_ 
- README.md _(The README.md file includes dependencies, project structure, running the Code for Results, and conclusion.)_
- requirements.txt _(The requirements file includes all libraries that need to be imported and installed.)_

## Running the Code for Results
1. Run the get_data.py file. _(This step is to get the data from Yelp API.)_
2. Run the clean_data.py file. _(This step is to clean the data from the raw data file.)_
3. Run the visualize_data.py file. _(This step is to visualize the analysis results by getting the return values from the run_analysis.py file.)_

## Conclusion
#### The analyses reveal key insights:
1. Customers prioritize food, service, and ambiance.
2. Higher Yelp ratings correspond to more positive sentiments.
3. Moderate positive link: Health scores correlate with Yelp ratings, emphasizing compliance.
4. Customer feedback displays linguistic diversity, predominantly in English.



