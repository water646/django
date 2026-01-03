import os
import requests
from django.contrib.auth import logout, authenticate
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework_simplejwt.tokens import RefreshToken

from firstpage.models import Chat, User, Audio
from dotenv import load_dotenv

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

load_dotenv()

guni_basedir = '/static'
run_basedir = 'http://127.0.0.1:8000/static'


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        action = data.get('action')

        if action == 'logout':
            logout(request)
            return JsonResponse({'label':5})

        if username == "" or password == "":
            return JsonResponse({'label':0})
        elif len(username) >= 20 or len(password) >= 20:
            return JsonResponse({'label':5})

        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse({'label':4})
        else:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({'access':str(refresh.access_token),'refresh':str(refresh),'label':3})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def main(request):
    if request.method == "GET":
        # user=request.session.get('username')
        user = request.user
        usermodel=User.objects.get(username=user)
        texts=list(Chat.objects.all().values())
        chatpics=[]
        for text in texts:
            chatpic=User.objects.get(username=text['outer']).headimg
            if not chatpic:
                chatpic="headimg.png"

            # chatpic=request.build_absolute_uri(f"../static/picture/{chatpic}")
            chatpic = f"{run_basedir}/picture/{chatpic}"
            # chatpic = f"/static/picture/{chatpic}"


            chatpics.append(chatpic)
        picpath=usermodel.headimg
        if not picpath:
            picpath='headimg.png'
        # pic = request.build_absolute_uri(f"../static/picture/{picpath}")
        pic = f"{run_basedir}/picture/{picpath}"
        # pic=f"/static/picture/{picpath}"
        return JsonResponse({'texts':texts,'user':user.username,'pic':pic,'chatpics':chatpics})
    if request.method == "POST":
        # data = json.loads(request.body)
        chat = request.data.get('chat')
        usname = request.user.username
        # usname = data.get('usname')
        data = Chat(text=chat,outer=usname)
        data.save()
        return JsonResponse({'success':True})

@api_view(['GET', 'POST'])
def delete(request):
    # if request.method == "POST":
    #     data = json.loads(request.body)
    #     message = data.get('dels')
    #     Chat.objects.filter(text=message).delete()
    #     return JsonResponse({'success':True})
    if request.method == "POST":
        data = json.loads(request.body)
        delelist = data.get('delelist')
        for id in delelist:
            chat = Chat.objects.filter(id=id)
            chat.delete()
        return JsonResponse({'success':True})


@api_view(['GET', 'POST'])
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if username == "" or password == "":
            return JsonResponse({'label': 0})
        elif len(username) >= 20 or len(password) >= 20:
            return JsonResponse({'label': 5})

        try:
            user = User.objects.get(username=username)
            return JsonResponse({'label':2})
        except:
            user = User(username=username)
            user.set_password(password)
            user.save()
            return JsonResponse({'label': 1})
            # data = User(username=username, password=password)
            # data.save()
            # return JsonResponse({'label': 1})


@api_view(['GET', 'POST'])
def askds(request):
    if request.method == "POST":
        data = json.loads(request.body)
        question = data.get('question')
        question += '(回答尽量精简)'

        # 构造请求头
        api_key = os.getenv('DEEPSEEK_API_KEY')
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 构造请求体
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        try:
            # 发送请求头和请求体，等待DeepSeek响应
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

        # 把回复存入session
        # request.session['response'] = response_text
        # 添加错误详情到上下文
        return JsonResponse({'answer':response_text})

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def info(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('obj')
        # master_name = request.session.get('username')
        # master = User.objects.get(username=master_name)
        master = request.user
        try:
            user=User.objects.get(username=name)
            user_dict=model_to_dict(user)

            if not user_dict['headimg']:
                user_dict['headimg'] = f"{run_basedir}/picture/headimg.png"
                # user_dict['headimg']=f"/static/picture/headimg.png"
            else:
                user_dict['headimg'] = f"{run_basedir}/picture/{user_dict['headimg']}"
                # user_dict['headimg']=f"/static/picture/{user_dict['headimg']}"
            if master.root==False:
                user_dict['password']='***'
                return JsonResponse({'success':True,'user':user_dict})
            else:
                return JsonResponse({'success':True,'user':user_dict})
        except:
            return JsonResponse({'success':False})

@api_view(['GET', 'POST'])
def baidumap(request):
    if request.method == "GET":
        ak='AweccL9v4u4lghltk5na2vcMmvjel4CH'
        website=f'https://api.map.baidu.com/api?v=3.0&ak={ak}'
        resp=requests.get(website)
        return HttpResponse(resp.content,content_type='application/javascript')

import requests
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def get_route(request):

    data = json.loads(request.body)
    origin = data.get('origin')
    destination = data.get('destination')
    method = data.get('meth')


    ak = '7QhSUO0b4IQxm7oL6MyYae2xk1EtvY9X'  # 放在后端，前端看不到

    url = f'https://api.map.baidu.com/direction/v2/{method}'
    params = {
        'origin': origin,
        'destination': destination,
        'ak': ak,
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        baidu_data = response.json()

    return JsonResponse({
                    'status': 0,
                    'result': baidu_data['result']
                })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authstatus(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'logged': True,
            'username': request.user.username
        })
    else:
        return Response({'logged': False})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def modifypwd(request):
    if request.method == "POST":
        data = json.loads(request.body)
        originpwd=data.get('originpwd')
        oncepwd=data.get('oncepwd')
        twicepwd=data.get('twicepwd')
        user = request.user
        username = user.username
        # try:
        #     basename=User.objects.get(username=username)
        # except:
        #     return JsonResponse({'logged':False})

        if user.check_password(originpwd):
            if oncepwd == twicepwd:
                user.set_password(oncepwd)
                user.save()
                return JsonResponse({'modify':0})
            else:
                return JsonResponse({'modify':1})
        else:
            return JsonResponse({'modify': 2})
        # if originpwd == basename.password:
        #         if oncepwd == twicepwd:
        #             basename.password = oncepwd
        #             basename.save()
        #             return JsonResponse({'modify':0})
        #         else:
        #             return JsonResponse({'modify':1})
        # else:
        #     return JsonResponse({'modify':2})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def uploadimg(request):
    if request.method == "POST":
        img=request.FILES.get('file')
        # username = request.session.get('username')
        user = request.user
        username = user.username

        # usermodel=User.objects.get(username=username)
        _,ext=os.path.splitext(img.name)

        img.name=user.username+ext
        user.headimg=img.name
        user.save()

        with open(f'static/picture/{img.name}','wb') as f:
            f.write(img.read())

        return JsonResponse({'logged':True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def postmusic(request):
    if request.method == "POST":
        audio=request.FILES.get('file')

        user = request.user
        username = user.username

        try:
            searchmusic = Audio.objects.get(name=audio.name)
            return JsonResponse({'success':False})
        except:
            data = Audio(name=audio.name,uploader=username)
            data.save()

            with open(f'static/music/{audio.name}','wb') as f:
                f.write(audio.read())

            return JsonResponse({'success':True})

@api_view(['GET', 'POST'])
def getmusic(request):
    if request.method == "GET":
        musics = list(Audio.objects.all().values())
        # url = request.build_absolute_uri('/static/music/')
        url = f"{run_basedir}/music/"
        # url = '/static/music/'
        return JsonResponse({'musics':musics,'url':url})

@api_view(['GET', 'POST'])
def deletemusic(request):
    if request.method == "POST":
        data = json.loads(request.body)
        deletelist = data.get('deletelist')
        for name in deletelist:
            audio = Audio.objects.get(name=name)
            audio.delete()
        return JsonResponse({'success':True})





