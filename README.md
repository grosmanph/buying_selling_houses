# House Flipping in King County, USA
## Using data to decide whether to buy a house, and when to sell it

<p align="center">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRVwb8uOqxd9D_S0SJSo8cN3rGhRnUe1-yf_g&usqp=CAU"/>
</p>

# Abstract
I delivered here a complete data-driven business plan. By parametrizing what is deemed as "good business", it was possible to create indicators of houses well-suited for maximizing profits with flipping. The main insights gotten from the exploratory data analysis reassured some hypotheses and pointed out new ways of doing business.

# Introduction
House flipping is when someone buys a property and holds onto it for a short time and then sells it (the flip part) in the hopes of making a profit. Instead of buying a home to live in, you’re buying a home as a real estate investment.

Sometimes, flipping a house means the temporary owner has to make a lot of repairs or renovations, and other times it’s owning the property until you can sell it for more than you paid for it, plus whatever you put in to fix it up. The goal is to buy low and sell high, invest your own sweat equity to cut costs and earn a profit in a relatively short amount of time — usually within months or a year

In this challenge we are facing a question that may arise for anyone in flipping - 
which assets should we buy and how long should we wait before selling them?

To answer the business questions, we started by downloading the public data from [ ![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white)](https://www.kaggle.com/harlfoxem/housesalesprediction). The dataset contains house sale prices, and many more features, for King County, which includes Seattle. It contains data from homes sold between May 2014 and May 2015. Usually, people use this dataset to build regression models for predicting house prices. Instead, since I am not interested in building any machine learning model (in this project), my approach relies on getting insights from a well-performed exploratory data analysis (EDA).

All visualizations are available online on an application made using ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) and hosted on [![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)](https://dashboard-kc-hdata-pa.herokuapp.com/). It can be accessed by anyone on mobile or desktop. Click [here](https://dashboard-kc-hdata-pa.herokuapp.com/) to be redirected.

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
3) Egineer features: `month`, `year`, `old`, `season`, `basement`, `to_renovate`
4) Create visualizations for price variations according to: `month`-`year` (season), `zipcode` (region)
5) Draw hypotheses and test them

# Main Insights

* New houses are not quite more expensive than houses labelled as old (Built before 1960). On average, new houses are only 3.99% more expensive than old houses. As prices do not vary much according to the year of construction (yr_built), buying new houses gives higher profits; newer houses demand fewer expenditures.
<p align="center">
  <img src="https://i.postimg.cc/JnJYHs26/avg-price-new-VSold.png"/>
</p>

* Houses with no basement are 22.79% bigger than houses with a basement, considering the average square footage of the lot. Furthermore, houses having no basement are 21.73% cheaper on average. This means we can buy houses with no basement in good conditions to build a basement before selling it for a higher price.
<p align="center">
  <img src="https://i.postimg.cc/5ygQ2M87/avg-price-basement.png" width=450/>
  <img src="https://i.postimg.cc/jjfWJfzJ/avg-sqft-Liv-basement.png" width=450/>
</p>

* On average, houses having a waterfront view are 211.76% more expensive. This means that in case we find a house, having a waterfront view, being sold for a price lower than the regional average price we should buy it regardless of its condition. 
<p align="center">
  <img src="https://i.postimg.cc/MTvjKL9q/avg-price-waterfront.png"/>
</p>

# Business Results

### Hypothesis 1: Houses having a waterfront view are, on average, more expensive.
Indeed, the affirmative above is true. It is reasonable saying that, considering the same region, a house having a waterfront view would cost more than a house without it. What we did not know previously, is how much more expensive it is. By performing an EDA we were able to say that houses with a waterfront view are around 210% more expensive, on average.

That huge difference in prices leads us to the following possible **business action**: houses with a waterfront view being sold for a price smaller than the regional average price should be bought no matter its condition. Since this kind of house is much more expensive than ordinary houses, having the chance of buying one of them for a very low price would make us able to practice a bigger profit margin - 80%, for instance.
  
### Hypothesis 2: Old houses are way cheaper than newer houses.
This hypothesis is pretty much false. Our intuition would tell us that an old house, but not way too old, would cost less than a brand-new house. Counterintuitively, the EDA showed us that prices of new houses differ by around only 4% from prices of old houses. In this case, old houses are way too far from being way cheaper than newer houses.

Translating it to a possible **business action**, I would say that it is more suitable choosing newer houses rather than old houses. The tiny difference in prices may not compensate possible expenditures with renovation, in case one go for an older house.

### Hypothesis 3: Houses with no basement are bigger and cost less.
At first, there is nothing wrong with thinking that way; having a basement is for sure something that increases a house's price. The bar plot above shows us that houses with no basement are 22.79% bigger than houses with a basement, considering the average square footage of the lot, and that houses having no basement are 21.73% cheaper on average.

Having said that, if one had the chance of buying a house with no basement, in good conditions, the **business action** could be using the free space on the lot to invest in constructing new facilities before selling the house for an even higher price.

### Hypothesis 4: Houses are renovated 30 years after they were built, on average.
As we were shown by descriptive statistics, this hypothesis does not hold at all considering the data we have on hand. According to the descriptive values (table below), houses take around 56 years to be renovated. Considering the left edge of the dispersion range (std), it is likely that a house may need to be renovated 32 years after it was built. 

|                 | Mean | Std Dev | Min | Median |  Max  |
| --------------- | ---- | ------- | --- | ------ | ----- |
| **to_renovate** | 56.3 | 24.0    | 6.0 | 54.0   | 114.0 |

These results are really important since they reassure our previous consideration that it would be more profitable to buy newer houses. Now, this **business action** has no bias; houses in good conditions, being sold at a price lower than the regional average, and having no more than 32 years since their construction, are a must-buy. These criteria indicate an excellent business opportunity, according to our assumptions.

### Hypothesis 5: House prices vary through seasons and are cheaper in winter
Prices are a bit lower in winter, but as we can effortlessly notice from the bar chart below, there is no substantial season-to-season variation of house prices. Taking into account the relative deviation from one average price to another, we may not assign these small variations to climate changes caused by transitions among the seasons. More YoY data is needed to infer that.
<p align="center">
  <img src="https://i.postimg.cc/kXxhQmkY/avg-price-season.png"/>
</p>

As a **result**, we could say that there is no preferred season to sell a house; we can sell it as soon as possible to increase the net working capital.

# Concluding Remarks

I delivered here a complete data-driven business plan that makes the action of identifying potential business opportunities from a wide range of possibilities scalable and unbiased. By parametrizing what is deemed as "*good business*", it was possible to create indicators of houses well-suited for maximizing profits in flipping. Further, by making assumptions about the main features involved in the case, I outlined a solution planning that saved me time and gave me the right directions to search for answers. The main insights gotten from the exploratory data analysis reassured some hypotheses and pointed out new ways of doing business, as we did with houses having a waterfront view or houses with a basement, for example.

The created solution also provides a user-friendly interactive online application that can be accessed by anyone on mobile or desktop, which makes our solution reliable, accessible, shareable, and easy to reach. From that application, I could visualize descriptive statistics from a variety of features like central tendencies of prices, dispersive metrics for the number of bedrooms, and much more. All the assertive visualizations made the processes of decision-making and business planning faster and less biased. 

As a major result, according to the assumptions made for this solution, this project forecasts 23% of profit, which amounts to 457410805.18 USD.

# Possible Next Steps

* Make a list of priority criteria to organize the houses pointed as potential businesses in order of "*should-buy-ASAP*".
* Creating a machine learning model to predict the price of a house according to its relevant features.
* Creating a machine learning model to, given a set of features like price, # of bedrooms, etc., classify the area where a house should be built.
* Build a recommender system
