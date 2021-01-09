from django.db import models
from django.urls import reverse

# Create your models here.


class Industry(models.Model):
    """Model representing a website industries."""
    name = models.CharField(max_length=200, help_text='Enter a website industry (e.g. e-commerce)')

    class Meta:
        ordering = ['name']


class AreaServed(models.Model):
    """Model representing a website Area Served."""
    name = models.CharField(max_length=100, primary_key=True,
                            help_text='Is it World wide service website or for specific area')

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class User(models.Model):
    """Model representing a users."""
    id = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=100, blank=False, null=False)

    # Whether this user can access the admin site.
    is_staff = models.BooleanField(default=False)

    # Whether this user account should be considered active. We set this flag to False instead of deleting accounts.
    # That way, if your applications have any foreign keys to users, the foreign keys won’t break.
    is_active = models.BooleanField(default=True)

    # Is an admin؟
    is_superuser = models.BooleanField(default=False)

    # this user has all permissions without explicitly assigning them.
    is_authenticated = models.BooleanField(default=True)

    # A datetime of the user’s last login
    last_login = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True, )
    email = models.EmailField(unique=True, )
    user_picture = models.ImageField(help_text="Upload the picture of user.", blank=True, null=True, )
    bio = models.CharField(max_length=50, blank=True, null=True, )
    date_of_birth = models.DateField(auto_now_add=True)

    # when the account was created. Is set to the current date/time by default when the account is created.
    date_joined = models.DateTimeField(auto_now_add=True, )

    # language = models

    class Meta:
        ordering = ['id', 'email']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}; {self.last_name} {self.first_name}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this User."""
        return reverse('user-detail', args=[str(self.id)])


class Founder(models.Model):
    """Model representing a founders."""
    name = models.CharField(max_length=100, primary_key=True)
    user_id = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                blank=True,
                                null=True, )

    class Meta:
        ordering = ['name']


class Website(models.Model):
    """Model representing a Website."""
    website_domain_name = models.CharField(unique=True, max_length=71, primary_key=True,
                                           help_text='Website hostname without sub-domain and top-level-domain')

    name = models.CharField(max_length=200, unique=True, blank=False)

    description = models.TextField(max_length=1000, help_text='Enter a brief description of the website')

    founded = models.DateField(help_text='When was this website created?', blank=True, null=True, )
    modified = models.DateTimeField(auto_now_add=True, help_text='When was this page created?')

    writen_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Null has no effect on Many To Many Field.
    founders = models.ManyToManyField(Founder, help_text='Who made this website?', blank=True)

    # ManyToManyField used because industry can contain many websites. websites can cover many types.
    # industry class has already been defined so we can specify the object above.
    # Null has no effect on Many To Many Field.
    industry = models.ManyToManyField(Industry, help_text='Select a type for this website', blank=True)

    # Null has no effect on Many To Many Field.
    subsidiaries = models.ManyToManyField("self", max_length=200, blank=True,
                                          help_text='the companies that is owned or controlled by this company')

    brand_picture = models.ImageField(null=True, blank=True, help_text="Upload the picture of website's brand.")

    headquarters = models.CharField(max_length=200,
                                    help_text='The location where most of the important'
                                              + ' functions of an organization are coordinated.',
                                    blank=True)

    numberOfEmployees = models.CharField(max_length=200, null=True, blank=True)

    areaServed = models.ForeignKey(AreaServed, on_delete=models.SET_NULL, null=True)

    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-likes', 'dislikes', 'name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this Website."""
        return reverse('website-detail', args=[str(self.website_domain_name)])


class Comment(models.Model):
    """Model representing a Comment."""
    comment_id = models.AutoField(primary_key=True)

    # Foreign Key used because comments can only have one website, but websites can have multiple comments
    website_id = models.ForeignKey(Website, on_delete=models.CASCADE)

    # Foreign Key used because comments can only have one user, but users can have multiple comments
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now_add=True, help_text='When was this page created?')
    comment = models.CharField(max_length=600)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    rate_to_web = models.PositiveSmallIntegerField(blank=True, null=True, )

    # Foreign Key used because replies can only have one comment, but  comments have multiple replies
    reply = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        """String for representing the Model object."""
        comment_details = f'(User: {self.user_id}, ID: {self.comment_id}, '
        comment_details += f'Comment to: {self.website_id}, Reply to: {self.reply})'
        return comment_details

    def get_absolute_url(self):
        """Returns the url to access a detail record for this User."""
        return reverse('comment-detail', args=[str(self.comment_id)])
