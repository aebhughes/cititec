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

def get_data(user, dt_from=0, dt_to=0):
    payload = PARAMS
    payload['user'] = user
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
    r = response('recenttracks', None)
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
    Currently, the API only releases 10 per page, and we are restricted from
    increasing it by using &limit=
    '''
    with open('{}.json'.format(user)) as infile:
        try:
            existing = json.load(infile)
            dt_from = existing[-1][0]
        except ValueError:
            existing = []
            dt_from = 0
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
    with open('{}.json'.format(user), 'w') as outfile:
        json.dump(existing, outfile)

    
def display_results(user):
    with open('{}.json'.format(user)) as infile:
        tracks = json.load(infile)
    except ValueError:
        print('No data to display')
        return
    tracks = {}
    artists = {}
        
    # total unique tracks
    

if __name__ == '__main__':
    user = check_args()
    get_recent_tracks(user, f)
    display_results(user)
