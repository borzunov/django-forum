from django import forms


class PostForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Message'}))


class TopicForm(forms.Form):
    topic_title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Message'}))
