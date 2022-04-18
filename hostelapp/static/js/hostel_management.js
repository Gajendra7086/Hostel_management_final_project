function emailChecker(email){
    email = email.toUpperCase()
    $.ajax({
    type:'POST',
    url:'/check_hostler_email/',
    data:{
        email:email,
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        },
    success:function(data){
                let emailText = document.getElementById('email_text');
                if( data == 'not unique'){
                emailText.style.color = "red";
                emailText.innerHTML = "Already have an account";
                document.getElementById('generate_otp_button').disabled=true
                }
                else if(data == 'unique'){
                    emailText.style.color = "green";
                    emailText.innerHTML = "available";
                    document.getElementById('generate_otp_button').disabled=false
                }
                else{
                emailText.style.color = "red";
                emailText.innerHTML = "not a valid mail";
                document.getElementById('generate_otp_button').disabled=true
                    }
        return data
        }
    })
}