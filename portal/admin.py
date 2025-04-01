from django.contrib import admin
from portal.models.company_model import Company
from portal.models.job_application_model import JobApplication
from portal.models.job_category_model import JobCategory
from portal.models.job_model import Job
from portal.models.job_owner_model import JobOwner
from portal.models.job_seeker_profile_model import JobSeekerProfile
from portal.models.saved_jobs_model import SavedJob
from portal.models.skill_model import Skill


admin.site.register(Company)
admin.site.register(JobApplication)
admin.site.register(JobCategory)
admin.site.register(Job)
admin.site.register(JobOwner)
admin.site.register(JobSeekerProfile)
admin.site.register(SavedJob)
admin.site.register(Skill)

