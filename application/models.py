from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


def application_path(instance, filename):
    return 'application/{0}/{1}'.format(
        instance.postdoc_data.name, str(filename)
    )


class Postdoc(models.Model):
    """An instance of this class represents a postdoc candidate."""
    name = models.CharField(_('Name'), max_length=255)
    date = models.DateField(_('Date'), default=now, editable=False)
    email = models.EmailField(_('Email'))
    cpf = models.CharField(_('CPF'), max_length=15, blank=True)
    passport = models.CharField(_('Passport / RNE'), max_length=50, blank=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    mobile_phone = models.CharField(_('Mobile phone'), max_length=20, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Postdoc')
        verbose_name_plural = _('Postdocs')
        ordering = ('-date',)


class PostdocFile(models.Model):
    """An instance of this class represents a file from a postdoc candidate. """
    postdoc_data = models.ForeignKey(Postdoc, related_name='postdoc_files')
    file = models.FileField(_('File'), upload_to=application_path)

    def __str__(self):
        return self.file.name


class Research(models.Model):
    """An instance of this class represents a researcher contact of a postdoc candidate."""
    postdoc_candidate = models.ForeignKey(Postdoc)
    name = models.CharField(_('Name'), max_length=255, blank=True)
    affiliation = models.CharField(_('Affiliation'), max_length=255, blank=True)
    email = models.EmailField(_('Email'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Research')
        verbose_name_plural = _('Researchers')
        ordering = ('name',)


class FeatureCard(models.Model):
    """An instance of this class represents a card item."""
    title = models.CharField(_('Title'), max_length=255)
    description = models.CharField(_('Description'), max_length=255)
    link = models.CharField(_('Link'), max_length=255)
    image = models.ImageField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Card')
        verbose_name_plural = _('Cards')
        ordering = ('title',)

class SwiperCard(models.Model):
    """An instance of this class represents a card item."""
    title = models.CharField(_('Title'), max_length=255)
    description = models.CharField(_('Description'), max_length=255)
    link = models.CharField(_('Link'), max_length=255)
    image = models.ImageField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Swipper Card')
        verbose_name_plural = _('Swipper Cards')
        ordering = ('title',)
