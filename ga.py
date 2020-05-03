
import config
import math
import urllib
import requests
import json

from models import *
from apiclient.discovery import build
from google.oauth2.service_account import Credentials

"""
[
    'v'      :1,
    'tid'    :'UA-52479722-1',
    'cid'    :'555',
    't'      :'transaction',
    'ti'     :'9998',
    'tr'     :'100',
    'tt'     :'10',       налоги
    'cu'     :'AUD',     валюта
    'pa'     :'purchase',
    'pr[1]id':'1',
    'pr[1]nm':'Test Product',
    'pr[1]ca':'Test Category',
    'pr[1]qt':'2',
    'pr[1]pr':'100',
    'cd1':'Сustom Dimension 1'
    dh Document Host,
    dp Document Path
]
"""

class gaTracker:

    def __init__(self):
        """Constructor"""
        self.url = "https://ssl.google-analytics.com/collect"
        self.ver = 1

    def sendPageview(self, cid, tid, dh, dp):
        """Формирование строки для отправки"""

        hit = {'v':self.ver,
                't':'pageview',
                'tid':tid,
                'cid': cid,
                'dh':dh,
                'dp':dp,
                'cd1':cid
            }

        params = urllib.parse.urlencode(hit)
        url = '{}?{}'.format(self.url, params)

        requests.post(url)

        return url

    def storeOutputMessage(self, message_id, message):
        """Разбор исходящего сообщения"""
        url = '-'
        dh = config.ga_host
        tid =  config.ga_tracker
        cid = message_id

        try:
            text = message['text']

    #             getattr(message, 'text', 'not_s')

            if text is not None:
                dp = str(text)
            else:
                dp = 'not_set'

        except Exception as e:
            dp = str(e) + 'error'

        dp = 'bot: {}'.format(dp)

        url = self.sendPageview(cid, tid, dh, dp)

        return  url


    def storeInputMessage(self, message):
        """Разбор входящего сообщения"""
        cid = '0'
        url = 'not_set'
        dh = config.ga_host
        tid =  config.ga_tracker

        try:

            cid = message.from_user.id
            text = getattr(message, 'text', '-')

            #call_text = getattr(message, 'data', '-')
            #text = str(text) + str(call_text)

            if text is not None:
                dp = str(text)
            else:
                dp = 'not_set'

        except Exception as e:
            dp = str(e) + 'error'

        dp = 'human: {}'.format(dp)
        url = self.sendPageview(cid, tid, dh, dp)

        return  url
    # def get_sessions(self):
    #     scopes = ['https://www.googleapis.com/auth/analytics.readonly']
    #     with open(config.ga_key_file_location) as file:
    #         keyfile_dict = json.load(file)
    #
    #     analytics = self.initialize_analyticsreporting(scopes,keyfile_dict)
    #
    #     r = self.get_report(analytics, config.ga_view)
    #     r = self.handle_response(r)
    #     return r


    # def initialize_analyticsreporting(self, scopes,keyfile_dict):
    #     """Initializes an Analytics Reporting API V4 service object.
    #     Returns:  An authorized Analytics Reporting API V4 service object.
    #     """
    #     credentials = Credentials.from_service_account_info(
    #     keyfile_dict, scopes=scopes)
    #     analytics = build('analyticsreporting', 'v4', credentials=credentials)
    #
    #     return analytics


    # def get_report(self,analytics, view_id):
    #     """Queries the Analytics Reporting API V4"""
    #
    #     r = {
    #       'reportRequests': [
    #       {
    #           'viewId': view_id,
    #           'dateRanges': [{'startDate': '90daysAgo', 'endDate': 'today'}],
    #           'metrics': [{'expression': 'ga:sessions'}],
    #           'dimensions': [{'name': 'ga:pagePath'}],
    #           "dimensionFilterClauses": [{
    #             "filters": [
    #               {
    #                 "dimensionName": "ga:pagePath",
    #                 "operator": "PARTIAL",
    #                 "expressions": ["catalog"]
    #               }
    #             ]
    #           }]
    #       }]
    #     }
    #
    #     return analytics.reports().batchGet(body=r).execute()




    # def handle_response(self, response):
    #     x =[]
    #     report_data = response['reports'][0]['data']
    #     for r in report_data['rows']:
    #         x.append([r['dimensions'][0], r['metrics'][0]['values'][0]])
    #     return x
