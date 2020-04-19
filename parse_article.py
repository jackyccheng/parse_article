import bs4, requests
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
    parsed = bs4.BeautifulSoup(link.text, "html.parser")

    # Splits out lines by html paragraph, then into a list
    paragraph = ['p']
    txt = [t for t in parsed.find_all(text=True) if t.parent.name in paragraph]
    characters = list("".join(txt))

    # Removes digits from list
    char_x_int = [x for x in characters if not (x.isdigit())]

    # Turns list into dataframe for easier manipulation
    df = pd.DataFrame(char_x_int)
    df.rename(columns = {df.columns[0]:'char'}, inplace=True)

    # Manipulates to exclude certain characters and return top 20 by frequency
    final_df = df[(df.char != '。') & (df.char != '，') & (df.char != ' ')
              & (df.char != '.') & (df.char != '"') & (df.char != '、')
              & (df.char != '”') & (df.char != ',')]

    top_df = final_df['char'].value_counts().head(20)

    print(top_df)

if __name__ == '__main__':

    get_article(link=options.link)
