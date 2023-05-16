from flask import Blueprint, render_template, abort,request, session, redirect, url_for
from sqlalchemy import *
from database import conn
# Create a blueprint object
home_page = Blueprint('home_page', __name__,template_folder='templates')

# Create a route decorator
@home_page.route('/')
def show_home():
    conn.execute(text(f'delete from discounts where date(now()) > disc_exp;;'))
    conn.commit()
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
    vendors = conn.execute(text('select * from vendors')).all()
    newest_products = conn.execute(text(
        f'select config_id,prod_no,title,description,color,size,price,qty,display_pic,config_display from product_details natural join product_mast order by config_id desc limit 6;')).all()
    discount_products = conn.execute(text(f'select pd.config_id,pd.prod_no,p.title,p.description,pd.color,pd.size,price,round(pd.price - (pd.price * coalesce(d.disc_amt,0)),2),timestampdiff(day,date(now()),date(d.disc_exp)),pd.qty,p.display_pic,pd.config_display from product_details pd natural join product_mast p join discounts d on (pd.prod_no=d.prod_no)')).all()
    return render_template('base.html', current_user=current_user, current_ven=current_ven, admin=admin,
                           user_reg_message=user_reg_message, vendor_reg_message=vendor_reg_message,
                           ismessage=ismessage,  cart=cart, cart_items=cart_items,vendors=vendors,is_ven_message=is_ven_message,newest_products=newest_products,discount_products=discount_products)


