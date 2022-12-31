from bs4 import BeautifulSoup
from contextlib import closing
import requests
import getpass
import urllib3
import time
import sys
import os
import re
import hashlib
from PrettyPrint import *
from MyEncrypt import *
from ProgressBar import *
from hurry.filesize import size
import urllib.parse

def resume_download(res, video_url, filepath_name, savename, pos):
	resume_byte_pos = pos
	resume_header = {
		"Accept"           : "text/html,application/xhtml+xml,application/xml;\
	q=0.9,*/*;q=0.8",
		"Accept-Encoding"  : "gzip, deflate, br" ,
		"Accept-Language"  : "zh-TW" ,
	'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4)\
	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
		"Cache-Control": "max-age=0",
		"Upgrade-Insecure-Requests": "1",
		"Referer": "https://nportal.ntut.edu.tw/index.do?thetime=1556366755131",
		"Range": "bytes=%d-" % resume_byte_pos
	}
	print("啟動續傳，已下載: {:.2f} MB 原始: {}".format(resume_byte_pos/1024/1024, resume_byte_pos))

	with closing(res.get(video_url, headers=resume_header, stream=True, verify=False, allow_redirects=True )) as response:
		#處理下載大小進度條
		if response.headers.__contains__('content-length'):
			file_size = response.headers['content-length']  
		else:
			file_size = 0
		chunk_size = 1024 # 單次請求最大值
		content_size = int(file_size) # 內容體總大小
		progress = ProgressBar(savename+"續傳", total=content_size,
											unit="KB", chunk_size=chunk_size, run_status="正在下載", fin_status="下載完成")
		with open(filepath_name,'ab') as file:
			for data in response.iter_content(chunk_size=chunk_size):
				file.write(data)
				progress.refresh(count=len(data))
				
		file.close()
		progress.endPrint()