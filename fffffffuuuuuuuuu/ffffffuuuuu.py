#!/usr/bin/python

import json
import re
import urllib2

f_count = 2;
u_count = 2;
f = 'f'
u = 'u'

#url_template = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s'
url_template = 'http://www.google.com/search?aq=f&sourceid=chrome&ie=UTF-8&q=%s'

full_result =[]

# Loop over every combination of ffff's and uuuu's based on the above settings
for x in range(1, f_count + 1):
  for y in range(1, u_count + 1):
    query = (f * x) + (u * y)
    url = url_template % query

    req = urllib2.Request(url)
    # You should obviously change this. I don't think it matters what url it is,
    # but you should probably use your own site.
    # Without this, the google API will not accept many requests.
    req.add_header('Referer', 'http://blog.deconcept.com/')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.A.B.C Safari/525.13')
    data = urllib2.urlopen(req)
    #print 'requesting url %s' % url
    result = data.read()
    #parsed_result = json.loads(result)
    resultMatch = re.compile("t\s([0-9,]+)\sr")
    est_count = resultMatch.search(result).group(1).replace(',', '')
    #print est_count

    #try:
      #est_count = parsed_result['responseData']['cursor']['estimatedResultCount']
    #except KeyError:
      # Sometimes the API response is not complete,
      # so just set to 0 since it's probably 0 anyway
      #est_count = 0

    #print est_count

    full_result.append({
      'query': query,
      'count': int(est_count),
      'f': x,
      'u': y
    })

# After we get all the results, go through and set a % value,
# where 100% is the max count, and 0% is the lowest count.
max_value = 0.0

# First, find the max value of the set
for x in range(len(full_result)):
  current_count = full_result[x]['count']
  if max_value < current_count:
    max_value = float(current_count)

median = full_result[int(len(full_result) / 2)]['count']
#print "median is %s" % median


# Set the % value in each item (for display purposes)
for x in range(len(full_result)):
  current_item = full_result[x]
  #print current_item['count']
  #current_item['percent'] = int((current_item['count'] / max_value) * 100.0)
  current_item['percent'] = getPercent(current_item['count'], max_value)

# Spit out the data in json format so jquery/javascript can read it
print json.dumps(full_result, sort_keys=True, indent=4)



