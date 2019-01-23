from django import forms


class IssueForm(forms.Form):
    post = forms.CharField(widget=forms.TextInput(
#        attrs={
#            'class': 'form-control',
#            'placeholder': 'Write a post...'
#        }
    ))


# fields = ('post',)