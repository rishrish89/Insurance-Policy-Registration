document.addEventListener('DOMContentLoaded', function() {
    // Function to generate a random consumer ID
    function generateConsumerId() {
      const timestamp = new Date().getTime();
      const randomNum = Math.floor(1000000 + Math.random() * 9000000);;
      return `${randomNum}`;
    }

    // Set the generated consumer ID to the input field
    const consumerIdInput = document.getElementById('consumerId');
    consumerIdInput.value = generateConsumerId();
  });

function validateForm() {
  var password= document.getElementById('password').value;
  var contact= document.getElementById('contact').value;

  var  passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
  if (!passwordRegex.test(password)) {
    document.getElementById('passwordError').innerHTML='Password is too weak';
    return false;
  }

  var contactRegex= /^[6-9]\d{9}$/;
  if (contact.length !== 10 || !contactRegex.test(contact)) {
    document.getElementById('contactError').innerHTML='Invalid Contact Number';
    return false;
  }
  
  

  return true;
}

function validateMobileNumber(contact) {
  // Check if the input is a 10-digit number starting with 6, 7, 8, or 9
  const regex = /^[6-9]\d{9}$/;
  
  if (regex.test(contact)) {
    return "Valid mobile number!";
  } else {
    return "Invalid mobile number. Please enter a 10-digit number starting with 6, 7, 8, or 9.";
  }
}

function redirecttoAcknowledgement() {
  window.location.href="./acknowledgement.html"
}