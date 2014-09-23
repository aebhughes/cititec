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

# Standard set of error displays

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
    '''Standard error handling function'''

    if err_type == 'argv':
        print(NO_ARG)
    elif err_type == 'requests':
        print(CALL_FAIL.format(code))
    elif err_type == 'api':
        print(API_FAIL.format(code, message))
    else:
        print('unidentified error call. Code={}, msg={}'.format(code,message))
    sys.exit()

def check_args(args):
    '''
    Comprehensive argument handling. Argparse is not used because of
    possible efficacy issues
    '''
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
    '''
    Standardised API call. Returns a dictionary.
    '''
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
    '''
    Convert API response into a list of tuples containing relevant data only.
    '''
    r = response.get('recenttracks', None)
    records = []
    tracks = r.get('track', [])
    for track in tracks:
        records.append( (
                         int(track['date']['uts']),
                         track['name'],
                         track['artist']['#text']
                         ) )
    return records
        
def get_existing(user):
    '''
    Read persistent data.  Script can be changed over to JSON, YAML, Database
    etc. by changing this function and write_existing alone. 
    '''
    existing = []
    try:
        for line in open('{}.txt'.format(user), 'r'):
            inline = line.strip().split('|')
            rec = []
            for elem in inline:
                rec.append(elem.strip())
            rec[0] = int(rec[0])
            existing.append(tuple(rec))
    except IOError:
        open('{}.txt'.format(user), 'a').close()
    return existing
            
def write_existing(existing, user):
    '''
    Write persistent data.  Script can be changed over to JSON, YAML, Database
    etc. by changing this function and read_existing alone. 
    '''
    with (open('{}.txt'.format(user), 'w')) as outfile:
        for rec in existing:
            rec = list(rec)
            rec[0] = str(rec[0])
            outfile.write('|'.join(rec) + '\n')

def get_recent_tracks(user):
    '''
    1) Get saved persistent data, already sorted in date order
    2) Add new found API to front.  API query uses &from=
    3) Back fill missing data, using the &to=
    4) Only 5 API reads allowed.  New tracks collected first before backfill
    '''
    existing = get_existing(user)
    dt_from = 0
    if existing:
        dt_from = existing[-1][0]
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
    write_existing(existing, user)

    
def display_results(user):
    '''
    Display from exiting data file. Terminates if datafile empty.
    '''
    history = get_existing(user)
    if not history:
        print('No data to display')
        return
    print('You have listened to a total of {} tracks'.format(len(history)))
    artists = {}
    days = {}
    max_date = 0
    min_date = sys.maxint
    for rec in history:
        artist = rec[2]
        if artist in artists:
            artists[artist] += 1
        else:
            artists[artist] = 1
        dt = datetime.datetime.fromtimestamp(rec[0])
        daylit = dt.strftime('%A')
        if daylit in days:
            days[daylit] += 1
        else:
            days[daylit] = 1
        if rec[0] > max_date:
            max_date = rec[0]
        if rec[0] < min_date:
            min_date = rec[0]
    top_artists = Counter(artists)
    top5 = [x[0] for x in top_artists.most_common(5)]
    print('Your top favourite artists: {}'.format(','.join(top5)))

    oldest_dt = datetime.datetime.fromtimestamp(min_date)
    newest_dt = datetime.datetime.fromtimestamp(max_date)
    delta = newest_dt - oldest_dt
    avg = round(float(len(history)) / float(delta.days))
    print('You listen to and average of {} tracks a day.'.format(int(avg)))

    d = Counter(days)
    print('Your most active day is {}'.format(d.most_common(1)[0][0]))

if __name__ == '__main__':
    user = check_args(sys.argv)
    open('{}.txt'.format(user), 'a').close()
    get_recent_tracks(user)
    display_results(user)
