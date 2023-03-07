#This version contains 2-ring plot compared with competitors

import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
import os

import plotly.graph_objs as go
from pandas.tseries.offsets import DateOffset
from helper_function import chart_df
WORKING_PATH = ""




def compute_score(df, columns=None):
    if columns == None:
        score = df['ratings'].mean()
    else:
        score = df[df[columns] == 1].ratings.mean()
    return round(score, 2)


def get_distribution_list(df, column = None):
    rating_list = []
    if column == None:
        for rating in range(1,6):
            value = df[df['ratings'] == rating]
            rating_list.append(len(value))
    
    else:
        for rating in range(1,6):
            value = df[(df['ratings'] == rating) & (df[column] == 1)]
            rating_list.append(len(value))
    
    return rating_list
        


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

with open("UI-element/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
LOGO_PATH = "UI-element/lLogoIcon2-01.png"
logo = Image.open(LOGO_PATH)


#FRENCH STOP WORDS

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


all_comp_df = pd.read_csv('data/all_comp_df.csv',
                          index_col=0)

inner_df = all_comp_df[all_comp_df['company_name'] == 'carrefour']
inner_df['dates'] = pd.to_datetime(inner_df['dates'])

outer_df = all_comp_df[all_comp_df['company_name'] != 'carrefour']
outer_df['dates'] = pd.to_datetime(outer_df['dates'])


#FILTER
with st.sidebar:
    st.title("Comparison benchmark timeframe")
    time_cutoff = st.slider(
        'Select a benchmark timeframe',
        1, 24, 3)
    st.write('Compared to the', time_cutoff, ' months ago')
    
    st.markdown("---")

    selected_competitors = st.multiselect(
    "Choose companies for benchmarking",
    options= outer_df['company_name'].unique(),
    default= outer_df['company_name'].unique())

outer_df = outer_df[outer_df['company_name'].isin(selected_competitors)]


today = pd.Timestamp.today()
cut_off_3m_date = today - DateOffset(months=time_cutoff)

# Now filter every row of the dataframe tha is before the `cut_off_3m_date`
last_benchmark_df  = inner_df[inner_df['dates'] < cut_off_3m_date.tz_localize('utc')]

 #score for each value
    ## As of now
all_now_score = compute_score(inner_df, None)
be_now_score = compute_score(inner_df, 'clean_BE')
pd_now_score = compute_score(inner_df, 'clean_PD')
dm_now_score = compute_score(inner_df, 'clean_DM')
as_now_score = compute_score(inner_df, 'clean_AS')

## 3 months ago

all_benchmark_score = compute_score(last_benchmark_df, None)
be_benchmark_score = compute_score(last_benchmark_df, 'clean_BE')
pd_benchmark_score = compute_score(last_benchmark_df, 'clean_PD')
dm_benchmark_score = compute_score(last_benchmark_df, 'clean_DM')
as_benchmark_score = compute_score(last_benchmark_df, 'clean_AS')

## score delta
all_delta = round(all_now_score - all_benchmark_score, 2)
be_delta = round(be_now_score - be_benchmark_score , 2)
pd_delta = round(pd_now_score - pd_benchmark_score, 2)
dm_delta = round(dm_now_score - dm_benchmark_score, 2)
as_delta = round(as_now_score - as_benchmark_score, 2)


#CHART
color_palette = ['tomato', 'lightsalmon', 'gold', 'skyblue', 'dodgerblue']

all_class = [go.Pie(values=get_distribution_list(inner_df, None),
       labels = ['⭐', '⭐⭐','⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
       hole=0.2,
       sort=False,
       domain={'x':[0.2, 0.8], 'y':[0.1,0.9]},
       hovertemplate="<br><b>Carrefour</b><br>rating: %{label}<br>number of reviews:%{value}<br>"),
       go.Pie(values=get_distribution_list(outer_df, None),
       labels = ['⭐', '⭐⭐','⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
       hole=0.7,
       sort=False,
       domain={'x':[0.05,0.95], 'y':[0,1]},
       hovertemplate="<br><b>Competitors</b><br>rating: %{label}<br>number of reviews:%{value}<br>")
]


all_class_fig = go.Figure(data=all_class).update_traces(marker=dict(colors=color_palette),
                                        textposition ='inside').update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))


BE_class = [go.Pie(values=get_distribution_list(inner_df, 'clean_BE'),
       labels = ['⭐', '⭐⭐','⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
       hole=0.2,
       sort=False,
       domain={'x':[0.2, 0.8], 'y':[0.1,0.9]},
       hovertemplate="<br><b>Carrefour</b><br>rating: %{label}<br>number of reviews:%{value}<br>"),
       go.Pie(values=get_distribution_list(outer_df, 'clean_BE'),
       labels = ['⭐', '⭐⭐','⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
       hole=0.7,
       sort=False,
       domain={'x':[0.05,0.95], 'y':[0,1]},
       hovertemplate="<br><b>Competitors</b><br>rating: %{label}<br>number of reviews:%{value}<br>")
]


BE_class_fig = go.Figure(data=BE_class).update_traces(marker=dict(colors=color_palette),
                                        textposition ='inside').update_layout(showlegend=False)

PD_class = [go.Pie(values=get_distribution_list(inner_df, 'clean_PD'),
       labels = ['⭐', '⭐⭐','⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
       hole=0.2,
       sort=False,
       domain={'x':[0.2, 0.8], 'y':[0.1,0.9]},
       hovertemplate="<br><b>Carrefour</b><br>rating: %{label}<br>number of reviews:%{value}<br>"),
       go.Pie(values=get_distribution_list(outer_df, 'clean_PD'),
       labels = ['⭐', '⭐⭐','⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
       hole=0.7,
       sort=False,
       domain={'x':[0.05,0.95], 'y':[0,1]},
       hovertemplate="<br><b>Competitors</b><br>rating: %{label}<br>number of reviews:%{value}<br>")
]


PD_class_fig = go.Figure(data=PD_class).update_traces(marker=dict(colors=color_palette),
                                        textposition ='inside').update_layout(showlegend=False)


DM_class = [go.Pie(values=get_distribution_list(inner_df, 'clean_DM'),
       labels = ['⭐', '⭐⭐','⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
       hole=0.2,
       sort=False,
       domain={'x':[0.2, 0.8], 'y':[0.1,0.9]},
       hovertemplate="<br><b>Carrefour</b><br>rating: %{label}<br>number of reviews:%{value}<br>"),
       go.Pie(values=get_distribution_list(outer_df, 'clean_DM'),
       labels = ['⭐', '⭐⭐','⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
       hole=0.7,
       sort=False,
       domain={'x':[0.05,0.95], 'y':[0,1]},
       hovertemplate="<br><b>Competitors</b><br>rating: %{label}<br>number of reviews:%{value}<br>")
]


DM_class_fig = go.Figure(data=DM_class).update_traces(marker=dict(colors=color_palette),
                                        textposition ='inside').update_layout(showlegend=False)



AS_class = [go.Pie(values=get_distribution_list(inner_df, 'clean_AS'),
       labels = ['⭐', '⭐⭐','⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
       hole=0.2,
       sort=False,
       domain={'x':[0.2, 0.8], 'y':[0.1,0.9]},
       hovertemplate="<br><b>Carrefour</b><br>rating: %{label}<br>number of reviews:%{value}<br>"),
       go.Pie(values=get_distribution_list(outer_df, 'clean_AS'),
       labels = ['⭐', '⭐⭐','⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'],
       hole=0.7,
       sort=False,
       domain={'x':[0.05,0.95], 'y':[0,1]},
       hovertemplate="<br><b>Competitors</b><br>rating: %{label}<br>number of reviews:%{value}<br>")
]


AS_class_fig = go.Figure(data=AS_class).update_traces(marker=dict(colors=color_palette),
                                        textposition ='inside').update_layout(showlegend=False)
























# st.write(inner_df.shape, outer_df.shape)


st.write("""
        # Distribution of ratings toward 4 major topics from reviews on **Carrefour**
        """)
st.write(f"##### We have gather the total ouf {len(inner_df):,} reviews from Trustpilot webiste. The purpose is to see the how customers their shopping experience through major 4 topics within customer journeys.")

# print(os.getcwd())
# st.markdown(os.getcwd())

row1_col1, row1_col2 = st.columns([1.3,4])


with row1_col1:
    st.subheader("All reviews ratings")

with row1_col2:
    st.subheader("Now let's loook at the distribution broken down into 4 superclasses")
    
    
row2_col1, row2_col2, row2_col3, row2_col4, row2_col5 = st.columns([1.3, 1 ,1 ,1 ,1])

with row2_col1:
    st.metric(label = 'Overall Ratings', value = all_now_score, delta = f"{all_delta} from {time_cutoff} months ago")
    st.plotly_chart(all_class_fig, use_container_width=True)
with row2_col2:
    st.metric(label = '🛒 Buying Experience', value = be_now_score, delta = f"{be_delta} from {time_cutoff} months ago")
    st.plotly_chart(BE_class_fig, use_container_width=True)
with row2_col3:
    st.metric(label = '🥦 Product', value = pd_now_score, delta = f"{pd_delta} from {time_cutoff} months ago")
    st.plotly_chart(PD_class_fig, use_container_width=True)
with row2_col4:
    st.metric(label = '🚚 Delivery', value = dm_now_score, delta = f"{dm_delta} from {time_cutoff} months ago")
    st.plotly_chart(DM_class_fig, use_container_width=True)
with row2_col5:
    st.metric(label = '📞 After Sales', value = as_now_score, delta = f"{as_delta} from {time_cutoff} months ago")
    st.plotly_chart(AS_class_fig, use_container_width=True)





with st.expander("See most frequent words in each category"):
    expander_col1, expander_col2 = st.columns([2,2])
    with expander_col1:
        BE_text = inner_df[inner_df['clean_BE']==1].combined_reviews.to_string(header=False, index=False)
        DM_text = inner_df[inner_df['clean_DM']==1].combined_reviews.to_string(header=False, index=False)
        
        
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
            contour_color='white',
            height=250,
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
        PD_text = inner_df[inner_df['clean_PD']==1].combined_reviews.to_string(header=False, index=False)
        AS_text = inner_df[inner_df['clean_AS']==1].combined_reviews.to_string(header=False, index=False)
        
        
        wc3 = WordCloud(background_color='white',
            collocations=False,
            contour_width=1,
            contour_color='white',
            height=250,
            max_words=50,
            max_font_size= 100,
            stopwords=french_stopwords_list,
            prefer_horizontal=1)
        wc4 = WordCloud(background_color='white',
            collocations=False,
            contour_width=1,
            contour_color='white',
            height=250  ,
            max_words=50,
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
    st.image(logo, width = 50)
        

