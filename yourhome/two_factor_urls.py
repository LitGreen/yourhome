from django.urls import path
from two_factor.views import LoginView, SetupView, QRGeneratorView, SetupCompleteView, BackupTokensView, ProfileView, DisableView
from . import views

app_name = 'two_factor'

urlpatterns = [
    path('login_register/', views.login_register, name='login_register'),
    path('setup/', SetupView.as_view(), name='setup'),
    path('qrcode/', QRGeneratorView.as_view(), name='qr'),
    path('setup/complete/', SetupCompleteView.as_view(), name='setup_complete'),
    path('backup/tokens/', BackupTokensView.as_view(), name='backup_tokens'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('disable/', DisableView.as_view(), name='disable'),
]