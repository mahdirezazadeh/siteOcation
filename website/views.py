# from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
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

comments_counts_user = 10
comments_counts_website = 10
websites_count_website_list = 3
comments_counts_home = 10


# Create your views here.
def home(request):
    """View function for home page of site."""

    # Is user logged in?
    is_logged = request.session.get('is_logged', False)

    # websites = Website.objects.all()

    # get recent comments to show new users as for example
    recent_comments = Comment.objects.order_by('-modified')[:comments_counts_home]

    # get most liked comments to show new users as for example
    liked_comments = Comment.objects.order_by('-likes')[:comments_counts_home]

    # search form
    if request.method == 'POST':
        search_text = request.POST['input_search']
        searched_websites_name = Website.objects.filter(name__icontains=search_text)
        searched_websites_domain_name = Website.objects.filter(website_domain_name__icontains=search_text)
        searched_websites = searched_websites_name | searched_websites_domain_name

        paginator = Paginator(searched_websites, websites_count_website_list)

        page_number = request.GET.get('page')
        page_websites = paginator.get_page(page_number)
        add_website = AddWebsite()

        context = {
            'website_list': page_websites,
            'add_website': add_website,
        }
        # redirect to website list page
        return render(request, 'website_list.html', context=context)

    context = {
        'recent_comments': recent_comments,
        'is_logged': is_logged,
        'liked_comments': liked_comments,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home.html', context=context)


def website_detail(request, pk):
    """View function for website list page of site."""

    # The website that user is looking for
    website = Website.objects.get(website_domain_name=pk)

    # all comments for website by order of last modified
    comments_s = Comment.objects.filter(website_id=pk, reply=None, ).order_by('-modified')

    # comments paginator
    paginator = Paginator(comments_s, comments_counts_website)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

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
        'comment_form': comment_form,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'website_detail.html', context=context)


def user_detail(request, pk):
    """View function for user detail page of site."""

    # The page of owner user
    user_view = User.objects.get(id=pk)

    # The profile information of user
    # user_details = Profile.objects.get(user_id=user_view.id)

    # comments of user for websites
    p_comments = Comment.objects.filter(user_id=user_view.id, reply=None).order_by('-modified')

    # pagination of comments
    paginator = Paginator(p_comments, comments_counts_user)  # Show 10 contacts per page.
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

    # check that the user is looking his own profile
    if request.user == user_view:
        is_it_him = True
    else:
        is_it_him = False

    # delete button
    if is_it_him:
        if request.method == 'POST':
            id_comment = request.POST['delete_button']
            print(id_comment)
            Comment.objects.filter(comment_id=id_comment).delete()

    context = {
        'is_it_him': is_it_him,
        'user_view': user_view,
        # 'detail': user_details,
        'comments': comments,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'user_detail.html', context=context)


def about(request):
    """The About page of website that render static information"""
    return render(request, 'about-a.html')


def contact(request):
    """The contact page of website that render static information"""
    return render(request, 'contact.html')


def website_list_view(request):
    """The website list page of website that shows all websites on siteOcation"""

    # add website form
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

            return redirect('websites')
    else:
        add_website = AddWebsite()

    # all websites by order of last modifying to get more comments
    website = Website.objects.order_by('-modified')

    # pagination of websites
    paginator = Paginator(website, websites_count_website_list)
    page_number = request.GET.get('page')
    page_websites = paginator.get_page(page_number)

    context = {
        'website_list': page_websites,
        'add_website': add_website,
    }

    return render(request, 'website_list.html', context=context)


def create_account(request):
    """The Create Account page of website."""

    # if user not logged in can be create new account
    if not request.user.is_authenticated:
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

                print(request.GET.get('next'))

                return redirect(request.GET.get('next'))
        else:
            sign_up_form = SignUpForm()

        context = {
            'sign_up_form': sign_up_form,
        }
        return render(request, 'createAccount.html', context=context)

    raise PermissionDenied


@login_required
def edit_profile(request):
    """The Edit Account page of website."""
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        user_form = UserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            # making context to redirect the user to user detail page
            # The page of owner user
            user_view = request.user

            # comments of user for websites
            p_comments = Comment.objects.filter(user_id=user_view.id, reply=None).order_by('-modified')

            # pagination of comments
            paginator = Paginator(p_comments, comments_counts_user)  # Show 10 contacts per page.
            page_number = request.GET.get('page')
            comments = paginator.get_page(page_number)

            # check that the user is looking his own profile
            is_it_him = True

            context = {
                'is_it_him': is_it_him,
                'user_view': user_view,
                # 'detail': user_details,
                'comments': comments,
            }

            # Render the HTML template index.html with the data in the context variable
            return render(request, 'user_detail.html', context=context)

    else:
        user_form = UserForm(instance=request.user)

    context = {
            'user_form': user_form,
        }

    return render(request, 'editProfile.html', context=context)


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

#
# @login_required
# def renew_user_login_date(request, pk):
#     user = get_object_or_404(Profile, pk=pk)
#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#
#         # Create a form instance and populate it with data from the request (binding):
#         form = RenewLogin(request.POST)
#
#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             user.date_of_birth = form.cleaned_data['renew_date']
#             user.save()
#
#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('user-detail', args=[str(user.user.id)]))
#
#     # If this is a GET (or any other method) create the default form.
#     else:
#         proposed_renewal_date = datetime.date.today() - datetime.timedelta(weeks=52)
#         form = RenewLogin(initial={'renew_date': proposed_renewal_date})
#
#     context = {
#         'form': form,
#         'user_a': user,
#     }
#
#     return render(request, 'login_edit_time.html', context)
