import sys
import traceback
from app import create_app
from models import db, Admin

app = create_app()
app.config['TESTING'] = True

def audit():
    with app.test_client() as client:
        with app.app_context():
            admin = Admin.query.filter_by(username='admin').first()
            if not admin:
                from werkzeug.security import generate_password_hash
                admin = Admin(username='admin', password=generate_password_hash('admin'))
                db.session.add(admin)
                db.session.commit()
            
        with client.session_transaction() as sess:
            sess['_user_id'] = str(admin.id)
            sess['_fresh'] = True

        issues = []
        for rule in app.url_map.iter_rules():
            if 'GET' in rule.methods and not '<' in rule.rule:
                if 'static' in rule.rule: continue
                try:
                    resp = client.get(rule.rule)
                    if resp.status_code >= 400 and resp.status_code not in (405,):
                        issues.append(f"Route {rule.rule} returned {resp.status_code}")
                except Exception as e:
                    issues.append(f"Route {rule.rule} threw exception: {str(e)}")
                    # Optionally capture traceback if needed, but error message is enough for now

        if issues:
            print("Found issues:")
            for i in issues:
                print(i)
        else:
            print("All basic routes OK.")

if __name__ == '__main__':
    audit()
