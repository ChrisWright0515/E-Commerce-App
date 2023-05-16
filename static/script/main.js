const options = document.querySelectorAll('.prod_option')
const small_pics = document.querySelectorAll('.small_pic')
const big_pic = document.getElementById('big_pic')
let view_complaints_btn = document.querySelectorAll('.view_complaints_btn')
let stars = document.querySelectorAll('.star')
let filter_stars = document.querySelectorAll('.filter_star')
let chatWrapper = document.querySelectorAll('.chat_messages');
let show_sign_in_btn = document.querySelectorAll('show_sign_in')
chatWrapper.forEach(chat => {
    x = chat.scrollHeight;
    chat.scrollTo(0, x + 50)
});

function addSticky(){
    let nav = document.getElementById("nav-bar")
    let foot = document.getElementById("footer")
    let sticky = nav.offsetTop
    if (window.pageYOffset > sticky) {
        nav.classList.add("sticky")
        $('.head_input').addClass('placeholder_black')
        $('.head_submit').addClass('head_submit_white')
        foot.classList.remove("animate__slideOutDown")
        foot.classList.add("animate__slideInUp")
        foot.classList.add("footer-sticky")

    } else {
        nav.classList.remove("sticky");
        $('.head_input').removeClass('placeholder_black')
        $('.head_submit').removeClass('head_submit_white')
        foot.classList.remove("animate__slideInUp")
        foot.classList.add("animate__slideOutDown")
    }
};
$('#sign_in').on('click', () => {
    $('#login_form').slideToggle(500);
});

$('.show_sign_in').on('click', () => {
    $('#login_form').slideToggle(500);
});


$("#add_chat").on('click', () => {
    chat = document.getElementById('add_chat')
    form = chat.nextElementSibling
    form.style.display = 'flex'
    $(chat).slideUp(500)
});

function change_pic(){
    url = this.src
    big_src = big_pic.src
    big_pic.src = url
    this.src = big_src

}

function get_stars(){
    radio = this.previousElementSibling
    if (this.name == "star-outline"){
        radio.checked = true
        for (let i = 0; i < stars.length; i++) {
            stars[i].name = "star-outline"
        }
        for (let i = 0; i < radio.value; i++) {
            stars[i].name = "star"
        }
    }else{
        radio.checked = false
        for (let i = 0; i < stars.length; i++) {
            stars[i].name = "star-outline"
        }
    }
};
function get_filter_stars(){
    radio = this.previousElementSibling        
    for (let i = 0; i < filter_stars.length; i++) {
        filter_stars[i].name = "star-outline"
        filter_stars[i].removeEventListener('mouseover', fill_stars)
    }
    for (let i = 0; i < radio.value; i++) {
        filter_stars[i].name = "star"
    }
    radio.checked = true
    radio.form.submit()
    
};
function fill_stars(){
    radio = this.previousElementSibling
    for (let i = 0; i < filter_stars.length; i++) {
        filter_stars[i].name = "star-outline"
    }
    for (let i = 0; i < radio.value; i++) {
        filter_stars[i].name = "star"
    }
};
filter_stars.forEach(star => {
    star.addEventListener('mouseover', fill_stars)
});
filter_stars.forEach(star => {
    star.addEventListener('click', get_filter_stars)
});
stars.forEach(star => {
    star.addEventListener('click', get_stars)
});
small_pics.forEach(pic => {
    pic.addEventListener('click', change_pic)
})
options.forEach(option => {
    option.addEventListener('click',get_options)
})
$(".update_qty").keypress(function (evt) {
    evt.preventDefault();
});
view_complaints_btn.forEach(button => {
    button.addEventListener('click', () => {
        let icon = button.firstElementChild
        show_complaints = button.nextElementSibling
        if (show_complaints.style.display == 'none'){
            $(show_complaints).slideDown(500)
            icon.style.transform = 'rotate(180deg)'
            show_complaints.style.display = 'block'
        }else{
            $(show_complaints).slideUp(500)
            icon.style.transform = 'rotate(0deg)'
        }
    });
});