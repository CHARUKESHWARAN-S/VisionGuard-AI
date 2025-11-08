from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configuration
UPLOAD_FOLDER = r'C:\Users\mrcha\OneDrive\Desktop\Face-recognition-attendence-main\photos'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clear_upload_folder():
    # Delete all files in the upload folder
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Clear the upload folder before saving new images
        clear_upload_folder()
        
        family_members = []
        has_errors = False
        
        # Process each possible family member (up to 4)
        for i in range(1, 5):
            name = request.form.get(f'name_{i}')
            relation = request.form.get(f'relation_{i}')
            age_input = request.form.get(f'age_{i}')
            file = request.files.get(f'image_{i}')
            
            # Only process if at least name is provided
            if name:
                if not file or not allowed_file(file.filename):
                    flash(f'Please upload a valid image (JPG/PNG) for member {i}', 'error')
                    has_errors = True
                    continue
                
                # Age validation
                age = None
                if age_input:
                    try:
                        age = int(age_input)
                        if age < 1 or age > 120:
                            flash(f'Age for member {i} must be between 1-120', 'error')
                            has_errors = True
                            continue
                    except ValueError:
                        flash(f'Invalid age for member {i}', 'error')
                        has_errors = True
                        continue
                
                try:
                    # Get and preserve original file extension
                    file_ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = f"{i}.{file_ext}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    
                    family_members.append({
                        'id': i,
                        'name': name,
                        'relation': relation,
                        'age': age,
                        'image_filename': filename,
                        'image_format': file_ext.upper()
                    })
                except Exception as e:
                    flash(f'Error saving image for member {i}: {str(e)}', 'error')
                    has_errors = True
        
        if has_errors:
            return redirect(url_for('home'))
        
        if not family_members:
            flash('Please enter at least one family member', 'error')
            return redirect(url_for('home'))
        
        return redirect(url_for('success', count=len(family_members)))
    
    return render_template('home.html')

@app.route('/success')
def success():
    count = request.args.get('count', 0)
    return render_template('success.html', count=count)

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)