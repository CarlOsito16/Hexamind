#This version uses 5 stars instead of the sentiment cluster

import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image



st.set_page_config(
    page_title = 'Streamlit Sample Dashboard Template',
    page_icon = '✅',
    layout = 'wide'
)


with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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



def rating_to_sentiment(rating: float):
    if rating >= 4:
        sentiment = 'positive'
    elif rating == 3:
        sentiment = 'neutral'
    elif rating <= 2:
        sentiment = 'negative'
    
    return sentiment


# Now we would display score as a number of stars instead of the sentiment
def rating_to_star(rating: int):
    star = "⭐" * rating
    
    return star


color_map = {'⭐⭐⭐⭐⭐' : "dodgerblue",
             '⭐⭐⭐⭐': "skyblue",
             '⭐⭐⭐': "gold",
             '⭐⭐': "lightsalmon",
             '⭐': "tomato"}



LOGO_PATH = "lLogoIcon2-01.png"
logo = Image.open(LOGO_PATH)
df = pd.read_csv('20230220_selected_df.csv',
                 index_col=0)




#Define some data querying and aggregation
clean_superclass = ['clean_BE', 'clean_PD', 'clean_DM', 'clean_AS']
group_df  = df.loc[: , ['ratings', 'dates'] + clean_superclass ] #  we need to have 'dates' for further timedifference
group_df['sentiment'] = group_df['ratings'].apply(lambda x: rating_to_sentiment(x))
group_df['stars'] = group_df['ratings'].apply(lambda x: rating_to_star(int(x)))
group_df['topic_count'] = group_df.iloc[ :, 1:5].sum(axis= 1)
heamap_data = group_df.groupby('stars').sum().reset_index().iloc[: , 2:6].to_numpy()


# Transform the columns 'dates' to datetime format so as to use the .last method
group_df['dates'] = pd.to_datetime(group_df['dates'])
last_3m_df  = group_df.sort_values(by="dates",ascending=True).set_index("dates").last("3M")


category_orders_stars = {"stars": ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐",  "⭐⭐" ,"⭐" ]}

pie_fig = px.pie(data_frame= group_df,
       names = group_df.stars,
       color= "stars",
       color_discrete_map = color_map,
       category_orders = category_orders_stars,
       hole= 0.5)

# pie_fig.update_layout(legend=dict(
#     orientation="h",
#     yanchor="middle",
#     y= 1.15,
#     xanchor="center",
#     x= 0.5) ,
#                       autosize=True,
#                       width=500,
#                       height=500,)

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
                     category_orders = dict(stars=["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐",  "⭐⭐" ,"⭐" ]),
                    #  labels = ['1', '2', '3', '4', '5'],
                     color_discrete_map = color_map,
                     hole= 0.5)
class_1_fig.update_layout(showlegend=False,
                          width=350,
                          height=450)

class_2_fig = px.pie(data_frame= group_df[group_df['clean_PD'] == 1],
                     names = group_df[group_df['clean_PD'] == 1].stars,
                     color = "stars",
                     color_discrete_map = color_map,
                     category_orders = dict(stars=["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐",  "⭐⭐" ,"⭐" ]),
                     hole= 0.5)
class_2_fig.update_layout(showlegend=False,
                          width=350,
                          height=450)

class_3_fig = px.pie(data_frame= group_df[group_df['clean_DM'] == 1],
       names = group_df[group_df['clean_DM'] == 1].stars,
       color = 'stars',
       color_discrete_map = color_map,
       category_orders = dict(stars=["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐",  "⭐⭐" ,"⭐" ]),
       hole= 0.5)
class_3_fig.update_layout(showlegend=False,
                          width=350,
                          height=450)

class_4_fig = px.pie(data_frame= group_df[group_df['clean_AS'] == 1],
       names = group_df[group_df['clean_AS'] == 1].stars,
       color = 'stars',
       color_discrete_map = color_map,
       category_orders = dict(stars=["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐",  "⭐⭐" ,"⭐" ]),
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


st.write("""
         # Distribution of sentiments toward 4 major topics from reviews on **Carrefour**
         """)
st.write(f"##### We have gather the total ouf {len(group_df):,} reviews from Trustpilot webiste. The purpose is to see the how customers perceive through major 4 topics within customer journeys.")
st.markdown("---")


row1_col1, row1_col2 = st.columns([1.5,4])

with row1_col1:
    st.subheader("All reviews ratings")

with row1_col2:
    st.subheader("Now let's loook at the distribution broken down into 4 superclasses")



row2_col1, row2_col2, row2_col3, row2_col4, row2_col5 = st.columns([1.5, 1 ,1 ,1 ,1])

with row2_col1:
    st.metric(label = 'Overall Ratings', value = all_now_score, delta = f"{all_delta} from 3 months ago")
    st.plotly_chart(pie_fig, use_container_width=True)
with row2_col2:
    st.metric(label = '🛒 Buying Experience', value = be_now_score, delta = f"{be_delta} from 3 months ago")
    st.plotly_chart(class_1_fig, use_container_width=True)
with row2_col3:
    st.metric(label = '🥦 Product', value = pd_now_score, delta = f"{pd_delta} from 3 months ago")
    st.plotly_chart(class_2_fig, use_container_width=True)
with row2_col4:
    st.metric(label = '🚚 Delivery', value = dm_now_score, delta = f"{dm_delta} from 3 months ago")
    st.plotly_chart(class_3_fig, use_container_width=True)
with row2_col5:
    st.metric(label = '📞 After Sales', value = as_now_score, delta = f"{as_delta} from 3 months ago")
    st.plotly_chart(class_4_fig, use_container_width=True)





text = f"""
Looing at the {len(group_df)} reviews, `After Sales` is the category wiht the largest negative proportion, suggesting Carerfour to put priority into this service.
As for the positive proportion, the leading topic goes to `Product`, accounting for 33% compared to 28% from the average all reviews.
"""

st.text_area(label = 'Analysis',
             value = text )




last_row_col1, last_row_col2 = st.columns([25,1])

with last_row_col2:
    st.image(logo, width = 50)
