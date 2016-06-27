
from django.db import models
from django.utils.translation import ugettext as _


LOG_LEVEL= (
    ('INFO', 'Info'),
    ('ERROR', 'Error'),
    ('WARN', 'Warning'),
    )


class LogItem(models.Model):
    title = models.CharField(_("Log text"), max_length=255)
    log_level = models.CharField(_("Log level"), max_length=6, choices=LOG_LEVEL)
    date_added = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(_("Key"), max_length=50, blank=True)
    ip = models.CharField(_("Ip/User"), max_length=255, blank=True)
    json_dump = models.TextField(blank=True)

    class Meta:
        ordering=['date_added']

    def __unicode__(self):
        return "%s %s %s" % (self.title, self.log_level, self.date_added )
