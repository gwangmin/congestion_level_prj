from django import forms
from .models import Facility, Building, CCTV

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'intro', 'addr', 'web_addr', 'phone_num']

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'intro']

class CCTVForm(forms.ModelForm):
    class Meta:
        model = CCTV
        fields = ['rtsp_url'] # building 추가

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['subject', 'content'] # 폼에서 사용할 속성
#         widgets = {
#             'subject': forms.TextInput(attrs={'class': 'form-control'}),
#             'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
#         }
#         labels = {
#             'subject': '제목',
#             'content': '내용',
#         }
