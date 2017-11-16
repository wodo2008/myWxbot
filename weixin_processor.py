import requests
import json

def get_stats_data(sday,eday):
    token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential' \
                    '&appid=wx05343850acb08432&secret=2b83f796402b2483e76088936f21d7ef'
    data_url = 'https://api.weixin.qq.com/datacube/getusercumulate?access_token=%s'
    token_result = requests.post(token_url)
    token_data = json.loads(token_result.text)
    access_token = token_data['access_token']
    data = {}
    data['begin_date'] = sday
    data['end_date'] = eday

    data = json.dumps(data)
    stats_data = requests.post(data_url % access_token,data=data)
    print stats_data.text
    return get_cumulate_user(json.loads(stats_data.text))


def get_cumulate_user(oridata):
    return oridata['list'][0]['cumulate_user']

if __name__ == '__main__':
    sday = '2017-11-01'
    eday = '2017-11-01'
    get_stats_data(sday,eday)