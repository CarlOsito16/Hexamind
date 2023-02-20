import streamlit as st
import plotly.express as px
import pandas as pd



st.set_page_config(
    page_title = 'Streamlit Sample Dashboard Template',
    page_icon = '✅',
    layout = 'wide'
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


s = {'a': "rgb(235, 69, 95)", 
     'b': "rgb(255, 184, 76)",
     'c':'rgb(43, 52, 103)'}

color_map = {'positive' : "royalblue",
                      'neutral': 'gold',
                      'negative': 'tomato'}


df = pd.read_csv('20230220_selected_df.csv',
                 index_col=0)

st.write("""
         # Distribution of topics discussed from *Trustadvisor.com* on **Carrefour**
         """)

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

pie_fig.update_layout(legend=dict(
    orientation="h",
    yanchor="middle",
    y= 1.15,
    xanchor="center",
    x= 0.5
))


bar_fig = px.histogram(data_frame=group_df,
             x = 'topic_count',
             color= 'sentiment',
             color_discrete_map = color_map,
             text_auto =True,
             category_orders = {"sentiment": ['positive' ,'negative' 'neutral']})
            #  color_discrete_sequence = bar_new_color_discrete_sequence,
            

heatmap_fig = px.imshow(heamap_data,
                        labels=dict(x="4 Super Classes", y="Sentiment"),
                        x=['Buying Experience', 'Product', 'Delivery', 'After Sales'],
                        y=['Negative', 'Neutral', 'Positive'],
                        color_continuous_scale=['royalblue', 'gold', 'tomato'],
                        text_auto=True)



class_1_fig = px.pie(data_frame= group_df[group_df['clean_BE'] == 1],
       names = group_df[group_df['clean_BE'] == 1].sentiment,
       color = 'sentiment',
       color_discrete_map = color_map,
       category_orders = {"sentiment": ['positive' ,'negative' 'neutral']},
       hole= 0.5)

class_2_fig = px.pie(data_frame= group_df[group_df['clean_PD'] == 1],
       names = group_df[group_df['clean_PD'] == 1].sentiment,
       color = 'sentiment',
       color_discrete_map = color_map,
       category_orders = {"sentiment": ['positive' ,'negative' 'neutral']},
       hole= 0.5)

class_3_fig = px.pie(data_frame= group_df[group_df['clean_DM'] == 1],
       names = group_df[group_df['clean_DM'] == 1].sentiment,
       color = 'sentiment',
       color_discrete_map = color_map,
       category_orders = {"sentiment": ['positive' ,'negative' 'neutral']},
       hole= 0.5)

class_4_fig = px.pie(data_frame= group_df[group_df['clean_AS'] == 1],
       names = group_df[group_df['clean_AS'] == 1].sentiment,
       color = 'sentiment',
       color_discrete_map = color_map,
       category_orders = {"sentiment": ['positive' ,'negative' 'neutral']},
       hole= 0.5)




kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown("**All reviewsf**")
    st.plotly_chart(pie_fig, use_container_width=True)


with kpi2:
    
    with st.expander("Sentiment Count"):
        st.dataframe(data=group_df['sentiment'].value_counts().rename_axis('unique_values').reset_index(name='counts'),
             use_container_width=True)
    st.plotly_chart(heatmap_fig, use_container_width=True)
    
with kpi3:
    st.markdown("Looking at the how many topics each review is talking about")
    st.plotly_chart(bar_fig, use_container_width=True)
    

st.markdown("<hr/>",unsafe_allow_html=True)


st.markdown("## Distribution broken down into 4 super classes")

class1, class2, class3, class4 = st.columns(4)

with class1:
    st.markdown("#### Buying Experience")
    st.plotly_chart(class_1_fig, use_container_width=True)

with class2:
    st.markdown("#### Product")
    st.plotly_chart(class_2_fig, use_container_width=True)
    
with class3:
    st.markdown("#### Delivery Mode")
    st.plotly_chart(class_3_fig, use_container_width=True)
    
with class4:
    st.markdown("#### After Sales")
    st.plotly_chart(class_4_fig, use_container_width=True)