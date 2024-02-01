

from django.template.defaultfilters import slugify 
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.courses.models import Category, Course, Section


@receiver(pre_save, sender=Category)
def generate_slug_category(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    if not slug:
        text = instance.title
        text = text.strip()
        slug = '-'.join(text.split())
    instance.slug = slug



@receiver(pre_save, sender=Course)
def generate_slug_course(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    if not slug:
        text = instance.title
        text = text.strip()
        slug = '-'.join(text.split())
    instance.slug = slug


@receiver(pre_save, sender=Section)
def generate_slug_section(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    if not slug:
        text = instance.title
        text = text.strip()
        slug = '-'.join(text.split())
    instance.slug = slug
