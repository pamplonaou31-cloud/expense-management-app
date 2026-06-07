# Expense Management Application

A full-stack web application for managing personal expenses with user authentication, categorization, reporting, and data export features.

## Features

✅ **User Authentication**
- Secure user registration and login
- Password hashing with werkzeug
- Session management

✅ **Expense Management**
- Add, edit, and delete expenses
- Expense categorization
- Date and amount tracking
- Transaction descriptions

✅ **Reports & Analytics**
- Monthly expense reports
- Yearly expense reports
- Category-wise expense breakdown
- Visual charts and statistics dashboard

✅ **Data Export**
- Export expenses to PDF format
- Export expenses to Excel (XLSX) format
- Customizable export filters

✅ **Responsive Interface**
- Mobile-friendly design
- Bootstrap 5 framework
- Intuitive user interface
- Real-time charts using Chart.js

## Tech Stack

**Backend:**
- Python 3.8+
- Flask - Web framework
- Flask-SQLAlchemy - ORM
- Flask-Login - User session management

**Database:**
- SQLite - Lightweight database

**Frontend:**
- HTML5
- CSS3 (Bootstrap 5)
- JavaScript (Chart.js, DataTables)

**Export:**
- ReportLab - PDF generation
- openpyxl - Excel generation

## Project Structure

```
expense-management-app/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── run.sh                    # Application startup script
├── instance/
│   └── expenses.db          # SQLite database (created on first run)
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models
│   ├── auth.py              # Authentication routes
│   ├── expenses.py          # Expense management routes
│   ├── reports.py           # Reports generation routes
│   └── utils.py             # Utility functions
├── templates/
│   ├── base.html            # Base template
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard.html       # Dashboard with charts
│   ├── add_expense.html     # Add/Edit expense form
│   ├── expenses.html        # View all expenses
│   ├── reports.html         # Reports page
│   └── profile.html         # User profile
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   ├── js/
│   │   ├── charts.js        # Chart functionality
│   │   └── main.js          # Main JavaScript
│   └── images/
│       └── logo.png         # Application logo
└── README.md                # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pamplonaou31-cloud/expense-management-app.git
   cd expense-management-app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```
   Or use the provided script:
   ```bash
   bash run.sh
   ```

6. **Access the application:**
   - Open your browser and navigate to `http://localhost:5000`

## Usage

### 1. Registration
- Click on "Register" link
- Fill in username, email, and password
- Account will be created and automatically logged in

### 2. Add Expenses
- Click "Add Expense" button
- Fill in amount, category, date, and description
- Save expense

### 3. View Expenses
- Go to "Expenses" page
- View all expenses in a table format
- Edit or delete expenses as needed
- Search and filter expenses

### 4. View Reports
- Go to "Reports" section
- View monthly and yearly expense summaries
- See category-wise breakdown
- Download reports as PDF or Excel

### 5. Dashboard
- View pie charts of expense by category
- See monthly trend analysis
- Quick statistics (total, average, max)
- Recent transactions list

### 6. Export Data
- From Reports page, click "Export to PDF" or "Export to Excel"
- Select date range
- Download formatted report

## Database Schema

### User Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Expense Table
```sql
CREATE TABLE expense (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount FLOAT NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Category Table
```sql
CREATE TABLE category (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login
- `GET /logout` - User logout

### Expenses
- `GET /expenses` - View all expenses
- `POST /expenses/add` - Add new expense
- `GET /expenses/<id>/edit` - Edit expense page
- `POST /expenses/<id>/update` - Update expense
- `GET /expenses/<id>/delete` - Delete expense

### Reports
- `GET /reports` - View reports
- `GET /reports/monthly` - Monthly report
- `GET /reports/yearly` - Yearly report
- `GET /reports/export/pdf` - Export to PDF
- `GET /reports/export/excel` - Export to Excel

### Dashboard
- `GET /dashboard` - Main dashboard
- `GET /api/chart-data` - Chart data (JSON)
- `GET /api/statistics` - Statistics (JSON)

## Configuration

Edit `config.py` to customize:
- Database location
- Secret key
- Flask debug mode
- Session timeout
- Export settings

## Default Categories

- Food & Dining
- Transportation
- Shopping
- Entertainment
- Utilities
- Healthcare
- Education
- Other

## Security Features

✅ Password hashing with werkzeug.security
✅ SQL injection prevention with SQLAlchemy ORM
✅ CSRF protection with Flask-WTF
✅ Session-based authentication
✅ User data isolation

## Troubleshooting

### Database Issues
- Delete `instance/expenses.db` and restart the application
- Database will be recreated automatically

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify virtual environment is activated

## Performance Tips

- Use indexes on frequently queried columns
- Implement pagination for large datasets
- Cache frequently accessed reports
- Use AJAX for real-time updates

## Future Enhancements

- [ ] Budget limits and alerts
- [ ] Multi-currency support
- [ ] Recurring expenses
- [ ] Receipt image upload
- [ ] Mobile app
- [ ] Cloud backup
- [ ] Collaborative budgeting
- [ ] AI-powered categorization

## License

MIT License - Feel free to use this project for personal and commercial purposes.

## Support

For issues, questions, or suggestions, please create an issue on GitHub.

## Contributors

Contributions are welcome! Please fork the repository and submit a pull request.

---

**Made with ❤️ for better expense management**
