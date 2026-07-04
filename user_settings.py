from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Admin, generate_avatar_seed
import os
import cloudinary
import cloudinary.uploader
from PIL import Image
import io

user_settings_bp = Blueprint('user_settings', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_settings_bp.route('/account/settings', methods=['GET'])
@login_required
def settings_page():
    # If site admin, render with site admin base layout, else normal base
    if current_user.role == 'Site Admin':
        base_template = 'site_admin_base.html'
    else:
        base_template = 'base.html'
    return render_template('user_settings.html', base_template=base_template)

@user_settings_bp.route('/account/change_avatar', methods=['POST'])
@login_required
def change_avatar():
    action = request.form.get('action')
    
    if action == 'generate':
        current_user.avatar_seed = generate_avatar_seed()
        current_user.avatar_url = None
        current_user.avatar_public_id = None
        db.session.commit()
        flash('Avatar updated successfully.', 'success')
        return redirect(request.referrer or url_for('user_settings.settings_page'))
        
    elif action == 'upload':
        if 'avatar_file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.referrer or url_for('user_settings.settings_page'))
            
        file = request.files['avatar_file']
        
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.referrer or url_for('user_settings.settings_page'))
            
        if file and allowed_file(file.filename):
            # Check file size (5MB limit)
            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            if file_length > 5 * 1024 * 1024:
                flash('File size exceeds 5MB limit.', 'danger')
                return redirect(request.referrer or url_for('user_settings.settings_page'))
            file.seek(0)
            
            try:
                # Open image with Pillow
                img = Image.open(file)
                
                # Convert to RGB if it's RGBA (to save as JPEG/WebP or just standardize)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                # Resize and crop to 300x300 square
                width, height = img.size
                if width != height:
                    # Crop to square
                    min_dim = min(width, height)
                    left = (width - min_dim) / 2
                    top = (height - min_dim) / 2
                    right = (width + min_dim) / 2
                    bottom = (height + min_dim) / 2
                    img = img.crop((left, top, right, bottom))
                
                img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                
                # Save to bytes
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG', quality=85)
                img_byte_arr.seek(0)
                
                # Delete old avatar if exists
                if current_user.avatar_public_id:
                    try:
                        cloudinary.uploader.destroy(current_user.avatar_public_id)
                    except Exception as e:
                        print(f"Failed to delete old avatar: {e}")
                
                # Upload to Cloudinary
                upload_result = cloudinary.uploader.upload(
                    img_byte_arr,
                    folder="avatars",
                    public_id=f"user_{current_user.id}_{generate_avatar_seed()}"
                )
                
                current_user.avatar_url = upload_result.get('secure_url')
                current_user.avatar_public_id = upload_result.get('public_id')
                db.session.commit()
                flash('Avatar uploaded successfully.', 'success')
            except Exception as e:
                flash(f'An error occurred during upload: {str(e)}', 'danger')
        else:
            flash('Invalid file type. Please upload a JPG, PNG, or WEBP image.', 'danger')
            
    return redirect(request.referrer or url_for('user_settings.settings_page'))


@user_settings_bp.route('/account/change_password', methods=['POST'])
@login_required
def change_password():
    if current_user.role == 'Employee':
        flash('Employees cannot change their password.', 'danger')
        return redirect(request.referrer or url_for('user_settings.settings_page'))
        
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not check_password_hash(current_user.password, current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(request.referrer or url_for('user_settings.settings_page'))
        
    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(request.referrer or url_for('user_settings.settings_page'))
        
    current_user.password = generate_password_hash(new_password)
    db.session.commit()
    flash('Password updated successfully.', 'success')
    return redirect(request.referrer or url_for('user_settings.settings_page'))
