# House Flipping in King County, USA
## Using data to decide whether to buy houses, and when to sell them

<p align="center">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRVwb8uOqxd9D_S0SJSo8cN3rGhRnUe1-yf_g&usqp=CAU"/>
</p>

In this challenge we are facing a question that may arise for anyone in flipping - 
which assets should we buy and how long should we wait before selling them?

!TODO! Briefly describe main results and how I got them

To answer that questions, we started by downloading the public data from [ ![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white)](https://www.kaggle.com/harlfoxem/housesalesprediction). The dataset contains house sale prices, and many more features, for King County, which includes Seattle. It contains data from homes sold between May 2014 and May 2015. Usually, people use this dataset to build regression models for predicting house prices. Instead, since I am not interested in building any machine learning model (in this project), my approach relies on getting insights from a well-performed exploratory data analysis (EDA).

All visualizations are available online on an application made using ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) and hosted on [![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)](https://dashboard-kc-hdata-pa.herokuapp.com/). It can be accessed by anyone on mobile or desktop.

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
* No more than 12% of the house initial value will be spent in renovating it
* For houses in good conditions, 7% of the initial value will be the top limit for expenditures with renovation.

# Solution Planning

To save time in coding and performing the EDA, I list the to-take steps:

1) Download the data from [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction)
2) Check data types, missing values and duplicates
3) Egineer features: `month`, `year`, `old`, `season`, `basement`
4) Create visualizations for price variations according to: `month`-`year` (season), `zipcode` (region)
5) Draw hypotheses and test them

# Main Insights

* New houses are not quite more expensive than houses labelled as old (Built before 1960). On average, old houses are only **TODO**% cheaper than new houses. As prices do not vary much according to the year of construction (yr_built), buying new houses gives higher profits; newer houses demand fewer expenditures.
* Houses with no basemente are **TODO**% bigger than houses with basement (total area). 
* On average, houses having a waterfront view are **TODO**% more expensive. This means that in case we find a house, having a waterfront view, being sold for a price lower than the regional average price we should buy it regardless its condition. 

  
