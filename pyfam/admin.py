from django.contrib import admin
from pyfam.models import Member, Event, Address, Phone, Email

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0

class EmailInline(admin.TabularInline):
    model = Email
    extra = 0

class MemberAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,           {'fields': [('fam_id', 'gender'),
                                     ('last_name', 'maiden_name'),
                                     ('first_name', 'given_names')]}),
        ('Contact Info', {'fields': ['address'],
                          'classes': []}),
    ]
    inlines = [PhoneInline, EmailInline] # TODO: sort these to Contact Info
    # TODO: add relatives to form again
    list_display = ('fam_id', 'first_name', 'last_name')
    list_filter = ['fam_id']
    search_fields = ['fam_id', 'last_name', 'first_name']

admin.site.register(Member, MemberAdmin)
admin.site.register(Event)
admin.site.register(Address)
# admin.site.register(Phone)
# admin.site.register(Email)
