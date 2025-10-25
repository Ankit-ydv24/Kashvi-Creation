# Kashvi Creation - E-Commerce Platform

A full-featured Flask-based e-commerce web application with product catalog, customer reviews, shopping cart, and order management functionality.

## Features

- 🛍️ Product catalog with image uploads
- 👤 Customer registration and authentication
- ⭐ Product reviews and ratings
- 🛒 Shopping cart functionality
- 📦 Order management system
- 📄 PDF invoice generation
- 🔐 Admin panel for product and review management
- 📱 Responsive web interface

## Tech Stack

- **Backend:** Flask (Python web framework)
- **Database:** SQLAlchemy ORM with SQLite
- **Frontend:** HTML, CSS, JavaScript (templates in `templates/`)
- **PDF Generation:** ReportLab
- **File Uploads:** Werkzeug secure filename handling
- **Deployment:** Vercel-ready with `vercel.json`

## Project Structure

```
Kashvi-Creation/
├── app.py              # Main Flask application
├── db.py               # Database models and configuration
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment config
├── ecommerce.db        # SQLite database (auto-generated)
├── static/             # Static assets (CSS, JS, images)
│   └── uploads/        # Product image uploads
├── templates/          # HTML templates
└── instance/           # Instance-specific files
```

## Setup & Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Local Development

1. **Clone the repository**
   ```powershell
   git clone https://github.com/Ankit-ydv24/Kashvi-Creation.git
   cd Kashvi-Creation
   ```

2. **Create and activate a virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   The database will be created automatically on first run, or you can initialize it manually:
   ```powershell
   python db.py
   ```

5. **Run the application**
   ```powershell
   python app.py
   ```

6. **Access the app**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## Admin Access

Default admin credentials (configure in `app.py`):
- **Username:** `admin`
- **Password:** `password123`

⚠️ **Important:** Change these credentials before deploying to production.

## Key Functionality

### Product Management
- Add, edit, and delete products
- Upload product images
- Set pricing and descriptions

### Customer Features
- User registration and login
- Browse product catalog
- Add items to cart
- Place orders
- Write product reviews

### Order Processing
- Shopping cart management
- Order confirmation
- PDF invoice generation
- Order history tracking

### Review System
- Customers can rate and review products
- Admin can approve/hide reviews
- Display reviews on homepage and product pages

## Database Models

The application uses SQLAlchemy ORM with the following main models:
- `Product` - Product catalog items
- `Customer` - Registered users
- `Review` - Product reviews and ratings
- `Order` - Customer orders
- `Cart` - Shopping cart items

See `db.py` for complete model definitions.

## Deployment

### Vercel Deployment

The project includes `vercel.json` for easy deployment to Vercel:

1. Install Vercel CLI:
   ```powershell
   npm install -g vercel
   ```

2. Deploy:
   ```powershell
   vercel
   ```

3. Follow the prompts to complete deployment.

**Note:** For production, consider migrating from SQLite to a production database like PostgreSQL.

## File Upload Configuration

Allowed image formats: PNG, JPG, JPEG, GIF
Upload folder: `static/uploads/`

Ensure the upload directory exists and has proper write permissions.

## Security Considerations

- Update admin credentials before production deployment
- Use environment variables for sensitive configuration
- Enable HTTPS in production
- Implement CSRF protection (Flask-WTF is already included)
- Use strong secret keys for session management

## Dependencies

Core dependencies (see `requirements.txt` for full list):
- Flask 3.1.0
- SQLAlchemy 2.0.37
- Flask-SQLAlchemy 3.1.1
- ReportLab 4.3.1 (PDF generation)
- Pillow 11.1.0 (image processing)
- Werkzeug 3.1.3 (security utilities)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is available for educational and personal use. Add a LICENSE file if you plan to distribute it publicly.

## Support

For issues and questions, please open an issue on the GitHub repository.

---

**Kashvi Creation** - Building modern e-commerce experiences 🚀
