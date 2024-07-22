from django.urls import path
from .views import signup_view, login_view, logout_view, group_selection_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup/', group_selection_view, name='group-selection'),
    path('signup/<str:group_name>/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path("logout/", logout_view, name="logout"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]










# Appuser1 : hahahauser1
# Appuser2 : hahahauser2
# Appuser3 : hahahauser3
# Appuser4 : hahahauser4
# Appuser5 : hahahauser5
# Appuser6 : hahahauser6
# Appuser7 : hahahauser7
# Appuser8 : hahahauser8
# Appuser9 : hahahauser9
# Appuser10 : hahahauser10
# Appuser11 : hahahauser11
# Appuser12 : hahahauser12
# Appuser13 : hahahauser13

