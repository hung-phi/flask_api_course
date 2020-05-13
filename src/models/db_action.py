from src.db import db


class DBAction: # DBActionMixin
    @staticmethod
    def save_to_db(obj):
        db.session.add(obj)
        db.session.commit()

    @staticmethod
    def delete_from_db(obj):
        db.session.delete(obj)
        db.session.commit()
