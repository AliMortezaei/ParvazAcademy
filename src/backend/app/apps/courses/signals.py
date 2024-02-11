
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from jalali_date import datetime2jalali, date2jalali

from core import settings
from apps.courses.models import Category, Course, Section


@receiver(pre_save, sender=Category)
def generate_slug_category(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    if not slug:
        text = instance.title
        text = text.strip()
        slug = slugify(text, allow_unicode=True)
    instance.slug = slug



@receiver(pre_save, sender=Course)
def generate_course(sender, instance, *args, **kwargs):
    if instance.date_start:
        instance.date_start = str(date2jalali(instance.date_start))
    if not instance.image:
        instance.image = settings.DEFAULT_COURSE
    slug = slugify(instance.title)
    if not slug:
        text = instance.title
        text = text.strip()
        slug = slugify(text, allow_unicode=True)
    instance.slug = slug


@receiver(pre_save, sender=Section)
def generate_slug_section(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    if not slug:
        text = instance.title
        text = text.strip()
        slug = slugify(text, allow_unicode=True)
    instance.slug = slug



