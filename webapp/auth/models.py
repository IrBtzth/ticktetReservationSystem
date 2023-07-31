from . import bcrypt, AnonymousUserMixin
from .. import db

roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), nullable=False, index=True, unique=True)
    name=db.Column(db.String(255))
    lastName=db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(70), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    bookings = db.relationship('Bookings', backref='userb',lazy='dynamic')
    
    
    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('roles', lazy='dynamic')
    )

    feedback = db.relationship('Feedback', backref='userf',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def has_role(self, name):
        for role in self.roles:
            if role.name == name:
                return True
        return False

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    

    def __repr__(self):
        return '{}'.format(self.name)