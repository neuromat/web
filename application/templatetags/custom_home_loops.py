from django import template
from html import unescape

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