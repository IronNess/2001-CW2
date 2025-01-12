from config import db, ma  # Import database and Marshmallow instances

# Define the Trail model
class Trail(db.Model):
    __tablename__ = "trails"
    TrailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailName = db.Column(db.String(100), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=db.func.now())

# Define the TrailInfo model
class TrailInfo(db.Model):
    __tablename__ = "trail_info"
    TrailID = db.Column(db.Integer, db.ForeignKey("trails.TrailID"), primary_key=True)
    Description = db.Column(db.Text)
    Distance = db.Column(db.Float)
    Difficulty = db.Column(db.String(50))

# Define the Location model
class Location(db.Model):
    __tablename__ = "locations"
    LocationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailID = db.Column(db.Integer, db.ForeignKey("trails.TrailID"), nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    Sequence = db.Column(db.Integer, nullable=False)

# Define schemas for serialization
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

# Create schema instances for serialization
trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)

trail_info_schema = TrailInfoSchema()
trail_infos_schema = TrailInfoSchema(many=True)

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
