from django.conf.urls import include, url
from django.contrib import admin

from testing import accounts
from testing import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'iEnglish.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', accounts.login),
    url(r'^accounts/logout/$', accounts.logout),
    url(r'^accounts/register/$', accounts.register),
    url(r'^accounts/forgot/$', accounts.forgot),

    url(r'^$', views.main),
    url(r'^know/$', views.know),
    url(r'^know/test/([0-9]+)/$', views.test),
    url(r'^know/test/([0-9]+)/list$', views.list),
    url(r'^know/test/report/([0-9]+)$', views.report),
]
