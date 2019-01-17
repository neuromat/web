from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Subscription(models.Model):
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
