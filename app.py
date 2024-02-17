import streamlit as st
import preproccessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # byte_data is a stream we have to convert it into string
    data = bytes_data.decode("utf-8")
    df = preproccessor.preprocessor(data)

    st.dataframe(df)

    # fetching unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("show analysis with respect to", user_list)


    # stats 
    if st.sidebar.button("show analysis"):

        num_messages, num_words, num_media, num_url = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Total Media")
            st.title(num_media)
        
        with col4:
            st.header('Total URL')
            st.title(num_url)

    # timelime
    st.title('Montly Timeline')
    monthly_timeline_df = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()    
    ax.plot(monthly_timeline_df['time'], monthly_timeline_df['message'], color= 'green')
    plt.xticks(rotation= 'vertical')
    st.pyplot(fig)

    st.title('Daily Timeline')
    daily_timeline_df = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline_df['only_date'], daily_timeline_df['message'], color= 'black')
    plt.xticks(rotation= 'vertical')
    st.pyplot(fig)

    # activity map
    st.title('Activity Map')

    col1, col2 = st.columns(2)

    with col1:
        st.header('Most Active Day')
        most_active_day_df = helper.most_active_day(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(most_active_day_df.index, most_active_day_df.values)
        plt.xticks(rotation= 'vertical')
        st.pyplot(fig)

    with col2:
        st.header('Most Active Month')
        most_active_month_df = helper.most_active_month(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(most_active_month_df.index, most_active_month_df.values, color= 'orange')
        plt.xticks(rotation= 'vertical')
        st.pyplot(fig)


    activity_heatmap_df = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(activity_heatmap_df)
    st.pyplot(fig)
    

    # busiest person in group 
    if selected_user == 'Overall':
        st.title('Most Busy Users')
        x, new_df = helper.fetch_most_busy(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color= 'red')
            plt.xticks(rotation= 'vertical')
            st.pyplot(fig)
        
        with col2:
            st.dataframe(new_df)


    # wordcloud
    st.title('WordCloud')
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)


    # most common words
    st.title("most common words")
    most_common_words_df = helper.most_common_words(selected_user, df)
    
    fig, ax = plt.subplots()
    ax.barh(most_common_words_df[0], most_common_words_df[1])
    plt.xticks(rotation= 'vertical')
    st.pyplot(fig)


    # emoji analysis
    st.title("Emoji Analysis")

    col1, col2 = st.columns(2)

    with col1:
        emoji_df = helper.emoji_helper(selected_user, df)
        st.dataframe(emoji_df)

    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels= emoji_df[0].head())    # 
        st.pyplot(fig)
