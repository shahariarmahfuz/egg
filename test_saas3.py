from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import with_loader_criteria

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))

@event.listens_for(db.session, 'do_orm_execute')
def _do_orm_execute(execute_state):
    from flask import has_request_context, g
    if execute_state.is_select:
        if has_request_context() and getattr(g, 'business_id', None):
            b_id = g.business_id
            execute_state.statement = execute_state.statement.options(
                with_loader_criteria(
                    db.Model,
                    lambda cls: cls.business_id == b_id if hasattr(cls, 'business_id') else True,
                    include_aliases=True,
                    propagate_to_loaders=True,
                    track_closure_variables=False
                )
            )

with app.app_context():
    db.create_all()
    b1 = Business(name="B1")
    b2 = Business(name="B2")
    db.session.add_all([b1, b2])
    db.session.commit()
    
    u1 = User(name="U1", business_id=b1.id)
    u2 = User(name="U2", business_id=b2.id)
    u3 = User(name="U3", business_id=b2.id)
    db.session.add_all([u1, u2, u3])
    db.session.commit()

@app.route('/b/<int:b_id>')
def test(b_id):
    g.business_id = b_id
    users = User.query.all()
    return ','.join(u.name for u in users)

if __name__ == '__main__':
    with app.test_client() as client:
        print("B1:", client.get('/b/1').data.decode())
        print("B2:", client.get('/b/2').data.decode())
