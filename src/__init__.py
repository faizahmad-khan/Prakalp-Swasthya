# -*- coding: utf-8 -*-
"""
SwasthyaGuide - Source Code Package
Main application modules for healthcare chatbot
"""

from importlib import import_module


_EXPORT_MAP = {
    'SwasthyaGuide': ('src.chatbot', 'SwasthyaGuide'),
    'check_for_clinic_request': ('src.clinic_finder', 'check_for_clinic_request'),
    'extract_location': ('src.clinic_finder', 'extract_location'),
    'find_nearby_clinics': ('src.clinic_finder', 'find_nearby_clinics'),
    'Config': ('src.config_loader', 'Config'),
    'detect_emergency': ('src.emergency_handler', 'detect_emergency'),
    'get_emergency_response': ('src.emergency_handler', 'get_emergency_response'),
    'get_symptom_response': ('src.health_responses', 'get_symptom_response'),
    'get_general_health_tips': ('src.health_responses', 'get_general_health_tips'),
    'ImageAnalyzer': ('src.image_analyzer', 'ImageAnalyzer'),
    'detect_language': ('src.language_detector', 'detect_language'),
    'extract_symptoms': ('src.symptom_checker', 'extract_symptoms'),
}

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


def __getattr__(name):
    """Lazily import public symbols to avoid hard dependency failures at package import time."""
    if name not in _EXPORT_MAP:
        raise AttributeError(f"module 'src' has no attribute '{name}'")

    module_name, attr_name = _EXPORT_MAP[name]
    module = import_module(module_name)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value

__version__ = '2.0.0'
