import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import PyPDF2
import requests
from bs4 import BeautifulSoup
import io
import nltk

nltk.download('stopwords')
stop = nltk.corpus.stopwords.words('portuguese')

st.title('Análise Estatística de Texto')

option = st.selectbox('Como você deseja inserir o texto?', ('Digite o texto', 'Upload de PDF', 'Link da página web'))

text = ''
if option == 'Digite o texto':
    text = st.text_area('Digite seu texto aqui:')
elif option == 'Upload de PDF':
    pdf_file = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])
    if pdf_file is not None:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''.join(page.extract_text() for page in reader.pages)
elif option == 'Link da página web':
    page_url = st.text_input('Digite o URL da página:')
    if page_url:
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.get_text()

if text:
    # Remoção de caracteres indesejados e tokenização
    words = [word.lower() for word in text.split() if word.lower() not in stop]
    count = Counter(words)
    most_common_words = count.most_common(20)

    # Exibição das palavras mais comuns
    st.subheader('20 palavras mais frequentes')
    df = pd.DataFrame(most_common_words, columns=['Palavra', 'Frequência'])

    st.write(df)

    # Geração da nuvem de palavras
    wordcloud = WordCloud(width = 800, height = 400, background_color ='white').generate_from_frequencies(dict(count))
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
