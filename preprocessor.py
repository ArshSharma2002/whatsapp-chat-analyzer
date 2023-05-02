import re

import pandas as pd


def preprocess(data):
    # creating list of whole chat by split it into strings spliting where date & time coming
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    # messages is a list having strings with 'sender_name: chat'
    messages = re.split(pattern, data)[1:]
    # we are extracting date & time of each chat msg from whole chat and storing it in dates variable
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_msg': messages, 'msg_date': dates})
    # convert msg_date format type
    df['msg_date'] = pd.to_datetime(df['msg_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'msg_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_msg']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns=['user_msg'], inplace=True)

    df.head()
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df


