from config import db, ma

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

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
trail_info_schema = TrailInfoSchema()
trail_infos_schema = TrailInfoSchema(many=True)
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

