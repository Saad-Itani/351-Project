from flask import Flask, render_template, flash, redirect, request, url_for, session, g
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, IntegerField, FieldList, FormField, SelectField
from passlib.handlers.sha2_crypt import sha256_crypt

from functools import wraps
import sys
import datetime

app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@admin351'
app.config['MYSQL_DB'] = 'HOTELDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #this config line returns queries we execute as dictionaries, default is to return as a tuple; ex. User Login 
#init MYSQL
mysql = MySQL(app)

    
@app.template_global(name='zip')
def _zip(*args, **kwargs): #to not overwrite builtin zip in globals
    return __builtins__.zip(*args, **kwargs)


def isloggedin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))
    return wrap


"""
--------------------------------------------------------------
"""


@app.route('/reservation/<string:id>/')
@isloggedin
def view_reservation(id):
    breakfasts=None
    services=None
    rooms=None
    
    cur = mysql.connection.cursor()
    result=cur.execute('SELECT * FROM reservation WHERE invoiceNo=%s',[id])
    res = cur.fetchone()
    
    if result<1:
        flash("No reservation", 'danger')
        return redirect(url_for('dashboard'))
    if res['CID']!=session['cid']:
        flash("Cannot view this reservation",'danger')
        return redirect(url_for('dashboard'))
    
    result=cur.execute("""SELECT DISTINCT reserves.inDate, reserves.outDate, reserves.noOfDays, 
				            reserves.room_num, myroom.room_type, myroom.description
                          FROM reserves, review, reservation, myroom, hotel
                          WHERE reserves.hotelID = hotel.hotelID
                            AND reserves.hotelID = myroom.hotelID 
                            AND reservation.CID = review.CID
                            AND reserves.room_num = myroom.room_num
                            AND reserves.invoiceNo = %s""", [id])
    rooms=cur.fetchall()
    
    result = cur.execute("""SELECT DISTINCT includes.bType, breakfast.description, includes.num_of_breakfasts
                            FROM reserves, includes, reservation, breakfast, hotel
                            WHERE reserves.hotelID = hotel.hotelID
                                AND reserves.hotelID = includes.hotelID
                                AND reserves.invoiceNo = reservation.invoiceNo
                                AND includes.invoiceNo = reserves.invoiceNo
                                AND breakfast.hotelID = reserves.hotelID
                                AND reserves.invoiceNo = %s""", [id])
    
    result = cur.execute("""SELECT DISTINCT `contains`.sType
                               FROM reserves, `contains`, review, reservation, services, hotel
                               WHERE reserves.hotelID = hotel.hotelID
                                   AND reserves.hotelID = `contains`.hotelID 
                                   AND reservation.CID = review.CID 
                                   AND `contains`.invoiceNo = reserves.invoiceNo
                                   AND reserves.invoiceNo = %s""", [id])
    
    cur.close()
    return render_template('reservation.html', res=res, rooms=rooms)

"""
--------------------------------------------------------------
"""


"""
Reservation System
"""

class SearchHotelForm(Form):
    check_in = DateField('Check-In Date', [validators.DataRequired()], format='%m-%d-%Y')
    check_out = DateField('Check-Out Date', [validators.DataRequired()], format='%m-%d-%Y')
    num_rooms = IntegerField('Number of Rooms', [validators.DataRequired()])
    
class RoomNumEntry(Form):
    room_num=IntegerField()
    
class PickHotelForm(Form):
    hotel = IntegerField('Choose Hotel ID', [validators.DataRequired()])
    room_nums = FieldList(FormField(RoomNumEntry), [validators.DataRequired()], min_entries=1)

class ReservationInfo():
    num_rooms=0         #number of roooms to reserve
    room_nums=None      #room info
    hotel=None          #hotel id
    check_in=None       #check-in date
    check_out=None      #check-out date
    num_days=0          #length of stay
    cost=0              #total cost
    capacity=0          #total # of spots in the room
    #### SQL ####
    hotels_avail=None

res = None
    
# Search for Available Rooms
@app.route('/search_room', methods=['GET','POST'])
@isloggedin
def search_room():
    search_form = SearchHotelForm(request.form)

    cur = mysql.connection.cursor()
    cur.close()
    
    locations = dict()
    #if request.method=='POST' and search_form.validate():
    if request.method=='POST':
        country = search_form.country.data
        state = search_form.state.data
        check_in = search_form.check_in.data
        check_out = search_form.check_out.data
        num_rooms = search_form.num_rooms.data
        
        if num_rooms<1:
            flash("Must reserve atleast 1 room", 'danger')
            return render_template('1_search_room.html', form=search_form, loc=locations)
        
        if check_in<datetime.date.today():
            flash("Check-In Date must be today or later", 'danger')
            return render_template('1_search_room.html', form=search_form, loc=locations)
        
        if check_out<=check_in:
            flash("Check-Out Date must be at least one day later than Check-In Date", 'danger')
            return render_template('1_search_room.html', form=search_form, loc=locations)
        
        cur= mysql.connection.cursor()
        
        search_result = cur.execute("""SELECT DISTINCT r.hotelID, r.room_num, h.hotel_name, 
                                            r.price, r.capacity, 
                                            r.floor_no, r.description, r.room_type, 
                                            IFNULL(rd.discount, 'No Discount Available') AS DiscountPct
                                        FROM hotel AS h
                                        LEFT JOIN myroom AS r
                                            ON h.hotelID = r.hotelID
                                        LEFT JOIN reserves AS re
                                            ON r.hotelID = re.hotelID
                                                AND r.room_num = re.room_num
                                                AND (re.inDate <= '%s' OR re.outDate >= '%s')
                                        LEFT JOIN room_discount AS rd
                                            ON r.hotelID = rd.hotelID
                                                AND r.room_num = rd.room_no
                                                AND (rd.sdate >= '%s' AND rd.edate <= '%s')
                                        WHERE re.invoiceNo IS NULL
                                        AND h.country = '%s' AND h.state = '%s'
                                        ORDER BY r.hotelID, r.room_num;""",
                                    (check_in, check_out, check_in, check_out, country, state))

        hotels_avail = cur.fetchall()
        cur.close()
        
        #only collect list of hotels with more than specified number of rooms 
        #output lower room number error if not enough space
        if search_result==0:
            flash("No Rooms Available, try different search", 'danger')
            return render_template('1_search_room.html', form=search_form, loc=locations)
        
        count=0
        new_hotels_avail = dict()
        for room in hotels_avail:
            if not room['hotelID'] in new_hotels_avail:
                new_hotels_avail[room['hotelID']]=list()
                count+=1
            new_hotels_avail[room['hotelID']].append(room)
        
        for key in new_hotels_avail.keys():
            if len(new_hotels_avail[key])<num_rooms:
                new_hotels_avail[key]=None
                count-=1
                
        if count==0:
            flash("Not enough rooms available, try different search", 'danger')
            return render_template('____sameliink.html', form=search_form, loc=locations)
        
        global res
        res = ReservationInfo()
        res.num_rooms = num_rooms
        res.check_in = check_in
        res.check_out = check_out
        res.num_days = (check_out-check_in).days
        res.hotels_avail=new_hotels_avail        
        return redirect(url_for('pick_room'))
    return render_template('___.html', form=search_form, loc=locations)


# STEP 2 - Select Rooms to Reserve
@app.route('/pick_room', methods=['GET','POST'])
@isloggedin
def pick_room():
    global res
    
    room_fields = list()
    for i in range(1,res.num_rooms+1):
        room_fields.append({"room_num":"Enter Room #"+str(i)})
    reserve_form = PickHotelForm(request.form, room_nums=room_fields)
    if request.method=='POST' and reserve_form.validate():
        hotel = reserve_form.hotel.data
        room_nums = set([list(r.values())[0] for r in reserve_form.room_nums.data])
        
        #check sql query results from search_room to see if hotel exists
        if not hotel in res.hotels_avail.keys():
            flash("Hotel ID "+str(hotel)+" does not exist in table", 'danger')
            return render_template('___.html', form=reserve_form, res=res)
        
        if len(room_nums)<res.num_rooms:
            flash("Entered duplicate room numbers", 'danger')
            return render_template('____.html', form=reserve_form, res=res)
        
        #check sql query results from search_room to see if all room_numbers exist
        capacity=0
        total=0
        for num in room_nums:
            found=False
            for room in res.hotels_avail[hotel]:
                if (room['room_num']==num):
                    found=True
                    capacity+=room['capacity']
                    total = total + (room['price']*res.num_days)
                    total+=room['price']
                    break
            if not found:
                flash("Room Number "+str(num)+" does not exist in Hotel "+str(hotel), 'danger')
                return render_template('___.html', form=reserve_form, res=res)

        res.capacity=capacity
        res.cost=total
        res.hotel=hotel
        res.room_nums=room_nums
        return redirect(url_for('checkouttt.html'))
    
    return render_template('____.html', form=reserve_form, res=res)



class ReservationSummary():
    check_in=""
    num_days=""
    room_nums=""
    cost=""
    
    
# STEP 4 - Reservation Summary
@app.route('/summary', methods=['GET','POST'])
@isloggedin
def summary():
    global res
    summ = ReservationSummary()
    
    cur = mysql.connection.cursor()
    search_result = cur.execute("SELECT hotel_name, FROM hotel WHERE hotelID=%s", [res.hotel])
    hotel_info=cur.fetchone()
    cur.close()
    
    summ.check_in=str(res.check_in)
    summ.check_out=str(res.check_out)
    summ.num_days=str(res.num_days)
    summ.room_nums=", ".join([str(r) for r in res.room_nums])
    summ.cost = str(round(res.cost,2))
        
    if request.method=='POST':
        
        cur = mysql.connection.cursor()
        result = cur.execute("""INSERT INTO `reservation`(`CID`, `resDate`)
                                VALUES(%s, %s, NOW())""", (session['cid'], res.cost))
        mysql.connection.commit()
        for room in res.room_nums:  
            result = cur.execute("""INSERT INTO `reserves`(`invoiceNo`, `room_num`, `hotelID`, `noOfDays`, `inDate`, `outDate`)
                                    VALUES((SELECT MAX(invoiceNo) AS invNo FROM reservation), %s, %s, %s, %s, %s)""", 
                                    (room, res.hotel, res.num_days, res.check_in, res.check_out))
            mysql.connection.commit()
        for b,q in res.breakfasts:
            result = cur.execute("""INSERT INTO `includes`(`invoiceNo`, `hotelID`,`bType`, `num_of_breakfasts`)
                                    VALUES((SELECT MAX(invoiceNo) AS invNo FROM reservation), %s, %s, %s)""", 
                                    (res.hotel, b, q))
            mysql.connection.commit()
        for s in res.services:
            result = cur.execute("""INSERT INTO `contains`(`invoiceNo`, `hotelID`,`sType`, `num_of_services`)
				                    VALUES((SELECT MAX(invoiceNo) AS invNo FROM reservation), %s, %s, %s)""", 
                                    (res.hotel, s, 1))
            mysql.connection.commit()
        cur.close()
        
        res = None
        flash("Reservation successful!",'success')
        return redirect(url_for('home?.html'))
    return render_template('___.html', summ=summ, hotel=hotel_info)
