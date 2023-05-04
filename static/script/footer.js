function stickFooter(){
    let foot = document.getElementById("footer")
    let bottom = document.getElementById("bottom")
    let nav = document.getElementById("nav-bar")
    let windowsHeight = window.innerHeight
    var stickpoint = bottom.getBoundingClientRect().top
    if (stickpoint < windowsHeight - 50) {
//        nav.style.opacity = "0"
//        $(".logo").css('font-size', '70%')
        $("#nav-bar").css('font-size', '70%')
        $("#nav-bar").css('box-shadow', '0px')
        foot.classList.add("stick")
        foot.classList.remove("footer-sticky")


    } else {
//        nav.style.opacity = "1"
//        $(".logo").css('font-size', '100%')
        $("#nav-bar").css('font-size', '100%')
        $("#nav-bar").css('box-shadow', '0px 0px 5px black')
        foot.classList.remove("stick");
        foot.classList.add("footer-sticky")
    }
}
//function addSticky(){
//    let nav = document.getElementById("nav-bar")
//    let foot = document.getElementById("footer")
//    let sticky = nav.offsetTop
//    if (window.pageYOffset > sticky) {
//        nav.classList.add("sticky")
//        foot.classList.remove("animate__slideOutDown")
//        foot.classList.add("animate__slideInUp")
////        foot.classList.add("footer-sticky")
//
//    } else {
////        nav.classList.remove("sticky");
//        foot.classList.remove("animate__slideInUp")
//        foot.classList.add("animate__slideOutDown")
//    }
//}
$('.go_to_ven_sup').click(() => {
    $(".user_sup").addClass('animate__animated')
    $(".user_sup").toggleClass('animate__zoomOutLeft')
    $(".user_sup").removeClass('animate__zoomInRight')
    $(".user_sup").css("display", "none")

    $(".ven_sup").css("display", "flex")
    $(".ven_sup").addClass('animate__animated')
    $(".ven_sup").toggleClass('animate__zoomInRight')
    $(".ven_sup").removeClass('animate__zoomOutLeft')
});

$('.back-btn').click(() => {
    $(".ven_sup").removeClass('animate__zoomInRight')
    $(".ven_sup").addClass('animate__zoomOutLeft')
    $(".ven_sup").css("display", "none")

    $(".user_sup").css("display", "flex")
    $(".user_sup").addClass('animate__zoomInRight')
    $(".user_sup").removeClass('animate__zoomOutLeft')
});

window.addEventListener("scroll", addSticky);
window.addEventListener("scroll", stickFooter);