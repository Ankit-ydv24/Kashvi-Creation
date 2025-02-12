
import os
from flask import Flask,render_template,request,jsonify,url_for,redirect
from db import *
from db import SessionLocal, Product, Review, Customer
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from db import engine
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError







app = Flask(__name__)



UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


session = SessionLocal()


@app.route('/')
def hello_world():
    all_reviews = session.query(Review).filter_by(visibility_on_homepage = True).all()
    return render_template('index.html',all_reviews = all_reviews)

@app.route('/homepage')
def homepage():
    all_reviews = session.query(Review).filter_by(visibility_on_homepage = True).all()
    
        
    return render_template('index.html',all_reviews = all_reviews)






@app.route('/admin_page')
def admin():
    # Fetch all reviews
    all_reviews = session.query(Review).all()
    all_products = session.query(Product).all()
    return render_template('admin.html', all_reviews=all_reviews,all_products = all_products)

@app.route('/toggle_visibility/<int:review_id>', methods=['POST'])
def toggle_visibility(review_id):
    # Fetch the review by its ID
    review = session.query(Review).get(review_id)
    
    # Toggle the visibility_on_homepage value
    if review:
        review.visibility_on_homepage = not review.visibility_on_homepage
        session.commit()
    
    return redirect(url_for('admin'))



@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    # Fetch the review by its ID
    review = session.query(Review).get(review_id)
    
    if review:
        session.delete(review)
        session.commit()
    
    return redirect(url_for('admin'))

# Create a new session


@app.route('/review', methods=["POST"])
def review():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')  # Not used in model, but might be required
        phone = request.form.get('phone')  # Not used in model, but might be required
        message = request.form.get('message')

        # Validate required fields
        if not name or not message:
            return jsonify({"error": "Name and message are required"}), 400

        # Create a new Review object
        new_review = Review(
            customer_name=name,
            description=message,
            visibility_on_homepage=False  # Default value
        )

        # Save to database
        session.add(new_review)
        session.commit()

        return render_template('index.html')

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/addproduct', methods=['POST'])
def addproduct():
    # Get form data
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    variety = request.form['variety']
    # Check if image file exists and is allowed
    image_file = request.files.get('image')
    if image_file and allowed_file(image_file.filename):
        # Secure the filename and save the file
        filename = secure_filename(image_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(file_path)
        
        # Save product details to the database
        session = SessionLocal()
        try:
            new_product = Product(
                product_name=name,
                product_image=file_path,  # Save the file path
                selling_price=price,
                description=description,
                variety = variety
            )
            session.add(new_product)
            session.commit()
            return redirect(url_for('admin'))
        except Exception as e:
            session.rollback()
            return f"Error while adding product: {str(e)}"
        finally:
            session.close()
    else:
        return "Error: Invalid file format or no file uploaded!"



@app.route('/shopnow')
def shopnow():
    all_product = session.query(Product).all()
    return render_template('shopnow.html',all_product = all_product)

@app.route('/filter',methods = ['POST'])
def filter():
    variety = request.form['filter']
    if(variety == 'All'):
        all_product = session.query(Product).all()
        return render_template('shopnow.html',all_product = all_product)
    all_product = session.query(Product).filter_by(variety = variety).all()
    return render_template('shopnow.html',all_product = all_product)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    session = SessionLocal()

    try:
        # Extract customer details and cart data
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')
        
        cart_data = request.form.get('cart_product_data')
        cart_data = {} if not cart_data else eval(cart_data)  # Convert string to dictionary

        if not cart_data:
            return jsonify({"error": "Cart is empty"}), 400

        # Process customer and order (same logic as before)
        customer = session.query(Customer).filter_by(email=email).first()
        if not customer:
            customer = Customer(username=name, email=email, address=address, city=city, state=state, zip=zip_code)
            session.add(customer)
            session.commit()

        total_amount = 0
        invoice_items = []
        for product_id, quantity in cart_data.items():
            product = session.query(Product).filter_by(product_id=int(product_id)).first()
            if not product:
                return jsonify({"error": f"Product with ID {product_id} not found"}), 400

            unit_price = float(product.selling_price)
            total_amount += unit_price * quantity
            invoice_items.append(InvoiceItem(
                product_id=int(product_id),
                quantity=quantity,
                unit_price=unit_price
            ))

        invoice = Invoice(customer_id=customer.customer_id, total_amount=total_amount)
        session.add(invoice)
        session.commit()

        for item in invoice_items:
            item.invoice_id = invoice.invoice_id
            session.add(item)

        session.commit()

        # Return a response back to the frontend without redirecting
        return jsonify({
            "message": "Order placed successfully",
            "invoice_id": invoice.invoice_id,
            "total_amount": total_amount
        })

    except IntegrityError:
        session.rollback()
        return jsonify({"error": "Database error"}), 500

    finally:
        session.close()



if __name__ == '__main__':
    app.run(debug=True)