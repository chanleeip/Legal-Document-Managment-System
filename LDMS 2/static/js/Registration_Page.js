// Select all input elements for varification
const name = document.getElementById("name");
const email = document.getElementById("email");
const password = document.getElementById("password");
const phoneNumber = document.getElementById("phoneNumber");
const gender = document.registration;
const language = document.getElementById("language");
const zipcode = document.getElementById("zipcode");

// function for form varification
function formValidation() {

    // checking name length
    if (name.value.length < 2 || name.value.length > 20) {
        alert("Name length should be more than 2 and less than 21");
        name.focus();
        return false;
    }
    // checking email
    if (email.value.match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/)) {
        alert("Please enter a valid email!");
        email.focus();
        return false;
    }
    // checking password
    if (!password.value.match(/^.{5,15}$/)) {
        alert("Password length must be between 5-15 characters!");
        password.focus();
        return false;
    }
    // checking phone number
    if (!phoneNumber.value.match(/^[1-9][0-9]{9}$/)) {
        alert("Phone number must be 10 characters long number and first digit can't be 0!");
        phoneNumber.focus();
        return false;
    }
    // checking gender
    if (gender.gender.value === "") {
        alert("Please select your gender!");
        return false;
    }
    // checking language
    if (language.value === "") {
        alert("Please select your language!")
        return false;
    }
    // checking zip code
    if (!zipcode.value.match(/^[0-9]{6}$/)) {
        alert("Zip code must be 6 characters long number!");
        zipcode.focus();
        return false;
    }
    return true;
}