# House Flipping in King County, USA
## Using data to decide whether to buy houses, and when to sell them

In this challenge we are facing a question that may arise for anyone in flipping - 
which assets should we buy and how long should we wait before selling them?

!TODO! Briefly describe main results and how I got them

To answer that questions, we started by downloading the public data from [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction). The dataset contains house sale prices, and many more features, for King County, which includes Seattle. It contains data from homes sold between May 2014 and May 2015. Usually, people use this dataset to build regression models for predicting house prices. Instead, since I am not interested in predicting prices, my approach relies on getting insights from a well-performed data analysis (EDA).

All visualizations are available online on an application that can be accessed by anyone on mobile or desktop by clicking the following [link](https://dashboard-kc-hdata-pa.herokuapp.com/).

# Business Questions

Before starting coding and producing visualizations, it is convenient stating the main business questions. Since this project is business-oriented, we need to be reassured of what we are doing and where we are going.

### Question 1: Which houses should we buy?

What are the residential real states we should buy, and how much should we pay?

### Question 2: When should we sell?

Once I have bought a house, when is the best moment to sell it and how much should I charge?

# Assumptions

In this section, I make some assumptions about the dataset.
* Prices are season-dependent and may also vary among regions (zipcode)
* Houses built before 1960 are labelled as 'old'
* Prices below the regional average may indicate potential businesses
* Potential businesses should be evaluated by: condition, cheapness
* Selling prices might adjust according to season and location

# Solution Planning

To save time in coding and performing the EDA, I list the to-take steps:

1) Download the data from [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
2) Check data types, missing values and duplicates
3) Egineer features: `month`, `year`, `old`, `season`, `basement`
4) Create visualizations for price variations according to: `month`-`year` (season), `zipcode` (region)
5) Draw hypothesis and test them

# Main Insights
  
