# encoding: utf-8
"""
Create on: 2018-09-25 下午2:22
author: sato
mail: ysudqfs@163.com
life is short, you need python
"""

# 版本号规则验证
import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets


def version_validate(value):
    version = re.match('\d{1,2}\.\d{1,3}\.\d*$',value)
    if not version :
        raise ValidationError('版本号格式错误')


def app_validate(value):
    app = re.match('.*(apk|exe|mar|ipa|dmg|rpm|deb)$',value.name)
    if not app :
        raise ValidationError('客户端类型错误')


class upClientForm(forms.Form):
    name = forms.CharField(label='客户端名称',
        initial='Android SDK',
        max_length=50,
        error_messages={'required': '名称不能为空'},
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'Android SDK'}))

    description = forms.CharField(label='描述信息',
        max_length=100,
        error_messages={'required': 'aaaaaa',},
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'修复 XXX BUG'}))

    mark = forms.CharField(label='企业标识',
        initial='comm',
        max_length=10,
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'comm'}))

    version = forms.CharField(label='版本号',
        max_length=20,
        validators=[version_validate,],
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'1.5.1'}))

    force_verison = forms.CharField(label='强制升级版本号',
        initial='1.2.1',
        max_length=20,
        validators=[version_validate,],
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'1.0.1'}))

    device_type = forms.ChoiceField(label='客户端类型',
        choices=(('mobile-android','android sdk'),
            ('pc-win','windows'),
            ('pc-osx','max'),
            ('mobie-ios','ios sdk'),
            ('pc-linux-mips64-deepin','国产深度'),
            ('pc-linux-arm64-neokylin','中标麒麟'),
            ('pc-linux-arm64-zkfd','中科方德'),
            ('mobile-yuanxin','元心'),
            ('pc-linux-arm64-kylin','银河麒麟'),
            ('pc-linux-x86_64-ubuntu','ubuntu'),
            ),
        widget=widgets.Select(attrs={'class':'form-control','placeholder':'1.0.1'}))
    # package = fields.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})) # 多个文件
    files = forms.FileField(label='客户端文件',
        validators=[app_validate,],
        )