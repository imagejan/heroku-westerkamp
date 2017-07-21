from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy
from django_countries.fields import CountryField

class Member(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    OTHER = 'o'
    GENDER_CHOICES = (
        (MALE, _('male')),
        (FEMALE, _('female')),
        (OTHER, _('not specified'))
    )
    fam_id = models.CharField(_('fam ID'), max_length=20, unique=True)
    last_name = models.CharField(_('last name'), max_length=50)
    maiden_name = models.CharField(_('maiden name'), max_length=50, blank=True)
    first_name = models.CharField(_('first name'), max_length=50)
    given_names = models.CharField(_('given names'), max_length=100, blank=True)
    comment = models.CharField(_('comment'), max_length=200, blank=True)
    gender = models.CharField(_('gender'), max_length=1,
                              choices=GENDER_CHOICES,
                              default=OTHER)
    # birth defined in model Birth
    # marriage/divorce defined in model Event
    user = models.OneToOneField(User, blank=True, null=True)
    partner = models.OneToOneField('self', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=100, blank=True)
    death_date = models.DateField(blank=True, null=True)
    death_place = models.CharField(max_length=100, blank=True)
    is_alive = models.BooleanField(default=False)
    mother = models.ForeignKey('self',
                               related_name='mother_of',
                               blank=True,
                               null=True)
    father = models.ForeignKey('self',
                               related_name='father_of',
                               blank=True,
                               null=True)
    address = models.ForeignKey('Address',
                                blank=True,
                                null=True)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.fam_id + ' (' + self.first_name + ' ' + self.last_name + ')'
    def save(self, checkPartner = True, *args, **kwargs):
        if self.death_date is not None:
            self.is_alive = False
        super(Member, self).save()
        if self.partner and checkPartner:
            self.partner.partner = self
            self.partner.save(checkPartner = False)
    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')


class Event(models.Model):
    MARRIAGE = 'm'
    DIVORCE = 'd'
    TYPE_CHOICES = (
        (MARRIAGE, _('marriage')),
        (DIVORCE, _('divorce'))
    )
    p1 = models.ForeignKey(Member,
                           related_name='partner1')
    p2 = models.ForeignKey(Member,
                           related_name='partner2')
    date = models.DateField(_('date'), blank=True, null=True)
    place = models.CharField(_('place'), max_length=100, blank=True)
    type = models.CharField(_('type'), max_length=1,
                            choices=TYPE_CHOICES,
                            default=MARRIAGE)
    def __unicode__(self):
        return self.type + ' of ' + self.p1 + ' and ' + self.p2
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')

class Address(models.Model):
    addr1 = models.CharField(_('street'), max_length=200, blank=True)
    addr2 = models.CharField(_('street2'), max_length=200, blank=True)
    zip = models.CharField(_('zip'), max_length=10, blank=True)
    city = models.CharField(_('city'), max_length=200, blank=True)
    country = CountryField(_('country'), blank=True)
    def __unicode__(self):
        return self.addr1 + ', ' + self.zip + ' ' + self.city
    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')


class Phone(models.Model):
    HOME = 'h'
    WORK = 'w'
    MOBILE = 'm'
    OTHER = 'o'
    TYPE_CHOICES = (
        (HOME, pgettext_lazy('Phone number', 'Home')),
        (WORK, _('Work')),
        (MOBILE, _('Mobile')),
        (OTHER, _('Other'))
    )
    member = models.ForeignKey(Member)
    type = models.CharField(_('type'), max_length=1,
                            choices=TYPE_CHOICES,
                            default=OTHER)
    number = models.CharField(_('number'), max_length=50)
    primary = models.BooleanField(_('primary'), default=False)
    def __unicode__(self):
        return self.number
    class Meta:
        verbose_name = _('phone number')
        verbose_name_plural = _('phone numbers')

class Email(models.Model):
    member = models.ForeignKey(Member)
    address = models.EmailField(_('email address'))
    primary = models.BooleanField(_('primary'), default=False)
    def __unicode__(self):
        return self.address
    class Meta:
        verbose_name = _('email address')
        verbose_name_plural = _('email addresses')
