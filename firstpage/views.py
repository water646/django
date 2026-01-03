import os
import requests
import json
from django.http import JsonResponse

from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render,redirect

from .models import Chat,User
from dotenv import load_dotenv

#步骤：修改settings的INSTALLED_APP，编写函数，设置路由，修改网页为模板，
#注意变量使用双括号，语句使用括号百分号，可能需要设置时区

load_dotenv()

def index(request,usname):
    if request.method == "GET":
        texts=Chat.objects.all()

        # 获取session中的deepseek回复
        response=request.session.get('response')
        if response:        #获取后删除session
            del request.session['response']

        return render(request,'design1.html',context={'texts':texts,'usname':usname,'response':response})
    if request.method == "POST":
        chat=request.POST.get('shurukuang')
        usname=request.POST.get('usname')
        data=Chat(text=chat,outer=usname)
        data.save()
        texts = Chat.objects.all()

        context={'texts':texts,'usname':usname}

        return render(request,'design1.html',context=context)

def for_delete(request):
    if request.method == "POST":
        place=request.POST.get('dlt_num')
        usname=request.POST.get('usname')
        dlt=Chat.objects.filter(text=place)
        dlt.delete()
        return redirect('index',usname=usname)

def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username=="" or password=="":
            return render(request,'login.html',context={'label':2})

        if 'register' in request.POST:  #若为注册
            try:        #检测账号是否存在
                find=User.objects.get(username=username)
                return render(request,'login.html',context={'label':1})
            except:     #不存在则注册成功
                new_user=User(username=username,password=password)
                new_user.save()
                return render(request,'login.html',context={'label':0})

        if 'login' in request.POST:     #若为登录
             try:   #若账号存在
                check=User.objects.get(username=username)
                if check.password == password:
                   return redirect('index',usname=username)
                else:
                    return render(request,'login.html',context={'label':3})
             except:  #若账号不存在
                 return render(request,'login.html',context={'label':3})

def askds(request):
    if request.method == "POST":
        usname=request.POST.get('usname')
        question=request.POST.get('question')
        question=question+"(回答尽量精简)"

        # 构造请求头
        api_key = os.getenv('DEEPSEEK_API_KEY')
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        #构造请求体
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        try:
            #发送请求头和请求体，等待DeepSeek响应
            api_response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                json=data,
                headers=headers,
                timeout=15
            )

            # 如果状态码=200，表示成功
            if api_response.status_code == 200:
                response_json = api_response.json()  # 把返回的JSON数据转化为python字典
                if 'choices' in response_json and len(
                        response_json['choices']) > 0:  # 检查字典是否存在choice字段，且choice不为空，说明deepseek给了回复
                    response_text = response_json['choices'][0]['message']['content']  # 那就获取第一条回复的文本内容
                else:
                    error_details = "响应中缺少 'choices' 字段"  # 不存在choice的错误处理
                    response_text = f"API 响应格式错误: {json.dumps(response_json, indent=2)}"
            else:
                error_details = f"API 错误: {api_response.status_code}"  # deepseek回应失败的错误处理
                response_text = f"请求失败: {api_response.text}"

        except Exception as e:
            error_details = f"异常错误: {str(e)}"
            response_text = f"请求处理失败: {str(e)}"

        #把回复存入session
        request.session['response'] = response_text
        # 添加错误详情到上下文
        return redirect('index',usname=usname)

def redir(request):
    if request.method == "GET":
        return redirect('login')

def outer(request):
    if request.method == "GET":
        return render(request, 'vue_test.html')








