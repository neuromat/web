from django import template
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from mezzanine.accounts.admin import User
from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.generic.models import Keyword
from mezzanine.pages.models import Page
from ..models import FeatureCard, SwiperCard, Banner, SocialMediaLink, NeuroCineMat
from newsletter.models import  Newsletter

import math

register = template.Library()

@register.simple_tag
def show_page_content():
    """
    Should provide the rich html content of about page.
    """
    pages = Page.objects.all()
    # for page in pages:
    #     print(page)
    #     print(page.id)

    html_block = '<div class="post-feature-item"><div class="post-feature-image" style="background-image:url('')"></div>'
    html_block += '<div class="post-feature-info">'
    html_block += '<h3>CEPID Neuromat</h3>'
    html_block += '<p>O Centro de Pesquisa, ...</p>'
    html_block += '<p><a href="#">Conheça o projeto</a></p>'
    html_block += '</div> </div>'
    return html_block


@register.simple_tag
def blog_recent_posts(limit=4, page=1, tag=None, username=None, category=None):
    """
    Put a list of recently published blog posts into the template
    context. A tag title or slug, category title or slug or author's
    username can also be specified to filter the recent posts returned.

    Usage::

        {% blog_recent_posts 5 as recent_posts %}
        {% blog_recent_posts limit=5 tag="django" as recent_posts %}
        {% blog_recent_posts limit=5 category="python" as recent_posts %}
        {% blog_recent_posts 5 username=admin as recent_posts %}

    """
    blog_posts = BlogPost.objects.published().select_related("user")

    try:
        page = int(page)
    except:
        page = 1

    posts_per_page = 4
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)

    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            blog_posts = blog_posts.filter(keywords__keyword=tag)
        except Keyword.DoesNotExist:
            return []
    if category is not None:
        try:
            category = BlogCategory.objects.get(title_or_slug(category))
            blog_posts = blog_posts.filter(categories=category)
        except BlogCategory.DoesNotExist:
            return []
    if username is not None:
        try:
            author = User.objects.get(username=username)
            blog_posts = blog_posts.filter(user=author)
        except User.DoesNotExist:
            return []

    paginator = Paginator(blog_posts, posts_per_page)

    try:
        posts = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        posts = paginator.page(paginator.num_pages)

    return posts


@register.simple_tag
def newsletter_list():
    newsletter = Newsletter.objects.all().order_by('-number')[:4]
    return newsletter


@register.simple_tag
def feature_cards():
    cards = FeatureCard.objects.all()
    return cards


@register.simple_tag
def swiper_cards():
    """
    Provide a slideshow component with main products and internal links.
    """
    cards = SwiperCard.objects.all()
    return cards


@register.simple_tag
def get_banners():
    """
    Provide a slideshow component with main products and internal links.
    """
    banners = Banner.objects.all()
    return banners

@register.simple_tag
def get_social_media_links(list=False):
    """
    Provide a slideshow component with main products and internal links.
    """
    if list:
        list_template = "<ul>"

        for sociallink in SocialMediaLink.objects.all():
            list_template += '<li class="social-media-link"><a title="' + sociallink.title + '"target="_blank"' + \
             'href="' + sociallink.link + '"><i class="' + sociallink.icon_class + '"></i>' + \
                             sociallink.title + '</a></li>'
        list_template += "</ul>"
        return list_template
    else:
        links = SocialMediaLink.objects.all()
        return links

@register.simple_tag
def get_videos():
    """
    Provide a object with published videos
    """
    videos = NeuroCineMat.objects.all()
    return videos

@register.simple_tag
def get_categories():
    """
    Provide current categories list
    """

    categories = BlogCategory.objects.all()
    print(categories)

    pass