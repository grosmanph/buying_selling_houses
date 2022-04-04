## ====================
## 		Imports
## ====================
import geopandas
import streamlit as st
import pandas    as pd
import numpy     as np
import plotly.express as px
import folium
import sys

from datetime import date
from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster

## pre-defined functions
from my_methods import *

## ====================
## 	Streamlit Settings
## ====================
st.set_page_config( layout='wide' )

## ====================
## 		Execution
## ====================
if __name__ == "__main__":

	## --- data extraction
	df, mute = get_data( 'kc_house_data.csv' )
	df = df.head(8000) ## limiting to run faster; comment this line to see restults for the dataset as whole
	if mute == 0:
		sys.exit()
		
	geofile = get_geofile( 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson' )
	## --- data tranformation and feature engineering
	df = hand_nonunique( df, 'id' )
	
	df, mute = check_integers( df, ['bedrooms', 'bathrooms', 'floors', 'yr_built', 'yr_renovated', 'zipcode' ] )
	if mute == 0:
		sys.exit()

	df['date'] = pd.to_datetime(df['date']).apply(lambda x: x.date())
	df ['month'] = df['date'].apply( lambda x: x.month ).astype(np.int)
	df['year'] = df['date'].apply( lambda x: x.year )
	df['season'] = df['date'].apply( get_season ).astype(str)


	df['price_sqft'] = df['price']/df['sqft_living']

	df['old'] = df['yr_built'].apply(lambda x: 1 if x < 1960 else 0).astype(np.int64)

	df['to_renovate'] = df[['yr_built','yr_renovated']].apply( lambda x: x['yr_renovated'] - x['yr_built'] if x['yr_renovated'] != 0
														   else np.NaN, axis=1)


	## --- data loading
	st.title('Properties Flipping in King County')
	
	st.markdown( 'Welcome to the King County (KC) housing dashboard. '
				 'The dataset consists of house prices from King County an area in the US State of Washington, this data also covers Seattle. '
				 'Below you can have an overview of how the dataset looks like. Navigate through the sidebar to see the interactive options - '
				 'attributes (display options) can be filtered (adjusted) using it.' )
	st.markdown( '\n' )
	st.markdown( 'This dashboard is part of a complete project in business intelligence concerned with making a profit from flipping. '
				 'Click [here](https://github.com/grosmanph/buying_selling_houses) to get to the Github repo.' )
	st.markdown( '\n' )
	st.markdown( '**Disclaimer:** The data used in this application are public and were taken from '
				 '[Kaggle](https://www.kaggle.com/shivachandel/kc-house-data). The context exposed here is fictitious and has no commitment to reality. '
				 'The trends observed may not represent real-life behaviour.' )
	st.markdown( '---' )


	## --- data overview
	st.header('Data Overview')
	st.sidebar.title('Data Overview Options')
	f_attributes = st.sidebar.multiselect('Select attributes', options=df.columns.drop('id'))
	st.dataframe( display_data_overview( df, f_attributes ) )


	## --- statistics
	st.title( 'Statistics' )
	st.markdown( 'The most important metrics and statistics are shown in this section. '
				 'The main goal here is presenting a quantitative analysis of the data in a simple way. ' )
	st.markdown( '---' )
	c1, c2 = st.columns( (1,1) )

	st.sidebar.title('Averages by Zipcode Options')
	c1.header('Averaged Values by Zipcode')
	c1.markdown(
		'In the table below you can see averaged values for price, sqft_living, and price/sqft on each region (labelled by zipcode). Use sidebar options to filter.')
	f_zipcode = st.sidebar.multiselect('Select zipcodes to display', options=df['zipcode'].unique())
	to_disp, hei = display_data_averaged( df,f_zipcode )
	c1.dataframe( to_disp, height=hei  )

	st.sidebar.title( 'Descriptive Statistics Options' )
	c2.header( 'Descriptive Statistics' )
	c2.markdown( 'This table shows descriptive statistics for several attributes. You can control which attribute and metric are shown by using the options in the sidebar.' )
	c2.markdown( '\n' )
	f_att = st.sidebar.multiselect('Select attributes to describe',
								   options=df.select_dtypes( include=['int64', 'float64'] ).drop(['id', 'lat', 'long', 'zipcode', 'yr_renovated', 'waterfront', 'view'], axis=1))
	f_percentiles = st.sidebar.radio('Pick a percentile to show', options=(0.25, 0.5, 0.75),
									 format_func=lambda x: str(int(x * 100)) + '%',
									 help='The 50th percentile is the same as the median')
	to_disp, hei = display_descriptive(df, f_att, f_percentiles)
	c2.dataframe( to_disp, height=hei )

	f_att = st.sidebar.multiselect('Select attributes to plot distribution',
								   options=df.select_dtypes( include=['int64', 'float64'] ).drop(['id', 'lat', 'long', 'zipcode', 'yr_renovated', 'waterfront', 'view'], axis=1).columns,
								   default='to_renovate')
	st.header( 'Distribution of a selected feature' )
	st.markdown( 'Use the sidebar to select features to show their distribution. Default is `to_renovate`' )
	st.plotly_chart( display_dist_renv( df, f_att ), use_container_width=True )


	## --- maps (centificate expired)
	st.title( 'Maps' )
	st.markdown( 'This section is intended to display geographical data. Regions are separated by zip code. The first run may took a while.' )
	st.markdown( '---' )
	c1, c2 = st.columns( (1,1) )
	
	with c1:
		c1.header('House Markers Map')
		c1.markdown('You can see the portfolio density on the map below. Adjust the zoom by scrolling up or down.')
		folium_static( display_map_markers( df ) )
		
	with c2:
		c2.header('Prices Density Map')
		c2.markdown('The map below shows the density of prices. More expensive regions are shown in red while cheaper regions appear as light-yellow.')
		folium_static( display_map_density( df, geofile ) )


	## --- commercial
	st.title( 'Prices' )
	st.markdown( 'In this section, you can see figures related to commercial attributes like time evolution of prices, '
				 'average prices, how prices are distributed in the dataset, etc. Use the commercial options in the sidebar to filter these data.' )
	st.markdown( '---' )	
	switcher = {1: [display_price_yrbuilt, display_price_isold],
				2: display_price_date,
				3: [display_price_dist, display_price_basement] }

	st.sidebar.title('Commercial Options')

	com_opt = st.sidebar.radio('Select one of the following options to display commercial plots:',
							   options=('1 - Avg price per yr built',
										'2 - Daily price variations',
										'3 - Prices Distribution',
										'4 - Show all'),
							   index=3)

	com_opt = int(com_opt.split('-')[0].strip())
	
	if com_opt in switcher.keys():
		try:
			for call in switcher[com_opt]:
				call(df)
		except:
			switcher[com_opt](df)
	else:
		switcher[3][0]( df )
		c1, c2 = st.columns( (1,1) )
		with c1:
			switcher[1][0]( df )
		with c2:
			switcher[2]( df )
		display_price_waterfront( df )
		display_price_season( df )


	## --- physical
	st.title( 'Physical Attributes' )
	st.markdown( 'Below you can see histograms showing the distribution of the houses according to the selected attributes. '
				 'Use the sidebar to choose for displaying either one histogram or all available histograms.' )
	st.markdown( '---' )
	switcher = {1: 'bedrooms',
				2: 'bathrooms',
				3: 'floors',
				4: 'waterfront'}
				
	phys_opt = display_phys_radio()
	
	if phys_opt in switcher.keys():
		st.header( 'Houses Distribution per Number of '+switcher[phys_opt].capitalize() )
		display_att_hist(df, switcher[phys_opt])
	else:
		c1, c2 = st.columns( (1,1) )
		with c1:
			c1.header( 'Houses per Number of '+switcher[1].capitalize() )
			display_att_hist(df, switcher[1], 17)
			c1.header( 'Houses per Number of '+switcher[3].capitalize() )
			display_att_hist(df, switcher[3], 10)
		with c2:
			c2.header( 'Houses per Number of '+switcher[2].capitalize() )
			display_att_hist(df, switcher[2], 10)
			c2.header( 'Houses per Number of '+switcher[4].capitalize() )
			display_att_hist(df, switcher[4], 5)


	## --- final dataframe
	st.header('Business Opportunities')
	st.markdown('---')
	st.markdown(' Below we can see a table indicating houses met as potential business according to the pre-defined assumptions.')

	to_buy, tot_inv, tot_exp, perct, tot_prof = display_houses_tobuy( df )

	st.dataframe(to_buy)
	st.markdown( 'Total profit: {} USD, which represents {}% of the initial investment.'.format(tot_prof,perct) )
	st.markdown( 'Investiments: {} USD'.format(tot_inv,2) )
	st.markdown( 'Expenditures: {} USD'.format(tot_exp,2) )

	st.sidebar.title( 'About' )
	st.sidebar.markdown( '<div style="background-color:rgba(0, 166, 207, 0.36);">This application was developed by '
						 '<a href="https://br.linkedin.com/in/pedro-henrique-grosman-alves-377a33122"> Pedro Grosman </a> '
						 'for presentation purposes only. Feel free to message me in case you have any questions or requests.</div>',
						 unsafe_allow_html=True )
		

	

		

