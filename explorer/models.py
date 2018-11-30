# from ext import db
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

db = SQLAlchemy()
# conn = db.engine.connect()
# sql = db.engine.dialect

class BaseModel(db.Model):
    __abstract__ = True
    __tablename__ = None

    def __repr__(self):
        return self.__tablename__

    # def _row_to_dict(self):
    #     def as_dict(self):
    #         d = {}
    #         for column in row.__table__.columns:
    #             d[column.name] = str(getattr(row, column.name))
    #
    #         return d


class Disease(BaseModel):
    __tablename__ = 'diseases'
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String)
    disease_heb = db.Column(db.String)
    info = db.Column(db.String)
    info_heb = db.Column(db.String)
    wiki = db.Column(db.String)
    wiki_heb = db.Column(db.String)
    reports = db.relationship('Report', backref='reports', lazy=True)

    def __repr__(self):
        return f'Disease {self.disease}'

    @classmethod
    def get_disease_dict(cls):
        diseases = cls.query.all()
        ret = {d.disease.lower(): d.id for d in diseases}
        return ret

    @classmethod
    def get_reports(cls, disease_id):
        reports = cls.query.filter(cls.id == disease_id).first().reports
        return reports


class Report(BaseModel):
    __tablename__ = 'reports'
    id = db.Column(db.String, primary_key=True)
    date = db.Column(db.DateTime(), index=True)
    year = db.Column(db.Integer, index=True)
    week = db.Column(db.Integer, index=True)
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.id'), index=True)
    afula = db.Column(db.Integer)
    akko = db.Column(db.Integer)
    ashqelon = db.Column(db.Integer)
    beer_sheva = db.Column(db.Integer)
    hasharon = db.Column(db.Integer)
    hadera = db.Column(db.Integer)
    haifa = db.Column(db.Integer)
    jerusalem = db.Column(db.Integer)
    kinneret = db.Column(db.Integer)
    nazareth = db.Column(db.Integer)
    petach_tiqwa = db.Column(db.Integer)
    ramla = db.Column(db.Integer)
    rehovot = db.Column(db.Integer)
    tel_aviv = db.Column(db.Integer)
    zefat = db.Column(db.Integer)
    idf = db.Column(db.Integer)
    total = db.Column(db.Integer)
    sumtotal = db.Column(db.Integer)

    def __repr__(self):
        return "Disease {} on date {}".format(self.disease_id, self.date)

    @classmethod
    def get_reports_df(cls, disease_id):
        q = (cls
             .query
             .filter(cls.disease_id == disease_id)
             .order_by(cls.date))
        ret = pd.read_sql(q.statement, db.engine)
        return ret

    def get_df(self):
        pd.read_sql(self, db)
