from django.contrib import admin
from .models import Donor,Volunteer,DonationArea,Donation,Gallery
# Register your models here.
@admin.register(Donor)
class Doneradmin(admin.ModelAdmin):
    list_display=('id','user','contact','address','regdate')

@admin.register(Volunteer)
class volunterradmin(admin.ModelAdmin):
    list_display = ('id','user','contact','address','regdate')

@admin.register(DonationArea)
class DonationAreaadmin(admin.ModelAdmin):
    list_display = ('id','areaname','description','creationdate')
    
@admin.register(Donation)
class Donationadmin(admin.ModelAdmin):
    list_display = ('id','donor','volunteer','donationarea','donationname')
@admin.register(Gallery)
class Galleryadmin(admin.ModelAdmin):
    list_display = ('id','donation','deliverpic','creationdate')
