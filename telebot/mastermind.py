from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import re

class PinterestParser:

	def __init__(self, pin_url):
		self.op = webdriver.ChromeOptions()
		self.op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		self.op.add_argument("--headless")
		self.op.add_argument("--no-sandbox")
		self.op.add_argument("--disable-dev-sh-usage")
		# heroku deploy
		self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=self.op)
		# localy
		#self.PATH = '/home/sergei/code/test/instatest/app/chromedriver'
		#self.driver = webdriver.Chrome(executable_path=self.PATH, options=self.op)
		self.pin_url = pin_url

	def get_to_url(self, link):
		self.driver.get(link)
		return self.driver.current_url

	def fix_video_url(self, false_video_url):
		video_url = false_video_url.replace('hls', '720p').replace('m3u8', 'mp4')
		return video_url

	def get_pin_video_script(self):
		try:
			get_video_script = WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, '.Jea.jzS.mQ8.zI7.iyn.Hsu > script')))
			video_script = get_video_script.get_attribute('innerHTML')
			return video_script
		except:
			return None

	def get_pin_image(self):
		try:
			get_image = WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, '.zI7.iyn.Hsu > img')))
			image_url = get_image.get_attribute('src')
			return image_url
		except:
			return None

	def get_pin_media(self):

		video_script_str = self.get_pin_video_script()
		if video_script_str:

			video_script = json.loads(video_script_str)
			false_video_url = video_script['contentUrl']
			video_url = self.fix_video_url(false_video_url)
			return video_url

		else:
			image_url = self.get_pin_image()
			return image_url

	def close_browser(self):
		self.driver.quit()

help_message = '➕Send pin to this bot via Pinterest\n➕Or send him a https:// pin address'

def get_response(msg):

	if msg == '/help':
		return help_message

	get_pin_url = re.search("(?P<url>https?://[^\s]+)", msg)
	if get_pin_url:

		pin_url = get_pin_url.group('url')
		if ('https://pin.it' in pin_url) or ('.pinterest.' in pin_url):
			pin_obj = PinterestParser(pin_url)
			pin_obj.get_to_url(pin_obj.pin_url)
			media_link = pin_obj.get_pin_media()
			pin_obj.close_browser()
			link_answer = f'<a href="{media_link}">➕ Link</a>'
			
			return link_answer