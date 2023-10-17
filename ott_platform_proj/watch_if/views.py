from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .forms import UserRegistrationForm, MovieForm,  KidsForm, SubscriberRegistrationForm, UserProfileForm, MyLoginForm, EditMovieForm,EditKidsForm,SeriesForm,SeasonForm,EpisodeForm, CustomAdminUserForm, EditSeriesForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Movies, Tv_shows, Kids, Episode, Season, User,  Subscription, ViewedContent, Favorite,Subscriber, ContentType, CustomAdminUser
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.urls import reverse

# def Index(request):
#     return HttpResponse("<h1>cccWELCOME!!!!!</h1>")

def user_list(request):
    try:
        group = Group.objects.get(name='creator')
    except Group.DoesNotExist:
        group = None

    if group:
        users = User.objects.filter(groups=group)
        return render(request, 'admin_homepg.html', {'group_name': group, 'users': users})
    else:
        # Handle the case where the group doesn't exist
        return render(request, 'account/group_not_found.html', {'group_name': group})


def toggle_user_status(request, user_id):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f"user {user.username}'s status has been updated. ")
    else:
        messages.error(request, "You do not have permission")

    return redirect('user_list')

def home(request):
    return render(request, template_name='jumbo.html')

def logo(request):
    return render(request, template_name='power_puff_title.html')

def watchif(request):
    return render(request, template_name='title_name_watchif.html')


def register(request):
    if request.method == 'POST':
        #WILL GET THE POSTED VAR FROM   UserRegistrationForm
        user_reg_form = UserRegistrationForm(request.POST)
        #CHECKING IF THE POSTED REQUEST PARAMATERS ARE VALID
        if user_reg_form.is_valid():
            #receive the data, create the form, keep it temporarily without saving
            new_user= user_reg_form.save(commit=False)
            #set the password with the cleaned data for password
            #cleaned_data will automatically be calling the forms clean_password function
            new_user.set_password(user_reg_form.cleaned_data['password'])
            #permanently save the new user
            new_user.save()
            creator_group = Group.objects.get(name="creator")
            new_user.groups.add(creator_group)
            #after saving, render or display the template register_done.html
            return render(request,'account/register_done.html',{'user_reg_form':user_reg_form})
    else:     #if the user registration form is not valid or not submitted
     #in that case give the user, the blank registration form register.html
        user_reg_form = UserRegistrationForm()
    #IF THE USER IS NOT SUBMITTING the form,
    return render(request, 'account/register.html', {'user_reg_form': user_reg_form})

def register_subscriber(request):
    if request.method == 'POST':
        #WILL GET THE POSTED VAR FROM   UserRegistrationForm
        subscriber_reg_form = SubscriberRegistrationForm(request.POST)
        #CHECKING IF THE POSTED REQUEST PARAMATERS ARE VALID
        if subscriber_reg_form.is_valid():
            #receive the data, create the form, keep it temporarily without saving
            new_user= subscriber_reg_form.save(commit=False)
            #set the password with the cleaned data for password
            #cleaned_data will automatically be calling the forms clean_password function
            new_user.set_password(subscriber_reg_form.cleaned_data['password'])
            #permanently save the new user
            new_user.save()
            #add the user by default to the reviewers group
            subscriber_group = Group.objects.get(name='subscriber')
            new_user.groups.add(subscriber_group)

            #after saving, render or display the template register_done.html
            return render(request,'account/register_done.html',{'subscriber_reg_form':subscriber_reg_form})
    else:     #if the user registration form is not valid or not submitted
     #in that case give the user, the blank registration form register.html
     subscriber_reg_form = SubscriberRegistrationForm()
    #IF THE USER IS NOT SUBMITTING the form,
    return render(request, 'account/register_subscriber.html', {'subscriber_reg_form': subscriber_reg_form})

def user_login_view(request):
    if request.method == 'POST':
        #WILL GET THE POSTED VAR FROM MyLoginForm
        login_form = MyLoginForm(request.POST)
        #CHECKING IF THE POSTED REQUEST PARAMATERS ARE VALID
        if login_form.is_valid():
            #sanitizing the input using the cleaned_data attribute
            cleaned_data = login_form.cleaned_data
            #now we can proceed with the authentication
            auth_user = authenticate(request, username=cleaned_data['username'], password=cleaned_data['password'])
            if auth_user is not None:
                #if the aunthenticate fn returned a valida user
                #perform the login
                login(request, auth_user)
                return HttpResponse('<h1>Authenticated</h1>')
            else:
                return HttpResponse('<h1>Not Authenticated</h1>')

    else:
        #if the form submission was not POST, give login again
        login_form =MyLoginForm()

    return render(request, 'useraccount/userlogin.html', {'login_form':login_form})

def content_creator_home(request):
    return render(request, template_name='content_creator_homepg.html')

@login_required
def add_content_movies(request):
    if request.method == 'POST':
        # Process the form data for each content type
        movie_form = MovieForm(request.POST, request.FILES)
        # tv_show_form = TVShowForm(request.POST, request.FILES)
        # kids_form = KidsForm(request.POST, request.FILES)

        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.content_creator = request.user  # Assign the content creator
            movie.save()

        return redirect('movies')


    else:
        movie_form = MovieForm()
        # tv_show_form = TVShowForm()
        # kids_form = KidsForm()

    return render(request, 'account/add_content.html', {

        'movie_form': movie_form,})
        # 'tv_show_form': tv_show_form,
        # 'kids_form': kids_form,
@login_required
def edit_content_movies(request, movies_id):
    #get the get method variable and passing that along with the model
    post_details = get_object_or_404(Movies, id=movies_id)
    print(post_details)
    edit_post_form = EditMovieForm(request.POST or None, request.FILES or None, instance=post_details)
    # checking if the user posted the form by clicking submit
    if edit_post_form.is_valid():  #this will be true if the user is submitting the form
        # save the changes to database
        edit_post_form.save()
        # if save successful, redirect the user to homepage or listing page
        return redirect('movies')

        # IF THE USER IS NOT SUBMITTING the form,  render the fresh add post form
    return render(request, 'account/edit_content_movies.html', {'edit_post_form': edit_post_form})

@login_required
def delete_movies(request, movies_id):
    #get the get method variable and passing that along with the model
    post_details = get_object_or_404(Movies, id=movies_id)
    post_details.delete()
    return redirect('home_path')





@login_required
def add_content_kids(request):
    if request.method == 'POST':
        kids_form = KidsForm(request.POST, request.FILES)
        if kids_form.is_valid():
            kids_instance = kids_form.save(commit=False)
            kids_instance.content_creator = request.user
            kids_instance.save()
            return redirect('kids_content')  # Assuming you have a URL pattern named 'kids_content' for displaying kids' content
    else:
        kids_form = KidsForm()

    return render(request, 'account/add_content_kids.html', {
        'kids_form': kids_form,
    })


@login_required
def edit_content_kids(request, kids_id):
    #get the get method variable and passing that along with the model
    post_details = get_object_or_404(Kids, id=kids_id)
    print(post_details)
    edit_kids_form = EditKidsForm(request.POST or None, request.FILES or None, instance=post_details)
    # checking if the user posted the form by clicking submit
    if edit_kids_form.is_valid():  #this will be true if the user is submitting the form
        # save the changes to database
        edit_kids_form.save()
        # if save successful, redirect the user to homepage or listing page
        return redirect('kids_content')

        # IF THE USER IS NOT SUBMITTING the form,  render the fresh add post form
    return render(request, 'account/edit_content_kids.html', {'edit_kids_form': edit_kids_form})

@login_required
def delete_kids(request, kids_id):
    #get the get method variable and passing that along with the model
    kids_content  = get_object_or_404(Kids, id=kids_id)
    kids_content .delete()
    return redirect('home_path')

@login_required()
def add_series(request):
    if request.method == 'POST':
        series_form = SeriesForm(request.POST, request.FILES)
        season_form = SeasonForm(request.POST)

        if series_form.is_valid() and season_form.is_valid():
            series = series_form.save(commit=False)
            season = season_form.save(commit=False)

            season.tv_show = series

            series.save()
            season.save()
            return redirect('tv_shows')  # Redirect to a success page
    else:
        series_form = SeriesForm()
        season_form = SeasonForm()

    return render(request, 'account/add_content_tv_shows.html', {
        'series_form': series_form,
        'season_form': season_form,
    })



@login_required
def add_episode(request, tv_show_id, season_id):
    if request.method == 'POST':
        episode_form = EpisodeForm(request.POST)
        if episode_form.is_valid():
            episode = episode_form.save(commit=False)


            episode.tv_show_id = tv_show_id
            episode.season_id = season_id

            episode.save()

            return redirect('tv_shows')
            # Redirect or process as needed
    else:
        episode_form = EpisodeForm()

    return render(request, 'account/add_episode.html', {
        'episode_form': episode_form,
    })





def content_creator_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_content_creator:  # Assuming you have an 'is_content_creator' attribute in your User model
            login(request, user)
            # Redirect to the content creator dashboard or any other page
            return redirect('content_creator_dashboard')  # Change 'content_creator_dashboard' to your actual content creator dashboard URL name
        else:
            # Handle invalid login credentials here
            # You can add an error message and display it in the template
            return render(request, 'content_creator_login.html', {'error': 'Invalid login credentials'})

    return render(request, 'content_creator_login.html')

def content_creator_homepg(request):
    # Your view logic here
    return render(request, 'content_creator_homepg.html')


def movies_view(request):
        search_term = request.GET.get('searchpost')
        if search_term:
            # if there is a valid search term, filter the list of objects with it
            movies_list = Movies.objects.filter(title__icontains=search_term)
        else:
            movies_list = Movies.objects.all()


        # movies_list = Movies.objects.all()
        # print(movies_list)
        return render(request, 'movies_template.html', {'search_term':search_term ,'movies_list': movies_list})

def movies_details(request, movies_id):
    movies = get_object_or_404(Movies, id=movies_id)
    return render(request, 'movies_details.html', {'movies': movies})


def tv_shows_view(request):
    search_term = request.GET.get('searchpost')
    if search_term:
        # if there is a valid search term, filter the list of objects with it
        tv_shows = Tv_shows.objects.filter(title__icontains=search_term)
    else:
        tv_shows = Tv_shows.objects.all()
    #tv_shows = Tv_shows.objects.all()
    return render(request, 'tv_shows_template.html', {'search_term':search_term ,'tv_shows': tv_shows})



def tv_shows_details(request, tv_shows_id):
    tv_show = get_object_or_404(Tv_shows, id=tv_shows_id)
    seasons = Season.objects.filter(tv_show=tv_show).first()
    episodes = Episode.objects.filter(season=seasons)



    print(tv_show)
    print(seasons)
    print(episodes)

    return render(request, 'tv_shows_details.html', {'tv_show': tv_show, 'seasons': seasons, 'episodes': episodes})


def kids_content_view(request):
    search_term = request.GET.get('searchpost')
    if search_term:
        # if there is a valid search term, filter the list of objects with it
        kids_contents = Kids.objects.filter(title__icontains=search_term)
    else:
        kids_contents = Kids.objects.all()
    #kids_contents = Kids.objects.all()
    return render(request, 'kids_template.html', {'search_term':search_term ,'kids_contents': kids_contents})

def kids_details(request, kids_id):
    # Retrieve the Kids object with the given ID from the database
    kids_content = get_object_or_404(Kids, id=kids_id)

    # Pass the retrieved Kids object to the template for rendering
    return render(request, 'kids_details.html', {'kids_content': kids_content})


# def sub_login_view(request):
#     if request.method == 'POST':
#         # Get the username and password from the submitted form
#         username = request.POST['email']  # Assuming email is used as username
#         password = request.POST['password']
#
#         # Authenticate the user
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             # User is valid, log in the user
#             login(request, user)
#             # Redirect to a success page or homepage
#             return redirect('homepage')  # Replace 'homepage' with your actual homepage URL
#         else:
#             # Authentication failed, handle accordingly (e.g., show an error message)
#             return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
#
#     # If not a POST request, render the login page
#     return render(request, 'login.html')
#
# def sub_register(request):
#     if request.method == 'POST':
#         subscriber_form = SubscriberRegistrationForm(request.POST)
#         if subscriber_form.is_valid():
#             subscriber = subscriber_form.save(commit=False)
#             user = User.objects.create_user(
#                 username=subscriber_form.cleaned_data['user']['username'],
#                 password=subscriber_form.cleaned_data['user']['password']
#             )
#             subscriber.user = user
#             subscriber.save()
#             # Redirect to a subscriber dashboard or any other page
#             return redirect('subscriber_dashboard')  # Change to your actual subscriber dashboard URL name
#     else:
#         subscriber_form = SubscriberRegistrationForm()
#     return render(request, 'account/sub_register.html', {'form': subscriber_form})
#
# @login_required
# def sub_edit_profile(request):
#     if request.method == 'POST':
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
#         if profile_form.is_valid():
#             profile_form.save()
#             return redirect('profile_view')  # Change to your actual profile view URL name
#     else:
#         profile_form = UserProfileForm(instance=request.user.userprofile)
#     return render(request, 'edit_profile.html', {'form': profile_form})
#
#
#
# @login_required
# def subscribe(request, content_id):
#     # Get the content type based on the content_id
#     content_type = request.GET.get('content_type')  # Assuming content_type is passed in the request
#
#     # Map content_type to the appropriate content model
#     content_model = None
#     if content_type == 'movie':
#         content_model = Movies
#     elif content_type == 'tvshow':
#         content_model = Tv_shows
#     elif content_type == 'kids':
#         content_model = Kids
#
#     if content_model:
#         content = get_object_or_404(content_model, id=content_id)
#         subscriber = Subscriber.objects.get(user=request.user)
#         subscription, created = Subscription.objects.get_or_create(subscriber=subscriber,
#                                                                    content_type=ContentType.objects.get_for_model(
#                                                                        content_model), object_id=content.id)
#         if created:
#             return JsonResponse({'message': 'Subscription successful!'})
#         else:
#             return JsonResponse({'message': 'Already subscribed.'})
#     else:
#         return JsonResponse({'message': 'Invalid content type.'})
#
#
# @login_required
# def view_content(request, content_id):
#     # Get the content type based on the content_id
#     content_type = request.GET.get('content_type')  # Assuming content_type is passed in the request
#
#     # Map content_type to the appropriate content model
#     content_model = None
#     if content_type == 'movie':
#         content_model = Movies
#     elif content_type == 'tvshow':
#         content_model = Tv_shows
#     elif content_type == 'kids':
#         content_model = Kids
#
#     if content_model:
#         content = get_object_or_404(content_model, id=content_id)
#         subscriber = Subscriber.objects.get(user=request.user)
#         viewed_content, created = ViewedContent.objects.get_or_create(subscriber=subscriber,
#                                                                       content_type=ContentType.objects.get_for_model(
#                                                                           content_model), object_id=content.id)
#         if created:
#             return JsonResponse({'message': 'Content marked as viewed.'})
#         else:
#             return JsonResponse({'message': 'Content already marked as viewed.'})
#     else:
#         return JsonResponse({'message': 'Invalid content type.'})
#
#
# @login_required
# def remove_favorite(request, content_id):
#     # Get the content type based on the content_id
#     content_type = request.GET.get('content_type')  # Assuming content_type is passed in the request
#
#     # Map content_type to the appropriate content model
#     content_model = None
#     if content_type == 'movie':
#         content_model = Movies
#     elif content_type == 'tvshow':
#         content_model = Tv_shows
#     elif content_type == 'kids':
#         content_model = Kids
#
#     if content_model:
#         content = get_object_or_404(content_model, id=content_id)
#         subscriber = Subscriber.objects.get(user=request.user)
#         favorite = Favorite.objects.filter(subscriber=subscriber,
#                                            content_type=ContentType.objects.get_for_model(content_model),
#                                            object_id=content.id).first()
#         if favorite:
#             favorite.delete()
#             return JsonResponse({'message': 'Removed from favorites.'})
#         else:
#             return JsonResponse({'message': 'Not in favorites.'})
#     else:
#         return JsonResponse({'message': 'Invalid content type.'})

def admin(request):
    return render(request, 'admin.html')

def admin_home(request):
    # Retrieve the list of admin users
    if request.method == 'POST':
        # Handle any POST request logic here, if needed
        pass
    admin_home = CustomAdminUser.objects.all()
    return render(request, 'admin_homepg.html', {'admin_home': admin_home})

def add_user(request):
        add_user_form = CustomAdminUserForm(request.POST)
        if request.method == 'POST':
            if add_user_form.is_valid():
                new_user = add_user_form.save(commit=False)
                new_user.save()
                return redirect('admin_home')  # Redirect to the admin home page or any other URL
            else:
                add_user_form = CustomAdminUserForm()  # Create an empty form for GET requests


        return render(request, 'superadmin/add_users.html', {'add_user_form': add_user_form})

#
# def toggle_user_status(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#         enable = request.GET.get('enable')  # Get the 'enable' query parameter
#         if enable == 'true':
#             user.is_active = True
#         else:
#             user.is_active = False
#         user.save()
#         return JsonResponse({'is_active': user.is_active})
#     except User.DoesNotExist:
#         return JsonResponse({'error': 'User not found'}, status=404)

# def edit_Tv_shows(request, Tv_shows_id):
#     Tv_shows = get_object_or_404(Tv_shows, id=Tv_shows_id)
#     if request.method == 'POST':
#         form = EditSeriesForm(request.POST, request.FILES, instance=Tv_shows)
#         if form.is_valid():
#             form.save()
#             view_series_url = reverse ('view_series',args=[Tv_shows.id])
#             return redirect(view_series_url)# Redirect to a success page or series details page
#     else:
#         form = SeriesForm(instance=Tv_shows)
#     return render(request, 'edit/edit_series.html', {'edit_series_form': form, 'Tv_shows': Tv_shows})

# def edit_season(request, season_id):
#     season = get_object_or_404(Season, id=season_id)
#     if request.method == 'POST':
#         form = SeasonForm(request.POST, instance=season)
#         if form.is_valid():
#             form.save()
#             view_series_url = reverse('view_series', args=[season.series.id])
#             return redirect(view_series_url)
#     else:
#         form = SeasonForm(instance=season)
#     return render(request, 'edit/edit_season.html', {'edit_season_form': form, 'season': season})
#
# def edit_episode(request, episode_id):
#     episode = get_object_or_404(Episode, id=episode_id)
#     if request.method == 'POST':
#         form = EpisodeForm(request.POST, instance=episode)
#         if form.is_valid():
#             form.save()
#             view_series_url = reverse('view_series', args=[episode.season.series.id])
#             return redirect(view_series_url)
# # Redirect to a success page or episode details page
#     else:
#         form = EpisodeForm(instance=episode)
#     return render(request, 'edit/edit_episode.html', {'edit_episode_form': form, 'episode': episode})
# # Delete Series
# def delete_series(request, series_id):
#     series = get_object_or_404(Series, id=series_id)
#     series.delete()
# # Redirect to a success page or series list page
#     return redirect('series_path')
# # Delete Season
# def delete_season(request, season_id):
#     season = get_object_or_404(Season, id=season_id)
#     season.delete()
# # Redirect to a success page or series details page (or wherever appropriate)
#     return redirect('view_series', passed_id=season.series.id)
# # Delete Episode
# def delete_episode(request, episode_id):
#     episode = get_object_or_404(Episode, id=episode_id)
#     episode.delete()
# # Redirect to a success page or season details page (or wherever appropriate)
#     return redirect('view_series', passed_id=episode.season.series.id)