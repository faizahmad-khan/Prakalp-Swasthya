# -*- coding: utf-8 -*-
"""
SwasthyaGuide - Source Code Package
Main application modules for healthcare chatbot
"""

from .chatbot import SwasthyaGuide
from .clinic_finder import check_for_clinic_request, extract_location, find_nearby_clinics
from .config_loader import Config
from .emergency_handler import detect_emergency, get_emergency_response
from .health_responses import get_symptom_response, get_general_health_tips
from .image_analyzer import ImageAnalyzer
from .language_detector import detect_language
from .symptom_checker import extract_symptoms

__all__ = [
    'SwasthyaGuide',
    'check_for_clinic_request',
    'extract_location',
    'find_nearby_clinics',
    'Config',
    'detect_emergency',
    'get_emergency_response',
    'get_symptom_response',
    'get_general_health_tips',
    'ImageAnalyzer',
    'detect_language',
    'extract_symptoms',
]

__version__ = '2.0.0'
