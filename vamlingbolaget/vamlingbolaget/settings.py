# Django settings for vamlingbolaget project.
import os
PROJECT_ROOT = os.path.dirname(__file__)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Stockholm'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'sv-SE'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media'),



# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ROOT_DIR

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/theme/static/'

DIRECTORY =  os.path.join(ROOT_DIR, 'media/upload/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_DIR, '/theme/static'),
    
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@4ysa4i353-b!iwff6())2455g^s#zab!ep$bgn2**yjtii$j%'

# List of callables that know how to import templates from various sources.

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    ) # Optional

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'vamlingbolaget.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'vamlingbolaget.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.    
    #'/usr/lib/python2.7/site-packages/django/contrib/admin/media',
    os.path.join(ROOT_DIR, '/theme/templates'),
    
)

INSTALLED_APPS = (
    #'admin_tools',
    #'admin_tools.menu',
    #'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    #"django.contrib.comments",
    #'tagging',
    #'mptt',
    'accounts',
    #'zinnia',
    'filebrowser',
    'ckeditor',
    'grappelli',
    'django.contrib.admin',
    'rosetta',
    'modeltranslation',
    #installed apps
    'taggit',
    'tastypie',
    'imagekit',
    'south',
    'userena',
    'guardian',
    'easy_thumbnails',
    'gunicorn',
    #'photologue',
    #Our Apps
    'products',
    'cart',
    'blog',
    'frontpage',
    'gallery',
    'flatpages',
    'checkout',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

GRAPPELLI_ADMIN_TITLE = 'Vamlingbolaget Admin'

try:
    from .local_settings import *
except ImportError:
    pass

ADMIN_TOOLS_MENU = 'vamlingbolaget.menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'vamlingbolaget.dashboard.CustomIndexDashboard'

# sessions# Cookie name. This can be whatever you want.
SESSION_COOKIE_NAME = 'sessionid'
# The module to store sessions data.
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Age of cookie, in seconds (default: 2 weeks).
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# Whether a user's session cookie expires when the Web browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_SECURE = False


EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yourgmailaccount@gmail.com'
EMAIL_HOST_PASSWORD = 'yourgmailpassword'
USERENA_ACTIVATION_REQUIRED = False
ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'accounts.MyProfile'

gettext = lambda s: s

LANGUAGES = (
    ('sv', gettext('Swedish')),
    ('en', gettext('English')),
    )

MODELTRANSLATION_TRANSLATION_FILES = (
    'products.translation',
    'flatpages.translation',
    )

try:
    from .grappelli import *
except ImportError:
    pass

FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
FILEBROWSER_MEDIA_URL = MEDIA_URL
FILEBROWSER_STATIC_ROOT = STATIC_ROOT
FILEBROWSER_STATIC_URL = STATIC_URL
URL_FILEBROWSER_MEDIA = STATIC_URL + 'filebrowser/'
PATH_FILEBROWSER_MEDIA = STATIC_ROOT + 'filebrowser/'
URL_TINYMCE = STATIC_URL + 'tiny_mce/'
PATH_TINYMCE = STATIC_ROOT + 'tiny_mce/'