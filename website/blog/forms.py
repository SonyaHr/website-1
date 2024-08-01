from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory
from .models import Post, Profile, Comment, Tag, Photo, Subscriber, PostImage

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']

PostImageFormSet = modelformset_factory(PostImage, fields=['image'], extra=1, can_delete=True)

class UserRegistrationForm(UserCreationForm):
    telephone = forms.CharField(max_length=10)
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(user=user, telephone=self.cleaned_data['telephone'], avatar=self.cleaned_data['avatar'])
        return user

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    username = forms.CharField(max_length=30, required=True, help_text='Required.')
    telephone = forms.CharField(max_length=20, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'username', 'telephone', 'avatar']

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        profile.telephone = self.cleaned_data['telephone']
        profile.avatar = self.cleaned_data['avatar']
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            profile.save()
            user.save()
        return profile

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(label='Your email', max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))

    class Meta:
        model = Subscriber
        fields = ['email']

class PhotoForm(forms.ModelForm):
    image = forms.ImageField(
        label="Photo",
        error_messages={
            "required": "It is required field",
            "invalid_image": "It is wrong image format"
        }
    )

    class Meta:
        model = Photo
        fields = ['image']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'telephone']
