import requests
import json
import sys
from flask import Flask,url_for,render_template, flash, request, redirect
from wtforms import Form
import gc
import os

app=Flask(__name__)
app.config['DEBUG'] = True

@app.route('/', methods=['GET','POST']) 
def hello():
    return render_template('home.html');

@app.route('/output/' , methods=['GET','POST'])
def output():
	repository = request.args['repo']
	page_number = request.args.get('page-no', '1')
	url = 'https://api.github.com/search/issues?q='+ repository +'&page='+page_number+'&per_page=10'
	r = requests.get(url)
	data = json.loads(r.text)
	repo_arr=[]
	title_arr=[]
	no_arr=[]
	name_arr=[]
	time_arr=[]
	url_arr=[]
	body_arr=[]
	length = len(data['items'])
	if length==0 :
		return render_template('error.html')
	for i in range (0, length):
		a = data['items'][i]['repository_url']		
		abc=a.split('/')
		repo=abc[-2]+'/'+abc[-1]
		repo_arr.append(repo)	
		title=data['items'][i]['title']
		title_arr.append(title)
		url=data['items'][i]['html_url']
		url_arr.append(url);	
		no=str (data['items'][i]['number'])
		no_arr.append(no)	
		name=data['items'][i]['user']['login']
		name_arr.append(name)
		body=data['items'][i]['body']
		body_arr.append(body)
		t=str(data['items'][i]['created_at'])
		arr=t.split('T')
		time=arr[0]
		time_arr.append(time)
		count = data['total_count']
	return render_template('output.html',url_arr=url_arr, repo_arr=repo_arr, length=length, title_arr=title_arr, no_arr=no_arr, name_arr=name_arr, time_arr=time_arr, count=count, body_arr=body_arr)

if __name__=='__main__':
    app.run()
