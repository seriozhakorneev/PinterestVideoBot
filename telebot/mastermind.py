from PinParser import PinterestParser
import re

help_message = '➕Send pin to this bot via Pinterest\n➕Or send him a https:// pin address'

def get_response(msg):

	if msg == '/help':
		return help_message

	get_pin_url = re.search("(?P<url>https?://[^\s]+)", message)
	if get_pin_url:

		pin_url = get_pin_url.group('url')
		if ('https://pin.it' in pin_url) or ('.pinterest.' in pin_url):
			pin_obj = PinterestParser(pin_url)
			pin_obj.get_to_url(pin_obj.pin_url)
			media_link = pin_obj.get_pin_media()
			pin_obj.close_browser()
			link_answer = f'<a href="{media_link}">➕ Link</a>'
			
			return link_answer