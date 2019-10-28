from django import forms
from .models import Movie, Comment

YEARS= [x for x in range(1940,2021)]


class MovieForm(forms.ModelForm):

    open_date = forms.DateField(
        widget=forms.SelectDateWidget(years=YEARS),
    )

    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ['title', ]


class CommentForm(forms.ModelForm):

    content = forms.CharField(
        label='한줄평',
    )

    class Meta:
        model = Comment
        fields = ['content', 'score', ]
