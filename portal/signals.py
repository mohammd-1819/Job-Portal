from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.dispatch import receiver
from portal.models.company_model import Company
from portal.models.job_category_model import JobCategory
from portal.models.skill_model import Skill


@receiver([post_save, post_delete], sender=Company)
def clear_company_list_cache(sender, **kwargs):
    for page in range(1, 100):
        cache.delete(f'company_list_page_{page}')


@receiver([post_save, post_delete], sender=JobCategory)
def clear_job_category_list_cache(sender, **kwargs):
    for page in range(1, 100):
        cache.delete(f'job_category_list_page_{page}')


@receiver([post_save, post_delete], sender=Skill)
def clear_skill_list_cache(sender, **kwargs):
    for page in range(1, 100):
        cache.delete(f'skill_list_page_{page}')
