# Different imports for Flask, SQLAlchemy, and other necessary libraries. 
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Comment, Order
from .forms import EventsForm, CommentsForm, OrdersForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime
from decimal import Decimal



events_bp = Blueprint('events', __name__)

# Shows the event details page 
@events_bp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.event_id==id))
    # create the comment form
    form = CommentsForm()
    # If the database doesn't return a destination, show a 404 page
    if not event:
       abort(404)
    return render_template('event_details.html', event=event, form=form)


# Cancels an event and updates its status to "Cancelled" in DB 
@events_bp.route('/<id>/cancel', methods=['POST'])
#must be logged in in order to cancel event
@login_required
def cancel_event(id):
    #calls upon the specific event the user is wanting to cancel an event for from the DB
    event = db.session.scalar(db.select(Event).where(Event.event_id==id))
    #changes event status to cancelled
    event.event_status = "Cancelled"
    #commits change
    db.session.commit()
    #message to confirm cancellation
    flash('Event has been cancelled')
    #rredirects the user back to the event details page of the event they just cancelled
    return redirect(url_for('events.show', id=id))
    
  


# Displays a list of bookings made by the currently logged-in user
@events_bp.route('/history')
#must be logged in to see booking history
@login_required
def booking_history():
    #calls upon all order and event info from the DB of the events the user logged in has previously booked
    bookings = db.session.scalars(db.select(Order).join(Event).where(Order.user_id==current_user.user_id)).all()
    
    return render_template('booking_history.html', bookings=bookings)




# Allows a logged-in user to create a new event (GET shows form, POST submits)
@events_bp.route('/create', methods=['GET', 'POST'])
#must be logged in in order to create an event
@login_required
def create_event():
    create_event = EventsForm()
    if (create_event.validate_on_submit()==True):
        # call the function that checks and returns image
        db_file_path = check_upload_file(create_event)

        #get event details from form
        event_name=create_event.event_name.data
        start_time=create_event.start_time.data
        end_time=create_event.end_time.data
        STEM_category=create_event.STEM_category.data
        event_type=create_event.event_type.data
        event_address=create_event.event_address.data
        event_venue=create_event.event_venue.data
        ticket_price=create_event.ticket_price.data
        ticket_policy=create_event.ticket_policy.data
        max_num_tickets=create_event.max_num_tickets.data
        description=create_event.description.data
        
        new_event = Event(event_name=event_name, start_time=start_time, end_time=end_time, STEM_category=STEM_category, event_type=event_type, event_address=event_address, event_venue=event_venue, ticket_price=ticket_price, ticket_policy=ticket_policy, max_num_tickets=max_num_tickets, description=description, image=db_file_path, event_status="Open" , user_id=current_user.user_id)
        # add the object to the db session
        db.session.add( new_event )
        # commit to the database
        db.session.commit()
        #message to confirm that the new event has been created
        flash('Successfully created a new event')

        #Always end with redirect when form is valid, redirects user to the event details page of the event just created
        return redirect(url_for('events.show', id=new_event.event_id))

    return render_template('create_event.html', form=create_event, heading='Create Event', submit_label='Create Event')

# Uploads and stores an image file, returning the relative DB path
def check_upload_file(form):
  # get file data from form  
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/' + secure_filename(filename)
  # save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path


# Allows a logged-in user to update their own event 
@events_bp.route('/<id>/update', methods=['GET', 'POST'])  
# must be logged in in order to update event
@login_required
def update_event(id):
    #gets event details from the DB of the selected event
    update_event = Event.query.get(id)
    form = EventsForm(obj= update_event)
    
    if form.validate_on_submit():
       #populates the form with the existing event details for the event selected
       form.populate_obj(update_event) 

       #ensures the image is uploaded correctly
       db_file_path = check_upload_file(form)
       update_event.image = db_file_path 

       #commits the updated event details to the DB  
       db.session.commit()

       #message to confirm the success of the update
       flash('The event has successfully been updated')
       #sends users back to the event they just updated
       return redirect(url_for('events.show', id=update_event.event_id))

    return render_template('create_event.html', form=form, heading='Update Event Details', submit_label='Update Event')




# Allows logged-in users to book tickets for a selected event
@events_bp.route('/<id>/booking', methods=['GET', 'POST'])  
@login_required
def booking(id):
   #create the order form to book ticket/s
   booking_form = OrdersForm()
   event = db.session.scalar(db.select(Event).where(Event.event_id==id))
   if(booking_form.validate_on_submit()):
      # sets the ticket_quanity to equal the value inputted by user within the form (converts that value to an int)
      ticket_quantity = int(booking_form.ticket_quantity.data)
      #calculates the total price by multiplying the number of tickets with the ticket price of that event
      total_amount = ticket_quantity * int(event.ticket_price)

      new_booking = Order(created_at=datetime.now() ,ticket_quantity=ticket_quantity, user_id=current_user.user_id, event_id=event.event_id, total_amount=total_amount)
      
      #adds booking information to the orders table
      db.session.add(new_booking) 
      db.session.commit()  

      #message to confirm booking success
      flash('Successfully booked event')
      # redirects the user to the booking history to see the booking they just created as well as their old ones
      return redirect(url_for('events.booking_history')) 
   
   return render_template('userbook.html', form=booking_form, event=event, id=id, heading='Book Ticket')



# Handles creation of a new comment on an event 
@events_bp.route('/<id>/comment', methods=['POST'])
@login_required
def create_comment(id):
    form = CommentsForm()

    # Find the event by ID
    event = db.session.scalar(db.select(Event).where(Event.event_id == id))
    if not event:
        abort(404)

    if form.validate_on_submit():
        comment_text = form.text.data

        new_comment = Comment(
            text=comment_text,
            event_id=event.event_id,
            user_id=current_user.user_id
        )

        db.session.add(new_comment)
        db.session.commit()

        flash('Comment Successfully Added')
        return redirect(url_for('events.show', id=id))

    return render_template('event_details.html', event=event, form=form)



# Returns all events ordered by status (Open > Sold Out > Inactive > Cancelled)
def get_all_events_ordered_by_status():
    return db.session.scalars(
        db.select(Event).order_by(
            db.case(
                (Event.event_status == 'Open', 1),
                (Event.event_status == 'Sold Out', 2),
                (Event.event_status == 'Inactive', 3),
                (Event.event_status == 'Cancelled', 4),
            )
        )
    ).all()




  







        