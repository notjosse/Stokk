from flask import Blueprint, redirect, url_for, flash

from flask_login import login_required, current_user

coins_bp = Blueprint("coins", __name__)


@coins_bp.route('/reload')
@login_required
def reload():
    if current_user.reloads > 0:
        flash(f'Cannot request additional coin reloads.', category='danger')

    if current_user.budget < 50 and current_user.reloads == 0:
        flash(f'Your coins have been reloaded.', category='success')
        current_user.reload_coins()
        
    return redirect(url_for('historical_data.home'))