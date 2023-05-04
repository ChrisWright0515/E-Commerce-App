//$('.product_edit').on('click', () => {
//    console.log(this.parentNode)
//});
let edit_buttons = document.querySelectorAll(".product_edit")
let view_details = document.querySelectorAll(".view_details_btn")
let add_details = document.querySelectorAll(".add_variation")
let variation_settings = document.querySelectorAll(".edit_prod_details")
let add_images = document.querySelectorAll(".add_images")
let add_images_select = document.querySelectorAll(".add_images_select")
let add_variation_pic = document.querySelectorAll(".add_variation_pic")
let discount = document.querySelectorAll(".show_disc")
let disc_type = document.querySelectorAll(".disc_type")
function edit_product(){
    user_type = document.getElementById('user_type')
    this.style.display = 'none'
    let card = this.parentNode;
    child = card.children
    values = []
    form = child[9].nextElementSibling
    inputs = card.querySelectorAll('.product_input')
    picture = card.querySelectorAll('.img')
    source = picture[0].id
    first_form = form.firstElementChild
    for (const input of inputs){
        values.push(input.textContent)
    }
    form.innerHTML = `
        <div class="next_to">
            <p>Image URL:</p>
            <input class = "product_form_input" type="text" name="prod_img_url" value="${source}" id="">
        </div>

        <div class="next_to">
            <p>Product Name:</p>
            <input class = "product_form_input" type="text" name="prod_name" value="${values[1]}" id="">
        </div>

        <div class="underline"></div>

        <div class="next_to">
            <p>Description:</p>
            <input class = "product_form_input" type="text" name="prod_descr" value="${values[2]}" id="">
        </div>

        <div class="underline"></div>

        <div class="next_to">
            <p>Product Category:</p>
            <select name="prod_category" selected="${values[3]}">
                <option value="${values[3]}">${values[3]}</option>
                <option value="Game">Game</option>
                <option value="Console">Console</option>
                <option value="Accessory">Accessory</option>
            </select>
        </div>
        <input style="margin:.5rem auto;" type="submit" value="Edit Product">
    `
}
function add_prod_details(){
    last_row = this.previousElementSibling
    this.style.display = 'none';
    last_row.innerHTML = `
        <input class="detail_form_input" type="text" name="prod_color"placeholder="Color" id="">
        <input class="detail_form_input" type="text" name="prod_size"placeholder="Size" id="">
        <input class="detail_form_input" type="number" name="prod_price"placeholder="Price"step="0.01" id="">
        <input class="detail_form_input" type="number" name="prod_qty"placeholder="Quantity" id="">
        <button type="submit" class="add_variation_submit" value="Add"><ion-icon style="font-size: 32px;" name="add-circle-outline"></ion-icon><span>Add</span></button>

    `
}
function show_details(){
    parent = this.parentNode
    btn = this.firstElementChild
    popup = this.lastElementChild
    details = parent.nextElementSibling
    if(details.style.display == 'none'){
        $(details).slideDown(500)
        btn.style.transform = "rotate(180deg)"
        popup.textContent = "Hide Details"
    }
    else{
        $(details).slideUp(500)
        btn.style.transform = "rotate(360deg)"
        popup.textContent = "View Details"
    }
}
function edit_variations(){
    form = this.parentNode
    qty_el = this.previousElementSibling
    price_el = qty_el.previousElementSibling
    size_el = price_el.previousElementSibling
    color_el = size_el.previousElementSibling
    qty = qty_el.textContent
    price = price_el.textContent
    size = size_el.textContent
    color = color_el.textContent
    console.log(color,size,price,qty)
    form.innerHTML = `
        <input class="edit_prod_details_input" type="text" name="prod_color"placeholder="Color"value="${color}" id="">
        <input class="edit_prod_details_input" type="text" name="prod_size"placeholder="Size" id=""value="${size}">
        <input class="edit_prod_details_input" type="number" name="prod_price"placeholder="Price"step="0.01" id=""value="${price}">
        <input class="edit_prod_details_input" type="number" name="prod_qty"placeholder="Quantity" id=""value="${qty}">
        <button style="width:20%"class="edit_prod_details_input_submit" type="submit"><ion-icon style="font-size: 20px;" name="add-circle-outline"></ion-icon></button>
    `
}
function show_images_form(){
    form = this.parentNode
    console.log(form)
    num_pics = $(this).val()
    for(i=0; i < num_pics; i++){
        form.innerHTML += `<input type="text" name="img_url" id="">`
    }
    console.log(num_pics)
}
function add_prod_images(){
    select = this.querySelectorAll('.add_images_select')
    if (select[0].style.display == 'none'){
        select[0].style.display = 'block'
    }
//    select.forEach(button => {
//    button.style.display = 'block'
//});
}
function variation_pic(){
    console.log(this)
    form = this.parentNode
    form.innerHTML = `
        <input type="text" name="var_img_url" id="">
        <input type="submit" value="Add">
    `
}

function show_discount(){
    const disc_cont = this.nextElementSibling
    console.log(disc_cont)
    if (disc_cont.style.display == 'none'){
        $(disc_cont).slideDown(500)
        disc_cont.style.display = 'flex'
        disc_cont.style.margin = 'auto'
    }else{
        $(disc_cont).slideUp(500)
    }
}
function show_disc_dur(){
    parent = this.parentNode
    console.log(this.value)
    if (this.value == 'TIMED'){
        dur_input = parent.lastElementChild
        dur_input.style.display = 'block'
    }else{
        dur_input = parent.lastElementChild
        dur_input.value = ''
        dur_input.style.display = 'none'
    }
}
$('#add_product').on('click', () => {
    $('#add_product').hide()
    $('.create_prod_message').hide()
    $('.add_product').css("font-size", "60%") //hide()
    $('#add_product_form').slideDown(500);

});


edit_buttons.forEach(button => {
    button.addEventListener('click', edit_product)
});
view_details.forEach(button => {
    button.addEventListener('click', show_details)
});
add_details.forEach(button => {
    button.addEventListener('click', add_prod_details)
});
variation_settings.forEach(button => {
    button.addEventListener('click', edit_variations)
});
add_images.forEach(button => {
    button.addEventListener('click', add_prod_images)
});
add_images_select.forEach(button => {
    button.addEventListener('change', show_images_form)
});
add_variation_pic.forEach(button => {
    button.addEventListener('click', variation_pic)
});
discount.forEach(button => {
    button.addEventListener('click', show_discount)
});
disc_type.forEach(button => {
    button.addEventListener('change', show_disc_dur)
});