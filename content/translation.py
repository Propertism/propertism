from modeltranslation.translator import translator, TranslationOptions
from .models import (
    CompanyInfo, Service, CoreValue, TeamMember,
    ExpertiseArea, BlogPost
)


class CompanyInfoTranslationOptions(TranslationOptions):
    fields = ('company_name', 'tagline', 'about_mission', 'about_description', 
              'hero_eyebrow', 'hero_title', 'hero_description')


class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'full_description')


class CoreValueTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('name', 'role', 'department', 'bio')


class ExpertiseAreaTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class BlogPostTranslationOptions(TranslationOptions):
    fields = ('title', 'excerpt', 'content')


translator.register(CompanyInfo, CompanyInfoTranslationOptions)
translator.register(Service, ServiceTranslationOptions)
translator.register(CoreValue, CoreValueTranslationOptions)
translator.register(TeamMember, TeamMemberTranslationOptions)
translator.register(ExpertiseArea, ExpertiseAreaTranslationOptions)
translator.register(BlogPost, BlogPostTranslationOptions)
