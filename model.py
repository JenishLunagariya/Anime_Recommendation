import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import warnings
warnings.filterwarnings("ignore")

# read data
anime_df = pd.read_csv("./data/anime.csv")
# cleaning text
def text_cleaning(text):
    text = re.sub(r'&quot;','',text)
    text = re.sub(r'hack//','',text)
    text = re.sub(r'&#039','',text)
    text = re.sub(r'A&#039;s','',text)
    text = re.sub(r'I&#039','',text)
    text = re.sub(r'&amp;','',text)
    return text

anime_df['name'] = anime_df['name'].apply(text_cleaning)

# model
tfv = TfidfVectorizer(min_df=3,max_features=None,
    strip_accents='unicode',analyzer='word',
    token_pattern=r'\w{1,}', ngram_range=(1,3), stop_words='english')
anime_df['genre'] = anime_df['genre'].fillna('')
genres_str = anime_df['genre'].str.split(',').astype(str)
tfv_matrix = tfv.fit_transform(genres_str)

# sigmoid kernel
sig = sigmoid_kernel(tfv_matrix,tfv_matrix)
indices = pd.Series(anime_df.index, index = anime_df['name']).drop_duplicates()

# recommadation function
def give_rec(title, sig=sig):
    try:
        idx = indices[title]

        # get pairwise similarity score
        sig_scores = list(enumerate(sig[idx]))
        # sort the shows
        sig_scores = sorted(sig_scores, key=lambda x:x[1], reverse=True)
        # top 10 from sig_scores
        sig_scores = sig_scores[1:11]
        # show indices
        anime_indices = [i[0] for i in sig_scores]
        # return top 10 similar shows
        return pd.DataFrame({'Anime name':anime_df['name'].iloc[anime_indices].values, 'Rating':anime_df['rating'].iloc[anime_indices].values})
    except KeyError:
        return "Please Enter Appropriate Anime Name"
