from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Member(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    OTHER = 'o'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Not specified')
    )
    fam_id = models.CharField(max_length=20, unique=True)
    last_name = models.CharField(max_length=50)
    maiden_name = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50)
    given_names = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=200, blank=True)
    gender = models.CharField(max_length=1,
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


class Event(models.Model):
    MARRIAGE = 'm'
    DIVORCE = 'd'
    TYPE_CHOICES = (
        (MARRIAGE, 'Marriage'),
        (DIVORCE, 'Divorce')
    )
    p1 = models.ForeignKey(Member,
                           related_name='partner1')
    p2 = models.ForeignKey(Member,
                           related_name='partner2')
    date = models.DateField(blank=True, null=True)
    place = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=1,
                            choices=TYPE_CHOICES,
                            default=MARRIAGE)
    def __unicode__(self):
        return self.type + ' of ' + self.p1 + ' and ' + self.p2

class Address(models.Model):
    addr1 = models.CharField(max_length=200, blank=True)
    addr2 = models.CharField(max_length=200, blank=True)
    zip = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=200, blank=True)
    country = CountryField(blank=True)
    def __unicode__(self):
        return self.addr1 + ', ' + self.zip + ' ' + self.city

class Phone(models.Model):
    HOME = 'h'
    WORK = 'w'
    MOBILE = 'm'
    OTHER = 'o'
    TYPE_CHOICES = (
        (HOME, 'Home'),
        (WORK, 'Work'),
        (MOBILE, 'Mobile'),
        (OTHER, 'Other')
    )
    member = models.ForeignKey(Member)
    type = models.CharField(max_length=1,
                            choices=TYPE_CHOICES,
                            default=OTHER)
    number = models.CharField(max_length=50)
    primary = models.BooleanField(default=False)
    def __unicode__(self):
        return self.number

class Email(models.Model):
    member = models.ForeignKey(Member)
    address = models.EmailField()
    primary = models.BooleanField(default=False)
    def __unicode__(self):
        return self.address
