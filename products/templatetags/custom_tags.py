from django import template
from base.models import CompanyModel, User

register = template.Library()

@register.simple_tag
def get_company_logo(username):
    try:
        user = User.objects.get(username=username)
        company = CompanyModel.objects.get(company=user)
        return company.company_logo.url
    except User.DoesNotExist:
        return "User not found"
    except CompanyModel.DoesNotExist:
        return "Company not found"
