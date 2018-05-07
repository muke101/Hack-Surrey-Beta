import requests
import json
import pandas as pd
import numpy as np
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scipy import stats
import time as t
from tkinter import *
import tweepy
import datetime
import csv

def marco():
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': 'aa99d31882484f95bf7739d85112985e',
        'client_secret': '2c3faccea75f161ed2db069647e94dfb81c79d73a9346e413a104c530ddbe6dd',
        'scope': 'read_product_data read_financial_data read_content'
    }
    print('Connecting to Goldman Sachs')
    # create Session instance
    session = requests.Session()

    # make a POST to retrieve access_token
    auth_request = session.post('https://idfs.gs.com/as/token.oauth2', data=auth_data)
    access_token_dict = json.loads(auth_request.text)
    access_token = access_token_dict['access_token']

    # update session headers
    session.headers.update({'Authorization': 'Bearer ' + access_token})
    print('Connected successfully..')
    print('Access token:', access_token)

    request_url = 'https://api.marquee.gs.com/v1/data/USCANFPP_MINI/coverage?limit=10'
    request = session.get(url=request_url)
    data = json.loads(request.text)
    df = pd.DataFrame(data['results'])
    gsids = df.gsid
    df = df.values.astype(int)

    print("Starting ID call...")

    # conversion to json format
    request_url = r'https://api.marquee.gs.com/v1/assets/data/query'
    A = []
    for i in range(len(gsids)):
        req = {
            'where': {
                'gsid': list(map(str, (df[i]).tolist()))
            }
        }
        request = session.post(url=request_url, json=req)
        data = json.loads(request.text)
        tmp = data['results'][0]['name'].strip(' Inc').strip('-')
        tmp = (tmp.split()[0])
        print('Company collected:', tmp)
        A.append(tmp)
        # Just selecting the first 10
        if i >=9:
            break
    # Removing dulplicates!
    A = set(A)
    print('ID call complete!')
    print('Obtained:', len(A), 'companies!')
    return A


print('Connecting to Twitter:')
auth = tweepy.OAuthHandler("2DDepQNXr4h3Uubm5TolYq34t", "gxiJ3OGLxikjhFPLawruYk8WHVtX4eFbqZ6rqndUqqm7aC27ev")
auth.set_access_token("931147713885949952-2aBpA6uBrxp7RsfShe6giz93AI07YFf",
                      "U2mYjfd365tarRZnxTnNwtcOCFHyyj7rOTXJmbC01EDu3")

api = tweepy.API(auth)
name="@realDonaldTrump"
dates = []
text = []
end_date = datetime.datetime.utcnow() - datetime.timedelta(days=3600)
for status in tweepy.Cursor(api.user_timeline, tweet_mode='extended', id=name).items():
    dates.append(status.created_at)
    text.append(status.full_text)
    if status.created_at < end_date:
        break

def luke(companies):
    data = companies
    companyTweet = {}
    for row in data:
        for c, tweet in enumerate(text):
            if row[0] in tweet:
                companyTweet[dates[c]] = row[0]
    return companyTweet


def run_anal(companies, given_date):
    # Plotting parameters
    ys = 16
    xs = 16
    plt.rcParams['axes.linewidth'] = 2.0

    # Selecting the range to observe
    before = 14
    after = 14

    # flags for plotting
    p_flag = 0
    h_flag = 1
    bug_flag = 0

    # create Session instance
    session = requests.Session()
    for j in companies:
        request_url = 'https://api.iextrading.com/1.0/stock/' + j + '/chart/2y'
        request = session.get(url=request_url)
        data = json.loads(request.text)

        df = pd.DataFrame(data)
        df = df.values

        change = df[:, 0].astype(float)
        open = df[:, 8].astype(float)
        close = df[:, 3].astype(float)
        un_vol = df[:, 9].astype(float)
        vol = df[:, 10].astype(float)
        dates = df[:, 6]

        diff_ave3 = np.zeros(len(given_date))
        change_ave3 = np.zeros(len(given_date))
        for z, i in enumerate(given_date):
            # This is the date he was swore in??
            start = int(np.where(dates == 'Jan 20, 17')[0])

            select = int(np.where(dates == i)[0])
            s1 = select - before
            s2 = select + after

            Diff = np.subtract(close, open)
            diff_ave3[z] = np.average(Diff[select:select + 3]) - Diff[select]

            change_ave3[z] = np.average(change[select:select + 3]) - change[select]

            if bug_flag == 1:
                print('Date observing:', i)
                print(diff_ave3[z])
                print(change_ave3[z])

            if p_flag == 1:
                fig = plt.figure(figsize=(12, 6))
                gs = gridspec.GridSpec(3, 1)  # , width_ratios=[4, 4]) # height_ratios=[4, 4],
                # plt.errorbar(dates[s1:s2],y[s1:s2], xerr=change[s1:s2], yerr=change[s1:s2])
                ax0 = plt.subplot(gs[0])
                plt.plot(dates[s1:s2], open[s1:s2], label='Open')
                plt.plot(dates[s1:s2], close[s1:s2], label='Close')
                plt.scatter(dates[select], close[select], c='r')
                plt.scatter(dates[select], open[select], c='r')
                plt.legend(loc=4, fontsize=ys - 2)
                plt.ylabel('Price', fontsize=ys)
                plt.tick_params(axis='both', which='major', labelsize=ys - 2, direction='in', length=6, width=2)
                plt.tick_params(axis='both', which='minor', labelsize=ys - 2, direction='in', length=4, width=2)
                plt.tick_params(axis='both', which='both', top=True, right=True)
                plt.setp(ax0.get_xticklabels(), visible=False)
                plt.tight_layout()

                ax1 = plt.subplot(gs[1], sharex=ax0)
                plt.setp(ax1.get_xticklabels(), visible=False)
                plt.ylabel('Spread', fontsize=ys)
                plt.tick_params(axis='both', which='major', labelsize=ys, direction='in', length=6, width=2)
                plt.tick_params(axis='both', which='minor', labelsize=ys, direction='in', length=4, width=2)
                plt.tick_params(axis='both', which='both', top=True, right=True)
                plt.plot(dates[s1:s2], Diff[s1:s2])
                plt.scatter(dates[select], Diff[select], c='r')
                plt.tight_layout()

                ax2 = plt.subplot(gs[2], sharex=ax0)
                plt.plot(dates[s1:s2], change[s1:s2])
                plt.scatter(dates[select], change[select], c='r')

                plt.tick_params(axis='both', which='major', labelsize=ys, direction='in', length=6, width=2)
                plt.tick_params(axis='both', which='minor', labelsize=ys, direction='in', length=4, width=2)
                plt.tick_params(axis='both', which='both', top=True, right=True)
                plt.xlabel('Date', fontsize=xs)
                plt.ylabel('Change', fontsize=ys)
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()

        if h_flag == 1:
            plt.title(j.upper(), fontsize=ys)
            plt.tick_params(axis='both', which='major', labelsize=ys - 2, direction='in', length=6, width=2)
            plt.tick_params(axis='both', which='minor', labelsize=ys - 2, direction='in', length=4, width=2)
            plt.tick_params(axis='both', which='both', top=True, right=True)
            plt.ylabel('Price', fontsize=ys)
            plt.hist(diff_ave3)
            plt.hist(change_ave3)
            plt.tight_layout()
            plt.show()
        o_ave = min(np.average(diff_ave3), np.average(change_ave3))
        print('Trumps impact:', o_ave/open)


for keys, values in luke(marco(),name):
    run_anal(keys, values)
