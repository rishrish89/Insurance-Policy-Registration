history.pushState(null, null, document.URL);
        window.addEventListener('popstate', function () {
            history.pushState(null, null, document.URL);
        });

function validateLoginForm(){
    var username= document.getElementById('username').value;
    var password= document.getElementById('password').value;

    if (username==='' || password===''){
        document.getElementById('usernameError').innerHTML=(username==='')?'Username is required':'';
        document.getElementById('passwordError').innerHTML=(username==='')?'Password is required':'';
        return false;
    }
    
    return true;
}