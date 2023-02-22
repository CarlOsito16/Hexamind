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


pie_new_color_discrete_sequence = [ 'royalblue', 'tomato', 'gold']
bar_new_color_discrete_sequence = [ ' royalblue', 'royalblue', 'tomato', 'gold']


def rating_to_sentiment(rating: float):
    if rating >= 4:
        sentiment = 'positive'
    elif rating == 3:
        sentiment = 'neutral'
    elif rating <= 2:
        sentiment = 'negative'
    
    return sentiment

# Define some color map to match the sentiment label
color_map = {'positive' : "royalblue",
                      'neutral': 'gold',
                      'negative': 'tomato'}



LOGO_PATH = "lLogoIcon2-01.png"
logo = Image.open(LOGO_PATH)
df = pd.read_csv('20230220_selected_df.csv',
                 index_col=0)




#Define some data querying and aggregation
clean_superclass = ['clean_BE', 'clean_PD', 'clean_DM', 'clean_AS']
group_df  = df.loc[: , ['ratings'] + clean_superclass ]
group_df['sentiment'] = group_df['ratings'].apply(lambda x: rating_to_sentiment(x))
group_df['topic_count'] = group_df.iloc[ :, 1:5].sum(axis= 1)
heamap_data = group_df.groupby('sentiment').sum().reset_index().iloc[: , 2:6].to_numpy()




pie_fig = px.pie(data_frame= group_df,
       names = group_df.sentiment,
       color= 'sentiment',
       color_discrete_map = color_map,
       category_orders = {"sentiment": ['positive' ,'neutral' 'negative']},
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
       names = group_df[group_df['clean_BE'] == 1].sentiment,
       color = 'sentiment',
       color_discrete_map = color_map,
       category_orders = {"sentiment": ['positive' ,'negative' 'neutral']},
       hole= 0.5)
class_1_fig.update_layout(showlegend=False,
                          width=300,
                          height=450)

class_2_fig = px.pie(data_frame= group_df[group_df['clean_PD'] == 1],
       names = group_df[group_df['clean_PD'] == 1].sentiment,
       color = 'sentiment',
       color_discrete_map = color_map,
       category_orders = {"sentiment": ['positive' ,'negative' 'neutral']},
       hole= 0.5)
class_2_fig.update_layout(showlegend=False,
                          width=350,
                          height=450)

class_3_fig = px.pie(data_frame= group_df[group_df['clean_DM'] == 1],
       names = group_df[group_df['clean_DM'] == 1].sentiment,
       color = 'sentiment',
       color_discrete_map = color_map,
       category_orders = {"sentiment": ['positive' ,'negative' 'neutral']},
       hole= 0.5)
class_3_fig.update_layout(showlegend=False,
                          width=350,
                          height=450)

class_4_fig = px.pie(data_frame= group_df[group_df['clean_AS'] == 1],
       names = group_df[group_df['clean_AS'] == 1].sentiment,
       color = 'sentiment',
       color_discrete_map = color_map,
       category_orders = {"sentiment": ['positive' ,'negative' 'neutral']},
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
st.write(f"##### We have gather the total ouf {len(group_df):,} reviews from Trustpilot webiste. The purpose is to see the how customers perceive through major 4 topics within customer journeys.")
st.markdown("---")


row1_col1, row1_col2 = st.columns([1.5,4])

with row1_col1:
    st.subheader("All reviews ratings")

with row1_col2:
    st.subheader("Now let's loook at the distribution broken down into 4 superclasses")



row2_col1, row2_col2, row2_col3, row2_col4, row2_col5 = st.columns([1.5, 1 ,1 ,1 ,1])

with row2_col1:
    st.metric(label = 'Overall Ratings', value = round(group_df['ratings'].mean(), 2))
    st.plotly_chart(pie_fig, use_container_width=True)
with row2_col2:
    st.metric(label = '🛒 Buying Experience', value = round(group_df.query("clean_BE == 1")['ratings'].mean(), 2))
    st.plotly_chart(class_1_fig, use_container_width=True)
with row2_col3:
    st.metric(label = '🥦 Product', value = round(group_df.query("clean_PD == 1")['ratings'].mean(), 2))
    st.plotly_chart(class_2_fig, use_container_width=True)
with row2_col4:
    st.metric(label = '🚚 Delivery', value = round(group_df.query("clean_DM == 1")['ratings'].mean(), 2))
    st.plotly_chart(class_3_fig, use_container_width=True)
with row2_col5:
    st.metric(label = '📞 After Sales', value = round(group_df.query("clean_AS == 1")['ratings'].mean(), 2))
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

# col1, col2 ,col3= st.columns((1.5, 1, 1))


# with col1:
#     st.subheader("**All reviews**")
#     st.metric(label = 'Overall Ratings',
#           value = round(group_df['ratings'].mean(), 2))
#     st.plotly_chart(pie_fig, use_container_width=True)
    
# with col2:
#     st.subheader("Distribution broken down into 4 super classes")
#     st.plotly_chart(class_1_fig, use_container_width=True)
#     st.plotly_chart(class_2_fig, use_container_width=True)
        
# with col3:
#     st.markdown("")
#     st.markdown("")
#     st.markdown("")
#     st.markdown("")
#     st.plotly_chart(class_3_fig, use_container_width=True)
#     st.plotly_chart(class_4_fig, use_container_width=True)
    

# # st.markdown("<hr/>",unsafe_allow_html=True)


# # st.markdown("## Distribution broken down into 4 super classes")

# # class1, class2, class3, class4 = st.columns(4)

# # with class1:
# #     st.markdown("#### Buying Experience")
# #     st.plotly_chart(class_1_fig, use_container_width=True)

# # with class2:
# #     st.markdown("#### Product")
# #     st.plotly_chart(class_2_fig, use_container_width=True)
    
# # with class3:
# #     st.markdown("#### Delivery Mode")
# #     st.plotly_chart(class_3_fig, use_container_width=True)
    
# # with class4:
# #     st.markdown("#### After Sales")
# #     st.plotly_chart(class_4_fig, use_container_width=True)