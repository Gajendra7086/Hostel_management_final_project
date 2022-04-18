var passwordMatched = 0,emailVerified = 0,hostelName = 0
function mobileNumber(){
    let number = document.getElementById('id_mobile_no').value;
    let mobile_text = document.getElementById('mobile_text')
    if(number.length == 10)
    {
    mobile_text.innerHTML="";
    }
    else{
        mobile_text.style.color = "red";
        mobile_text.innerHTML = "wrong mobile number"
    }
}

function hostelNameChecker(hostel){
    hostel = hostel.toUpperCase();
    $.ajax({
        type:'POST',
        url:'/hostelNameChecker/',
        data:{
            hostel_name:hostel,
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
            },
        success:function(data){
            console.log(data)
            if(data == 'unique'){
            document.getElementById('hostelName-text').innerHTML="";
                hostelName=1
                }
            else if (data == 'not unique'){
            document.getElementById('hostelName-text').style.color="red";
             document.getElementById('hostelName-text').innerHTML = "Hostel name not available";
                hostelName=0
            }
        }
    })
}
var timeLeft = 60;
var timerId;
function countdown() {
    if (timeLeft == -1) {
        clearTimeout(timerId);
        document.getElementById('resend-btn').hidden=false;
        document.getElementById('resend-text').hidden=true;
    } else {
        document.getElementById('resend-text').innerHTML = timeLeft + ' seconds remaining';
        timeLeft--;
    }
}

function otpGenerator(){
    if (document.getElementById('id_username').value.length == 0){
        document.getElementById('email-text').innerHTML = "enter the valid email";
    }
    else{
        document.getElementById('email-text').innerHTML = "";
        $.ajax({
        type:'POST',
        url:'/emailGeneration/',
        data:{
            email:document.getElementById('id_username').value,
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
            },
        success:function(data){
            if(data == 'not valid'){
                document.getElementById('email-text').innerHTML = "enter the valid email";
                }
            else if (data == 'not unique'){
             document.getElementById('email-text').innerHTML = "entered email already exist";
            }
            else if(data == "send"){
                document.getElementById('otp').hidden=false;
                document.getElementById('otpGen').hidden=true;
                document.getElementById('valid-btn').hidden=false;
                timerId = setInterval(countdown, 1000);
                document.getElementById('id_username').readOnly=true;
                emailVerified = 1;
               }
        }
    })
    }
}

function otpValidator(){
    $.ajax({
            type:'POST',
            url:'/emailValidation/',
            data:{
                otp:document.getElementById('otp').value,
                csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
                },
            success:function(data){
                if (data == 'valid'){
                    document.getElementById('email-text').innerHTML = "email is validated successfully"
                    document.getElementById('email-text').style.color = "green"
                    document.getElementById('otp').hidden=true;
                    document.getElementById('otpGen').hidden=true;
                    document.getElementById('valid-btn').hidden=true;
                    document.getElementById('resend-btn').hidden=true;
                    document.getElementById('id_username').readOnly=true;
                }
                else{
                    document.getElementById('email-text').innerHTML = "wrong otp entered"
                }
            }
    })
}

function matchingOfPassword(){
    let password1 = document.getElementById('id_password').value;
    let password2 = document.getElementById('confirm_pass').value;
    if( password1 == password2){
        document.getElementById('password_text').innerHTML = "";
        passwordMatched = 1
//        document.getElementById('submit_button').disabled = false;
        }
    else
        {
//        document.getElementById('submit_button').disabled = true;
        passwordMatched=0
        document.getElementById('password_text').innerHTML = "passwords doesn't match";
        }
}
function nextPage(){
    var test = 0
    var fields = ['id_first_name','id_last_name','id_mobile_no','id_hostel_name',]
    for ( i=0;i<fields.length;i++){
        if(document.getElementById(fields[i]).value.length==0){
        document.getElementById(fields[i]).style.borderColor = "red"
        test = test+1
        }
        else{
        document.getElementById(fields[i]).style.borderColor = "#c3c3c3";
        }
    }
    if(document.getElementById('id_mobile_no').value.length != 10){
    document.getElementById('id_mobile_no').style.borderColor = "red"
    document.getElementById('mobile_text').innerHTML = "Mobile no must be 10 digit"
    test = test+1
    }
    if(test == 0 && hostelName == 1){
    document.getElementById('page1').hidden=true
    document.getElementById('page2').hidden=false}
}
function previousPage(){
    document.getElementById('page2').hidden=true;
    document.getElementById('page1').hidden=false;
}

function submitForm(){
    if(passwordMatched == 1){
        if(emailVerified == 1){
        document.getElementById('hostelCreation').submit();
        }
        else{
        document.getElementById('id_username').style.borderColor = "red";
        document.getElementById('email-text').innerHTML = "email not verified"
        }
    }
    else {
    document.getElementById('password_text').innerHTML = "password doesn't match";
    }
}
