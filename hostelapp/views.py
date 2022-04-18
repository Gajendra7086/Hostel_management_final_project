from django.contrib.auth.hashers import check_password
from django.contrib.messages import error
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader
from hostelproject import settings
from .forms import *
from .models import *
import random
from email_validator import validate_email


def check_mailid(email):
    if validate_email(email, check_deliverability=False):
        return True
    else:
        return False


def password_generator():
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = "".join(random.sample(s, 6))
    return password


def loginpage(request):
    form = loginForm()
    return render(request, 'loginpage.html', {'form': form})


def login_details(request):
    if request.session.has_key('logged_in_as_hostler'):
        return render(request, 'hostler.html')
    elif request.session.has_key('logged_in_as_admin'):
        return render(request, 'hostel_admin.html')
    elif request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_warden_owner:
                    login(request, user)
                    if user.details_status:
                        request.session['logged_in_as_admin'] = True
                        return render(request, 'hostel_admin.html')
                    else:
                        return redirect('/hostel_admin/hostel_details/')
                elif user.is_hostler:
                    login(request, user)
                    if user.details_status:
                        request.session['logged_in_as_hostler'] = True
                        return render(request, 'hostler.html')
                    else:
                        return redirect('/hosteler/hosteler_details/')
            else:
                error(request, 'Invalid username or password')
                return redirect(loginpage)
        else:
            error(request, 'Please enter the valid details')
            return redirect(loginpage)
    else:
        return redirect(loginpage)


def hostel_register(request):
    if request.method == 'POST':
        userform = user_creationForm(request.POST)
        if userform.is_valid:
            userform.save()
            return redirect(loginpage)
    userform = user_creationForm()
    return render(request, 'hostel_register.html', {'userform': userform})


def hostel_admin(request):
    return render(request, 'hostel_admin.html')


def hostel_details(request):
    if request.method == "POST":
        address = request.POST.get('hostel_address')
        no_of_rooms = request.POST.get('no_of_rooms')
        hostel_name = request.user
        Hostel(address=address, no_of_rooms=no_of_rooms, hostel_name_user=hostel_name,
               hostel_name=hostel_name.hostel_name).save()
        status = request.user
        status.details_status = True
        status.save()
        return render(request, 'hostel_admin.html')
    hostel_name = request.user.hostel_name
    return render(request, 'first/hostel_admin_first.html', {'hostel_name': hostel_name})


def hosteler_details(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_no = request.POST.get('mobile_no')
        addhar_no = request.POST.get('addhar_no')
        current_user = request.user
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.mobile_no = mobile_no
        current_user.addhar_no = addhar_no
        current_user.details_status = True
        current_user.save()
        return render(request, 'hostler.html')
    else:
        hostel_name = request.user.hostel_name
        return render(request, 'first/hosteler_first.html', {'hostel_name': hostel_name})


def emailValidation(request):
    otp = request.POST.get('otp')
    if request.session['otp'] == otp:
        return HttpResponse('valid')
    else:
        return HttpResponse('not valid')


def add_hostler(request):
    entered_email = request.POST.get('hostler_email')
    code = password_generator()
    name = request.POST.get('name')
    request.session['otp'] = code
    html_message = loader.render_to_string('emails/add_hostler_email.html', {'otp': code})
    mail = send_mail('Email Verification', '', settings.EMAIL_HOST_USER, [entered_email],
                     html_message=html_message,
                     fail_silently=False)
    if mail:
        hostel = Hostel.objects.get(hostel_name=request.user.hostel_name)
        Hostel_verification(email=entered_email, code=code, name=name, hostel_name=hostel).save()
        return redirect('/hostel_admin/verify_hostlers_page/')
    else:
        error(request, 'enter the correct Email id')
        return redirect('/hostel_admin/verify_hostler/')


def verify_hostlers_page(request):
    Hostel_id = Hostel.objects.get(hostel_name=request.user.hostel_name)
    details = Hostel_verification.objects.filter(hostel_name=Hostel_id.id)
    return render(request, 'verify_hostler.html', {'details': details})


def verify_hostler(request, id):
    code = request.POST.get('code')
    hostler_code = Hostel_verification.objects.get(id=id)
    if hostler_code.code == code:
        generated_password = password_generator()
        html_message = loader.render_to_string('emails/hostler_credential.html', {'otp': generated_password})
        mail = send_mail('Email Verification', '', settings.EMAIL_HOST_USER, [hostler_code.email],
                         html_message=html_message,
                         fail_silently=True)
        if mail:
            password = make_password(generated_password)
            User(username=hostler_code.email, password=password, is_hostler=True,
                 hostel_name=request.user.hostel_name).save()
            hostler_code.delete()
            return redirect(login_details)
        else:
            # error(request, 'enter the correct Email id')
            return redirect(verify_hostlers_page)
    else:
        return redirect(verify_hostlers_page)


def delete_verify_hostler(request, id):
    hostler_details = Hostel_verification.objects.get(id=id)
    hostler_details.delete()
    return redirect(verify_hostlers_page)


def hostler(request):
    return render(request, 'hostler.html')


def hostler_complain(request):
    if request.method == "POST":
        name = request.user
        hostel_name = Hostel.objects.get(hostel_name=request.user.hostel_name)
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Complain(name=name, hostel_name=hostel_name, subject=subject, message=message).save()
        return redirect('/hostler/complain_status/')
    else:
        return render(request, 'hostler_complain.html')


def hostler_complain_status(request):
    id = request.user.id
    data = Complain.objects.filter(name=id)
    return render(request, 'hostler_complain_status.html', {'data': data})


def hostel_admin_complains(request):
    Hostel_id = Hostel.objects.get(hostel_name=request.user.hostel_name)
    data = Complain.objects.filter(hostel_name=Hostel_id.id)
    return render(request, 'hostel_admin_complain_status.html', {'data': data})


def hostel_admin_payment(request):
    if request.method == "POST":
        hostel_id = Hostel.objects.get(hostel_name=request.user.hostel_name)
        hostel_name = Hostel.objects.get(hostel_name=hostel_id)
        slip_no = request.POST.get('slip_no')
        date = request.POST.get('date')
        name = request.POST.get('name')
        month_year = request.POST.get('month_year')
        amount = request.POST.get('amount')
        remark = request.POST.get('remark')
        Payment(hostel_name=hostel_name, slip_no=slip_no, date=date, name=name, month_year=month_year, amount=amount,
                remark=remark).save()
        return redirect('/hostel_admin/payment_list/')
    names = User.objects.filter(hostel_name=request.user.hostel_name).values_list('first_name', flat=True)
    hostel_id = Hostel.objects.get(hostel_name=request.user.hostel_name)
    slip_numbers = Payment.objects.filter(hostel_name=hostel_id).order_by('slip_no').values_list('slip_no', flat=True)
    try:
        slip_number = slip_numbers.last() + 1
    except:
        slip_number = 1
    return render(request, 'payment.html', {'names': names, 'slip_number': slip_number})


def hostel_admin_payment_list(request):
    hostel_id = Hostel.objects.get(hostel_name=request.user.hostel_name)
    data = Payment.objects.filter(hostel_name=hostel_id)
    return render(request, 'hostel_admin_payment_list.html', {'data': data})


def change_password(request):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    if check_password(old_password, request.user.password):
        request.user.password = make_password(new_password)
        request.user.save()
        username = request.user.username
        password = new_password
        user = authenticate(request, username=username, password=password)
        login(request, user)
        if user.is_warden_owner:
            request.session['logged_in_as_admin'] = True
            return render(request, 'hostel_admin.html')
        elif user.is_hostler:
            return render(request, 'hostler.html')
        return redirect('/login_details/')


def all_hostler(request):
    data = User.objects.filter(hostel_name=request.user.hostel_name, is_hostler=True)
    return render(request, 'all_hostler.html', {'data': data})


def change_complain_status(request, id):
    status = request.POST.get('status')
    complain = Complain.objects.get(id=id)
    complain.complain_status = status
    complain.save()

    return redirect(hostel_admin_complains)


def payment_receipt(request):
    data = Payment.objects.filter(name=request.user.first_name)
    return render(request, 'payment_receipt.html', {'data': data})


def forgot_password(request):
    email = request.POST.get('email')
    email = email.upper()
    try:
        user_data = User.objects.get(username=email)
        generated_password = password_generator()
        html_message = loader.render_to_string('emails/mail.html', {'otp': generated_password})
        mail = send_mail('Forgot Password', '', settings.EMAIL_HOST_USER, [email],
                         html_message=html_message,
                         fail_silently=True)
        if mail:
            password = make_password(generated_password)
            user_data.password = password
            user_data.save()
            return redirect(loginpage)
        else:
            error(request, 'Try again')
            return redirect(loginpage)
    except:
        error(request, 'User name not available')
        return redirect(loginpage)


def logout_user(request):
    logout(request)
    return render(request, 'logout.html')


# -------------------------------------------ajax--------------------------------------------------------
def check_hostler_email(request):
    entered_email = request.POST.get('email')
    if check_mailid(entered_email):
        all_users = User.objects.all()
        for single_user in all_users:
            if str(single_user.username) == entered_email:
                return HttpResponse('not unique')
        else:
            return HttpResponse('unique')
    else:
        return HttpResponse('no-mail')


def hostelNameChecker(request):
    name = request.POST.get('hostel_name')
    all_hostel = User.objects.filter(hostel_name=name).values_list('hostel_name', flat=True)
    if name in all_hostel:
        return HttpResponse('not unique')
    else:
        return HttpResponse('unique')


def emailGeneration(request):
    entered_email = request.POST.get('email')
    if check_mailid(entered_email):
        print('yes')
        all_users = User.objects.all()
        for single_user in all_users:
            if str(single_user.username) == entered_email:
                return HttpResponse('not unique')
        else:
            otp = password_generator()
            request.session['otp'] = otp
            html_message = loader.render_to_string('emails/otp_email.html', {'otp': otp})
            mail = send_mail('Email Verification', '', settings.EMAIL_HOST_USER, [entered_email],
                             html_message=html_message,
                             fail_silently=False)
            if mail:
                return HttpResponse('send')
            else:
                return HttpResponse('not send')
    else:
        return HttpResponse('not valid')
