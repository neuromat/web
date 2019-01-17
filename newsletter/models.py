import datetime

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from mezzanine.blog.models import BlogPost


class Newsletter(models.Model):
    """
    An instance of this class is a newsletter consisting of different posts of the same month/year.

    """
    number = models.CharField(_('Number'), max_length=100, unique=True)
    date = models.DateField(_('Date'), default=now)
    featured = models.ManyToManyField(
        BlogPost, blank=True, related_name='featured_post', limit_choices_to={
            'publish_date__month': datetime.datetime.now().strftime("%m"),
            'publish_date__year': datetime.datetime.now().strftime("%Y"),
            'categories__slug': 'newsletter'
        }
    )
    publication = models.ManyToManyField(
        BlogPost, blank=True, related_name='publication_post', limit_choices_to={
            'publish_date__month': datetime.datetime.now().strftime("%m"),
            'publish_date__year': datetime.datetime.now().strftime("%Y"),
            'categories__slug': 'publication'
        }
    )
    in_the_media = models.ManyToManyField(
        BlogPost, blank=True, related_name='in_the_media_post', limit_choices_to={
            'publish_date__month': datetime.datetime.now().strftime("%m"),
            'publish_date__year': datetime.datetime.now().strftime("%Y"),
            'categories__slug': 'news'
        }
    )
    opportunity = models.ManyToManyField(
        BlogPost, blank=True, related_name='opportunity_post', limit_choices_to={
            'categories__slug': 'opportunities'
        }
    )
    streaming = models.ManyToManyField(
        BlogPost, blank=True, related_name='streaming_post', limit_choices_to={
            'publish_date__month': datetime.datetime.now().strftime("%m"),
            'publish_date__year': datetime.datetime.now().strftime("%Y"),
            'categories__slug': 'streaming'
        }
    )
    event = models.ManyToManyField(
        BlogPost, blank=True, related_name='event_post', limit_choices_to={
            'categories__slug': 'events'
        }
    )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        ordering = ('number',)


class Subscription(models.Model):
    """
    An instance of this class is a person who want to receive our newsletter

    """
    email = models.EmailField(_('e-mail'), unique=True)
    create_date = models.DateTimeField(editable=False, default=now)
    status = models.BooleanField(_('Status'), default=False, db_index=True)
    status_date = models.DateTimeField(_('Status date'), null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        ordering = ('email',)
