class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=function.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

