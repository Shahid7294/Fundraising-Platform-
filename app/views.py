from django.shortcuts import redirect, render
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from .models import Donor,DonationArea,Gallery
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from datetime import date
# Create your views here.
def index(request):
    return render(request, "index.html")


def gallery(request):
    gallary=Gallery.objects.all()
    return render(request, "gallery.html",locals())


class login_admin(View):
    def get(self,request):
        form=LoginForm()
        return render(request, "login-admin.html",locals())
    def post(self,request):
        form=LoginForm(request.POST)
        us=request.POST['username']
        psw=request.POST['password']
        try:
            user=authenticate(username=us,password=psw)
            if user:
                if user.is_staff:
                    login(request , user)
                    return redirect('/index-admin')
                else:
                    messages.warning(request , 'Invalid Admin User')
            else:
                messages.warning(request , 'Invalid Username and password')
        except:
            messages.warning(request , 'Login Failed')
        return render(request, "login-admin.html",locals())

class login_donor(View):
    def get(self,request):
        form=LoginForm()
        return render(request, "login-donor.html",locals())
    def post(self,request):
        form=LoginForm(request.POST)
        us=request.POST['username']
        psw=request.POST['password']
        try:
            user=authenticate(username=us,password=psw)
            if user:
                donor_user = Donor.objects.filter(user_id=user.id)
                if donor_user:
                    login(request , user)
                    messages.success(request , 'Login Successfully')
                    return redirect('/index-donor')
                else:
                    messages.warning(request , 'Invalid Donor User')
            else:
                messages.warning(request , 'Invalid Username and password')
        except:
            messages.warning(request , 'Login Failed')
        return render(request, "login-donor.html",locals())
        
class login_volunteer(View):
    def get(self,request):
        form=LoginForm()
        return render(request, "login-volunteer.html",locals())
    def post(self,request):
        form=LoginForm(request.POST)
        us=request.POST['username']
        psw=request.POST['password']
        try:
            user=authenticate(username=us,password=psw)
            if user:
                donor_user = Volunteer .objects.filter(user_id=user.id)
                if donor_user:
                    login(request , user)
                    return redirect('/index-volunteer')
                else:
                    messages.warning(request , 'Invalid Volunteer User')
            else:
                messages.warning(request , 'Invalid Username and password')
        except:
            messages.warning(request , 'Login Failed')
        return render(request, "login-volunteer.html",locals())

class signup_donor(View):
    def get(self,request):
        form1=Userform()
        form2=Donersingupform()
        return render(request, "signup_donor.html",locals())
    def post(self,request):
        form1=Userform(request.POST)
        form2=Donersingupform(request.POST)
        if form1.is_valid() & form2.is_valid():
            un=request.POST['username']
            fn=request.POST['first_name']
            ln=request.POST['last_name']
            em=request.POST['email']
            psw=request.POST['password1']
            cn=request.POST['contact']
            up=request.FILES['userpic']
            ad=request.POST['address']
            try:
                user=User.objects.create_user(username=un,first_name=fn,last_name=ln,email=em,password=psw,)
                Donor.objects.create(user=user,contact=cn,userpic=up,address=ad)
                messages.success(request ,'Congratulations!! Donor Profile Created Successfully')
            except :
                messages.warning(request ,'Profile Not Created')
        return render(request,'signup_donor.html',locals())

class signup_volunteer(View):
    def get(self,request):
        form1=Userform()
        form2=voluntersingupform()
        return render(request, "signup_volunteer.html",locals())
    def post(self,request):
        form1=Userform(request.POST)
        form2=voluntersingupform(request.POST)
        if form1.is_valid() & form2.is_valid():
            un=request.POST['username']
            fn=request.POST['first_name']        
            ln=request.POST['last_name']        
            em=request.POST['email']        
            psw=request.POST['password1']
            con=request.POST['contact']
            up=request.FILES['userpic']
            ip=request.FILES['idpic']
            adr=request.POST['address']
            abm=request.POST['aboutme']
            try:
                user=User.objects.create_user(username=un,first_name=fn,last_name=ln,email=em,password=psw)
                Volunteer.objects.create(user=user,contact=con,userpic=up,idpic=ip,address=adr,aboutme=abm,status='pending')
                messages.success(request ,'Congratulations!! Volunteer  Profile Created Successfully')
            except:
                messages.warning(request ,'Profile Not Created')
            form1=Userform()
            form2=voluntersingupform()
            return render(request, "signup_volunteer.html",locals())
        
def index_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    totaldonations = Donation.objects.all().count()
    totaldonors = Donor.objects.all().count()
    totalvolunteers = Volunteer.objects.all().count()
    totalpendingdonations = Donation.objects.filter(status="pending").count()
    totalaccepteddonations = Donation.objects.filter(status="accept").count()
    totaldelivereddonations = Donation.objects.filter(status='Donation Delivered Successfully').count()
    totaldonationareas =DonationArea.objects.all().count()
    return render(request, "index-admin.html",locals())

# admin dashboard
def pending_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donation = Donation.objects.filter(status = 'pending')
    return render(request, "pending-donation.html",locals())

def accepted_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donation = Donation.objects.filter(status = 'accept')
    return render(request, "accepted-donation.html",locals())

def rejected_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donation = Donation.objects.filter(status = 'reject')
    return render(request, "rejected-donation.html",locals())

def volunteerallocated_donation(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donation = Donation.objects.filter(status = 'volunteer Allocated' )
    return render(request, "volunteerallocated-donation.html",locals())

def donationrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donation = Donation.objects.filter(status = 'Donation Received')
    return render(request, "donationrec-admin.html",locals())

def donationnotrec_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donation = Donation.objects.filter(status = 'Donation Not Received')
    return render(request, "donationnotrec-admin.html",locals())

def donationdelivered_admin(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donation = Donation.objects.filter(status = 'Donation Delivered Successfully')
    return render(request, "donationdelivered-admin.html",locals())

def all_donations(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donation = Donation.objects.all()
    return render(request, "all-donations.html",locals())

def delete_donation(request,pid):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donation = Donation.objects.get(id=pid)
    donation.delete()
    return redirect('all_donations')

def manage_donor(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    donor = Donor.objects.all()
    return render(request, "manage-donor.html",locals())

def new_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    volunteer = Volunteer.objects.filter(status = 'pending')
    return render(request, "new-volunteer.html",locals())

def accepted_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    volunteer = Volunteer.objects.filter(status = 'accept')
    return render(request, "accepted-volunteer.html",locals())

def rejected_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    volunteer = Volunteer.objects.filter(status = 'reject')
    return render(request, "rejected-volunteer.html",locals())

def all_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    volunteer = Volunteer.objects.all()
    return render(request, "all-volunteer.html",locals())

def delete_volunteer(request,pid):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('all_volunteer')

class add_area(View):
    def get(self,request):
        form=DonationAreaForm()
        return render(request, "add-area.html",locals())
    def post(self,request):
        form=DonationAreaForm(request.user)
        if not request.user.is_authenticated:
            return redirect('/login_admin')
        an = request.POST['areaname']
        des= request.POST['description']
        try:
            DonationArea.objects.create(areaname=an,description=des)
            messages.success(request,'Area Added Successfully')
        except:
            messages.success(request,'Area Not Added')
        return render(request, "add-area.html",locals())

class edit_area(View):
    def get(self,request,pid):
        form=DonationAreaForm()
        area=DonationArea.objects.get(id=pid)
        return render(request, "edit-area.html",locals())
    def post(self,request,pid):
        if not request.user.is_authenticated:
           return redirect('/login-admin')
        form=DonationAreaForm(request.POST)
        area=DonationArea.objects.get(id=pid)
        an=request.POST['areaname']
        des =request.POST['description']

        area.areaname = an
        area.description = des

        try:
            area.save()
            messages.success(request , 'Area Update Successfully')
            return redirect('manage_area')
        except:
            messages.warning(request , 'Area Not Updated')
        return render(request, "edit-area.html",locals())

def manage_area(request):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    area = DonationArea.objects.all()
    return render(request, "manage-area.html",locals())

def delete_area(request,pid):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    area = DonationArea.objects.get(id=pid)
    area.delete()
    return redirect('manage_area')

class changepwd_admin(View):
    def get(self,request):
        form=MyPasswordChangeForm(request.user)
        return render(request, "changepwd-admin.html",locals())
    def post(self,request):
        form=MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        old_psw=request.POST['old_password']
        new_psw=request.POST['new_password1']
        conf_new_psw=request.POST['new_password2']
        try:
            if new_psw==conf_new_psw:
                user = User.objects.get(id=request.user.id)
                if user.check_password(old_psw):
                    user.set_password(new_psw)
                    user.save()
                    messages.success(request , 'Change Password Successfully')
                else:
                    messages.warning(request , 'Old Password Not Matched')
            else:
                messages.warning(request , 'Old Password and New Password are different')
        except:
            messages.warning(request , 'Failed to Change Password ')
        return render(request, "changepwd-admin.html",locals())

def logoutuser(request):
    logout(request)
    return redirect("index")


# admin view details
class accepted_donationdetail(View):
    def get(self,request,pid):
        donation =Donation.objects.get(id=pid)
        donationarea =DonationArea.objects.all()
        # volunteer = Volunteer.objects.all()
        volunteer = Volunteer.objects.filter(status = 'accept')
        return render(request, "accepted-donationdetail.html",locals())
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation =Donation.objects.get(id=pid)
        donationareaid = request.POST['donationareaid']
        volunteerid = request.POST['volunteerid']
        adminremark  = request.POST['adminremark']
        da = DonationArea.objects.get(id=donationareaid)
        v =Volunteer.objects.get(id=volunteerid)

        try:
            donation.donationarea = da
            donation.volunteer =v
            donation.adminremark= adminremark
            donation.status = "volunteer Allocated"
            donation.volunteerremark = "Not Update Yet"
            donation.updationdate = date.today()
            donation.save()
            messages.success(request,'Volunteer Allocate Successfully')
        except:
            messages.warning(request,'Failed to allocate volunteer')
        return render(request, "accepted-donationdetail.html",locals())
        
class view_volunteerdetail(View):
    def get(self,request,pid):
        volunteer =Volunteer.objects.get(id=pid)
        return render(request, "view-volunteerdetail.html",locals())
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        volunteer =Volunteer.objects.get(id=pid)
        status = request.POST['status']
        adminremark  = request.POST['adminremark']
        try:
            volunteer.adminremark = adminremark
            volunteer.status = status
            volunteer.updationdate = date.today()
            volunteer.save()
            messages.success(request,'Volunteer Updated Successfully')
        except:
            messages.warning(request,'Volunteer Not Updated ')
        return render(request, "view-volunteerdetail.html",locals())

def view_donordetail(request, pid):
    if not request.user.is_authenticated:
        return redirect('/login-admin')
    donor = Donor.objects.get(id=pid)
    return render(request, "view-donordetail.html",locals())

class view_donationdetail(View):
    def get(self,request,pid):
        donation=Donation.objects.get(id=pid)
        return render(request, "view-donationdetail.html",locals())
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation = Donation.objects.get(id=pid)
        status = request.POST['status']
        adminremark = request.POST['adminremark']
        # print("status = ",status,"remark = ",adminremark)
        try:
            donation.adminremark = adminremark
            donation.status = status
            donation.updationdate = date.today()
            donation.save()
            messages.success(request,'Status & Remark Update Successfully')
        except:
            messages.warning(request , 'Faild to Updated Status & Remark')
        return render(request, "view-donationdetail.html",locals())
        
def delete_donor(request,pid):
    if not request.user.is_authenticated:
        return redirect('/login_admin')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('manage_donor')



# donor dashboard
def index_donor(request):
    if not request.user.is_authenticated:
            return redirect('/login-doner')
    user=request.user
    donor=Donor.objects.get(user=user)
    donationcount = Donation.objects.filter(donor=donor).count()
    acceptedcount = Donation.objects.filter(donor=donor,status = "accept").count()
    rejectedcount = Donation.objects.filter(donor=donor,status = "reject").count()
    pendingcount = Donation.objects.filter(donor=donor,status = "pending").count()
    deliveredcount = Donation.objects.filter(donor=donor,status = "Donation Deliverd Successfully").count()
    return render(request, "index-donor.html",locals())

class donate_now(View):
    def get(self,request):
        form=DonateNowForm()
        return render(request, "donate-now.html",locals())
    def post(self,request):
        form=DonateNowForm(request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-doner')
        if form.is_valid():
            user=request.user
            donor=Donor.objects.get(user=user)
            dn=request.POST['donationname']
            dp=request.FILES['donatiopic']
            cl=request.POST['collectionloc']
            dcp=request.POST['description']
            try:
                Donation.objects.create(donor=donor,donationname=dn,donatiopic=dp,collectionloc=cl,description=dcp,status='pending',donationdate=date.today())
                messages.success(request ,'Congratulations!! Donor Profile Created Successfully')
            except :
                messages.warning(request ,'Profile Not Created')
        return render(request, "donate-now.html",locals())
    
def donation_history(request):
    if not request.user.is_authenticated:
        return redirect('/login-donor')
    user=request.user
    donor=Donor.objects.get(user = user)
    donation=Donation.objects.filter(donor = donor)
    return render(request, "donation-history.html",locals())

class profile_donor(View):
    def get(self,request):
        form1=Userform()
        form2=Donersingupform()
        user=request.user
        donor=Donor.objects.get(user=user)
        return render(request, "profile-donor.html",locals())
    def post(self,request):
        if not request.user.is_authenticated:
            return redirect('/login-donor')
        form1=Userform(request.POST)
        form2=Donersingupform(request.POST)

        user=request.user
        donor=Donor.objects.get(user=user)

        fn = request.POST['firstname']
        ln = request.POST['lastname']
        contact = request.POST['contact']
        address = request.POST['address']

        donor.user.first_name = fn
        donor.user.last_name = ln
        donor.contact = contact
        donor.address = address
        try:
            userpic = request.FILES['userpic']
            donor.userpic = userpic
            donor.save()
            donor.user.save()
            messages.success(request , 'Profile Updated Successfully')
        except Exception as e:
            messages.warning(request , 'Profile Update Failed'+e)
        return render(request, "profile-donor.html",locals())
        
class changepwd_donor(View):
    def get(self,request):
        form=MyPasswordChangeForm(request.user)
        return render(request, "changepwd-donor.html",locals())
    def post(self,request):
        form=MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-doner')
        old_psw=request.POST['old_password']
        new_psw=request.POST['new_password1']
        conf_new_psw=request.POST['new_password2']
        try:
            if new_psw==conf_new_psw:
                user = User.objects.get(id=request.user.id)
                if user.check_password(old_psw):
                    user.set_password(new_psw)
                    user.save()
                    messages.success(request , 'Change Password Successfully')
                else:
                    messages.warning(request , 'Old Password Not Matched')
            else:
                messages.warning(request , 'Old Password and New Password are different')
        except:
            messages.warning(request , 'Failed to Change Password ')
        return render(request, "changepwd-donor.html",locals())
    

# volunteer dashboard
def index_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_volunteer')
    user=request.user
    volunteer = Volunteer.objects.get(user=user)
    totalCollectionReq = Donation.objects.filter(volunteer=volunteer,status = 'volunteer Allocated').count()
    totalRecDonation = Donation.objects.filter(volunteer=volunteer,status = 'Donation Received').count()
    totalNotRecDonation = Donation.objects.filter(volunteer=volunteer,status = 'Donation NotReceived').count()
    totalDonationDelivered = Donation.objects.filter(volunteer=volunteer,status='Donation Delivered Successfully').count()
    return render(request, "index-volunteer.html",locals())

def collection_req(request):
    if not request.user.is_authenticated:
        return redirect('/login_volunteer')
    user=request.user
    volunteer = Volunteer.objects.get(user=user)
    donation= Donation.objects.filter(volunteer=volunteer,status="volunteer Allocated")
    return render(request, "collection-req.html",locals())

def donationrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_volunteer')
    user=request.user
    volunteer = Volunteer.objects.get(user=user)
    donation= Donation.objects.filter(volunteer=volunteer,status = "Donation Received")
    return render(request, "donationrec-volunteer.html",locals())

def donationnotrec_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_volunteer')
    user=request.user
    volunteer = Volunteer.objects.get(user=user)
    donation= Donation.objects.filter(volunteer=volunteer,status = "Donation Not Received")
    return render(request, "donationnotrec-volunteer.html",locals())

def donationdelivered_volunteer(request):
    if not request.user.is_authenticated:
        return redirect('/login_volunteer')
    user = request.user
    volunteer = Volunteer.objects.get(user=user)
    donation = Donation.objects.filter(volunteer = volunteer , status = 'Donation Delivered Successfully')
    return render(request, "donationdelivered-volunteer.html",locals())

class profile_volunteer(View):
    def get(self,request):
        form1=Userform()
        form2=voluntersingupform()
        user=request.user
        volunteer = Volunteer.objects.get(user=user)
        return render(request, "profile-volunteer.html",locals())
    def post(self,request):
        if not request.user.is_authenticated:
            return redirect('/login_volunteer')
        form1 = Userform(request.POST)
        form2 = voluntersingupform(request.POST)

        user=request.user
        volunteer = Volunteer.objects.get(user=user)

        fn = request.POST['firstname']
        ln = request.POST['lastname']
        contact = request.POST['contact']
        address = request.POST['address']
        aboutme = request.POST['aboutme']

        volunteer.user.first_name =fn
        volunteer.user.last_name =ln
        volunteer.contact =contact
        volunteer.address =address
        volunteer.aboutme =aboutme

        try:
            userpic =request.FILES['userpic']
            volunteer.userpic = userpic
            idpic = request.FILES['idpic']
            volunteer.idpic =idpic
            volunteer.save()
            volunteer.user.save()
            messages.success(request , 'Profile Updated Successfully')
        except Exception as e:
            messages.warning(request , 'Profile Updated Failed')
        return render(request, "profile-volunteer.html",locals())

class changepwd_volunteer(View):
    def get(self,request):
        form=MyPasswordChangeForm(request.user)
        return render(request, "changepwd-volunteer.html",locals())
    def post(self,request):
        form=MyPasswordChangeForm(request.user,request.POST)
        if not request.user.is_authenticated:
            return redirect('/login-volunteer')
        old_psw=request.POST['old_password']
        new_psw=request.POST['new_password1']
        conf_new_psw=request.POST['new_password2']
        try:
            if new_psw==conf_new_psw:
                user = User.objects.get(id=request.user.id)
                if user.check_password(old_psw):
                    user.set_password(new_psw)
                    user.save()
                    messages.success(request , 'Change Password Successfully')
                else:
                    messages.warning(request , 'Old Password Not Matched')
            else:
                messages.warning(request , 'Old Password and New Password are different')
        except:
            messages.warning(request , 'Failed to Change Password ')
        return render(request, "changepwd-volunteer.html",locals())


# view details
def donationdetail_donor(request, pid):
    if not request.user.is_authenticated:
        return redirect('/login-volunteer')
    donation = Donation.objects.get(id=pid)
    return render(request, "donationdetail-donor.html",locals())

class donationcollection_detail(View):
    def get(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation=Donation.objects.get(id=pid)
        return render(request,"donationcollection-detail.html",locals())
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation=Donation.objects.get(id=pid)
        status=request.POST['status']
        volunteerremark = request.POST['volunteerremark']
        try:
            donation.status=status
            donation.volunteerremark=volunteerremark
            donation.updationdate=date.today()
            donation.save()
            messages.success(request,'Volunteer Status & Remark update Successfully')
        except:
            messages.warning(request,'Failed to update Volunteer Status & Remark')
        return render(request,"donationcollection-detail.html",locals())
       
class donationrec_detail(View):
    def get(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation=Donation.objects.get(id=pid)
        return render(request, "donationrec-detail.html",locals())
    def post(self,request,pid):
        if not request.user.is_authenticated:
            return redirect('/login-admin')
        donation=Donation.objects.get(id=pid)
        status = request.POST['status']
        deliverypic = request.FILES['deliverypic']
        try:
            donation.status = status
            donation.updationdate = date.today()
            donation.save()
            Gallery.objects.create(donation =donation,deliverpic=deliverypic)
            messages.success(request,'Donation Delivered Successfully')
        except:
            messages.warning(request,'Donation Delivered Faild')
        return render(request, "donationrec-detail.html",locals())
    
