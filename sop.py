#!/usr/bin/env python
# coding:utf-8

import json
import requests
import os
import os.path
import subprocess

import time
t = time.localtime()
path_name = f'pixiv-{t.tm_year}-{t.tm_mon}-{t.tm_mday}/'

rank_url = 'https://www.pixiv.net/ranking.php'

headers = {'Host': 'pixiv.net',
		   'User-Agent': 'Mozilla/5.0 (Android 6.0; Mobile; rv:60.0) Gecko/60.0 Firefox/60.0',
		   'Referer': 'https://www.pixiv.net/'}


def get_page(p):
	url = f'{rank_url}?format=json&p={p}'
	print(f'Get page {p}')
	cmd = f'curl -o {path_name}page-{p}.json {url}'
	print(cmd)
	proc = subprocess.Popen(cmd , stdin=subprocess.DEVNULL,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	output, error = proc.communicate()
	print(output.decode(), error.decode())
	print(f'Get page {p} Success')


def load_page(p):
	print(f'Load page {0}')
	with open(path_name + f'page-{p}.json', 'r') as f:
		data = json.load(f)
	image_list = {}
	for image_data in data['contents']:
		r = get_image(image_data)
		if r:
			image_list.update(r)
	with open(path_name + f'image_url-{p}.json', 'w') as f:
		json.dump(image_list, f)
	print(f'Load page {0} and generate image url list Success')


def get_image(data):
	print(f'Get image {data["rank"]}')
	url = data['url'].replace('c/240x480/img-master/', 'img-original/').replace('_master1200', '')
	rank = int(data['rank'])
	title = data['title']
	page_count = int(data['illust_page_count'])
	if page_count > 5:
		return {}
	extensions = ['png', 'jpg', 'gif']
	ext_s = 'png'
	for ext in extensions:
		real_url = url.replace('.jpg', '.'+ext)
		proc = subprocess.Popen(f"wget --referer 'https://www.pixiv.net/' --user-agent 'Mozilla/5.0 (Android 6.0; Mobile; rv:60.0) Gecko/60.0 Firefox/60.0' --spider {real_url}" , stdin=subprocess.DEVNULL,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		output, error = proc.communicate()
		sta = error.strip().split(b'\n')[-1]
		if(sta == b'Remote file exists.'):
			print(f'Sure that image extension is {ext}')
			ext_s = ext
			break
	else:
		print('Can not sure image extension')
		print(f'Get image {rank} Fail')
		return {}
	url = url.replace('.jpg', '.'+ext_s)
	url_list = {}
	for count in range(page_count):
		url_list[f'{rank}-{count}.{ext_s}'] = (url.replace('_p0', f'_p{count}'))
	print(f'Get image {rank} Success')
	return url_list


def download_image(p):
	with open(path_name + f'image_url-{p}.json', 'r') as f:
		image_list = json.load(f)
	for name in image_list:
		print(f'Get {name}')
		proc = subprocess.Popen(f"wget --referer 'https://www.pixiv.net/' --user-agent 'Mozilla/5.0 (Android 6.0; Mobile; rv:60.0) Gecko/60.0 Firefox/60.0' -O {path_name}{name} {image_list[name]}" , stdin=subprocess.DEVNULL,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		output, error = proc.communicate()
		print('Ok')


if __name__ == "__main__":
	if not os.path.exists(path_name):
		os.mkdir(path_name)
		print("Create path:" + path_name)
	get_page(0)
	input()
	load_page(0)
	download_image(0)
