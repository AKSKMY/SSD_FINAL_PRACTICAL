from flask import Flask, render_template, request, redirect, url_for, Response
from html import escape
import re

app = Flask(__name__)

# Function to sanitize the search term (prevent XSS)
def sanitize_search_term(search_term):
    # Use escape to prevent XSS by escaping HTML special characters
    sanitized_term = escape(search_term)
    return sanitized_term

# Function to check for SQL injection
def is_sql_injection(search_term):
    # Simple check for SQL injection patterns like ' OR 1=1 -- or DROP
    sql_patterns = [r"'.*--", r"'.*#'", r"OR\s+1\s*=\s*1", r"DROP\s+TABLE"]
    for pattern in sql_patterns:
        if re.search(pattern, search_term, re.IGNORECASE):
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def home():
    search_term = ''
    error_message = ''
    
    if request.method == 'POST':
        search_term = request.form['search-term']  # Capture the search term from the form
        
        # Check for SQL Injection
        if is_sql_injection(search_term):
            error_message = "SQL Injection detected! Please provide a valid search term."
            search_term = ''  # Clear the search term
        
        # Sanitize for XSS
        elif search_term != '':
            sanitized_term = sanitize_search_term(search_term)
            
            # If no issues with XSS and SQL injection, proceed to the new page
            if sanitized_term != search_term:
                error_message = "XSS Attack detected! Please provide a valid search term."
                search_term = ''  # Clear the search term
            else:
                return redirect(url_for('display_search', search_term=sanitized_term))
    
    return render_template('home.html', search_term=search_term, error_message=error_message)

@app.route('/search', methods=['GET'])
def display_search():
    search_term = request.args.get('search_term', '')
    return render_template('search_results.html', search_term=search_term)

if __name__ == '__main__':
    app.run(debug=False)
