from config import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

class Trail(db.Model):
    __tablename__ = "trails"
    __table_args__ = {"schema": "TrailApp"}
    TrailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailName = db.Column(db.String(100), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=db.func.now())

class TrailInfo(db.Model):
    __tablename__ = "TrailInfo"
    __table_args__ = {"schema": "TrailApp"}
    TrailID = db.Column(db.Integer, db.ForeignKey("TrailApp.trails.TrailID"), primary_key=True)
    Description = db.Column(db.Text)
    Distance = db.Column(db.Float)
    Difficulty = db.Column(db.String(50))
    RouteType = db.Column(db.String(50))
    EstimatedTime = db.Column(db.String(50))
    ElevationGain = db.Column(db.Float)
    LengthKM = db.Column(db.Float)

class Location(db.Model):
    __tablename__ = "locations"
    __table_args__ = {"schema": "TrailApp"}
    LocationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailID = db.Column(db.Integer, db.ForeignKey("TrailApp.trails.TrailID"), nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    Sequence = db.Column(db.Integer, nullable=False)

class Tag(db.Model):
    __tablename__ = "Tags"
    __table_args__ = {"schema": "TrailApp"}
    TagID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)

class TrailTag(db.Model):
    __tablename__ = "TrailTags"
    __table_args__ = {"schema": "TrailApp"}
    TrailID = db.Column(db.Integer, db.ForeignKey("TrailApp.trails.TrailID"), primary_key=True)
    TagID = db.Column(db.Integer, db.ForeignKey("TrailApp.Tags.TagID"), primary_key=True)



class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'TrailApp'}
    UserID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255))
    RoleID = db.Column(db.Integer, db.ForeignKey('TrailApp.roles.RoleID'))

    
    role = db.relationship('Role', backref='users')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.PasswordHash.encode('utf-8'))

class Role(db.Model):
    __tablename__ = "roles"
    __table_args__ = {"schema": "TrailApp"}
    RoleID = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.String(50))

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True

class TrailInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailInfo
        load_instance = True

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True

class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        load_instance = True

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
trail_info_schema = TrailInfoSchema()
trail_infos_schema = TrailInfoSchema(many=True)
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

