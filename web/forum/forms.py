from django import forms


class PostForm(forms.Form):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Сообщение'}))


class TopicForm(forms.Form):
    topic_title = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Название темы'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Сообщение'}))
