document.addEventListener('DOMContentLoaded', function() {
const urlParams= new URLSearchParams(window.location.search);
const custID=urlParams.get('consumerId');
const custName=urlParams.get('name');
const Email=urlParams.get('email');

document.getElementById('ackCustomerId').innerHTML= custID || "NA";
document.getElementById('ackCustomerName').innerHTML= custName || "NA";
document.getElementById('ackCustomerEmail').innerHTML= Email || "NA";

});