"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# para colocar translation no projeto. Possibilidade de mudar o idioma
# nas configurações
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    #################################################################
    ### Página Principal (http://localhost:8000/admin/core/user/) ###
    #################################################################
    ordering = ['id']
    list_display = ['email', 'name']
    ##########################################################################
    ### Editando user - clicando em cima dele (/admin/core/user/1/change/) ###
    ##########################################################################
    # customize fields displayed on admin page instead of showing the default
    # ones for BaseUserAdmin. If you change the titles below, it will change
    # in the admin page also
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']

    ###################################################################
    ### Criando user - clicando em add user (/admin/core/user/add/) ###
    ###################################################################
    # Customizando os fields da page de add user
    add_fieldsets = (
        (None, {
            # css classes
            'classes': ('wide',),
            # fields que aparecem na tela
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

admin.site.register(models.User, UserAdmin)