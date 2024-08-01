from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    image = forms.ImageField(
        label="Photo",
        error_messages={
            "required": "It is required field",
            "invalid_image": "It is wrong image format"
        }
    )
    description = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Enter description (optional)"})
    )

    class Meta:
        model = Photo
        fields = ['image', 'description']
