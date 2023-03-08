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
# from helper_function import chart_df
WORKING_PATH = ""




def compute_score(df, columns=None):
    if columns == None:
        score = df['ratings'].mean()
    else:
        score = df[df[columns] == 1].ratings.mean()
    return round(score, 1)

def dot_to_comma(number):
    comma_num = str(number).replace('.', ',')
    return comma_num


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


# st.markdown(
#     """
# <style>
# [data-testid="stMetricValue"] {
#     font-size: 50px;
# }

# [data-testid="stImage"] {}
# </style>,

# """,
#     unsafe_allow_html=True,
# )

some_css = """

<style>
[data-testid="stMetricValue"] {
    font-size: 50px;
}

.small-font {
    font-size:10px ;
    color: white;
}

.side-bar-font {
    color:white;
}

[data-testid="stAppViewContainer"] {
    color: 'white';
}

</style>
"""


st.markdown(some_css, unsafe_allow_html=True)






with open("UI-element/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
LOGO_PATH = "UI-element/lLogoIcon2-01.png"
logo = Image.open(LOGO_PATH)

WHITE_LOGO_PATH = "UI-element/OriginalLogoIconWhite-01.png"
white_logo = Image.open(WHITE_LOGO_PATH)


# def img_to_bytes(img_path):
#     img_bytes = Path(img_path).read_bytes()
#     encoded_img = base64.b64encode(img_bytes).decode()
#     return encoded_img

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
    a, b, c  = st.columns([1,2, 0.2])
    with a:
        # link = 'http://www.hexamind.ai/'
        # image_base64 = "https://img2.freepng.fr/20181227/jy/kisspng-agumon-tai-kamiya-portable-network-graphics-drawin-agumon-png-6-ampquot-png-image-5c2504863e8812.0474668915459298622561.jpg"
        # html = f"<a href='{link}'><img src='data:image/png;base64,{image_base64}'></a>" 
        # st.markdown(html, unsafe_allow_html=True)
        
        
        html = """
        <a href='http://www.hexamind.ai/'> 
        <img src='https://uploads-ssl.webflow.com/63f612a19c5c59312c05d479/63f61d38d0d2e50f9c9d49f7_OriginalLogoIconWhite-01-p-500.png'
        width="75"> 
        </a> 
        """
        st.markdown(html, unsafe_allow_html=True)
        # st.image(white_logo, width=75)
        
        
        
        
        # st.markdown("""
        # <a href='http://www.hexamind.ai/'>
        # <img src = WHITE_LOGO_PATH>
        # </a>
        # """)
        
        # st.markdown("[![Foo](LOGO_PATH)](http://google.com.au/)")
        
    with b:
        st.write("<h1 class='side-bar-font'>HEXAMIND</p>",
             unsafe_allow_html=True)
        
    st.write(""" """)
    st.write("<p class='side-bar-font'>Veuillez choisir des entreprises pour l'analyse comparative</p>",
             unsafe_allow_html=True)
    selected_competitors = st.multiselect(
        label="",
    options= outer_df['company_name'].unique(),
    default= outer_df['company_name'].unique())
    
    
    
    st.markdown("   ---")
    
    
    about_hexamind_1 = """
    Hexamind une société formée autour de passionnés d’IA, docteurs pour certains, passés par des universités américaines (Yale, Stanford) et par de grandes ESN généralistes (Cap, SopraSteria, Accenture) ou plus focalisées (Niji). Nous nous sommes spécialisés sur les algorithmes de traitement du langage  appliqués à la relation client : analyse des mails, chatbot, speech-to-text, etc.
    """
    
    about_hexamind_2 = """Hexamind intervient en conseil pour l’identification des opportunités, en produisant des maquettes sur des cycles courts et en développant des solutions adaptées à votre contexte. L'objectif est de ne mobiliser que très peu vos équipes techniques (pour extraire les données) et de permettre de se focaliser sur la valeur métier tout en se projetant sur de vraies solutions techniques
    """
    
    st.write("<h3 class='side-bar-font'>HEXAMIND</p>",
             unsafe_allow_html=True)
    st.write(f"<p class='small-font'>{about_hexamind_1}</p>",
             unsafe_allow_html=True)
    
    st.write(f"<p class='small-font'>{about_hexamind_2}</p>",
             unsafe_allow_html=True)
    # st.title("Comparison benchmark timeframe")
    # time_cutoff = st.slider(
    #     'Select a benchmark timeframe',
    #     1, 24, 3)
    # st.write('Compared to the', time_cutoff, ' months ago')
    
    st.markdown("---")


outer_df = outer_df[outer_df['company_name'].isin(selected_competitors)]


today = pd.Timestamp.today()
cut_off_3m_date = today - DateOffset(months=3)

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
as_delta = round(as_now_score - as_benchmark_score, 2  )


#CHART
# color_palette = ['tomato', 'lightsalmon', 'gold', 'skyblue', 'dodgerblue']
color_palette = ['lightskyblue', 'deepskyblue', 'dodgerblue', 'royablue', 'midnightblue']


# midnightblue
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
         ### Tableau de bord du parcours client de Carrefour issu des revues Trustpilot
         """)

st.write("""
         Trustpilot permet aux utilisateurs de poster des revues sur leurs fournisseurs et de donner une note de satisfaction **de 1 à 5**. Le nombre de revues est souvent supérieur à plusieurs milliers. Il est donc long et fastidieux, en dehors d’une moyenne globalisée, d’obtenir une vision agrégée qui permette de tirer des enseignements pour les fournisseurs. 
         """)

st.write("Ce tableau de bord est issu d’une analyse par IA des revues et permet de les ventiler en fonction de la phase de l’expérience client : achat, livraison, utilisation du produit ou du service, après-vente. L’analyse est effectuée sur plusieurs enseignes d’un même secteur afin de permettre une comparaison avec la concurrence. ")

# st.write("""
#         # Distribution of ratings toward 4 major topics from reviews on **Carrefour**
#         """)
# st.write(f"##### We have gather the total ouf {len(inner_df):,} reviews from Trustpilot webiste. The purpose is to see the how customers perceive their shopping experience through major 4 topics within customer journeys.")

# print(os.getcwd())
# st.markdown(os.getcwd())

# row1_col1, row1_col2 = st.columns([1.3,4])


# with row1_col1:
#     st.subheader("All reviews ratings")

# with row1_col2:
#     st.subheader("Now let's loook at the distribution broken down into 4 superclasses")
    
    
row2_col1, row2_col2, row2_col3, row2_col4, row2_col5 = st.columns([1.3, 1 ,1 ,1 ,1])

with row2_col1:
    st.metric(label = 'Notes globales', value = dot_to_comma(all_now_score), delta = f"{dot_to_comma(all_delta)} des 3 derniers mois")
    st.plotly_chart(all_class_fig, use_container_width=True)
with row2_col2:
    st.metric(label = "🛒 Expérience d'achat", value = dot_to_comma(be_now_score), delta = f"{dot_to_comma(be_delta)} des 3 derniers mois")
    st.plotly_chart(BE_class_fig, use_container_width=True)
with row2_col4:
    st.metric(label = '🥦 Produit', value = dot_to_comma(pd_now_score), delta = f"{dot_to_comma(pd_delta)} des 3 derniers mois")
    st.plotly_chart(PD_class_fig, use_container_width=True)
with row2_col3:
    st.metric(label = '🚚 Livraison', value = dot_to_comma(dm_now_score), delta = f"{dot_to_comma(dm_delta)} des 3 derniers mois")
    st.plotly_chart(DM_class_fig, use_container_width=True)
with row2_col5:
    st.metric(label = '📞 Après-vente ', value = dot_to_comma(as_now_score), delta = f"{dot_to_comma(as_delta)} des 3 derniers mois")
    st.plotly_chart(AS_class_fig, use_container_width=True)



st.write("""
         ##### Hexamind : l’IA pour la relation client
         """)
st.write("Les graphiques ci-dessus contiennent 2 anneaux, **l'anneau intérieur** représentant Carrefour et **l'anneau extérieur** les concurrents sélectionnés")

st.write("""
         Cette démonstration vise à illustrer une capacité d’analyse du traitement du langage.  Elle est réalisée par Hexamind qui s’appuient sur des technologies opensource de type chat GPT disponibles sur Hugging Face. Les modèles utilisés ont été entraînés par Hexamind sur un corpus en français et les revues de Trustpilot.
         """)



with st.expander("Voir les mots les plus fréquents dans chaque catégorie"):
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
        axes[0].set_title("Nuage de mots pour l'expérience d'achat")
        axes[0].axis('off')
        
        
        axes[1].imshow(DM_wc, interpolation='bilinear')
        axes[1].set_title("Nuage de mots pour livraison")
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
        axes_[0].set_title("Nuage de mots pour produit")
        axes_[0].axis('off')
        
        
        axes_[1].imshow(AS_wc, interpolation='bilinear')
        axes_[1].set_title("Nuage de mots pour après-vente ")
        axes_[1].axis('off')
        st.pyplot(fig_)

# last_row_col1, last_row_col2 = st.columns([22,1])

# with last_row_col2:
#     st.image(logo, width = 50)
        

