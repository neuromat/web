from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Postdoc(models.Model):
    """
    An instance of this class represents a postdoc candidate.

    """
    name = models.CharField(_('Name'), max_length=255)
    date = models.DateField(_('Date'), default=now, editable=False)
    email = models.EmailField(_('Email'))
    cpf = models.CharField(_('CPF'), max_length=15, unique=True, blank=True)
    passport = models.CharField(_('Passport / RNE'), max_length=50, blank=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    mobile_phone = models.CharField(_('Mobile phone'), max_length=20, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Postdoc')
        verbose_name_plural = _('Postdocs')
        ordering = ('name',)


class Research(models.Model):
    """
    An instance of this class represents a researcher contact of a postdoc candidate.

    """
    postdoc_candidate = models.ForeignKey(Postdoc)
    name = models.CharField(_('Name'), max_length=255)
    affiliation = models.CharField(_('Affiliation'), max_length=255)
    email = models.EmailField(_('Email'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Research')
        verbose_name_plural = _('Researchers')
        ordering = ('name',)
