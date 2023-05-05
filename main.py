from io import BytesIO

from flask import Flask, render_template, request, session, redirect, url_for
from sqlalchemy import Column, INTEGER, String, Numeric, Float, create_engine, text
import json
import base64
from functions import *

app = Flask(__name__)
# CODE
db_url = 'mysql://root:0515@localhost/game_store'
engine = create_engine(db_url, echo=True)
conn = engine.connect()
app.secret_key = generate_random_string(10)


@app.route('/')
def show_home():
    if 'current_ven' in session:
        current_ven = True
    else:
        current_ven = False
    if 'current_user' in session:
        current_user = True
        admin = False
        username = session['current_user']
        cart = conn.execute(text(
            f'select count(config_id) from cart_items where user_no in (select user_no from users_mast where username = \'{username}\')')).all()
        cart_items = conn.execute(text(
            f'select * from cart_items where user_no in (select user_no from users_mast where username = \'{username}\');')).all()
        print(cart_items)
        print(cart[0][0])
    else:
        current_user = False
        cart = False
        cart_items = False
    if 'admin' in session:
        admin = True
    else:
        admin = False
    if 'reg_message' in session:
        user_reg_message = session.pop('reg_message')
        ismessage = True
    else:
        user_reg_message = False
        ismessage = False
    if 'ven_message' in session:
        vendor_reg_message = session.pop('ven_message')
        is_ven_message = True
    else:
        vendor_reg_message = False
        is_ven_message = False
    display_pic = conn.execute(text('select display_pic from product_mast'))
    return render_template('base.html', current_user=current_user, current_ven=current_ven, admin=admin,
                           user_reg_message=user_reg_message, vendor_reg_message=vendor_reg_message,
                           ismessage=ismessage, display_pic=display_pic, cart=cart, cart_items=cart_items)


# @app.route('/register')
# def show_register_form():
#     return redirect(url_for('show_home'))


@app.route('/register', methods=['POST'])
def create_account():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    username = request.form.get('username')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm_password')
    if first_name != '' and last_name != '' and username != '' and phone != '' and email != '' and password != '' and confirm_pass != '':
        dupe_username = conn.execute(text(f'select username from users_mast where username = \'{username}\'')).all()
        if len(dupe_username) < 1:
            dupe_phone = conn.execute(text(f'select phone_number from users_mast where phone_number = {phone}')).all()
            if len(dupe_phone) < 1:
                if check_email(email):
                    dupe_email = conn.execute(
                        text(f'select email from users_mast where email = \'{email}\'')).all()
                    if len(dupe_email) < 1:
                        if check_pass(password) == 'Good':
                            if password == confirm_pass:
                                session['reg_message'] = 'Account Created.'
                                if 'ven_message' in session:
                                    session.pop('ven_message')
                                hash_pass = hashing(password).hexdigest()
                                conn.execute(text(
                                    f'insert into users_mast (first_name,last_name,phone_number,email,username,password) values (\'{first_name.title()}\',\'{last_name.title()}\',{phone},\'{email.lower()}\',\'{username.lower()}\',\'{hash_pass}\')'))
                                conn.commit()
                                return redirect(url_for('show_home'))
                            else:
                                session['reg_message'] = 'Passwords do not match.'
                                if 'ven_message' in session:
                                    session.pop('ven_message')
                                return redirect(url_for('show_home'))
                        elif check_pass(password) == 'Num':
                            session['reg_message'] = 'Password must contain at least 1 Number.'
                            if 'ven_message' in session:
                                session.pop('ven_message')
                            return redirect(url_for('show_home'))
                        elif check_pass(password) == 'Lower':
                            session['reg_message'] = 'Password must contain at least 1 Lowercase Letter.'
                            if 'ven_message' in session:
                                session.pop('ven_message')
                            return redirect(url_for('show_home'))
                        elif check_pass(password) == 'Upper':
                            session['reg_message'] = 'Password must contain at least 1 Uppercase Letter.'
                            if 'ven_message' in session:
                                session.pop('ven_message')
                            return redirect(url_for('show_home'))
                        elif check_pass(password) == 'Special':
                            session['reg_message'] = 'Password must contain at least 1 Special Character.'
                            if 'ven_message' in session:
                                session.pop('ven_message')
                            return redirect(url_for('show_home'))
                        else:
                            session['reg_message'] = 'Password must be at least 8 characters long.'
                            if 'ven_message' in session:
                                session.pop('ven_message')
                            return redirect(url_for('show_home'))
                    else:
                        session['reg_message'] = 'Email Already Exists.'
                        if 'ven_message' in session:
                            session.pop('ven_message')
                        return redirect(url_for('show_home'))
                else:
                    session['reg_message'] = 'Enter valid email.'
                    if 'ven_message' in session:
                        session.pop('ven_message')
                    return redirect(url_for('show_home'))
            else:
                session['reg_message'] = 'Phone Number Already Exists.'
                if 'ven_message' in session:
                    session.pop('ven_message')
                return redirect(url_for('show_home'))
        else:
            session['reg_message'] = 'Username Already Exists.'
            if 'ven_message' in session:
                session.pop('ven_message')
            return redirect(url_for('show_home'))
    else:
        session['reg_message'] = 'Please Enter All Fields'
        if 'ven_message' in session:
            session.pop('ven_message')
        return redirect(url_for('show_home'))


@app.route('/register/vendor')
def show_vendor_register_form():
    return redirect(url_for('show_home'))


@app.route('/register/vendor', methods=['POST'])
def create_vendor_account():
    company = request.form.get('name')
    username = request.form.get('username')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_pass = request.form.get('confirm_password')
    if company != '' and username != '' and phone != '' and email != '' and password != '' and confirm_pass != '':
        dupe_company = conn.execute(text(f'select first_name from users_mast where first_name = \'{company}\'')).all()
        if len(dupe_company) < 1:
            dupe_username = conn.execute(text(f'select username from users_mast where username = \'{username}\'')).all()
            if len(dupe_username) < 1:
                dupe_phone = conn.execute(
                    text(f'select phone_number from users_mast where phone_number = {phone}')).all()
                if len(dupe_phone) < 1:
                    dupe_email = conn.execute(text(f'select email from users_mast where email = \'{email}\'')).all()
                    if len(dupe_email) < 1:
                        if check_pass(password) == 'Good':
                            if password == confirm_pass:
                                message = 'Account Created. Wait for Admin Approval before login.'
                                hash_pass = hashing(password).hexdigest()
                                conn.execute(text(
                                    f'insert into users_mast (first_name,phone_number,email,username,password,type) values (\'{company.lower()}\',{phone},\'{email.lower()}\',\'{username.lower()}\',\'{hash_pass}\',\'VEN\')'))
                                conn.commit()
                                session['ven_message'] = 'Account Created. Wait for Admin Approval before login.'
                                if 'reg_message' in session:
                                    session.pop('reg_message')
                                return redirect(url_for('show_home'))
                            else:
                                session['ven_message'] = 'Passwords do not match.'
                                if 'reg_message' in session:
                                    session.pop('reg_message')
                                return redirect(url_for('show_home'))
                        elif check_pass(password) == 'Num':
                            session['ven_message'] = 'Password must contain at least 1 Number.'
                            if 'reg_message' in session:
                                session.pop('reg_message')
                            return redirect(url_for('show_home'))
                        elif check_pass(password) == 'Lower':
                            session['ven_message'] = 'Password must contain at least 1 Lowercase Letter.'
                            if 'reg_message' in session:
                                session.pop('reg_message')
                            return redirect(url_for('show_home'))
                        elif check_pass(password) == 'Upper':
                            session['ven_message'] = 'Password must contain at least 1 Uppercase Letter.'
                            if 'reg_message' in session:
                                session.pop('reg_message')
                            return redirect(url_for('show_home'))
                        elif check_pass(password) == 'Special':
                            session['ven_message'] = 'Password must contain at least 1 Special Character.'
                            if 'reg_message' in session:
                                session.pop('reg_message')
                            return redirect(url_for('show_home'))
                        else:
                            session['ven_message'] = 'Password must be at least 8 characters long.'
                            if 'reg_message' in session:
                                session.pop('reg_message')
                            return redirect(url_for('show_home'))
                    else:
                        session['ven_message'] = 'Email Already Exists.'
                        if 'reg_message' in session:
                            session.pop('reg_message')
                        return redirect(url_for('show_home'))
                else:
                    session['ven_message'] = 'Phone Number Already exists.'
                    if 'reg_message' in session:
                        session.pop('reg_message')
                    return redirect(url_for('show_home'))
            else:
                session['ven_message'] = 'Username Already Exists.'
                if 'reg_message' in session:
                    session.pop('reg_message')
                return redirect(url_for('show_home'))
        else:
            session['ven_message'] = 'Company Name Already Exists.'
            if 'reg_message' in session:
                session.pop('reg_message')
            return redirect(url_for('show_home'))
    else:
        session['ven_message'] = 'Please enter all fields.'
        if 'reg_message' in session:
            session.pop('reg_message')
        return redirect(url_for('show_home'))


@app.route('/login')
def show_login():
    return redirect(url_for('show_home'))


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('login_name')
    password = request.form.get('login_pass')
    names = conn.execute(text('select username,email from users_mast')).all()
    usernames = []
    for item in names:
        usernames.append(item)
    for name in usernames:
        if username.lower() == name[0].lower() or username.lower() == name[1].lower():
            hash_pass = hashing(password).hexdigest()
            saved_pass = conn.execute(text(
                f'select password from users_mast where username = \'{username}\' or email = \'{username}\'')).all()
            if hash_pass == saved_pass[0][0]:
                approved_user = conn.execute(text(
                    f'select type from users_mast where username = \'{username}\' or email = \'{username}\'')).all()
                if approved_user[0][0] == 'CUS':
                    session['current_user'] = name[0]
                    return redirect(url_for('show_home'))
                elif approved_user[0][0] == 'VEN':
                    approved = conn.execute(text(
                        f'select * from vendors where user_no in (select user_no from users_mast where username = \'{name[0]}\')')).all()
                    if len(approved) > 0:
                        session['current_ven'] = name[0]
                        return redirect(url_for('show_home'))
                    else:
                        login_message = 'Must be approved by admin.'
                        return render_template('base.html', login_message=login_message)
                elif approved_user[0][0] == 'ADM':
                    all_accounts = conn.execute(text('select * from users_mast')).all()
                    accounts = format_account_cookies(all_accounts)
                    # session['current_ven'] = name[0]
                    session['admin'] = name[0]
                    print(session['admin'])
                    return redirect(url_for('show_home'))
            else:
                login_message = 'Incorrect Password.'
                return render_template('base.html', login_message=login_message)
    else:
        login_message = 'No usernames match.'
        return render_template('base.html', login_message=login_message)
    # return render_template('base.html')


@app.route('/account/<user_type>')
def show_account_page(user_type):
    if 'current_ven' in session:
        if 'edit_prod_message' in session:
            edit_message = session.pop('edit_prod_message')
        else:
            edit_message = False
        if 'create_prod_message' in session:
            create_message = session.pop('create_prod_message')
        else:
            create_message = False
        if 'add_var_message' in session:
            add_var_message = session.pop('add_var_message')
        else:
            add_var_message = False
        if 'edit_prod_variation' in session:
            edit_prod_variation = session.pop('edit_prod_variation')
        else:
            edit_prod_variation = False
        if 'add_pic_message' in session:
            add_pic_message = session.pop('add_pic_message')
        else:
            add_pic_message = False
        if 'add_variation_pic' in session:
            add_variation_pic = session.pop('add_variation_pic')
        else:
            add_variation_pic = False
        if 'disc_message' in session:
            disc_message = session.pop('disc_message')
        else:
            disc_message = False
        current_user = session['current_ven']
        user_info = conn.execute(
            text(f'select * from users_mast natural join vendors where username = \'{current_user}\'')).all()

        phone = phone_format(str(user_info[0][3]))
        all_products = conn.execute(text(
            f'select prod_no,title,description,category,display_pic,pm.vendor_id from product_mast pm natural join vendors natural join users_mast where username = \'{current_user}\' ;')).all()
        product_details = conn.execute(text(
            f'select pd.config_id,pd.prod_no,pd.color,pd.size,pd.price,pd.qty,pd.config_display from product_details pd natural join product_mast natural join vendors natural join users_mast where username = \'{current_user}\' ')).all()
        product_count = conn.execute(text(
            f'select count(category),category from product_mast where vendor_id = \'{user_info[0][8]}\' group by category')).all()
        all_discounts = conn.execute(text('select prod_no,disc_type,disc_amt,disc_exp from discounts;')).all()
        disc_user = put_in_list(all_discounts,0)
        disc_type = put_in_list(all_discounts,1)
        disc_exp = put_in_list(all_discounts, 2)
        discounts = [disc_user,disc_type,disc_exp]
        stock = conn.execute(text(f'select sum(qty),prod_no from product_details group by prod_no;')).all()
        prod_nums = put_in_list(stock, 1)
        qty = put_in_list(stock, 0)
        inventory = [prod_nums, qty]
        print(product_details)
        return render_template('account.html', user_info=user_info[0], phone=phone,
                               all_products=all_products, product_details=product_details,
                               product_count=product_count, inventory=inventory, current_ven=current_user,
                               edit_message=edit_message, create_message=create_message,
                               add_var_message=add_var_message, edit_prod_variation=edit_prod_variation,
                               add_pic_message=add_pic_message, add_variation_pic=add_variation_pic,
                               disc_message=disc_message,discounts=discounts, admin=False)
    elif 'admin' in session:
        if 'edit_prod_message' in session:
            edit_message = session.pop('edit_prod_message')
        else:
            edit_message = False
        if 'create_prod_message' in session:
            create_message = session.pop('create_prod_message')
        else:
            create_message = False
        if 'add_var_message' in session:
            add_var_message = session.pop('add_var_message')
        else:
            add_var_message = False
        if 'edit_prod_variation' in session:
            edit_prod_variation = session.pop('edit_prod_variation')
        else:
            edit_prod_variation = False
        if 'add_pic_message' in session:
            add_pic_message = session.pop('add_pic_message')
        else:
            add_pic_message = False
        if 'add_variation_pic' in session:
            add_variation_pic = session.pop('add_variation_pic')
        else:
            add_variation_pic = False
        if 'disc_message' in session:
            disc_message = session.pop('disc_message')
        else:
            disc_message = False
        current_user = session['admin']
        user_info = conn.execute(
            text(f'select * from users_mast where username = \'{current_user}\'')).all()
        all_products = conn.execute(text(
            f'select prod_no,title,description,category,display_pic,vendor_id from product_mast ')).all()
        product_details = conn.execute(text(
            f'select config_id,prod_no,color,size,price,qty,config_display from product_details')).all()
        product_count = conn.execute(text(
            f'select count(category),category from product_mast group by category')).all()
        user_count = conn.execute(text(
            f'select count(user_no),type from users_mast group by type')).all()
        all_discounts = conn.execute(text('select prod_no,disc_type,disc_amt,disc_exp from discounts;')).all()
        disc_user = put_in_list(all_discounts, 0)
        disc_type = put_in_list(all_discounts, 1)
        disc_exp = put_in_list(all_discounts, 2)
        discounts = [disc_user, disc_type, disc_exp]
        print(user_count)
        print(all_products)
        phone = phone_format(str(user_info[0][3]))
        stock = conn.execute(text(f'select sum(qty),prod_no from product_details group by prod_no;')).all()
        prod_nums = put_in_list(stock, 1)
        qty = put_in_list(stock, 0)
        inventory = [prod_nums, qty]
        print(inventory)
        return render_template('account.html', user_info=user_info[0], phone=phone,
                               all_products=all_products, product_details=product_details,
                               product_count=product_count, user_count=user_count, inventory=inventory,
                               current_ven=current_user,
                               edit_message=edit_message, create_message=create_message,
                               add_var_message=add_var_message, edit_prod_variation=edit_prod_variation,
                               add_pic_message=add_pic_message, add_variation_pic=add_variation_pic,
                               disc_message=disc_message,discounts=discounts, admin=True)
    else:
        return redirect(url_for('show_home'))


@app.route('/account/allaccounts_<user_type>')
def show_accounts(user_type):
    if 'admin' in session:
        if 'approve_vendor_message' in session:
            approve_vendor_message = session.pop('approve_vendor_message')
        else:
            approve_vendor_message = False
        current_user = session['admin']
        user_info = conn.execute(
            text(f'select * from users_mast where username = \'{current_user}\'')).all()
        product_count = conn.execute(text(
            f'select count(category),category from product_mast group by category')).all()
        user_count = conn.execute(text(
            f'select count(user_no),type from users_mast group by type')).all()
        phone = phone_format(str(user_info[0][3]))
        all_accounts = conn.execute(text('select * from users_mast')).all()
        vendors_id = conn.execute(text('select user_no from vendors')).all()
        conf_vendors = conn.execute(text('select vendor_id from vendors')).all()
        vendors_name = one_list_row(conf_vendors)
        vendor_id = one_list_row(vendors_id)
        vendors = [vendor_id, vendors_name]
        print(vendors)
        return render_template('admin_accounts.html', user_info=user_info[0], phone=phone, product_count=product_count,
                               user_count=user_count, all_accounts=all_accounts, phone_format=phone_format,
                               vendors=vendors, approve_vendor_message=approve_vendor_message, admin=True)
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>approve_vendor<user_no>')
def show_approve_vendor(user_type, user_no):
    if 'admin' in session:
        return redirect(url_for('show_accounts', user_type=user_type))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>approve_vendor<user_no>', methods=['POST'])
def approve_vendor(user_type, user_no):
    if 'admin' in session:
        vendor_id = request.form.get('vendor_id')
        if vendor_id != '':
            dupe_id = conn.execute(text(f'select * from vendors where vendor_id = \'{vendor_id.upper()}\'')).all()
            if len(dupe_id) < 1:
                session['approve_vendor_message'] = 'Vendor Added'
                conn.execute(
                    text(f'insert into vendors (user_no,vendor_id) values ({user_no}, \'{vendor_id.upper()}\')'))
                conn.commit()
                return redirect(url_for('show_accounts', user_type=user_type))
            else:
                session['approve_vendor_message'] = 'Vendor ID already exists'
                return redirect(url_for('show_accounts', user_type=user_type))
        else:
            session['approve_vendor_message'] = 'Please Enter all Fields'
            return redirect(url_for('show_accounts', user_type=user_type))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>/create')
def show_vendor_create_page(user_type):
    if 'current_ven' in session:
        return redirect(url_for('show_account_page', user_type='VEN'))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>/create', methods=['POST'])
def create_product(user_type):
    url = request.form.get('prod_img_url')
    prod_name = request.form.get('prod_name')
    prod_descr = request.form.get('prod_descr')
    prod_category = request.form.get('prod_category')
    if 'current_ven' in session:
        username = session['current_ven']
        vend_id = conn.execute(
            text(f'select vendor_id from vendors natural join users_mast where username = \'{username}\';')).all()
        if url != '' and prod_name != '' and prod_descr != '' and prod_category != '':
            dupe_name = conn.execute(text(
                f'select title from product_mast where title = \'{prod_name.lower()}\' and vendor_id = \'{vend_id[0][0]}\'')).all()
            if len(dupe_name) < 1:
                vend_info = conn.execute(text(
                    f'select vendor_id,type from vendors natural join users_mast where username = \'{username}\'')).all()
                vend_id = vend_info[0][0]
                conn.execute(text(
                    f'Insert into product_mast (title,description,added_by,vendor_id,category,display_pic) values (\'{prod_name.lower()}\', \'{prod_descr.lower()}\',\'{user_type}\',\'{vend_id.upper()}\',\'{prod_category}\',\'{url}\')'))
                conn.commit()
                session['create_prod_message'] = 'Product Added'
                return redirect(url_for('show_account_page', user_type=user_type))
            else:
                session['create_prod_message'] = 'Product already exists'
                return redirect(url_for('show_account_page', user_type=user_type))
        else:
            session['create_prod_message'] = 'Please enter all fields'
            return redirect(url_for('show_account_page', user_type=user_type))

    elif 'admin' in session:
        vend_id = request.form.get('vend_id')
        if url != '' and prod_name != '' and prod_descr != '' and prod_category != '' and vend_id != '':
            dupe_name = conn.execute(text(
                f'select title from product_mast where title = \'{prod_name.lower()}\' and vendor_id = \'{vend_id.upper()}\'')).all()
            if len(dupe_name) < 1:
                isvendor = conn.execute(text(f'select * from vendors where vendor_id = \'{vend_id.upper()}\'')).all()
                if len(isvendor) > 0:
                    session['create_prod_message'] = 'Product Added'
                    conn.execute(text(
                        f'Insert into product_mast (title,description,added_by,vendor_id,category,display_pic) values (\'{prod_name.lower()}\', \'{prod_descr.lower()}\',\'{user_type}\',\'{vend_id.upper()}\',\'{prod_category}\',\'{url}\')'))
                    conn.commit()
                    return redirect(url_for('show_account_page', user_type=user_type))
                else:
                    session['create_prod_message'] = 'Vendor does not exist'
                    return redirect(url_for('show_account_page', user_type=user_type))
            else:
                session['create_prod_message'] = 'Product already exists'
                return redirect(url_for('show_account_page', user_type=user_type))
        else:
            session['create_prod_message'] = 'Please enter all fields'
            return redirect(url_for('show_account_page', user_type=user_type))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>/delete<prod_no>')
def delete_product(user_type, prod_no):
    if request.method == 'POST':
        print()
    else:
        if 'current_ven' in session or 'admin' in session:
            return redirect(url_for('show_account_page', user_type=user_type))
        else:
            return redirect(url_for('show_home'))


@app.route('/account/<user_type>/edit<prod_no>')
def show_vendor_edit_page(user_type, prod_no):
    if 'current_ven' in session:
        return redirect(url_for('show_account_page', user_type='VEN'))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>/edit<prod_no>', methods=['POST'])
def edit_product(user_type, prod_no):
    name = request.form.get('prod_name')
    display_pic = request.form.get('prod_img_url')
    description = request.form.get('prod_descr')
    category = request.form.get('prod_category')
    if 'current_ven' in session:
        username = session['current_ven']
        vend_id = conn.execute(
            text(f'select vendor_id from vendors natural join users_mast where username =\'{username}\'')).all()
        if name != '' and display_pic != '' and description != '' and category != '':
            dupe_title = conn.execute(text(
                f'select title from product_mast where title = \'{name.lower()}\' and vendor_id = \'{vend_id[0][0]}\' and prod_no not in ({prod_no})')).all()
            if len(dupe_title) < 1:
                conn.execute(text(
                    f'update product_mast set title = \'{name}\', description = \'{description}\',category = \'{category}\',display_pic = \'{display_pic}\' where prod_no = {prod_no} '))
                conn.commit()
                session['edit_prod_message'] = 'Product Edited.'
                return redirect(url_for('show_account_page', user_type=user_type))
            else:
                check_prod = conn.execute(text(
                    f'select prod_no from product_mast where title = \'{name}\' and vendor_id = \'{vend_id[0][0]}\'')).all()
                if check_prod[0][0] == prod_no:
                    session['edit_prod_message'] = 'Product Edited.'
                    return redirect(url_for('show_account_page', user_type=user_type))
                else:
                    session['edit_prod_message'] = 'Product already exists'
                    return redirect(url_for('show_account_page', user_type=user_type))
        else:
            session['edit_prod_message'] = 'Please enter all fields'
            return redirect(url_for('show_account_page', user_type=user_type))

    elif 'admin' in session:
        if name != '' and display_pic != '' and description != '' and category != '':
            vend_id = conn.execute(text(f'select vendor_id from product_mast where prod_no = {prod_no}')).all()
            dupe_title = conn.execute(text(
                f'select * from product_mast where title = \'{name.lower()}\' and vendor_id = \'{vend_id[0][0]}\' and prod_no not in ({prod_no})')).all()
            if len(dupe_title) < 1:
                conn.execute(text(
                    f'update product_mast set title = \'{name.lower()}\', description = \'{description.lower()}\',category = \'{category}\',display_pic = \'{display_pic}\' where prod_no = {prod_no} '))
                conn.commit()
                session['edit_prod_message'] = 'Product Edited.'
                return redirect(url_for('show_account_page', user_type=user_type))
            else:
                session['edit_prod_message'] = 'Product name already exists'
                return redirect(url_for('show_account_page', user_type=user_type))
        else:
            session['edit_prod_message'] = 'Please enter all fields'
            return redirect(url_for('show_account_page', user_type=user_type))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>/add<prod_no>')
def show_add_detail(user_type, prod_no):
    if 'current_ven' in session:
        return redirect(url_for('show_account_page', user_type=user_type))
    elif 'admin' in session:
        return redirect(url_for('show_accounts_page', user_type=user_type))
    else:

        return redirect(url_for('show_home'))


@app.route('/account/<user_type>/add<prod_no>', methods=['POST'])
def add_product_detail(user_type, prod_no):
    prod_color = request.form.get('prod_color')
    prod_size = request.form.get('prod_size')
    prod_price = request.form.get('prod_price')
    prod_qty = request.form.get('prod_qty')
    if 'current_ven' in session or 'admin' in session:
        if prod_price != '' and prod_qty != '':
            dupe_prod = conn.execute(text(
                f'select * from product_details where prod_no = {prod_no} and color = \'{prod_color.upper()}\' and size = \'{prod_size.upper()}\'')).all()
            if len(dupe_prod) < 1:
                conn.execute(text(
                    f'insert into product_details (prod_no,color,size,price,qty) values ({prod_no}, \'{prod_color.upper()}\', \'{prod_size.upper()}\', {float(prod_price):.2f}, {prod_qty})'))
                conn.commit()
                session['add_var_message'] = 'Variation Added'
                return redirect(url_for('show_account_page', user_type=user_type))
            else:
                session['add_var_message'] = 'Product Variation Already Exists'
                return redirect(url_for('show_account_page', user_type=user_type))
        else:
            session['add_var_message'] = 'Product Price and Product Quantity Cannot be Empty'
            return redirect(url_for('show_account_page', user_type=user_type))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>/configs<config_id>')
def show_edit_variations(user_type, config_id):
    if 'current_ven' in session:
        return redirect(url_for('show_account_page', user_type=user_type))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>/configs<config_id>/<prod_no>', methods=["POST"])
def edit_variations(user_type, config_id, prod_no):
    if 'current_ven' in session or 'admin' in session:
        prod_color = request.form.get('prod_color')
        prod_size = request.form.get('prod_size')
        prod_price = request.form.get('prod_price')
        prod_qty = request.form.get('prod_qty')
        prod_size = str(prod_size)
        if prod_price != '' and prod_qty != '':
            itself = conn.execute(text(
                f'select * from product_details where prod_no = {prod_no} and color = \'{str(prod_color).upper()}\' and size = \'{prod_size.upper()}\'')).all()
            if len(itself) > 0:
                if int(config_id) == int(itself[0][0]):
                    session['edit_prod_variation'] = "Product Edited"
                    conn.execute(text(
                        f'update product_details set color = \'{prod_color.upper()}\', size = \'{prod_size.upper()}\', price = \'{float(prod_price):.2f}\', qty = {int(prod_qty)} where config_id = {int(config_id)}'))
                    conn.commit()
                    print(prod_qty)
                    return redirect(url_for('show_account_page', user_type=user_type))
                else:
                    session['edit_prod_variation'] = "Product Already Exists"
                    return redirect(url_for('show_account_page', user_type=user_type))
            else:
                session['edit_prod_variation'] = "Product Edited"
                conn.execute(text(
                    f'update product_details set color = \'{prod_color.upper()}\', size = \'{prod_size.upper()}\', price = \'{float(prod_price):.2f}\', qty = {int(prod_qty)} where config_id = {int(config_id)}'))
                conn.commit()
                print(prod_qty)
                return redirect(url_for('show_account_page', user_type=user_type))
        else:
            session['edit_prod_variation'] = "Product Price and Quantity Cannot be Empty"
            return redirect(url_for('show_account_page', user_type=user_type))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>add_image<prod_no>')
def show_add_images(user_type, prod_no):
    if 'current_ven' in session or 'admin' in session:
        return redirect(url_for('show_account_page', user_type=user_type))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>add_image<prod_no>', methods=['POST'])
def add_prod_images(user_type, prod_no):
    if 'current_ven' in session or 'admin' in session:
        pics = request.form
        prod_pics = []
        for image in pics:
            prod_pics.append(pics[image])
            print(pics[image])
        for image in prod_pics:
            if image != '':
                dupe_img = conn.execute(
                    text(f'select img_url from product_imgs where img_url = \'{image}\' and prod_no = {prod_no}')).all()
                if len(dupe_img) < 1:
                    conn.execute(text(f'insert into product_imgs (prod_no,img_url) values ({prod_no}, \'{image}\')'))
                    conn.commit()
                else:
                    session['add_pic_message'] = 'Image url already exists for this product'
                    return redirect(url_for('show_account_page', user_type=user_type))
            else:
                session['add_pic_message'] = 'Url is empty'
                return redirect(url_for('show_account_page', user_type=user_type))
        session['add_pic_message'] = 'Picture Added'
        return redirect(url_for('show_account_page', user_type=user_type))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>add_variation<config_id>', methods=['GET', 'POST'])
def add_variation_picture(user_type, config_id):
    if 'current_ven' in session or 'admin' in session:
        if request.method == 'POST':
            pic = request.form.get('var_img_url')
            conn.execute(text(f'update product_details set config_display = \'{pic}\' where config_id = {config_id}'))
            conn.commit()
            session['add_variation_pic'] = 'Picture Added'
            return redirect(url_for('show_account_page', user_type=user_type))
        else:
            return redirect(url_for('show_account_page', user_type=user_type))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>/discount<prod_no>', methods=['GET', 'POST'])
def add_discount(user_type, prod_no):
    if request.method == 'POST':
        disc_type = request.form.get('disc_type')
        disc_amt = request.form.get('disc_amt')
        disc_dur = request.form.get('disc_dur')
        if disc_type != 'Discount Type' and disc_amt != '':
            if disc_type == 'UNTIMED':
                dupe_disc = conn.execute(text(f'select * from discounts where prod_no = {prod_no}')).all()
                if len(dupe_disc) < 1:
                    conn.execute(text(
                        f'insert into discounts (prod_no,disc_type,disc_amt,added_by) values ({prod_no},\'{disc_type}\',{int(disc_amt) / 100}, \'{user_type}\')'))
                    conn.commit()
                    session['disc_message'] = 'Discount Added'
                    return redirect(url_for('show_account_page', user_type=user_type))
                else:
                    session['disc_message'] = 'Discount already exists for that product'
                    return redirect(url_for('show_account_page', user_type=user_type))
            else:
                dupe_disc = conn.execute(
                    text(f'select * from discounts where prod_no = {prod_no}')).all()
                if len(dupe_disc) < 1:
                    if disc_dur != '':
                        conn.execute(text(
                            f'insert into discounts (prod_no,disc_type,disc_amt,disc_exp,added_by) values ({prod_no},\'{disc_type}\',{int(disc_amt) / 100},date(date_add(now(), interval {disc_dur} day)),\'{user_type}\' )'))
                        conn.commit()
                        session['disc_message'] = 'Discount Added'
                        return redirect(url_for('show_account_page', user_type=user_type))
                    else:
                        session['disc_message'] = 'Please Enter All Fields'
                        return redirect(url_for('show_account_page', user_type=user_type))
                else:
                    session['disc_message'] = 'Discount already exists for that product'
                    return redirect(url_for('show_account_page', user_type=user_type))
        else:
            session['disc_message'] = 'Please Enter All Fields'
            return redirect(url_for('show_account_page', user_type=user_type))
    else:
        if 'current_ven' in session or 'admin' in session:
            return redirect(url_for('show_account_page', user_type=user_type))
        else:
            return redirect(url_for('show_home'))


@app.route('/products')  # GET PROD_NO
def show_all_products():
    if 'current_user' in session:
        current_user = session['current_user']
        products = conn.execute(text(
            f'select config_id,prod_no,title,description,color,size,price,qty,display_pic,config_display from product_details natural join product_mast;')).all()
        cart = conn.execute(text(
            f'select count(config_id) from cart_items where user_no in (select user_no from users_mast where username = \'{current_user}\')')).all()
        return render_template('products.html', products=products, current_user=current_user, cart=cart)
    elif 'admin' in session:
        admin = session['admin']
        products = conn.execute(text(
            f'select config_id,prod_no,title,description,color,size,price,qty,display_pic,config_display from product_details natural join product_mast;')).all()
        print(products)
        return render_template('products.html', products=products, cart=False, admin=admin)
    elif 'current_ven' in session:
        current_ven = session['current_ven']
        products = conn.execute(text(
            f'select config_id,prod_no,title,description,color,size,price,qty,display_pic,config_display from product_details natural join product_mast;')).all()
        print(products)
        return render_template('products.html', products=products, cart=False, current_user=current_ven)
    else:
        products = conn.execute(text(
            f'select config_id,prod_no,title,description,color,size,price,qty,display_pic,config_display from product_details natural join product_mast;')).all()
        print(products)
        return render_template('products.html', cart=False, products=products)


@app.route('/product/<config_id>')
def show_product(config_id):
    if 'add_to_cart_message' in session:
        add_cart_message = session.pop('add_to_cart_message')
    else:
        add_cart_message = False
    if 'current_user' in session:
        username = session['current_user']
        product = conn.execute(text(
            f'select pd.config_id,pd.prod_no,p.title,p.description,pd.color,pd.size,pd.price,round(pd.price - (pd.price * coalesce(d.disc_amt,0)),2)as new_price,pd.qty,p.display_pic,pd.config_display from product_mast p left join discounts d on (d.prod_no = p.prod_no) left join product_details pd on (pd.prod_no = p.prod_no) where config_id = {config_id} ;')).all()
        images = conn.execute(text(
            f'SELECT img_url FROM product_imgs WHERE prod_no in( select prod_no from product_details where config_id = {config_id})')).all()
        cart = conn.execute(text(
            f'select count(config_id) from cart_items where user_no in (select user_no from users_mast where username = \'{username}\')')).all()
        imgs = []
        for img in images:
            img_format = str(img).strip('(\'\',)')
            imgs.append(img_format)
        print(product)
        current_user = session['current_user']
        return render_template('product.html', product=product[0], imgs=imgs, current_user=current_user,
                               add_cart_message=add_cart_message, cart=cart)
    else:
        product = conn.execute(text(
            f'select pd.config_id,pd.prod_no,p.title,p.description,pd.color,pd.size,pd.price,round(pd.price - (pd.price * coalesce(d.disc_amt,0)),2)as new_price,pd.qty,p.display_pic,pd.config_display from product_mast p left join discounts d on (d.prod_no = p.prod_no) left join product_details pd on (pd.prod_no = p.prod_no) where config_id = {config_id} ;')).all()
        images = conn.execute(text(
            f'SELECT img_url FROM product_imgs WHERE prod_no in( select prod_no from product_details where config_id = {config_id})')).all()
        imgs = []
        for img in images:
            img_format = str(img).strip('(\'\',)')
            imgs.append(img_format)
        return render_template('product.html', product=product[0], imgs=imgs, cart=False, current_user=False)


@app.route('/product/<config_id>/add')
def show_add_to_cart(config_id):
    return redirect(url_for('show_product', config_id=config_id))


@app.route('/product/<config_id>/add', methods=['POST'])
def add_to_cart(config_id):
    if 'current_user' in session:
        # qty = request.form.get('quantity')
        # if qty != 'Select Quantity':
        #     print(qty)
        username = session['current_user']
        user_no = conn.execute(text(f'select user_no from users_mast where username = \'{username}\'')).all()
        dupe_cart_item = conn.execute(
            text(f'select * from cart_items where user_no = {user_no[0][0]} and config_id = {config_id}')).all()
        if len(dupe_cart_item) < 1:
            session['add_to_cart_message'] = 'Added to Cart'
            prod_name = conn.execute(text(
                f'select title from product_mast natural join product_details where config_id = {config_id}')).all()
            old_price = conn.execute(text(
                f'select price from product_details natural join product_mast where config_id = {config_id}')).all()
            disc_amt = conn.execute(text(
                f'select coalesce(d.disc_amt,0) as disc_price from product_mast p left join discounts d on (d.prod_no = p.prod_no) left join product_details pd on (pd.prod_no = p.prod_no) where pd.config_id = {config_id}')).all()
            after_disc = conn.execute(text(
                f'select truncate(pd.price - (pd.price * coalesce(d.disc_amt,0)),2) as New_price from product_mast p left join discounts d on (d.prod_no = p.prod_no) left join product_details pd on (pd.prod_no = p.prod_no) where pd.config_id = {config_id}')).all()
            print(
                f'{user_no[0][0]}, {config_id},\'{prod_name[0][0]}\', {old_price[0][0]}, {disc_amt[0][0]},{after_disc[0][0]},')
            conn.execute(text(
                f'insert into cart_items (user_no,config_id,prod_name,prod_old_price,discount,price_after_disc,qty,total) values ({user_no[0][0]}, {config_id},\'{prod_name[0][0]}\', {old_price[0][0]:.2f}, {disc_amt[0][0]:.2f}, {after_disc[0][0]}, 1,{float(after_disc[0][0]) * 1}  )'))
            conn.commit()
            # conn.execute(text(f'update product_details set qty = (qty - {qty}) where config_id = {config_id}'))
            # conn.commit()
            return redirect(url_for('show_product', config_id=config_id))
        else:
            session['add_to_cart_message'] = 'Item already in cart'
            return redirect(url_for('show_product', config_id=config_id))
    # else:
    #     session['add_to_cart_message'] = 'Please select quantity'
    #     return redirect(url_for('show_product', config_id=config_id))
    else:
        session['add_to_cart_message'] = 'Must be signed in to add to cart'
        return redirect(url_for('show_product', config_id=config_id))


@app.route('/user/')
def show_user_page():
    if 'current_user' in session:
        if 'edit_cart_message' in session:
            edit_cart_message = session.pop('edit_cart_message')
        else:
            edit_cart_message = False
        current_user = session['current_user']
        cart = conn.execute(text(
            f'select count(config_id) from cart_items where user_no in (select user_no from users_mast where username = \'{current_user}\')')).all()
        cart_items = conn.execute(text(
            f'select cart_item_id,ci.user_no,ci.config_id,prod_name,prod_old_price,discount,price_after_disc,ci.qty as cart_qty,pd.qty as stock,p.description,pd.color,pd.size,ci.total,p.display_pic,pd.config_display from cart_items ci join product_details pd on (ci.config_id=pd.config_id) natural join product_mast p where user_no in (select user_no from users_mast where username = \'{current_user}\')')).all()
        user_info = conn.execute(text(
            f'select * from users_mast where user_no in (select user_no from users_mast where username = \'{current_user}\')')).all()
        phone = phone_format(str(user_info[0][3]))
        total = conn.execute(text(
            f'select round(sum(price_after_disc * qty),2) from cart_items where user_no in (select user_no from users_mast where username = \'{current_user}\') ')).all()
        print(cart_items)
        return render_template('user_account.html', user_info=user_info[0], phone=phone, cart_items=cart_items,
                               current_user=current_user, total=total[0], edit_cart_message=edit_cart_message,cart=cart)
    else:
        return redirect(url_for('show_home'))


@app.route('/user/cart/addqty/<cart_item_id>')
def show_add_qty(cart_item_id):
    if 'current_user' in session:
        return redirect(url_for('show_user_page'))
    else:
        return redirect(url_for('show_home'))


@app.route('/user/cart/addqty/<cart_item_id>', methods=["POST"])
def add_qty(cart_item_id):
    change_qty = request.form.get('change_qty')
    if 'current_user' in session:
        username = session['current_user']
        print(change_qty)
        instock = conn.execute(text(
            f'select pd.qty from cart_items ci join product_details pd on(ci.config_id=pd.config_id) where cart_item_id = {cart_item_id}')).all()
        print(instock[0])
        if int(change_qty) <= instock[0][0]:
            session['edit_cart_message'] = 'Cart Updated'
            conn.execute(text(
                f'update cart_items set qty = {int(change_qty)}, total = (price_after_disc * {int(change_qty)}) where cart_item_id = {cart_item_id}'))
            conn.commit()
            return redirect(url_for('show_user_page'))
        else:
            session['edit_cart_message'] = 'Quantity not available'
            return redirect(url_for('show_user_page'))
    else:
        return redirect(url_for('show_home'))


@app.route('/user/cart/deleteItem/<cart_item_id>')
def del_cart_item(cart_item_id):
    if 'current_user' in session:
        print("DELETE")
        session['edit_cart_message'] = 'Cart Updated'
        conn.execute(text(f'delete from cart_items where cart_item_id = {cart_item_id}'))
        conn.commit()
        return redirect(url_for('show_user_page'))
    else:
        return redirect(url_for('show_home'))


@app.route('/user/cart/delete/')
def delete_cart():
    if 'current_user' in session:
        username = session['current_user']
        conn.execute(text(f'delete from cart_items where user_no in (select user_no from users_mast where username = \'{username}\')'))
        conn.commit()
        return redirect(url_for('show_user_page'))
    else:
        return redirect(url_for('show_home'))


@app.route('/user/order')
def order_cart():
    if 'current_user' in session:
        username = session['current_user']
        number = conn.execute(text(f'select user_no from users_mast where username = \'{username}\'')).all()
        user_no = number[0][0]
        quantities = conn.execute(text(f'select ci.qty,pd.qty from cart_items ci join product_details pd on (ci.config_id=pd.config_id) where user_no = {user_no}')).all()
        if check_cart_qty(quantities):
            session['edit_cart_message'] = 'Cart Ordered'
            # cart_items = conn.execute(text(f'select * = {user_no} and status = \'Pending\'')).all()
            total = conn.execute(text(
                f'select round(sum(price_after_disc * qty),2) from cart_items where user_no = {user_no} ')).all()
            conn.execute(text(f'insert into orders (user_no,total) values ({user_no},{total[0][0]})'))
            conn.commit()
            order_no = conn.execute(text(f'select order_no from orders where user_no = {user_no} and status = \'Pending\'')).all()
            conn.execute(text(f'insert into order_details (order_no,config_id,qty,price_paid) select o.order_no,ci.config_id,ci.qty,ci.total from orders o join cart_items ci on (o.user_no=ci.user_no) where ci.user_no = {user_no} and o.status = \'Pending\''))
            conn.commit()
            conn.execute(text(f'delete from cart_items where user_no = {user_no} and status = \'In Cart\''))
            conn.commit()
            return redirect(url_for('show_user_page'))
        else:
            session['edit_cart_message'] = 'Order Failed'
            return redirect(url_for('show_user_page'))
    else:
        return redirect(url_for('show_home'))


@app.route('/account/<user_type>/orders')
def show_admin_orders(user_type):
    if 'current ven' in session:
        current_user = session['current_ven']
        user_info = conn.execute(
            text(f'select * from users_mast natural join vendors where username = \'{current_user}\'')).all()
        phone = phone_format(str(user_info[0][3]))
        all_products = conn.execute(text(
            f'select prod_no,title,description,category,display_pic,pm.vendor_id from product_mast pm natural join vendors natural join users_mast where username = \'{current_user}\' ;')).all()
        # product_details = conn.execute(text(
        #     f'select pd.config_id,pd.prod_no,pd.color,pd.size,pd.price,pd.qty,pd.config_display from product_details pd natural join product_mast natural join vendors natural join users_mast where username = \'{current_user}\' ')).all()
        product_count = conn.execute(text(
            f'select count(category),category from product_mast where vendor_id = \'{user_info[0][8]}\' group by category')).all()
        orders = conn.execute(text(f'select * from orders where  user_no = {user_info[0][0]} and status \'Pending\''))
        print("VENDOR")
        return render_template('admin_orders.html', user_info=user_info[0], phone=phone,
                               all_products=all_products, orders=orders, admin=False,
                               product_count=product_count,  current_ven=current_user)
    elif 'admin' in session:
        print()
    else:
        return redirect(url_for('show_home'))

@app.route('/logout')
def logout():
    if 'current_user' in session:
        session.pop('current_user')
    if 'current_ven' in session:
        session.pop('current_ven')
    if 'admin' in session:
        session.pop('admin')
    return redirect(url_for('show_home'))


if __name__ == '__main__':
    app.run(debug=True)
