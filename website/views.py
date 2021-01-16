# from django.http import Http404
from django.shortcuts import render
# from django.shortcuts import get_object_or_404
from django.views import generic
from website.models import Website
from website.models import Profile
from website.models import Comment
from django.contrib.auth.models import User as User_in_built
# from website.models import Industry
# from website.models import AreaServed
# from website.models import Founder


# Create your views here.
def home(request):
    """View function for home page of site."""

    # Is user logged in?
    is_logged = request.session.get('is_logged', False)

    # Generate counts of some of the main objects
    num_websites = Website.objects.all().count()

    # Available books (status = 'a')
    num_worldwide_websites = Website.objects.filter(areaServed__exact='World wide').count()

    # The 'all()' is implied by default.
    num_users = Profile.objects.count()

    # websites = Website.objects.all()

    recent_comments = Comment.objects.order_by('-modified')[:10]

    liked_comments = Comment.objects.order_by('-likes')[:10]

    context = {
        'num_websites': num_websites,
        'num_worldwide_websites': num_worldwide_websites,
        'num_users': num_users,
        # 'websites': websites,
        'recent_comments': recent_comments,
        'is_logged': is_logged,
        'liked_comments': liked_comments,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'home.html', context=context)


def website_detail(request, pk):
    """View function for home page of site."""

    # Available books (status = 'a')
    website = Website.objects.get(website_domain_name=pk)

    comments = reversed(Comment.objects.filter(website_id=pk, reply=None))

    context = {
        'website': website,
        'comments': comments,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'website_detail.html', context=context)


def user_detail(request, pk):
    """View function for home page of site."""

    # Available books (status = 'a')
    user = User_in_built.objects.get(id=pk)

    user_details = Profile.objects.get(user_id=user.id)

    comments = reversed(Comment.objects.filter(user_id=user.id, reply=None))

    context = {
        'userview': user,
        'detail': user_details,
        'comments': comments,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'user_detail.html', context=context)


def about(request):
    return render(request, 'about-a.html')


def contact(request):
    return render(request, 'contact.html')


class WebsiteListView(generic.ListView):
    model = Website
    template_name = 'website/website_list.html'
    paginate_by = 3
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
