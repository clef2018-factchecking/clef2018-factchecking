# URL filter for the CLEF-2018 Fact Checking Lab

import sys
if sys.version_info[0] < 3:
	import urllib2 as urllib
	import cookielib as cookielib
else:
	import urllib.request as urllib
	import http.cookiejar as cookielib

# Impersonate some real user agent so less network requests fail (URL expansion)
_USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0'

# Each item is tested for containment within the lower cased URL
# Logical AND for items in a single row
MATCHERS_ALL = [
	# Fact-checking sites US
	['factcheck.org'],
	['politifact'],
	['snopes'],
	['truthorfiction'],
	['climatefeedback'],
	['gossipcop'],
	# Sites with fact-checking sections US
	['apnews', 'not-real-news'],
	['apnews', 'fact-check'],
	['washingtonpost', 'fact-check'],
	['azcentral', 'fact-check'],
	['cbslocal', 'reality-check'],
	['thenevadaindependent', 'fact-check'],
	['thegazette', 'fact-check'],
	['thegazette', 'factchecker'],
	['nytimes', 'fact-check'],
	['bridgemi', 'michigan-truth-squad'],
	['channel3000', 'reality-check'],
	['kmov', 'fact-check'],
	['npr', 'fact-check'],
	['qctimes', 'fact-check'],
	['politico', 'fact-check'],
	['weeklystandard', 'fact-check'],
	['ballotpedia', 'fact_check'],
	['wral', 'fact-check'],
	['abcnews', 'fact-check'],
	['chicagotribune', 'fact-check'],
	['cnn', 'fact-check'],
	['theguardian', 'fact-check'],
	['usatoday', 'fact-check'],
	# UK & other
	['hoax-slayer'],
	['fullfact'],
	['factcheckni'],
	['theconversation', 'fact-check'],
	['bbc', 'realitycheck'],
	['bbc', 'reality-check'],
	['channel4', 'factcheck'],
	['theferret', 'fact-check'],
	['theferret', 'fact-service'],
	['abc', 'fact-check'],
	['pbs', 'fact-check'],
	['foxnews', 'fact-check'],
	# Possibly Arabic
	['factnameh'],
	['rouhanimeter'],
	['thewhistle'],
	['morsimeter'],
	['larbitrefact'],
	['meter.iwatch'],
	['sebsimeter'],
	['jomaameter'],
	['essidmeter'],
	# Special phrases English
	['debate-highlighted'],
	['debate-transcript-annotated'],
	['fact check'],
	['fact%20check'],
	['fact+check'],
	['fact_check'],
	['fact-check'],
	['factcheck'],
	['reality check'],
	['reality%20check'],
	['reality+check'],
	['reality_check'],
	['reality-check'],
	['realitycheck'],
	['fake news'],
	['fake%20news'],
	['fake+news'],
	['fake_news'],
	['fake-news'],
	['fakenews']
]

MATCHERS_SIMPLE = [
	['factcheck'],
]

# Makes an HTTP HEAD request to the provied url and then returns the possibly expanded URL from the response
def _expand_url(url):
	request = urllib.Request(url)
	request.get_method = lambda : 'HEAD'
	request.add_header('User-Agent', _USER_AGENT)
	cj = cookielib.CookieJar()
	opener = urllib.build_opener(urllib.HTTPCookieProcessor(cj))
	response = opener.open(request)
	return response.geturl()

def _check_matchers(urlString, allMatchers = True):
	urlLower = urlString.lower()
	matchers = MATCHERS_ALL if allMatchers else MATCHERS_SIMPLE
	return any([all([item in urlLower for item in row]) for row in matchers])

def _is_url_bad(urlString, allMatchers = True):
	if not isinstance(urlString, str):
		print('Error, the provided parameter is not a string. Cannot determine if it is BAD.')
		return False

	if _check_matchers(urlString, allMatchers):
		return True
	try:
		urlExpanded = _expand_url(urlString)
	except:
		print('Error while expanding URL "' + urlString + '":', str(sys.exc_info()[1]))
		print('Cannot currently determine if the URL is BAD, examine manually.')
		return False
	return _check_matchers(urlExpanded, allMatchers)

def is_url_bad_task1(urlString):
	return _is_url_bad(urlString)

def is_url_bad_task2(urlString):
	return _is_url_bad(urlString, False)

EXAMPLES = [
	# BAD for both tasks:
	'https://www.factcheck.org/2018/03/trump-veterans-choice-program/',
	'https://www.channel4.com/news/factcheck/ann-coulters-10-misleading-claims-about-immigrants-and-mass-shootings',
	'http://bit.ly/2IA2znR',
	# BAD for task1, OK for task2:
	'https://www.washingtonpost.com/news/fact-checker/wp/2018/02/18/fact-checking-trumps-error-filled-tweet-storm-about-the-russia-investigation/',
	'http://www.thegazette.com/subject/news/government/fact-check/fact-checking-the-speech-trump-plays-loose-with-facts-20170621',
	'https://twitter.com/snopes/status/963534404047048710',
	'http://bit.ly/2CMmrAl',
	# OK for both tasks:
	'https://www.washingtonpost.com/news/tripping/wp/2017/11/30/car-rental-companies-find-a-way-to-ding-motorists-for-electronic-tolling/',
	'https://en.wikipedia.org/wiki/Donald_Trump',
	'http://goo.gl/eRJPti'
]

if __name__ == '__main__':
	for site in EXAMPLES:
		labelTask1 = 'BAD' if is_url_bad_task1(site) else 'OK '
		labelTask2 = 'BAD' if is_url_bad_task2(site) else 'OK '
		print('task1: ' + labelTask1, 'task2: ' + labelTask2, site)
