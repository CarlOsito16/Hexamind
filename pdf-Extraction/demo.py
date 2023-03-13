import streamlit as st
import pdfquery
import re
import pyperclip
import pandas as pd

# Set page layout
st.set_page_config(page_title="PDF Text Extractor", page_icon=":books:")


# pdf = pdfquery.PDFQuery('attestation.pdf')
# pdf.load()

def clean_text_data(text):
    return text.split(': ')[1]


def clean_year(text):
    output = re.compile("scolaire (.*),").search(text).group(1)
    return output


def use_pdfquery(pdf_file):
    pdf = pdfquery.PDFQuery(pdf_file)
    pdf.load()
    lastname = pdf.pq('LTTextLineHorizontal:contains("Nom")').text()
    name = pdf.pq('LTTextLineHorizontal:contains("Prénom")').text()
    id  = pdf.pq('LTTextLineHorizontal:contains("id")').text()
    school  = pdf.pq('LTTextLineHorizontal:contains("tudiant")').text()
    address  = " ".join(pdf.pq('LTTextLineHorizontal:contains("pourra")').text().split(", ")[1:])
    year = pdf.pq('LTTextLineHorizontal:contains("l’année scolaire")').text()
    certify_date = pdf.pq('LTTextLineHorizontal:in_bbox("33.431, 390.629, 138.602, 401.629")').text()[-10:]
    
    return {'lastname': clean_text_data(lastname),
            'name': clean_text_data(name),
            "id": clean_text_data(id),
            'school': clean_text_data(school),
            'address' : address,
            'academic_year': clean_year(year),
            'certify_date': certify_date}


st.write("## Extract the MAISEL Agreement form")  
with st.expander('MAISEL agreement form example'):
    st.image("maisel_example.png")    
uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file is not None:
    st.write(f'A file has been uploaded')
    result = use_pdfquery(uploaded_file)
    st.json(result)
    dict_button = st.button("Copy JSON to clipboard")
    
    st.markdown("---")
    
    df = pd.DataFrame(result, index=[0])
    st.table(df)
    df_button = st.button("Copy Table to clipoboard")
    
    
    if dict_button:
        pyperclip.copy(str(result)) #must transform dictionary to string for pyperclip to work
        st.success("Json copied to clipboard!") 
        
    elif df_button:
        df.to_clipboard(index=False)
        st.success('DataFrame copied to clipboard!')
        
else:
    st.write("No file uploaded")
    
print(type(uploaded_file))