const options = document.querySelectorAll('.prod_option')
const small_pics = document.querySelectorAll('.small_pic')
const big_pic = document.getElementById('big_pic')
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


    function change_pic(){
        console.log(this.src)
        url = this.src
        big_src = big_pic.src
        big_pic.src = url
        this.src = big_src

    }
    function get_options(){
        console.log(this.value)
    }

small_pics.forEach(pic => {
    pic.addEventListener('click', change_pic)
})
options.forEach(option => {
    option.addEventListener('click',get_options)
})
$(".update_qty").keypress(function (evt) {
    evt.preventDefault();
});