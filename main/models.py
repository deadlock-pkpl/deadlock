from django.db import models

class SiteTheme(models.Model):
    bg_color = models.CharField(max_length=20, default="#fafaf9")
    font_family = models.CharField(max_length=100, default="'DM Sans', sans-serif")
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj