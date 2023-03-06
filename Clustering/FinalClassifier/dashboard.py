#This version uses 5 stars instead of the sentiment cluster

import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
import os

from pandas.tseries.offsets import DateOffset
WORKING_PATH = ""

print(os.getcwd())

st.set_page_config(
    page_title = 'Streamlit Sample Dashboard Template',
    page_icon = '✅',
    layout = 'wide'
)


st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 50px;
}
</style>
""",
    unsafe_allow_html=True,
)

print(os.getcwd())

with open("UI-element/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
LOGO_PATH = "UI-element/lLogoIcon2-01.png"
logo = Image.open(LOGO_PATH)


with st.sidebar:
    st.title("Comparison benchmark timeframe")
    time_cutoff = st.slider(
        'Select a benchmark timeframe',
        1, 24, 3)
    st.write('Compared to the', time_cutoff, ' months ago')




# opening the file in read mode
my_file = open("french_stopword.txt" , 'r')
  
# reading the file
data = my_file.read()
  
# replacing end of line('/n') with ' ' and
# splitting the text it further when '.' is seen.
french_stopwords_list = data.replace('\n', ' ').split(" ")
  
# # printing the data
print(french_stopwords_list[:5])
french_stopwords_list.extend(['carrefour', 'bonjour', "j'ai"])
my_file.close()

# Now we would display score as a number of stars instead of the sentiment
def rating_to_star(rating: int):
    star = "⭐" * rating
    
    return star

color_map = {'⭐⭐⭐⭐⭐' : "dodgerblue",
             '⭐⭐⭐⭐': "skyblue",
             '⭐⭐⭐': "gold",
             '⭐⭐': "lightsalmon",
             '⭐': "tomato"}


df = pd.read_csv('data/final_carrefour_df_with_label.csv',
                 index_col=0)
all_comp_df = pd.read_csv('data/all_comp_df.csv',
                          index_col=0)
#Define some data querying and aggregation
clean_superclass = ['clean_BE', 'clean_PD', 'clean_DM', 'clean_AS']
group_df  = df.loc[: , ['ratings', 'dates'] + clean_superclass ] #  we need to have 'dates' for further timedifference
group_df['stars'] = group_df['ratings'].apply(lambda x: rating_to_star(int(x)))
group_df['topic_count'] = group_df.iloc[ :, 1:5].sum(axis= 1)

# Transform the columns 'dates' to datetime format so as to use the .last method
group_df['dates'] = pd.to_datetime(group_df['dates'])

# Declare today time and compute time difference set to 3 months ago
today = pd.Timestamp.today()
cut_off_3m_date = today - DateOffset(months=time_cutoff)

# Now filter every row of the dataframe tha is before the `cut_off_3m_date`
last_3m_df  = group_df[group_df['dates'] < cut_off_3m_date.tz_localize('utc')]


#score for each value
## As of now
all_now_score = round(group_df['ratings'].mean(), 2)
be_now_score = round(group_df.query("clean_BE == 1")['ratings'].mean(), 2)
pd_now_score = round(group_df.query("clean_PD == 1")['ratings'].mean(), 2)
dm_now_score = round(group_df.query("clean_DM == 1")['ratings'].mean(), 2)
as_now_score = round(group_df.query("clean_AS == 1")['ratings'].mean(), 2)

## 3 months ago

all_3m_score = round(last_3m_df['ratings'].mean(), 2)
be_3m_score = round(last_3m_df.query("clean_BE == 1")['ratings'].mean(), 2)
pd_3m_score = round(last_3m_df.query("clean_PD == 1")['ratings'].mean(), 2)
dm_3m_score = round(last_3m_df.query("clean_DM == 1")['ratings'].mean(), 2)
as_3m_score = round(last_3m_df.query("clean_AS == 1")['ratings'].mean(), 2)

## score delta
all_delta = round(all_now_score - all_3m_score, 2)
be_delta = round(be_now_score - be_3m_score , 2)
pd_delta = round(pd_now_score - pd_3m_score, 2)
dm_delta = round(dm_now_score - dm_3m_score, 2)
as_delta = round(as_now_score - as_3m_score, 2)


#DASHBOARD ELEMENT




category_orders_stars = {"stars": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐",  "⭐⭐" ,"⭐" ]}

pie_fig = px.pie(data_frame= group_df,
       names = group_df.stars,
       color= "stars",
       color_discrete_map = color_map,
       category_orders = category_orders_stars,
       hole= 0.5)

pie_fig.update_layout(legend=dict(
    orientation="v",
    yanchor="middle",
    y= 0.9,
    xanchor="center",
    x= -0.1) ,
                      autosize=True,
                      width=300,
                      height=450)




class_1_fig = px.pie(data_frame= group_df[group_df['clean_BE'] == 1],
                     names = group_df[group_df['clean_BE'] == 1].stars,
                     color = group_df[group_df['clean_BE'] == 1].stars,
                     category_orders = category_orders_stars,
                     color_discrete_map = color_map,
                     hole= 0.5)
class_1_fig.update_layout(showlegend=False,
                          width=350,
                          height=450)

class_2_fig = px.pie(data_frame= group_df[group_df['clean_PD'] == 1],
                     names = group_df[group_df['clean_PD'] == 1].stars,
                     color = "stars",
                     color_discrete_map = color_map,
                     category_orders = category_orders_stars,
                     hole= 0.5)
class_2_fig.update_layout(showlegend=False,
                          width=350,
                          height=450)

class_3_fig = px.pie(data_frame= group_df[group_df['clean_DM'] == 1],
       names = group_df[group_df['clean_DM'] == 1].stars,
       color = 'stars',
       color_discrete_map = color_map,
       category_orders = category_orders_stars,
       hole= 0.5)
class_3_fig.update_layout(showlegend=False,
                          width=350,
                          height=450)

class_4_fig = px.pie(data_frame= group_df[group_df['clean_AS'] == 1],
       names = group_df[group_df['clean_AS'] == 1].stars,
       color = 'stars',
       color_discrete_map = color_map,
       category_orders = category_orders_stars,
       hole= 0.5)
class_4_fig.update_layout(showlegend=False,
                          width=350,
                          height=450,
                          legend=dict(
                                orientation="h",
                                yanchor="middle",
                                y= 1.15,
                                xanchor="center",
                                x= 0.5
                            ))



st.write("""
         # Distribution of sentiments toward 4 major topics from reviews on **Carrefour**
         """)
st.write(f"##### We have gather the total ouf {len(df):,} reviews from Trustpilot webiste. The purpose is to see the how customers perceive through major 4 topics within customer journeys.")
# print(os.getcwd())
st.markdown(os.getcwd())




row1_col1, row1_col2 = st.columns([1.5,4])

with row1_col1:
    st.subheader("All reviews ratings")

with row1_col2:
    st.subheader("Now let's loook at the distribution broken down into 4 superclasses")



row2_col1, row2_col2, row2_col3, row2_col4, row2_col5 = st.columns([1.5, 1 ,1 ,1 ,1])

with row2_col1:
    st.metric(label = 'Overall Ratings', value = all_now_score, delta = f"{all_delta} from {time_cutoff} months ago")
    st.plotly_chart(pie_fig, use_container_width=True)
with row2_col2:
    st.metric(label = '🛒 Buying Experience', value = be_now_score, delta = f"{be_delta} from {time_cutoff} months ago")
    st.plotly_chart(class_1_fig, use_container_width=True)
with row2_col3:
    st.metric(label = '🥦 Product', value = pd_now_score, delta = f"{pd_delta} from {time_cutoff} months ago")
    st.plotly_chart(class_2_fig, use_container_width=True)
with row2_col4:
    st.metric(label = '🚚 Delivery', value = dm_now_score, delta = f"{dm_delta} from {time_cutoff} months ago")
    st.plotly_chart(class_3_fig, use_container_width=True)
with row2_col5:
    st.metric(label = '📞 After Sales', value = as_now_score, delta = f"{as_delta} from {time_cutoff} months ago")
    st.plotly_chart(class_4_fig, use_container_width=True)





text = f"""
Looing at the {len(group_df)} reviews, `After Sales` is the category wiht the largest negative proportion, suggesting Carerfour to put priority into this service.
As for the positive proportion, the leading topic goes to `Product`, accounting for 11.6% compared to 7.45% from the average all reviews.
"""

st.text_area(label = 'Analysis',
             value = text )


with st.expander("See most frequent words in each category"):
    expander_col1, expander_col2 = st.columns([2,2])
    with expander_col1:
        BE_text = df[df['clean_BE']==1].combined_reviews.to_string(header=False, index=False)
        DM_text = df[df['clean_DM']==1].combined_reviews.to_string(header=False, index=False)
        
        
        wc1 = WordCloud(background_color='white',
               collocations=False,
               contour_width=1,
               contour_color='white',
               height=250,
               max_words=50,
               max_font_size= 100,
               stopwords=french_stopwords_list,
               prefer_horizontal=1)
        wc2 = WordCloud(background_color='white',
               collocations=False,
               contour_width=1,
               height=250,
               contour_color='white',
               max_words=50,
               max_font_size= 100,
               stopwords=french_stopwords_list,
               prefer_horizontal=1)
        
        BE_wc = wc1.generate(BE_text)
        DM_wc = wc2.generate(DM_text)
        
        fig, axes = plt.subplots(2, 1, figsize = (3,5) )
        axes[0].imshow(BE_wc, interpolation='bilinear')
        axes[0].set_title('Word cloud for Buying Experience')
        axes[0].axis('off')
        
        
        axes[1].imshow(DM_wc, interpolation='bilinear')
        axes[1].set_title('Word cloud for Delivery Mode')
        axes[1].axis('off')
        st.pyplot(fig)
       
    with expander_col2:
        PD_text = df[df['clean_PD']==1].combined_reviews.to_string(header=False, index=False)
        AS_text = df[df['clean_AS']==1].combined_reviews.to_string(header=False, index=False)
        
        
        wc3 = WordCloud(background_color='white',
               collocations=False,
               contour_width=1,
               contour_color='white',
               max_words=50,
               height=250,
               max_font_size= 100,
               stopwords=french_stopwords_list,
               prefer_horizontal=1)
        wc4 = WordCloud(background_color='white',
               collocations=False,
               contour_width=1,
               contour_color='white',
               max_words=50,
               height=250,
               max_font_size= 100,
               stopwords=french_stopwords_list,
               prefer_horizontal=1)
        
        PD_wc = wc3.generate(PD_text)
        AS_wc = wc4.generate(AS_text)
        
        fig_, axes_ = plt.subplots(2, 1, figsize = (3,5) )
        axes_[0].imshow(PD_wc, interpolation='bilinear')
        axes_[0].set_title('Word cloud for Product')
        axes_[0].axis('off')
        
        
        axes_[1].imshow(AS_wc, interpolation='bilinear')
        axes_[1].set_title('Word cloud for After Sales')
        axes_[1].axis('off')
        st.pyplot(fig_)

last_row_col1, last_row_col2 = st.columns([22,1])

with last_row_col2:
    st.image(logo, width = 75)
    
# with last_row_col3:
#     st.write("HEXAMIND")