let approve_vendor_btn = document.querySelectorAll('.approve_vendor')

function approve_vendor(){
    form = this.previousElementSibling
    $(this).hide()
    form.innerHTML = `
        <input type="text" class="vend_id_input" name="vendor_id"maxlength="3" id="">
        <input type="submit" value="Add Vendor">
    `
}

approve_vendor_btn.forEach(button => {
    button.addEventListener('click', approve_vendor)
});