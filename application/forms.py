# -*- coding: utf-8 -*-
from django import forms
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _

from application.models import Postdoc, Research


class PostdocForm(forms.ModelForm):

    class Meta:
        model = Postdoc
        exclude = ['date']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'required': "",
                                     'data-error': _('This field must be filled.')}),
            'email': TextInput(attrs={
                'class': 'form-control', 'type': 'email', 'data-error': _('Incorrect e-mail'),
                'pattern': '^[_A-Za-z0-9-\+]+(\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\.[A-Za-z0-9]+)*(\.[A-Za-z]{2,})$'}),
            'cpf': TextInput(attrs={'class': 'form-control'}),
            'passport': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control telephone_number', 'pattern': '^[+- ()0-9]+'}),
            'mobile_phone': TextInput(attrs={'class': 'form-control telephone_number', 'pattern': '^[+- ()0-9]+'}),
        }


class ResearchForm(forms.ModelForm):

    class Meta:
        model = Research
        fields = ['name', 'affiliation', 'email']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': _('Name')}),
            'affiliation': TextInput(attrs={'class': 'form-control', 'placeholder': _('Affiliation')}),
            'email': TextInput(attrs={
                'class': 'form-control', 'type': 'email', 'data-error': _('Incorrect email'), 'placeholder': _('Email'),
                'pattern': '^[_A-Za-z0-9-\+]+(\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\.[A-Za-z0-9]+)*(\.[A-Za-z]{2,})$'}),
        }
