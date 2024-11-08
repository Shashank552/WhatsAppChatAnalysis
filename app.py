import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title(selected_user + " Chat Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text("Total Messages")
            st.subheader(num_messages)
        with col2:
            st.text("Total Words")
            st.subheader(words)
        with col3:
            st.text("Total Media Shared")
            st.subheader(num_media_messages)
        with col4:
            st.text("Total Links Shared")
            st.subheader(num_links)

        # monthly timeline
        st.header("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'], color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)
        
        # daily timeline
        st.header("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['only_date'], daily_timeline['message'], color="black")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.subheader("Most busy month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="red")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        st.header("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)




        #finding active users 
        if selected_user == "Overall":
            st.title("Most active users")
            x, new_df = helper.most_busy_users(df)

            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                fig, ax = plt.subplots()
                ax.pie(x.values, labels=x.index, autopct='%1.1f%%')
                st.pyplot(fig)
                #st.dataframe(new_df)
        
        # word cloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title("Most Common Words")
        st.pyplot(fig)


        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        fig, ax = plt.subplots()
        ax.bar(emoji_df[0].head(), emoji_df[1].head())
        st.pyplot(fig)