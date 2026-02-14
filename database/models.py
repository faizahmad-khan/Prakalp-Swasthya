# -*- coding: utf-8 -*-
"""
Database Models for SwasthyaGuide
SQLAlchemy ORM models for PostgreSQL
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Clinic(Base):
    """Model for storing clinic/pharmacy information"""
    __tablename__ = 'clinics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), index=True)
    area = Column(String(100), index=True)
    location_key = Column(String(200), index=True)  # e.g., "Lucknow_Gomti_Nagar"
    timing = Column(String(200))
    phone = Column(String(20))
    specialties = Column(JSON)  # Array of specialties
    fees = Column(String(100))
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Clinic(id={self.id}, name='{self.name}', city='{self.city}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'area': self.area,
            'timing': self.timing,
            'phone': self.phone,
            'specialties': self.specialties,
            'fees': self.fees,
            'latitude': self.latitude,
            'longitude': self.longitude
        }


class Conversation(Base):
    """Model for storing user conversation history"""
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), index=True)  # WhatsApp phone number or unique session ID
    user_phone = Column(String(20), index=True)
    user_name = Column(String(100), nullable=True)
    language = Column(String(20), default='hindi')
    message_type = Column(String(20))  # 'text', 'image', 'voice'
    user_message = Column(Text)
    bot_response = Column(Text)
    detected_intent = Column(String(50))  # 'symptom_check', 'clinic_search', 'emergency', 'general'
    detected_symptoms = Column(JSON, nullable=True)  # Array of symptoms
    detected_location = Column(String(100), nullable=True)
    is_emergency = Column(Boolean, default=False)
    image_url = Column(String(500), nullable=True)
    image_analysis = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, session='{self.session_id}', intent='{self.detected_intent}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'user_phone': self.user_phone,
            'language': self.language,
            'message_type': self.message_type,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'detected_intent': self.detected_intent,
            'detected_symptoms': self.detected_symptoms,
            'detected_location': self.detected_location,
            'is_emergency': self.is_emergency,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Message(Base):
    """Model for storing individual messages in a conversation"""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), index=True)
    sender = Column(String(20))  # 'user' or 'bot'
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, sender='{self.sender}')>"


class Analytics(Base):
    """Model for storing usage analytics and metrics"""
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    metric_type = Column(String(50), index=True)  # 'total_users', 'active_users', 'messages_count'
    metric_name = Column(String(100))
    metric_value = Column(Integer, default=0)
    language = Column(String(20), nullable=True)
    location = Column(String(100), nullable=True)
<<<<<<< HEAD
    extra_data = Column(JSON, nullable=True)  # Renamed from 'metadata' to avoid SQLAlchemy conflict
=======
    extra_data = Column(JSON, nullable=True)  # Renamed from 'metadata' (reserved in SQLAlchemy)
>>>>>>> refs/remotes/origin/main
    
    def __repr__(self):
        return f"<Analytics(id={self.id}, type='{self.metric_type}', value={self.metric_value})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'metric_type': self.metric_type,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'language': self.language,
            'location': self.location,
            'extra_data': self.extra_data
        }


class UserProfile(Base):
    """Model for storing user profile information"""
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=True)
    preferred_language = Column(String(20), default='hindi')
    location = Column(String(100), nullable=True)
    total_conversations = Column(Integer, default=0)
    last_active = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserProfile(id={self.id}, phone='{self.phone_number}', name='{self.name}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'name': self.name,
            'preferred_language': self.preferred_language,
            'location': self.location,
            'total_conversations': self.total_conversations,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
