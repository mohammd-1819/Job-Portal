from django.urls import path
from .views import job_category_view, company_view, job_view, job_seeker_view, job_application_view, saved_job_view, \
    employer_dashboard_view

app_name = 'portal'

urlpatterns = [
    path('job/category/all/', job_category_view.JobCategoryListView.as_view(), name='jov-category-list'),
    path('job/category/<str:name>/', job_category_view.JobCategoryDetailView.as_view(), name='jov-category-detail'),
    path('job/category/create', job_category_view.CreateJobCategoryView.as_view(), name='jov-category-create'),
    path('job/category/<str:name>/remove/', job_category_view.RemoveJobCategoryView.as_view(),
         name='jov-category-remove'),

    path('company/all', company_view.CompanyListView.as_view(), name='company-list'),
    path('company/add/', company_view.AddCompanyView.as_view(), name='company-add'),
    path('company/<str:company_name>/update/', company_view.UpdateCompanyView.as_view(), name='company-update'),
    path('company/<str:company_name>/remove/', company_view.RemoveCompanyView.as_view(), name='company-remove'),

    path('skill/all/', job_view.SkillListView.as_view(), name='skill-list'),
    path('skill/add/', job_view.AddSkillView.as_view(), name='skill-add'),
    path('skill/<str:name>/detail', job_view.SkillDetailView.as_view(), name='skill-detail'),
    path('skill/<str:name>/remove', job_view.RemoveSkillView.as_view(), name='skill-remove'),

    path('job/seeker/<str:username>/', job_seeker_view.JobSeekerDetailView.as_view(), name='job-seeker-detail'),
    path('job/seeker/profile/create/', job_seeker_view.CreateJobSeekerProfileView.as_view(),
         name='job-seeker-profile-create'),
    path('job/seeker/profile/update/', job_seeker_view.UpdateJobSeekerProfileView.as_view(),
         name='job-seeker-profile-update'),

    path('job/seeker/profile/remove/', job_seeker_view.RemoveJobSeekerProfileView.as_view(),
         name='job-seeker-profile-remove'),

    path('job/application/company/all/', job_application_view.JobApplicationListView.as_view(),
         name='job-application-company-list'),

    path('job/application/<str:application_id>/detail', job_application_view.JobApplicationDetailView.as_view(),
         name='job-application-detail'),

    path('job/application/request/', job_application_view.CreateJobApplicationRequest.as_view(),
         name='job-application-request'),

    path('job/application/<str:application_id>/cancel', job_application_view.CancelApplicationRequest.as_view(),
         name='job-application-cancel'),

    path('job/application/<str:application_id>/status/', job_application_view.JobApplicationStatusView.as_view(),
         name='job-application-status'),

    path('job/save/', saved_job_view.AddSavedJobView.as_view(), name='job-save-add'),
    path('job/save/all/', saved_job_view.UserSavedJobListView.as_view(), name='job-save-user-list'),
    path('job/save/<str:saved_job_id>/remove/', saved_job_view.RemoveSaveJobView.as_view(), name='job-save-remove'),

    path('employer/jobs/', employer_dashboard_view.EmployerJobListView.as_view(), name='employer-job-list'),
    path('employer/applications/', employer_dashboard_view.EmployerJobApplicationRequestView.as_view(),
         name='employer-application-list'),
]
