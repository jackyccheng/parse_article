from bs4 import BeautifulSoup
import requests
import pandas as pd
import argparse

# Setting my arguments to pass through
parser = argparse.ArgumentParser()
parser.add_argument(
    '-l', '--link',
    help = 'required switch, input news article link'
    )

options = parser.parse_args()

def get_article(link):
    """
    Passed url of news article
    Outputs characters in article by frequency
    """
    # Parses url link to get output of html content
    link = requests.get(link)
    link.raise_for_status()
    link.encoding = 'utf-8'
    parsed = BeautifulSoup(link.text, "html.parser")

    # Splits out lines by html paragraph, then into a list
    paragraph = ['p']
    txt = [t for t in parsed.find_all(text=True) if t.parent.name in paragraph]
    everything = list("".join(txt))

    # Removing some things from full list
    removewords = ['。', '，', ' ', '.', '"', '、', '”', ',', '%', '“']
    resultwords = [t for t in everything if t not in removewords]
    char_et_al = ' '.join(resultwords)

    # Removes digits from list
    characters = [x for x in char_et_al if not (x.isdigit())]

    # Turns list into dataframe for easier manipulation
    df = pd.DataFrame(characters)
    df.rename(columns = {df.columns[0]:'char'}, inplace=True)

    top_df = df['char'].value_counts().head(100)
    print(top_df)

if __name__ == '__main__':
    get_article(link=options.link)
