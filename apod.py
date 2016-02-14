try:
	import urllib2
except:
	print "[APOD] Install latest version of python2.7"

try:
	from bs4 import BeautifulSoup as bs
except:
	print "[APOD] BeautifulSoup package required"
	print "[APOD] please Install BeautifulSoup"
	print "Go to https://pypi.python.org/pypi/beautifulsoup4"

from time import strftime, time

from utils.Error_codes import Error_codes



class APOD_Downloader():
	def __init__(self, error_codes):
		self.BASE_URL = "http://apod.it"
		self.error_codes = error_codes

	def get_apod_url(self):
		img = strftime("%y%m%d")
		img_url = self.BASE_URL + "/" + img
		return img_url

	def get_image_url(self, img_url):
		try:
			req = urllib2.urlopen(img_url) 

		except urllib2.HTTPError, e:
			print "[APOD] Failed to connect", e.getcode()
			print "[APOD]",self.error_codes.error_code_status(e.getcode())
			print "[APOD]", "Exiting..."
			return selferror_codes.err["HTTPERR"]

		except urllib2.URLError, e:
			print "[APOD]", e.args[0]
			print "[APOD]", "Internet Connection not working"
			print "[APOD]", "Exiting..."
			return self.error_codes.err["URLERR"]

		# Reading the page source of the apod.nasa.gov page
		page_html = req.read()
		soup = bs(page_html, "html.parser")

		images = soup.find_all("a")
		
		# The second link is the image location 
		# for the higest resolution version
		try:
			image_location = images[1].get("href")
		except:
			return self.error_codes.err["NOIMG"]

		# Sample Image location
		# http://apod.nasa.gov/apod/image/1602/HeartCloud_Kunze_4650.jpg

		full_res_image_url = "http://apod.nasa.gov/" + image_location
		return full_res_image_url

	def download_image(self, url):
		file_name = url.split('/')[-1]
		try:
			u = urllib2.urlopen(url)
			meta = u.info()
			# meta info  
			# Server: WebServer/1.0
			# Last-Modified: Sat, 13 Feb 2016 00:00:31 GMT
			# ETag: "13b612a-fef4a-52b9b78d985c0"
			# Accept-Ranges: bytes
			# Keep-Alive: timeout=5, max=100
			# Content-Type: image/jpeg
			# Connection: close
			# Date: Sun, 14 Feb 2016 12:33:23 GMT
			# Age: 3378
			# Content-Length: 1044298
			file_size = int(meta.getheaders("Content-length")[0])
			file_type = meta.getheaders("Content-Type")[0]

			if (file_type != "image/jpeg"):
				print "[APOD]", "The content hosted on apod.nasa.gov is not an image"
				return self.error_codes.err["NOIMG"]
			# Block size of each download packet is kept 4 KB
			block_sz = 4096

			# Stores the total file downloaded
			file_dl = 0

			#stating time of download
			start_time = time()
			running_time = start_time

			# file name is same as the name of the image in the apod link
			f = open(file_name, "wb")

			while True:
				buffer = u.read(block_sz)
				if not buffer:
					break
				file_dl += len(buffer)
				f.write(buffer)
				curr_time = time()
				if (curr_time - running_time >= 0.25):
					print "[APOD] Downloaded %.2f KB of %.2f KB \r" %(file_dl / 1024.0, file_size / 1024.0),
					running_time = curr_time
			end_time = time()
			f.close()
			print

			try:
				# checking if the total size of the file downloaded and the actual size of the file 
				# are same or not, it not an assertion error is raised and the program exits
				assert file_dl == file_size
			except AssertionError:
				print "[APOD]", "File download incomplete or corrupt, please try again"
				print "[APOD]", "Exiting..."
				return self.error_codes.err['INCOMPDL']

			print "[APOD] Downloaded %.2f KB in %.2fs"%((file_size / 1024.0), (end_time - start_time))

		except urllib2.HTTPError, e:
			print "[APOD] Failed to connect", e.getcode()
			print "[APOD]",self.error_codes.error_code_status(e.getcode())
			print "[APOD]", "Exiting..."
			return self.error_codes.err["HTTPERR"]

		except urllib2.URLError, e:
			print "[APOD]", e.args[0]
			print "[APOD]", "Internet Connection not working"
			print "[APOD]", "Exiting..."
			return self.error_codes.err["URLERR"]

	def apod_download(self):
		apod_url = self.get_apod_url();
		if (apod_url not in self.error_codes.get_error_list()):
			img_url = self.get_image_url(apod_url)
			if (img_url not in self.error_codes.get_error_list()):
				self.download_image(img_url)
			else:
				return
		else:
			return

if __name__ == "__main__":
	ec = Error_codes()
	apod = APOD_Downloader(ec)
	apod.apod_download()