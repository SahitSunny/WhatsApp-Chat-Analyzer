from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # total number of messages in group / person
    num_messgaes = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    # number of words in group / person
    num_words = len(words)

    # total number of media 
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # total number of  URL shared
    urls = []
    extractor = URLExtract()
    for message in df['message']:
        urls.extend(extractor.find_urls(message))
    num_url = len(urls)

    return num_messgaes, num_words, num_media, num_url
   

        
def fetch_most_busy(df):
    x = df['user'].value_counts().head(5)

    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns= {'user' : 'name', 'count' : 'percent'})
    return x, df

def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width= 500, height= 500, min_font_size= 10, background_color= 'white')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep= " "))
    return df_wc

def most_common_words(selected_user, df):

    # removing stopwords it is not english it is hinglish
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_words_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    df['only_date'] = df['date'].dt.date
    daily_timeline_df = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline_df

def most_active_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    most_active_day_df = df['day_name'].value_counts()
    return most_active_day_df

def most_active_month(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    most_active_month_df = df['month'].value_counts()
    return most_active_month_df


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    activity_heatmap_df = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_heatmap_df