''' A script to dump People profiles out to a CSV ''


import hashlib
import time
import urllib
try: 
	import json
except ImportError:
	import simplejson as json
	
##########

debug = True #True / False

##########

class Mixpanel(object):
	
	def __init__(self, api_key, api_secret):
		self.api_key = api_key
		self.api_secret = api_secret
	
	def request(self, params):
		'''let's craft the http request'''
		params['api_key']=self.api_key
		params['expire'] = int(time.time())+600 # 600 is ten minutes from now
		if 'sig' in params: del params['sig']
		params['sig'] = self.hash_args(params)
		
		request_url = 'https://mixpanel.com/api/2.0/segmentation?' + self.unicode_urlencode(params)
		
		if debug:
			print request_url
		else:
			request = urllib.urlopen(request_url)
			data = request.read()
			return json.loads(data)
		
	def hash_args(self, args, secret=None):
		'''Hash dem arguments in the proper way
		
			join keys - values and append a secret -> md5 it'''
		
		for a in args:
			if isinstance(args[a], list): args[a] = json.dumps(args[a])
			
		args_joined = ''
		for a in sorted(args.keys()):
			if isinstance(a, unicode):
				args_joined += a.encode('utf-8')
			else:
				args_joined += str(a)
				
			args_joined += "="
			
			if isinstance(args[a], unicode):
				args_joined += args[a].encode('utf-8')
			else:
				args_joined += str(args[a])
				
		hash = hashlib.md5(args_joined)

		if secret:
			hash.update(secret)
		elif self.api_secret:
			hash.update(self.api_secret)
		sig = hash.hexdigest()
		if debug:
			print "arg_string = %s\nSignature = %s" % (args_joined,sig)
				
		return sig
		
	def unicode_urlencode(self, params):
		''' Convert stuff to json format and correctly handle unicode url parameters'''
		
		if isinstance(params, dict):
			params = params.items()
		for i, param in enumerate(params):
			if isinstance(param[1], list):
				params[i] = (param[0], json.dumps(param[1]),)
		
		result = urllib.urlencode(
			[(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])
		
		return result
			
if __name__ == '__main__':
	api = Mixpanel(
		api_key = 'api_key',
		api_secret = 'api_secret'
	)
	
	data = api.request({
		'selector':'STUFF',
	})









'
