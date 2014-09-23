#!/usr/bin/python
# -*- code: utf-8 -*-

from __future__ import unicode_literals, print_function
import requests
import datetime
import json
import sys
from collections import Counter

BASE_URL ='http://ws.audioscrobbler.com/2.0/'
API_KEY = '37ec4aba2276f65295c2401e38355447'
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
        print(CALL_FAIL.format(code))
    elif err_type == 'api':
        print(API_FAIL.format(code, message))
    else:
        print('unidentifed error call. Code={}, msg={}'.format(code,message))
    sys.exit()

def check_args(args):
    if len(args) < 2:
        fail_on_error('argv')
    user = args.pop()
    payload = PARAMS
    payload['method'] = 'user.getInfo'
    payload['user'] = user
    r = requests.get(BASE_URL, params=payload)
    if r.status_code == 200:
        d = r.json()
        if 'error' in d:
            fail_on_error('api', code=d['error'], message=d['message'])
        return user
    fail_on_error('requests', code=r.status_code)

def get_data(user, dt_from=0, dt_to=0):
    payload = PARAMS
    payload['user'] = user
    payload['method'] = 'user.getrecenttracks'
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

def create_rec(response):
    r = response.get('recenttracks', None)
    records = []
    if r:
        tracks = r.get('tracks', [])
        for track in r.get('tracks', []):
            records.append( (
                             track['date']['uts'],
                             track['name'],
                             track['artist']['#text']
                             ) )
    return records
        
def get_recent_tracks(user):
    '''
    '''
    with open('{}.json'.format(user)) as txtfile:
        try:
            existing = json.load(txtfile)
            dt_from = 0
            if existing:
                dt_from = existing[-1][0]
            print('read user file')
        except ValueError:
            existing = []
            dt_from = 0
            print('empty file')
    new = []
    old = []
    newrecs = True
    for page in xrange(5):
        if newrecs:
            if dt_from > 0:
                d = get_data(user,dt_from=dt_from)
            else:
                d = get_data(user)   # new file
            rec = create_rec(d)
            print('d=', d)
            if rec:
                new = new + rec
            else:
                newrec = False
        else:
            existing = sorted(existing + new)
            dt_to = existing[0][0] 
            d = get_data(user,dt_to=dt_to)
            rec = create_rec(d)
            old = old + rec
    existing = sorted(new + existing + old)
    print('Existing', existing)
    with open('{}.json'.format(user), 'w') as outfile:
        json.dump(existing, outfile)
    print('write to', user)

    
def display_results(user):
    with open('{}.json'.format(user), 'r') as infile:
        try: 
            d = infile.read() 
            history = json.load(d)
        except ValueError:
            print('No data to display')
            return
    print('You have listened to a total of {} tracks'.format(len(history)))
    artists = {}
    for rec in history:
        artist = rec[2]
        if artist in artists:
            artists[artist] += 1
        else:
            artists[artist] = 1
    d = Counter(artists)
    p = []
    for artist, count in d.most_common(5): 
        p.append(artist)
    print('Your top favourite artists: {}'.format(','.join(p)))

if __name__ == '__main__':
    user = check_args(sys.argv)
    open('{}.json'.format(user), 'a').close()
    get_recent_tracks(user)
    display_results(user)
