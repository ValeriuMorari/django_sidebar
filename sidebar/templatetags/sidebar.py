from django import template

register = template.Library()


@register.inclusion_tag('sidebar/user.html', takes_context=True)
def add_user_profile(context):
    return {
        'initials': f'{context.request.user.profile.givenName[0]}{context.request.user.profile.sn[0]}',
        'surname': f'{context.request.user.profile.sn}',
        'name': f'{context.request.user.profile.givenName if not None else context.request.user.username}',
        'email': f'{context.request.user.email}',
        'user_profile_link': f'user_profile/{context.request.user.profile.pk}',
        'logout_link': 'logout',
    }
