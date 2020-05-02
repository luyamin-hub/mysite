from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.generic import FormView
from .models import  UserExtension

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名或邮箱', 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名或邮箱'})
    )
    password = forms.CharField(label='密码', 
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        #判断用户名和密码是否都正确
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            #判断填入的邮箱是否存在，并取出该用户名所对应的用户
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                #判断密码的合法性
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(
        label='用户名', 
        max_length=30,
        min_length=3,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30位用户名'})
    )
    email = forms.EmailField(
        label='邮箱', 
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'})
    )
    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
        )
    )
    password = forms.CharField(
        label='密码', 
        min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'})
    )
    password_again = forms.CharField(
        label='再输入一次密码', 
        min_length=6,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再输入一次密码'})
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断验证码
        code = self.request.session.get('register_verification_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code


            
class ModifyForm(forms.Form):
    #required=True 是指输入框为输入框的形式，否则为显示框
    username = forms.CharField(label='用户名',
                               min_length=2,
                               max_length=30,
                               widget=forms.TextInput(
                                             attrs={'class':'form-control','placeholder':'请输入3-30位用户名'}))
    nickname = forms.CharField(label='昵称',
                               min_length=2,
                               max_length=30,
                               required=False,
                               widget=forms.TextInput(
                                             attrs={'class':'form-control','placeholder':'请输入2-30位昵称'}))
    sex = forms.ChoiceField(label='性别',
                            required=False, 
                            choices=[('---','---'),('男', '男'), ('女', '女'), ('保密', '保密')]) 
 

    telephone = forms.CharField(label='电话',
                                min_length=7,
                                max_length=12,
                                required=False,
                                widget=forms.TextInput(
                                             attrs={'class':'form-control','placeholder':'请输入7-12位电话'}))
    user_logo = forms.FileField(label='头像',
                                 required=False)
    qq_number = forms.CharField(label='QQ号',
                              min_length=8,
                              max_length=15,
                              required=False,
                              widget=forms.TextInput(
                                           attrs={'class':'form-control','placeholder':'请输入8-15位QQ号'}))  
    birthday = forms.DateTimeField(label='出生日期',
                                    required=False,
                                    widget=forms.DateTimeInput(
                                               attrs={'class':'form-control','placeholder':'请输入出生日期'}))                   
    school = forms.CharField(label='学校名称',
                               min_length=4,
                               max_length=15,
                               required=False,
                               widget=forms.TextInput(
                                             attrs={'class':'form-control','placeholder':'请输入4-15位学校名称'}))
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ModifyForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        user_id=self.user.id
        username = self.cleaned_data['username']
        if User.objects.exclude(id=user_id).filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username
        
    def clean_nickname(self):
        user_id=self.user.id
        nickname = self.cleaned_data['nickname']
        if nickname :
            if UserExtension.objects.exclude(id=user_id).filter(nickname=nickname).exists():
                raise forms.ValidationError('昵称已存在')
        return nickname

    def clean_sex(self):
        sex = self.cleaned_data['sex']
        return sex

    def clean_telephone(self):
        user_id=self.user.id
        telephone = self.cleaned_data['telephone']
        if telephone :
           if UserExtension.objects.exclude(id=user_id).filter(telephone=telephone).exists():
              raise forms.ValidationError('该电话已存在')
        return telephone
    
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='旧的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入旧的密码'}
        )
    )
    new_password = forms.CharField(
        label='新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的密码'}
        )
    )
    new_password_again = forms.CharField(
        label='请再次输入新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请再次输入新的密码'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 验证新的密码是否一致
        new_password = self.cleaned_data.get('new_password', '')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        # 验证旧的密码是否正确
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧的密码错误')
        return old_password

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class':'form-control', 'placeholder':'请输入绑定过的邮箱'}
        )
    )

    new_password = forms.CharField(
        label='新的密码', 
        widget=forms.PasswordInput(
            attrs={'class':'form-control', 'placeholder':'请输入新的密码'}
        )
    )

    verification_code = forms.CharField(
        label='验证码',
        required=False,
        widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}
        )
    )
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        # 判断验证码
        code = self.request.session.get('forgot_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return verification_code        

