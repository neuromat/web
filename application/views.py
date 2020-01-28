from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from .forms import PostdocForm, ResearchForm
from .models import Postdoc, PostdocFile, Research

from mezzanine.blog.models import BlogPost, BlogCategory


def category_page(request, template_name="blog_list_category.html"):

    blog_posts = BlogPost.objects.published(for_user=request.user)
    print(blog_posts)
    urlstring = request.path.rpartition('/')
    category = urlstring[2]
    # print(category)
    blog_posts = blog_posts.filter(categories=None)

    context = {"blog_posts": blog_posts, "test": category}
    return render(request, template_name, context)


def postdoc(request, template_name="postdoc.html"):
    candidate_form = PostdocForm(request.POST or None)
    research_inlineformset = inlineformset_factory(Postdoc, Research, form=ResearchForm, extra=3, can_delete=False)

    if request.method == "POST":
        if request.POST['action'] == "save":
            candidate_form = PostdocForm(request.POST, request.FILES)

            if candidate_form.is_valid():
                candidate = candidate_form.save()
                researchers = research_inlineformset(request.POST, instance=candidate)

                if researchers.is_valid():
                    researchers.save()

                for file in request.FILES.getlist('file'):
                    new_file = PostdocFile(postdoc_data=candidate, file=file)
                    new_file.save()

                messages.success(request, _('Application created successfully.'))
                redirect_url = reverse('home')
                return HttpResponseRedirect(redirect_url)

            else:
                messages.warning(request, _('Information not saved.'))

        else:
            messages.warning(request, _('Action not available.'))

    context = {"candidate_form": candidate_form,
               "research_inlineformset": research_inlineformset,
               "creating": True}

    return render(request, template_name, context)
