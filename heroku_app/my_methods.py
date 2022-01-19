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

@st.cache(allow_output_mutation=True)
def get_data(path):
    """
        Read a comma-separated values (csv) file into a DataFrame.

        Inputs: path: str, path object or file-like object
                Any valid string path is acceptable. The string can be a URL
                Valid URL schemes include http, ftp, s3, gs, and file. For
                file URLs, a host is expected.

        Returns: (DataFrame or TextParser, check)
                 A CSV file is returned as two-dimensional data structure with
                 labeled axes.
    """
    try:
        data = pd.read_csv(path)
        return (data, 1)
    except:
        st.write('No data could be read.')
        return (0, 0)


@st.cache(allow_output_mutation=True)
def get_season(dt):
    ## --- 1: Winter, 2: Spring, 3: Summer, 4: Autumn
    Y = 2000  # dummy leap year to allow input X-02-29 (leap day)
    seasons = [('Win', (date(Y, 1, 1), date(Y, 2, 28))),
               ('Spr', (date(Y, 3, 1), date(Y, 5, 31))),
               ('Sum', (date(Y, 6, 1), date(Y, 8, 31))),
               ('Aut', (date(Y, 9, 1), date(Y, 11, 30))),
               ('Win', (date(Y, 12, 1), date(Y, 12, 31)))]
    dt = dt.replace(year=Y)
    return next(season for season, (start, end) in seasons if start <= dt <= end)


@st.cache(allow_output_mutation=True)
def get_geofile(url):
    geofile = geopandas.read_file(url)

    return geofile


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def check_integers(data, features=None):
    """
        Convert type of selected features of a pandas DataFrame to integer.
        If no feature is passed, then all entries will become integer.

        Inputs: data: pandas DataFrame
                A pandas DataFrame instance contaning the passed features
                to transform in integers. Any valid non-empty DataFrame is acceptable.

                features: str, list or array-like object
                Any array-like object listing the features on which data transformation
                will be applied. If None, then all features will become integer.

        Returns: (pandas DataFrame, check)
    """

    if isinstance(data, pd.DataFrame):
        if features == None:
            if_data = data.select_dtypes(include=['int64', 'float64']).astype(int)
            data.loc[:, if_data.columns] = if_data
            return data
        else:
            list(features)
            data.loc[:, features] = data[features].astype(int)
            return (data, 1)


    else:
        st.write('Invalid data format for input data. It should be an instance of pandas DataFrame. ')
        return (data, 0)


@st.cache(allow_output_mutation=True)
def to_str_fromdt(arg):
    """
        Convert arg to datetime object and then transforms it into
        a date-format string according to the formatting: YYYY-mm-dd

        Inputs: arg: int, float, str, datetime, list, tuple, 1-d array, Series
                The object to convert to a date-format string

        Returns: str
                If parsing succeeded. Return type depends on input.
    """
    try:
        return pd.to_datetime(arg).dt.strftime('%Y-%m-%d')
    except:
        st.write('No date object transformed.')
        return arg


@st.cache(allow_output_mutation=True)
def hand_nonunique(data, feat='id'):
    """
        Return DataFrame with duplicate rows removed by keeping
        the most recent value.

        Inputs: data: pandas DataFrame
                The data frame to remove duplicate rows

                feat: column label or sequence of labels, optional
                Only consider certain columns for identifying duplicates, by default
                use id column.

        Returns: DataFrame
                 DataFrame with duplicates removed.
    """

    try:
        return data.drop_duplicates(subset=feat, keep='last')
    except:
        st.write('No duplicate values were removed.\n\n')
        return data


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def display_data_overview(data, attributes):
    if attributes == []:
        return data
    else:
        to_show = list(attributes)
        to_show.append('id')
        return data[to_show[::-1]]


# return None

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def display_data_averaged(data, zipcodes):
    try:
        dcount = data[['id', 'zipcode']].groupby('zipcode').count()
        dprice = data[['price', 'zipcode']].groupby('zipcode').mean()
        dsqft = data[['sqft_living', 'zipcode']].groupby('zipcode').mean()
        dppsf = data[['price_sqft', 'zipcode']].groupby('zipcode').mean().reset_index()

        m1 = pd.merge(dcount, dprice, on='zipcode', how='inner')
        m2 = pd.merge(m1, dsqft, on='zipcode', how='inner')
        data = pd.merge(m2, dppsf, on='zipcode', how='inner')

        data.columns = ['Zipcode', 'Total Houses', 'Price', 'Sqft Living', 'Price/Sqft']

        if zipcodes == []:
            return (data, 195)
        else:
            return (data[data['Zipcode'].isin(f_zipcode)], None)
    except:
        st.write('Streamlit is unable to display averaged data by zipcodes.')


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def display_descriptive(data, atts, percts):
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    desc = num_attributes.drop(['id', 'lat', 'long', 'zipcode', 'yr_renovated', 'waterfront', 'view'], axis=1)

    desc = desc.describe(percentiles=[percts])
    desc = desc.rename(
        index={'count': '# entries', 'mean': 'Mean', 'std': 'Std Dev', 'min': 'Min', '50%': 'Median', 'max': 'Max'})

    if atts == []:
        return (desc, 205)
    else:
        desc = desc[atts]
        return (desc, 205)


def display_dist_renv(data, atts):
    num_attributes = data.select_dtypes(include=['int64', 'float64'])
    dens = num_attributes.drop(['id', 'lat', 'long', 'zipcode', 'yr_renovated', 'waterfront', 'view'], axis=1)

    dens_plot = px.histogram(data, x=atts)

    return dens_plot


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def display_map_markers(data):
    data = data.head(500)

    b_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)
    marker_cluster = MarkerCluster().add_to(b_map)

    for name, row in data.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold {0} USD on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format(
                          row['price'], row['date'], row['sqft_living'], row['bedrooms'], row['bathrooms'],
                          row['yr_built'])).add_to(marker_cluster)

    return b_map


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def display_map_density(data, geodata):
    data = data.head(500)

    df_map = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df_map.columns = ['Zipcode', 'Price']

    geodata = geodata[geodata['ZIP'].isin(df_map['Zipcode'].tolist())]

    b_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)
    b_map.choropleth(data=df_map, geo_data=geodata, columns=['Zipcode', 'Price'], key_on='feature.properties.ZIP',
                     fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2, legend_name='Average Price')

    return b_map


def display_price_yrbuilt(data):
    ## --- Filtering by yr_built
    min_yr_built = int(data['yr_built'].min())
    max_yr_built = int(data['yr_built'].max())

    f_yr_built = st.sidebar.slider('Select year built range', min_yr_built, max_yr_built, (min_yr_built, max_yr_built))

    data_yr = data[data['yr_built'].between(f_yr_built[0], f_yr_built[1])]
    data_yr = data_yr.groupby('yr_built').mean().reset_index()

    yr_built_plot = px.line(data_yr, x='yr_built', y='price',
                            labels={'price': 'Average Price (USD)', 'yr_built': 'Year of Construction'})
    st.header('Average Price per Year Built')
    st.markdown(
        'How prices vary according to the year houses were built. You can filter the horizontal axis range using the commercial options in the sidebar.')
    st.plotly_chart(yr_built_plot, use_container_width=True)

    return None


def display_price_season(data):
    ## --- grouping data by year and season
    data_season = data[['price', 'year', 'season']].groupby(['year', 'season']).mean().reset_index()

    season_plot = px.histogram(data_season, x='year', y='price', color='season', barmode='group',
                               labels={'year': 'Year', 'season': 'Season'}).update_yaxes(
        {'title': 'Average Price (USD)'})
    st.header('Average Price per Meteorological Season')
    st.markdown('The bar chart below shows how average prices vary according to seasons from 2014 to 2015.')
    st.plotly_chart(season_plot, use_container_width=True)


def display_price_isold(data):
    ## --- selecting average prices
    data_isold = data[['price', 'old']].groupby('old').mean().reset_index()
    perc_dif = (abs(data_isold.iloc[0]['price'] - data_isold.iloc[1]['price']) / data_isold.iloc[1]['price']) * 100.

    isold_plot = px.bar(data_isold, x='old', y='price', labels={'price': 'Average Price (USD)', 'old': ''})
    isold_plot.update_layout(xaxis=dict(tickmode='array',
                                        tickvals=[0, 1],
                                        ticktext=['New Houses', 'Old Houses']))
    st.header('Average Price for New and Old Houses')
    st.markdown('From the bar plot below we can see that the average price for new houses deviates {}% relatively '
                'from the average price of old houses.'.format(str(round(perc_dif, 2))))
    st.plotly_chart(isold_plot, use_container_width=True)
    return None


def display_price_basement(data):
    ## --- selecting average price and average total area according to basement
    data_basement = data[['price', 'sqft_basement', 'sqft_lot']]
    data_basement['sqft_basement'] = data_basement['sqft_basement'].apply(lambda x: 1 if x > 0 else 0).astype(np.int64)
    data_basement = data_basement.groupby('sqft_basement').mean().reset_index()

    perc_dif_price = (abs(data_basement.iloc[0]['price'] - data_basement.iloc[1]['price']) / data_basement.iloc[1][
        'price']) * 100
    perc_dif_price = str(round(perc_dif_price, 2))

    perc_dif_area = (abs(data_basement.iloc[0]['sqft_lot'] - data_basement.iloc[1]['sqft_lot']) / data_basement.iloc[1][
        'sqft_lot']) * 100
    perc_dif_area = str(round(perc_dif_area, 2))

    basement_plot_price = px.bar(data_basement, x='sqft_basement', y='price', labels={'price': 'Average Price (USD)',
                                                                                      'sqft_basement': ''})
    basement_plot_price.update_layout(xaxis=dict(tickmode='array',
                                                 tickvals=[0, 1],
                                                 ticktext=['No Basement', 'Has Basement']))

    basement_plot_area = px.bar(data_basement, x='sqft_basement', y='sqft_lot',
                                labels={'sqft_lot': 'Average square footage lot',
                                        'sqft_basement': ''})
    basement_plot_area.update_layout(xaxis=dict(tickmode='array',
                                                tickvals=[0, 1],
                                                ticktext=['No Basement', 'Has Basement']))

    st.header('Average Price and Average Total Area vs Basement')
    st.markdown(
        'As we can see from the bar plot below, houses having no basement are {}% cheaper on average. Furthermore, these houses are, on average, '
        '{}% bigger considering their total area.'.format(perc_dif_price, perc_dif_area))
    ca, cb = st.columns((1, 1))
    with ca:
        ca.plotly_chart(basement_plot_price, use_container_width=True)
    with cb:
        cb.plotly_chart(basement_plot_area, use_container_width=True)

    return None


def display_price_waterfront(data):
    ## --- selecting average price accordin to waterfront
    data_waterfront = data[['price', 'waterfront']].groupby('waterfront').mean().reset_index()

    perc_dif_price = (abs(data_waterfront.iloc[0]['price'] - data_waterfront.iloc[1]['price']) /
                      data_waterfront.iloc[0]['price']) * 100
    perc_dif_price = str(round(perc_dif_price, 2))

    price_plot = px.bar(data_waterfront, x='waterfront', y='price', labels={'price': 'Average Price (USD)',
                                                                            'waterfront': ''})
    price_plot.update_layout(xaxis=dict(tickmode='array',
                                        tickvals=[0, 1],
                                        ticktext=['No Waterfront', 'Waterfront View']))

    st.header('Average Price vs Waterfront View')
    st.markdown(
        'This bar plot tells us that houses having a waterfront view cost {}% more, on average.'.format(perc_dif_price))
    st.plotly_chart(price_plot, use_container_width=True)

    return None


def display_price_date(data):
    ## --- Filtering by date
    min_date = data['date'].min()
    max_date = data['date'].max()

    f_date = st.sidebar.slider('Select date range', min_date, max_date, (min_date, max_date))

    data_dt = data[data['date'].between(f_date[0], f_date[1])]
    data_dt = data_dt.groupby('date').mean().reset_index()

    date_plot = px.line(data_dt, x='date', y='price')
    st.header('Daily Price Evolution')
    st.markdown(
        'Daily price variation according to the date of registration. You can filter the horizontal axis range using the commercial options in the sidebar.')
    st.plotly_chart(date_plot, use_container_width=True)

    return None


def display_price_dist(data):
    ## --- Price distribution

    f_zipcode = st.sidebar.multiselect('Select zip codes to display prices distribution',
                                       options=data['zipcode'].sort_values().unique())

    data_pr = data.loc[data['zipcode'].isin(f_zipcode), ['price', 'zipcode']] if sum(
        data['zipcode'].isin(f_zipcode)) > 0 \
        else data[['price', 'zipcode']].copy()

    min_price = int(data_pr['price'].min())
    max_price = int(data_pr['price'].max())
    avg_price = int(data_pr['price'].mean())

    f_price = st.sidebar.slider('Select price range', min_price, max_price, (min_price, max_price))

    data_pr = data_pr[data_pr['price'].between(f_price[0], f_price[1])]

    price_plot = px.histogram(data_pr, x='price', color='zipcode' if f_zipcode != [] else None,
                              marginal='box')
    st.header('Prices Distribution')
    st.markdown(
        'An histogram showing how prices are distributed in the dataset. You can adjust the horizontal axis range using the commercial options in the sidebar.')
    st.plotly_chart(price_plot, use_container_width=True)

    return None


def display_phys_radio():
    st.sidebar.title('Physical Attributes')

    phys_opt = st.sidebar.radio('Select one of the following options to display attributes plots:',
                                options=('1 - Houses per bedrooms',
                                         '2 - Houses per bathrooms',
                                         '3 - Houses per floors',
                                         '4 - Houses per waterfront view',
                                         '5 - Show all'),
                                index=4)

    phys_opt = int(phys_opt.split('-')[0].strip())

    return phys_opt


def display_att_hist(data, col, nbins=30):
    data = data[col]

    fig = px.histogram(data, x=col, nbins=nbins)
    st.plotly_chart(fig, use_container_width=True)

    return None


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def display_houses_tobuy(data):
    avg_price_reg = data[['price', 'zipcode']].groupby('zipcode').mean()

    ## --- selecting houses in good conditions (condition >= 4)
    to_buy_good = data[data['condition'] >= 4]
    to_buy_good = to_buy_good.loc[to_buy_good['price'].values <
                                  avg_price_reg.loc[to_buy_good['zipcode'], 'price'].values]
    to_buy_good['condition'] = to_buy_good['condition'].apply(lambda x: 'good').astype(str)

    ## --- selecting houses having waterfront view
    to_buy_wat = data[data['waterfront'] > 0]
    to_buy_wat = to_buy_wat.loc[to_buy_wat['price'].values <
                                avg_price_reg.loc[to_buy_wat['zipcode'], 'price'].values]
    to_buy_wat['condition'] = to_buy_wat['condition'].apply(lambda x: 'good' if x >= 4
    else 'ok' if x == 3
    else 'poor')

    ## --- calculating prices
    to_buy = pd.concat([to_buy_good, to_buy_wat]).drop_duplicates('id', keep=False).drop(
        ['view', 'grade', 'lat', 'long'], axis=1)
    to_buy.rename(columns={'price': 'purc_price'}, inplace=True)
    to_buy['sell_price'] = to_buy[['purc_price', 'waterfront']].apply(
        lambda x: x['purc_price'] * 1.3 if x['waterfront'] < 1 else
        x['purc_price'] * 1.5, axis=1)
    to_buy['expend'] = to_buy[['purc_price', 'condition']].apply(
        lambda x: x['purc_price'] * 0.07 if x['condition'] == 'good' else
        x['purc_price'] * 0.12, axis=1)
    to_buy['profit'] = to_buy['sell_price'] - to_buy['expend'] - to_buy['purc_price']

    tot_prof = np.round(to_buy['profit'].sum(), 2)
    tot_exp = to_buy['expend'].sum()
    tot_inv = to_buy['purc_price'].sum()
    perct = np.round((tot_prof / tot_inv) * 100, 2)

    return (to_buy, tot_inv, tot_exp, perct, tot_prof)
