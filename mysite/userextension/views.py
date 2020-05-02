import string
import random
import time
import os
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import  UserExtension
from .forms import LoginForm,RegForm,ModifyForm,ChangePasswordForm,ForgotPasswordForm
  
def login_for_modal(request): 
    if request.method == 'POST': 
      data = {}
      login_form = LoginForm(request.POST)
      if login_form.is_valid():
          user = login_form.cleaned_data['user']
          auth.login(request, user)
          data['status'] = 'SUCCESS'
      else:
          data['status'] = 'ERROR'
    return JsonResponse(data)

# def login(request): 
#      if request.method == 'POST':
#        login_form = LoginForm(request.POST)
#        if login_form.is_valid():
#            user = login_form.cleaned_data['user']
#            auth.login(request,user)
#            return redirect(request.GET.get('from',reverse('home')))
#      else:
#          login_form = LoginForm()    
#      context = {}
#      context['login_form'] = login_form
#      return render(request,'login.html',context)

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 清除session
            del request.session['register_verification_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()    
    context = {}
    context['reg_form'] = reg_form
    return render(request,'register.html',context)

#发送验证码
def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}

    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now            
            # 发送邮件
            send_mail(
                '博客主题：%s' % send_for,
                '验证码：%s' % code,
                '2039013391@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
#登出
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))
#个人用户信息
def user_info(request):
    context = {}
    return render(request, 'user_info.html', context)
#修改用户个人信息
def modify(request,user_id):
    redirect_to = reverse('home')
    if request.method == 'POST':
       modify_form = ModifyForm(request.POST,request.FILES,user=request.user)
       if modify_form.is_valid():
           username = modify_form.cleaned_data['username']
           nickname = modify_form.cleaned_data['nickname']
           sex = modify_form.cleaned_data['sex']
           telephone = modify_form.cleaned_data['telephone']
           new_user_logo = modify_form.cleaned_data['user_logo']
           qq_number = modify_form.cleaned_data['qq_number']
           birthday = modify_form.cleaned_data['birthday']
           school = modify_form.cleaned_data['school']
           old_user_logo = get_object_or_404(User,id=user_id).extension.user_logo           
           #修改用户
           user=get_object_or_404(User,id=user_id)
           user.username = username
           #如果上传照片
           if new_user_logo:
              # 设置新图片保存路径
              new_fname='%s/user/%s'%(settings.MEDIA_ROOT,new_user_logo.name)
              # 将新图片写入保存路径
              fn = open(new_fname,'wb')
              for img in new_user_logo.chunks():
                  fn.write(img)
              fn.close()
              user.extension.user_logo = new_user_logo
              #判断旧照片是否存在
              if old_user_logo:
                #设置旧照片保存路径
                old_fname = '%s/%s'%(settings.MEDIA_ROOT,old_user_logo.name)
                #将旧照片删除
                os.remove(old_fname)  
           #如果不上传照片   
           else:
                user.extension.user_logo = old_user_logo
           user.extension.nickname = nickname
           user.extension.sex = sex
           user.extension.telephone = telephone
           user.extension.qq_number = qq_number
           user.extension.birthday = birthday
           user.extension.school = school
           user.save()
           #登录用户
           user = auth.authenticate(username=username)
           auth.login(request,user)
           return redirect(request.GET.get('from',reverse('home')))
    else:
        user=get_object_or_404(User,id=user_id)
        modify_form = ModifyForm(initial={'username':user.username, 'nickname':user.extension.nickname,
                                       'sex':user.extension.sex,'telephone':user.extension.telephone,
                                       'user_logo':user.extension.user_logo,'qq_number':user.extension.qq_number,
                                       'birthday':user.extension.birthday,'school': user.extension.school })                                      
    context = {}
    context['page_title'] = '个人资料修改'
    context['form_title'] = '个人资料修改'
    context['submit_text'] = '保存'
    context['return_back_url']= redirect_to
    context['form'] = modify_form
    context['form_type'] = 'ModifyForm'
    return render(request,'form.html',context)
#登录后修改密码
def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '保存'
    context['form'] = form
    context ['form_type'] = 'ChangePasswordForm'
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

#登录前修改密码
def forgot_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '保存'
    context['form'] = form
    context['form_type'] = 'ForgotPasswordForm'
    context['return_back_url'] = redirect_to
    return render(request, 'forgot_password.html', context)
