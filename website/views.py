# from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
import datetime
from django.utils import timezone

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from website.forms import SignUpForm
from website.forms import AddComment
from website.forms import UserForm
from website.forms import AddWebsite

from django.views import generic
from website.models import Website
from website.models import Profile
from website.models import Comment
from website.models import AreaServed

from website.forms import RenewLogin
# from website.models import Industry
# from website.models import AreaServed
# from website.models import Founder


# Create your views here.
def home(request):
    """View function for home page of site."""

    # Is user logged in?
    is_logged = request.session.get('is_logged', False)

    # websites = Website.objects.all()

    recent_comments = Comment.objects.order_by('-modified')[:10]

    liked_comments = Comment.objects.order_by('-likes')[:10]

    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        # profile_form = ProfileForm(request.POST)
        if sign_up_form.is_valid():
            user_saved = sign_up_form.save()
            user_saved.refresh_from_db()
            user_saved.save()

            username = sign_up_form.cleaned_data.get('username')
            raw_password = sign_up_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            # profile = profile_form.user()
            login(request, user)

            return redirect('home')
    else:
        sign_up_form = SignUpForm()

    if request.method == 'POST':
        add_website = AddWebsite(request.POST)
        # profile_form = ProfileForm(request.POST)
        if add_website.is_valid():
            saved_website = add_website.save(commit=False)
            saved_website.writen_by = request.user.profile
            # saved_website.modified = timezone.now
            #
            # saved_website.founded = AddWebsite.cleaned_data('founded')
            # saved_website.areaServed = AreaServed.objects.get(name='world wide')
            saved_website.save()

            return redirect('home')
    else:
        add_website = AddWebsite()

    context = {
        'recent_comments': recent_comments,
        'is_logged': is_logged,
        'liked_comments': liked_comments,
        'sign_up_form': sign_up_form,
        'add_website': add_website,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home.html', context=context)


def website_detail(request, pk):
    """View function for home page of site."""

    # Available books (status = 'a')
    website = Website.objects.get(website_domain_name=pk)

    comments = reversed(Comment.objects.filter(website_id=pk, reply=None))

    # create Account form
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        # profile_form = ProfileForm(request.POST)
        if sign_up_form.is_valid():
            user_saved = sign_up_form.save()
            user_saved.refresh_from_db()

            user_saved.save()

            username = sign_up_form.cleaned_data.get('username')
            raw_password = sign_up_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            # profile = profile_form.user()
            login(request, user)

            return redirect(website.get_absolute_url())
    else:
        sign_up_form = SignUpForm()

    # add comment form
    if request.method == 'POST':
        comment_form = AddComment(request.POST)
        # profile_form = ProfileForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user_id = request.user.profile
            comment.website_id = website
            comment.modified = timezone.now()
            comment.comment = comment.comment
            comment_form.save()
            return redirect(website.get_absolute_url())
    else:
        comment_form = AddComment()

    context = {
        'website': website,
        'comments': comments,
        'sign_up_form': sign_up_form,
        'comment_form': comment_form,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'website_detail.html', context=context)


def user_detail(request, pk):
    """View function for home page of site."""

    # Available books (status = 'a')
    user_view = User.objects.get(id=pk)

    user_details = Profile.objects.get(user_id=user_view.id)

    comments = reversed(Comment.objects.filter(user_id=user_view.id, reply=None))
    #
    # paginator = Paginator(comments, 5)  # Show 25 contacts per page.
    # page_number = request.GET.get('page')
    # page_comments = paginator.get_page(page_number)

    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        # profile_form = ProfileForm(request.POST)
        if sign_up_form.is_valid():
            user_saved = sign_up_form.save()
            user_saved.refresh_from_db()
            user_saved.save()

            username = sign_up_form.cleaned_data.get('username')
            raw_password = sign_up_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            # profile = profile_form.user()
            login(request, user)

            return redirect('home')
    else:
        sign_up_form = SignUpForm()

    if request.user == user_view:
        profile = True
    else:
        profile = False

    if profile:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return HttpResponseRedirect(reverse('user-detail', request.user.id))
        else:
            user_form = UserForm(instance=request.user)

        context = {
            'is_it_him': profile,
            'user_view': user_view,
            'detail': user_details,
            'comments': comments,
            'user_form': user_form,
            'sign_up_form': sign_up_form,
        }
    else:
        context = {
            'is_it_him': profile,
            'user_view': user_view,
            'detail': user_details,
            'comments': page_comments,
            'sign_up_form': sign_up_form,
        }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'user_detail.html', context=context)


def about(request):
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        # profile_form = ProfileForm(request.POST)
        if sign_up_form.is_valid():
            user_saved = sign_up_form.save()
            user_saved.refresh_from_db()
            user_saved.save()

            username = sign_up_form.cleaned_data.get('username')
            raw_password = sign_up_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            # profile = profile_form.user()
            login(request, user)

            return redirect('home/websites')
    else:
        sign_up_form = SignUpForm()

    context = {
        'sign_up_form': sign_up_form,
    }
    return render(request, 'about-a.html', context=context)


def contact(request):
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        # profile_form = ProfileForm(request.POST)
        if sign_up_form.is_valid():
            user_saved = sign_up_form.save()
            user_saved.refresh_from_db()
            user_saved.save()

            username = sign_up_form.cleaned_data.get('username')
            raw_password = sign_up_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            # profile = profile_form.user()
            login(request, user)

            return redirect('home/websites')
    else:
        sign_up_form = SignUpForm()

    context = {
        'sign_up_form': sign_up_form,
    }
    return render(request, 'contact.html', context=context)


def website_list_view(request):
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        # profile_form = ProfileForm(request.POST)
        if sign_up_form.is_valid():
            user_saved = sign_up_form.save()
            user_saved.refresh_from_db()
            user_saved.save()

            username = sign_up_form.cleaned_data.get('username')
            raw_password = sign_up_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            # profile = profile_form.user()
            login(request, user)

            return redirect('home/websites')
    else:
        sign_up_form = SignUpForm()

    website = Website.objects.all()
    paginator = Paginator(website, 1)  # Show 5 contacts per page.

    page_number = request.GET.get('page')
    page_websites = paginator.get_page(page_number)

    context = {
        'website_list': page_websites,
        'sign_up_form': sign_up_form,
    }

    return render(request, 'website_list.html', context=context)


# class WebsiteListView(generic.ListView):
#     model = Website
#     template_name = 'website/website_list.html'
#     paginate_by = 3
    # context_object_name = 'my_book_list'  # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


# class WebisteDetailView(generic.ListView):
#     # model = Website
#     template_name = 'website/website_detail.html'
#
#     def get_queryset(self):
#         self.website = get_object_or_404(Website, name=self.kwargs['website_domain_name'])
#         return Website.objects.filter(website_domain_name=self.website)

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in the publisher
    #     context['website_domain_name'] = self.website
    #     return context
    # def as_view(self, pk):
    #     queryset = Website.objects.filter(publisher__name='ACME Publishing')
    #     return queryset
    #
    # def book_detail_view(self, primary_key):
    #     try:
    #         website = Website.objects.get(pk=primary_key)
    #     except Website.DoesNotExist:
    #         raise Http404('website does not exist')
    #
    #     return render(self, "website/website_detail.html", context={'website': website})


@login_required
def renew_user_login_date(request, pk):
    user = get_object_or_404(Profile, pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewLogin(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            user.date_of_birth = form.cleaned_data['renew_date']
            user.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('user-detail', args=[str(user.user.id)]))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() - datetime.timedelta(weeks=52)
        form = RenewLogin(initial={'renew_date': proposed_renewal_date})

    context = {
        'form': form,
        'user_a': user,
    }

    return render(request, 'login_edit_time.html', context)
