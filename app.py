
import os
import json
from flask import Flask,render_template,request,jsonify,url_for,redirect,send_file
from db import *
from db import SessionLocal, Product, Review, Customer
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from db import engine
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Using joinedload
from sqlalchemy.orm import joinedload





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
    # all_invoice = session.query(Invoice).all()
    all_invoice = session.query(Invoice).join(Invoice.customer).all()
    all_invoice_item = session.query(InvoiceItem).all()
    return render_template('admin.html', all_reviews=all_reviews,all_products = all_products,all_invoice = all_invoice)

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

@app.route('/delete_product',methods = ["POST"])
def delete_product():
    product_id = request.form['id']
    product = session.query(Product).get(product_id)
    
    if product:
        session.delete(product)
        session.commit()
    
    return redirect(url_for('admin'))
    




@app.route('/shopnow')
def shopnow():
    invoice = request.args.get('invoice')
    all_product = session.query(Product).all()
    return render_template('shopnow.html', all_product=all_product, invoice=invoice)

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
    customer_added = False
    curr_invoice = 0
    try:
        # Extract customer details
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')

        # Extract and parse cart data
        cart_data = request.form.get('cart_product_data')
        cart = json.loads(cart_data) if cart_data else {}

        # Check if the customer exists
        customer = session.query(Customer).filter_by(email=email).first()
        if not customer:
            customer = Customer(username=name, email=email, address=address, city=city, state=state, zip=zip_code)
            session.add(customer)
            session.commit()
            customer_added = True

        # Calculate total amount
        total_amount = 0
        for product_id, quantity in cart.items():
            product = session.query(Product).get(int(product_id))
            if product:
                total_amount += product.selling_price * cart[product_id]['quantity']


        # Create invoice
        if cart:
            invoice = Invoice(customer_id=customer.customer_id, total_amount=total_amount)
            session.add(invoice)
            session.commit()
            curr_invoice = invoice.invoice_id
            # Add invoice items
            # Add invoice items
            for product_id, item in cart.items():
                product = session.query(Product).get(int(product_id))
                if product:
                    quantity = item['quantity']
                    unit_price = float(item['price'])
                    invoice_item = InvoiceItem(
                        invoice_id=invoice.invoice_id,
                        product_id=product.product_id,
                        quantity=quantity,
                        unit_price=unit_price
                    )
                    session.add(invoice_item)


            session.commit()

    finally:
        session.close()

    return redirect(url_for('shopnow', showModal='true', customer_added=customer_added,invoice = curr_invoice))





@app.route('/generate_invoice/<int:invoice_id>')
def generate_invoice(invoice_id):
    session = SessionLocal()

    invoice = session.query(Invoice).options(
        joinedload(Invoice.customer),
        joinedload(Invoice.invoice_items).joinedload(InvoiceItem.product)
    ).get(invoice_id)

    if not invoice:
        session.close()
        return "Invoice not found"

    pdf_dir = os.path.join('static', 'invoice')
    os.makedirs(pdf_dir, exist_ok=True)

    file_path = os.path.join(pdf_dir, f'invoice_{invoice_id}.pdf')

    try:
        doc = SimpleDocTemplate(file_path, pagesize=A4, title=f"Invoice {invoice_id}")
        elements = []
        styles = getSampleStyleSheet()

        # Add logo
        logo_path = os.path.join("static", "images", "img-20250204-wa0006-224x224.jpg")
        if os.path.exists(logo_path):
            elements.append(Image(logo_path, width=160, height=160))
        elements.append(Spacer(1, 10))

        # Add company name and Hindi tagline

       
        elements.append(Spacer(1, 10))

        # Line separator
        elements.append(Paragraph("<hr width='100%'/>", styles["Normal"]))
        elements.append(Spacer(1, 10))

        # Customer details
        customer_details = f"""
        <b>Customer:</b> {invoice.customer.username}<br/>
        <b>Email:</b> {invoice.customer.email}<br/>
        <b>Address:</b> {invoice.customer.address}, {invoice.customer.city}, {invoice.customer.state}<br/>
        
        <b>Zip:</b> {invoice.customer.zip}
        """
        elements.append(Paragraph(customer_details, styles["Normal"]))
        elements.append(Spacer(1, 20))

        # Invoice table
        data = [["Product", "Quantity", "Unit Price", "Total"]]
        for item in invoice.invoice_items:
            total = float(item.quantity) * float(item.unit_price)
            data.append([item.product.product_name, str(item.quantity), f"{item.unit_price}", f"{total}"])

        table = Table(data, hAlign='LEFT', colWidths=[130, 80, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.royalblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.gold),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Total Amount at Bottom Right
        elements.append(Paragraph(f"<b>Total Amount:</b> {invoice.total_amount} Rupees", styles["Normal"]))
        elements.append(Spacer(1, 30))

        # Thank You Message at Bottom
        elements.append(Paragraph('<font size="16">Thank you for visiting Kashvi Creation!</font>', styles["Normal"]))

        # Build PDF
        doc.build(elements)
        session.close()

        # Send file as response
        response = send_file(file_path, as_attachment=True)
        response.headers['X-Redirect'] = url_for('shopnow')  
        return response

    except Exception as e:
        session.close()
        raise e

if __name__ == '__main__':
    app.run(debug=True)