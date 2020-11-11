function IsButtonNeeded() {
    var mybutton = document.getElementById("myBtn");

    if (document.body.scrollTop > 0 || document.documentElement.scrollTop > 0) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

function ShowButton() {
    document.getElementById("myBtn").style.display = "block";
}

function topFunction() {
    var mybutton = document.getElementById("myBtn");

    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera

    mybutton.style.display = "none";
}