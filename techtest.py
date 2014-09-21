#!/usr/bin/python
# -*- code: utf-8 -*-

from __future__ import unicode_literals, print_function
import requests
import datetime
import json
import sys

BASE_URL ='http://ws.audioscrobbler.com/2.0/'
API_KEY = '37ec4aba2276f65295c2401e38355447'
API_KEY = '7ec4aba2276f65295c2401e38355447'
PARAMS = {'api_key': API_KEY, 'format': 'json', 'method': 'user.getRecentTracks'}

NO_ARG = '''
    Username required.
    USAGE:
        python techtest.py <username>
    '''
CALL_FAIL = '''
    Status code from API request: {}
    Call to API failed.
'''
API_FAIL = '''
    Status code from Last.FM API: {}
    Last.FM API says: "{}"
'''

def fail_on_error(err_type, code=0, message=''):
    if err_type == 'argv':
        print(NO_ARG)
    elif err_type == 'requests':
        print(CALL_FAIL.format(code)
    elif err_type == 'api':
        print(API_FAIL.format(code, message)
    else:
        print('unidentifed error call. Code={}, msg={}'.format(code,message)
    sys.exit()

def get_data(user, page=1, dt_from=0, dt_to=0):
    payload = PARAMS
    payload['user'] = user
    payload['page'] = page
    if dt_from > 0:
        payload['from'] = dt_from
    elif dt_to > 0:
        payload['to'] = dt_to
    r = requests.get(BASE_URL, params=payload)
    if r.status_code == 200:
        d = r.json()
        if 'error' in d:
            fail_on_error('api', code=d['error'], message=d['message'])
        return r.json()
    fail_on_error('requests', code=r.status_code)

def get_recent_tracks(user):
    '''
    Currently, the API only releases 10 per page, and we are restricted from
    increasing it by using &limit=
    '''
    for page in xrange(1,6):
        d = get_data(user)
        w = d['recenttracks']
        for t in w['tracks']:
            track.append(t)
    if 'track' in w:
        tracks = w['track']
        for track in tracks:
            name = track['name']
            artist = track['artist']['#text']
            track_date = track['date']
            date_uts = track_date['uts']
            date_text = track_date['#text']
            dt = datetime.datetime.fromtimestamp(int(date_uts))
            print('{}, ({}). Date: {} {}'.format(name, artist, date_uts,
                                                 dt.strftime('%Y/%m/%d')))
        return
    print(json.dumps(d, sort_keys=True, indent=3))
    
def check_args():
    if len(sys.argv) < 2:
        fail_on_error('argv')
    payload = PARAMS
    payload['method'] = 'user.getInfo'
    payload['user'] = sys.argv[1]
    r = requests.get(BASE_URL, params=payload)
    if r.status_code == 200:
        d = r.json()
        if 'error' in d:
            fail_on_error('api', code=d['error'], message=d['message'])
        return sys.argv[1]
    fail_on_error('requests', code=r.status_code)

if __name__ == '__main__':
    user = check_args()
    get_recent_tracks(user)
