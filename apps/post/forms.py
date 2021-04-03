from django import forms

from apps.post.models import Post, Comment


class PostModelForm(forms.ModelForm):
    # a form for Post model to create and update a post
    class Meta:
        model = Post
        # other fields will added automatically
        fields = ['content', 'image']


class CommentModelform(forms.ModelForm):
    # a form for Comment model to create a comment
    body = forms.CharField(label='',
                           widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))

    class Meta:
        model = Comment
        fields = ['body']
