from django import forms


class EmployeeRequest(forms.Form):
    url = forms.URLField(required=True)
    user = forms.CharField(required=True)
    password = forms.CharField(required=True)
    clubid = forms.CharField(required=True)
