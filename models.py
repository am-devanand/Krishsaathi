# KrishiSaathi - SQL models for farmers and preferences

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Farmer(db.Model):
    """Farmer: name, mobile (unique), language, district, village. Persisted for sessions."""
    __tablename__ = 'farmers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    mobile: Mapped[str] = mapped_column(String(15), unique=True, nullable=False, index=True)
    language_code: Mapped[str] = mapped_column(String(5), default='hi', nullable=False)
    state: Mapped[str] = mapped_column(String(10), default='', nullable=False)
    district: Mapped[str] = mapped_column(String(80), default='', nullable=False)
    village: Mapped[str] = mapped_column(String(80), default='', nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    crops: Mapped[list['FarmerCrop']] = relationship('FarmerCrop', back_populates='farmer', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mobile': self.mobile,
            'language_code': self.language_code,
            'state': self.state,
            'district': self.district,
            'village': self.village,
        }


class FarmerCrop(db.Model):
    """Crop details per farmer: type, stage, season. One farmer can have multiple crops."""
    __tablename__ = 'farmer_crops'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    farmer_id: Mapped[int] = mapped_column(Integer, ForeignKey('farmers.id', ondelete='CASCADE'), nullable=False)
    crop_type: Mapped[str] = mapped_column(String(40), nullable=False)   # paddy, wheat, cotton, etc.
    stage: Mapped[str] = mapped_column(String(30), default='', nullable=False)  # sowing, vegetative, etc.
    season: Mapped[str] = mapped_column(String(20), default='', nullable=False)  # kharif, rabi, etc.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    farmer: Mapped['Farmer'] = relationship('Farmer', back_populates='crops')
