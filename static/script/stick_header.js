function addSticky(){
    let nav = document.getElementById("nav-bar")
    let foot = document.getElementById("footer")
    let sticky = nav.offsetTop
    if (window.pageYOffset > sticky) {
        nav.classList.add("sticky")
        $('.head_input').addClass('placeholder_black')
        $('.head_submit').addClass('head_submit_white')


    } else {
        nav.classList.remove("sticky");
        $('.head_input').removeClass('placeholder_black')
        $('.head_submit').removeClass('head_submit_white')

    }
};

window.addEventListener("scroll", addSticky);