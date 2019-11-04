from django import template
from html import unescape

from django.db.models import Q
from mezzanine.accounts.admin import User
from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.generic.models import Keyword
from mezzanine.pages.models import Page

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

    html_block =  '<div class="post-feature-item"><div class="post-feature-image" style="background-image:url('')"></div>'
    html_block += '<div class="post-feature-info">'
    html_block += '<h3>CEPID Neuromat</h3>'
    html_block += '<p>O Centro de Pesquisa, ...</p>'
    html_block += '<p><a href="#">Conheça o projeto</a></p>'
    html_block += '</div> </div>'
    return html_block


@register.simple_tag
def project_swiper_component():
    """
    Provide a slidehow component with main products and internal links.
    """
    pass


@register.simple_tag
def blog_recent_posts(limit=8, tag=None, username=None, category=None):
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
    return list(blog_posts[:limit])