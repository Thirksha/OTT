from django import forms
from .models import User, Movies, Kids, Subscriber,UserProfile,Tv_shows,Episode,Season, CustomAdminUser


class MyLoginForm(forms.Form):
    # create two fields in the form for user and password
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    # only thing we have do is compare password
    # creating a charfield obj by passing value into the constructor

    class Meta:
        # In Meta , we specify which model the form is for and the fields
        model = User
        fields = ('username', 'first_name', 'email', 'password')

    # nameing convention is clean _<field_name
    def clean_password2(self):
        # clean the in the context
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password not matching')
        return cd['password2']


class SubscriberRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    # only thing we have do is compare password
    # creating a charfield obj by passing value into the constructor

    class Meta:
        # In Meta , we specify which model the form is for and the fields
        model = User
        fields = ('username', 'first_name', 'email', 'password')

    # nameing convention is clean _<field_name
    def clean_password2(self):
        # clean the in the context
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password not matching')
        return cd['password2']




class MovieForm(forms.ModelForm):
   class Meta:
      model = Movies
      fields = ['category', 'subcategory', 'title', 'description', 'duration', 'language', 'image', 'video_url']

class EditMovieForm(forms.ModelForm):
   class Meta:
      model = Movies
      fields = ['category', 'subcategory', 'title', 'description', 'duration', 'language', 'image', 'video_url']



class KidsForm(forms.ModelForm):
    class Meta:
        model = Kids
        fields = ['category', 'subcategory', 'title', 'description', 'duration', 'language', 'image', 'video_url']


class EditKidsForm(forms.ModelForm):
    class Meta:
        model = Kids
        fields = ['category', 'subcategory', 'title', 'description', 'duration', 'language', 'image', 'video_url']



class SeriesForm(forms.ModelForm):
    class Meta:
        model = Tv_shows
        fields = ['category', 'subcategory', 'title', 'description', 'language', 'image']

class EditSeriesForm(forms.ModelForm):
    class Meta:
        model = Tv_shows
        fields = ['category', 'subcategory', 'title', 'description', 'language', 'image']



# class for add form of season
class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields =['season_number']


# class for add form of episode
class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields =['title','episode_number','release_date','duration','video_url']





class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'age', 'gender', 'email', 'phone_number']



class CustomAdminUserForm(forms.ModelForm):
    class Meta:
        model = CustomAdminUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']


