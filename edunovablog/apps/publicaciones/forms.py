from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'data-role': 'tagsinput',
            'placeholder': 'Agrega tags separados por coma'
        })
    )
    class Meta:
        model = Post
        fields = ['titulo', 'subtitulo', 'contenido', 'publicado', 'categorias', 'imagen' ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'publicado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'categorias': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'imagen': forms.FileInput(attrs={'class':'form-control'})
        }