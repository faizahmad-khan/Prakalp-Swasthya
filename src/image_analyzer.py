# -*- coding: utf-8 -*-
"""
Advanced Image Analysis Module
Analyzes medical images for skin conditions, rashes, and diagnostics
Enhanced with AI-powered analysis, color detection, and texture analysis
"""

import base64
import io
import os
import json
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from PIL import Image, ImageEnhance, ImageFilter, ImageStat
from datetime import datetime
import hashlib


class ImageAnalyzer:
    """Handles advanced medical image analysis"""
    
    def __init__(self):
        """Initialize the advanced image analyzer"""
        self.supported_formats = ['jpg', 'jpeg', 'png', 'webp']
        self.max_image_size = 10 * 1024 * 1024  # 10MB
        self.min_image_size = 1024  # 1KB
        
        # Enhanced skin condition categories with characteristics
        self.skin_conditions = {
            'rash': {
                'keywords': ['redness', 'irritation', 'bumps', 'patches'],
                'color_range': [(150, 50, 50), (255, 150, 150)],  # Red tones
                'severity_levels': ['mild', 'moderate', 'severe']
            },
            'acne': {
                'keywords': ['pimples', 'blackheads', 'whiteheads', 'spots'],
                'color_range': [(200, 150, 150), (255, 200, 200)],
                'severity_levels': ['mild', 'moderate', 'severe', 'cystic']
            },
            'eczema': {
                'keywords': ['dry', 'scaly', 'itchy', 'inflamed'],
                'color_range': [(180, 100, 100), (240, 180, 180)],
                'severity_levels': ['mild', 'moderate', 'severe']
            },
            'fungal': {
                'keywords': ['circular', 'ring', 'scaling', 'athlete'],
                'color_range': [(200, 150, 120), (255, 220, 200)],
                'severity_levels': ['localized', 'spreading', 'widespread']
            },
            'psoriasis': {
                'keywords': ['thick', 'silvery', 'scaly', 'plaques'],
                'color_range': [(190, 140, 140), (250, 200, 200)],
                'severity_levels': ['mild', 'moderate', 'severe']
            },
            'burn': {
                'keywords': ['redness', 'blistering', 'peeling'],
                'color_range': [(180, 80, 80), (255, 150, 150)],
                'severity_levels': ['first_degree', 'second_degree', 'third_degree']
            },
            'insect_bite': {
                'keywords': ['swelling', 'red', 'bump', 'bite'],
                'color_range': [(160, 100, 100), (255, 180, 180)],
                'severity_levels': ['mild', 'moderate', 'allergic_reaction']
            },
            'allergy': {
                'keywords': ['hives', 'urticaria', 'welts', 'swelling'],
                'color_range': [(180, 120, 120), (255, 190, 190)],
                'severity_levels': ['mild', 'moderate', 'severe', 'anaphylaxis']
            },
            'melanoma_warning': {
                'keywords': ['mole', 'dark', 'irregular', 'asymmetric'],
                'color_range': [(30, 15, 10), (100, 60, 40)],
                'severity_levels': ['monitor', 'consult_immediately']
            }
        }
        
        # Image analysis history for tracking
        self.analysis_history = []
    
    def validate_image(self, image_data: bytes, content_type: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Enhanced image validation with metadata extraction
        Returns: (is_valid, error_message, metadata)
        """
        # Check size
        if len(image_data) > self.max_image_size:
            return False, "Image too large. Please send an image smaller than 10MB.", None
        
        if len(image_data) < self.min_image_size:
            return False, "Image too small. Please send a clear image.", None
        
        # Check format and extract metadata
        try:
            image = Image.open(io.BytesIO(image_data))
            format_lower = image.format.lower() if image.format else ''
            
            if format_lower not in self.supported_formats:
                return False, f"Unsupported format. Please send: {', '.join(self.supported_formats)}", None
            
            # Check dimensions
            width, height = image.size
            if width < 100 or height < 100:
                return False, "Image resolution too low. Please send a clearer image.", None
            
            # Extract metadata
            metadata = {
                'format': image.format,
                'mode': image.mode,
                'size': (width, height),
                'file_size': len(image_data),
                'aspect_ratio': round(width / height, 2),
                'timestamp': datetime.now().isoformat(),
                'image_hash': hashlib.md5(image_data).hexdigest()
            }
            
            # Extract EXIF data if available
            if hasattr(image, '_getexif') and image._getexif():
                metadata['exif'] = self._extract_exif_data(image)
            
            return True, "Image valid", metadata
            
        except Exception as e:
            return False, f"Invalid image file. Error: {str(e)}", None
    
    def _extract_exif_data(self, image: Image.Image) -> Dict:
        """Extract relevant EXIF metadata"""
        try:
            exif = image._getexif() or {}
            relevant_tags = {
                'DateTime': 306,
                'Make': 271,
                'Model': 272,
                'Orientation': 274,
                'Flash': 37385
            }
            
            extracted = {}
            for name, tag_id in relevant_tags.items():
                if tag_id in exif:
                    extracted[name] = exif[tag_id]
            
            return extracted
        except:
            return {}
    
    def preprocess_image(self, image_data: bytes, enhance: bool = True) -> Tuple[Image.Image, Image.Image]:
        """
        Advanced image preprocessing with enhancement options
        Returns: (original_image, enhanced_image)
        """
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Store original
        original = image.copy()
        
        # Resize if too large (max 1024x1024 for processing)
        max_dimension = 1024
        if max(image.size) > max_dimension:
            ratio = max_dimension / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            original = original.resize(new_size, Image.Resampling.LANCZOS)
        
        # Apply enhancements if requested
        if enhance:
            enhanced = self._enhance_image(image)
        else:
            enhanced = image
        
        return original, enhanced
    
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """
        Apply multiple enhancement techniques for better analysis
        """
        # Adjust contrast
        contrast_enhancer = ImageEnhance.Contrast(image)
        image = contrast_enhancer.enhance(1.2)
        
        # Adjust sharpness
        sharpness_enhancer = ImageEnhance.Sharpness(image)
        image = sharpness_enhancer.enhance(1.3)
        
        # Adjust brightness slightly
        brightness_enhancer = ImageEnhance.Brightness(image)
        image = brightness_enhancer.enhance(1.1)
        
        # Apply light denoising
        image = image.filter(ImageFilter.MedianFilter(size=3))
        
        return image
    
    def analyze_colors(self, image: Image.Image) -> Dict[str, Any]:
        """
        Advanced color analysis for skin condition detection
        """
        # Convert to numpy array for analysis
        img_array = np.array(image)
        
        # Calculate color statistics
        r_channel = img_array[:, :, 0]
        g_channel = img_array[:, :, 1]
        b_channel = img_array[:, :, 2]
        
        color_stats = {
            'mean_rgb': [
                float(np.mean(r_channel)),
                float(np.mean(g_channel)),
                float(np.mean(b_channel))
            ],
            'std_rgb': [
                float(np.std(r_channel)),
                float(np.std(g_channel)),
                float(np.std(b_channel))
            ],
            'dominant_color': self._get_dominant_color(img_array),
            'redness_score': self._calculate_redness_score(r_channel, g_channel, b_channel),
            'color_variance': float(np.std(img_array)),
            'inflammation_indicators': self._detect_inflammation(img_array)
        }
        
        return color_stats
    
    def _get_dominant_color(self, img_array: np.ndarray) -> List[int]:
        """Extract dominant color from image"""
        # Reshape image to 2D array of pixels
        pixels = img_array.reshape(-1, 3)
        
        # Calculate mean color (simple dominant color detection)
        dominant = np.mean(pixels, axis=0)
        
        return [int(c) for c in dominant]
    
    def _calculate_redness_score(self, r: np.ndarray, g: np.ndarray, b: np.ndarray) -> float:
        """
        Calculate redness score - higher values indicate more inflammation
        """
        # Redness is typically when R channel is significantly higher than G and B
        r_mean = np.mean(r)
        g_mean = np.mean(g)
        b_mean = np.mean(b)
        
        # Normalize redness score (0-100)
        if g_mean > 0 and b_mean > 0:
            redness = ((r_mean - g_mean) + (r_mean - b_mean)) / 2
            score = max(0, min(100, redness / 2.55))  # Normalize to 0-100
        else:
            score = 0
        
        return float(score)
    
    def _detect_inflammation(self, img_array: np.ndarray) -> Dict[str, Any]:
        """
        Detect signs of inflammation based on color patterns
        """
        r_channel = img_array[:, :, 0]
        g_channel = img_array[:, :, 1]
        b_channel = img_array[:, :, 2]
        
        # Calculate inflammation metrics
        r_mean = np.mean(r_channel)
        g_mean = np.mean(g_channel)
        
        # Red-dominant regions
        red_dominant = np.sum((r_channel > g_channel + 20) & (r_channel > b_channel + 20))
        total_pixels = r_channel.size
        
        inflammation = {
            'red_dominant_percentage': float(red_dominant / total_pixels * 100),
            'likely_inflamed': red_dominant / total_pixels > 0.3,
            'severity_estimate': 'high' if red_dominant / total_pixels > 0.5 else 
                                'medium' if red_dominant / total_pixels > 0.3 else 'low'
        }
        
        return inflammation
    
    def analyze_texture(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze image texture for detecting skin irregularities
        """
        # Convert to grayscale for texture analysis
        gray_image = image.convert('L')
        gray_array = np.array(gray_image)
        
        # Calculate texture features
        texture_stats = {
            'smoothness': self._calculate_smoothness(gray_array),
            'uniformity': self._calculate_uniformity(gray_array),
            'entropy': self._calculate_entropy(gray_array),
            'edge_density': self._calculate_edge_density(gray_array),
            'texture_type': 'rough' if self._calculate_smoothness(gray_array) < 0.5 else 'smooth'
        }
        
        return texture_stats
    
    def _calculate_smoothness(self, gray_array: np.ndarray) -> float:
        """Calculate smoothness metric"""
        variance = np.var(gray_array)
        smoothness = 1 - (1 / (1 + variance))
        return float(smoothness)
    
    def _calculate_uniformity(self, gray_array: np.ndarray) -> float:
        """Calculate uniformity metric"""
        histogram, _ = np.histogram(gray_array.flatten(), bins=256, range=(0, 256))
        histogram = histogram / histogram.sum()
        uniformity = np.sum(histogram ** 2)
        return float(uniformity)
    
    def _calculate_entropy(self, gray_array: np.ndarray) -> float:
        """Calculate entropy (randomness) in image"""
        histogram, _ = np.histogram(gray_array.flatten(), bins=256, range=(0, 256))
        histogram = histogram / histogram.sum()
        histogram = histogram[histogram > 0]
        entropy = -np.sum(histogram * np.log2(histogram))
        return float(entropy)
    
    def _calculate_edge_density(self, gray_array: np.ndarray) -> float:
        """Calculate edge density using gradient"""
        # Simple edge detection using gradients
        grad_x = np.abs(np.gradient(gray_array, axis=1))
        grad_y = np.abs(np.gradient(gray_array, axis=0))
        edge_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Calculate percentage of edge pixels
        edge_threshold = np.mean(edge_magnitude) + np.std(edge_magnitude)
        edge_pixels = np.sum(edge_magnitude > edge_threshold)
        edge_density = edge_pixels / gray_array.size
        
        return float(edge_density)
    
    def analyze_image_comprehensive(self, image: Image.Image, enhanced_image: Image.Image) -> Dict:
        """
        Comprehensive image analysis combining multiple techniques
        """
        width, height = image.size
        
        # Perform all analyses
        color_analysis = self.analyze_colors(enhanced_image)
        texture_analysis = self.analyze_texture(enhanced_image)
        quality_score = self._assess_image_quality(image)
        
        # Combine results
        analysis = {
            'resolution': f"{width}x{height}",
            'aspect_ratio': round(width / height, 2),
            'format': image.format,
            'quality_score': quality_score,
            'color_analysis': color_analysis,
            'texture_analysis': texture_analysis,
            'total_pixels': width * height,
            'enhancement_applied': True
        }
        
        return analysis
    
    def detect_skin_condition_type(self, color_analysis: Dict, texture_analysis: Dict) -> Dict[str, Any]:
        """
        Detect potential skin condition type based on visual analysis
        """
        findings = []
        confidence_scores = {}
        
        redness_score = color_analysis.get('redness_score', 0)
        inflammation = color_analysis.get('inflammation_indicators', {})
        texture_type = texture_analysis.get('texture_type', 'unknown')
        
        # Analyze for different conditions
        if redness_score > 30:
            if inflammation.get('red_dominant_percentage', 0) > 40:
                findings.append({
                    'condition': 'inflammatory_skin_condition',
                    'confidence': 'moderate',
                    'indicators': ['high_redness', 'inflammation_detected']
                })
                confidence_scores['inflammatory'] = min(95, redness_score + 20)
            
            if texture_type == 'rough':
                findings.append({
                    'condition': 'possible_rash_or_eczema',
                    'confidence': 'moderate',
                    'indicators': ['redness', 'rough_texture']
                })
                confidence_scores['rash_eczema'] = 65
        
        if texture_analysis.get('edge_density', 0) > 0.15:
            findings.append({
                'condition': 'irregular_surface_texture',
                'confidence': 'low-moderate',
                'indicators': ['high_edge_density', 'texture_variation']
            })
            confidence_scores['irregular_texture'] = 55
        
        # Check for dark spots (melanoma warning)
        dominant_color = color_analysis.get('dominant_color', [128, 128, 128])
        if all(c < 80 for c in dominant_color) and sum(dominant_color) < 180:
            findings.append({
                'condition': 'dark_pigmentation',
                'confidence': 'low',
                'indicators': ['dark_coloration'],
                'warning': 'URGENT: Dark or irregular moles should be checked by a dermatologist immediately'
            })
            confidence_scores['pigmentation_concern'] = 40
        
        return {
            'findings': findings,
            'confidence_scores': confidence_scores,
            'requires_professional_evaluation': len(findings) > 0
        }
    
    def _assess_image_quality(self, image: Image.Image) -> str:
        """Assess image quality for medical analysis"""
        width, height = image.size
        total_pixels = width * height
        
        if total_pixels >= 1000000:  # 1MP+
            return "excellent"
        elif total_pixels >= 500000:  # 500K+
            return "good"
        elif total_pixels >= 200000:  # 200K+
            return "moderate"
        else:
            return "low"
    
    def analyze_skin_condition(self, image_data: bytes, language: str = 'english') -> Dict:
        """
        Advanced skin condition analysis with comprehensive diagnostics
        Combines color analysis, texture detection, and pattern recognition
        """
        # Validate image with metadata
        is_valid, message, metadata = self.validate_image(image_data, 'image/jpeg')
        if not is_valid:
            return {
                'success': False,
                'error': message,
                'analysis': None
            }
        
        # Preprocess and enhance image
        try:
            original_image, enhanced_image = self.preprocess_image(image_data, enhance=True)
            
            # Perform comprehensive analysis
            comprehensive_analysis = self.analyze_image_comprehensive(original_image, enhanced_image)
            
            # Detect potential conditions
            condition_detection = self.detect_skin_condition_type(
                comprehensive_analysis['color_analysis'],
                comprehensive_analysis['texture_analysis']
            )
            
            # Generate severity assessment
            severity = self._assess_severity(
                comprehensive_analysis['color_analysis'],
                comprehensive_analysis['texture_analysis']
            )
            
            # Generate detailed recommendations
            recommendations = self._get_detailed_recommendations(
                condition_detection,
                severity,
                language
            )
            
            # Build complete analysis report
            analysis = {
                'metadata': metadata,
                'image_quality': comprehensive_analysis['quality_score'],
                'resolution': comprehensive_analysis['resolution'],
                'analysis_timestamp': datetime.now().isoformat(),
                'visual_analysis': {
                    'color_metrics': {
                        'mean_rgb': comprehensive_analysis['color_analysis']['mean_rgb'],
                        'redness_score': comprehensive_analysis['color_analysis']['redness_score'],
                        'dominant_color': comprehensive_analysis['color_analysis']['dominant_color'],
                        'inflammation': comprehensive_analysis['color_analysis']['inflammation_indicators']
                    },
                    'texture_metrics': {
                        'smoothness': comprehensive_analysis['texture_analysis']['smoothness'],
                        'texture_type': comprehensive_analysis['texture_analysis']['texture_type'],
                        'edge_density': comprehensive_analysis['texture_analysis']['edge_density'],
                        'entropy': comprehensive_analysis['texture_analysis']['entropy']
                    }
                },
                'condition_detection': condition_detection,
                'severity_assessment': severity,
                'recommendations': recommendations,
                'confidence_level': self._calculate_overall_confidence(condition_detection),
                'disclaimer': self._get_disclaimer(language),
                'next_steps': self._get_next_steps(severity, language)
            }
            
            # Store in history for tracking
            self.analysis_history.append({
                'timestamp': datetime.now().isoformat(),
                'image_hash': metadata['image_hash'],
                'findings': condition_detection['findings'],
                'severity': severity
            })
            
            return {
                'success': True,
                'error': None,
                'analysis': analysis
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error processing image: {str(e)}",
                'analysis': None
            }
    
    def _assess_severity(self, color_analysis: Dict, texture_analysis: Dict) -> Dict[str, Any]:
        """
        Assess severity level based on multiple factors
        """
        redness_score = color_analysis.get('redness_score', 0)
        inflammation = color_analysis.get('inflammation_indicators', {})
        red_percentage = inflammation.get('red_dominant_percentage', 0)
        
        # Calculate composite severity score
        severity_score = 0
        
        # Redness contribution
        if redness_score > 60:
            severity_score += 3
        elif redness_score > 40:
            severity_score += 2
        elif redness_score > 20:
            severity_score += 1
        
        # Inflammation contribution
        if red_percentage > 50:
            severity_score += 3
        elif red_percentage > 30:
            severity_score += 2
        elif red_percentage > 15:
            severity_score += 1
        
        # Texture contribution
        if texture_analysis.get('edge_density', 0) > 0.2:
            severity_score += 1
        
        # Determine severity level
        if severity_score >= 6:
            level = 'severe'
            urgency = 'high'
        elif severity_score >= 4:
            level = 'moderate'
            urgency = 'medium'
        elif severity_score >= 2:
            level = 'mild'
            urgency = 'low'
        else:
            level = 'minimal'
            urgency = 'routine'
        
        return {
            'level': level,
            'urgency': urgency,
            'score': severity_score,
            'max_score': 7,
            'description': self._get_severity_description(level, urgency)
        }
    
    def _get_severity_description(self, level: str, urgency: str) -> str:
        """Get human-readable severity description"""
        descriptions = {
            'severe': 'Significant visible changes detected. Immediate medical attention recommended.',
            'moderate': 'Noticeable skin changes detected. Medical consultation recommended within 1-2 days.',
            'mild': 'Minor skin changes detected. Monitor and consult doctor if worsens.',
            'minimal': 'Minimal changes detected. Continue monitoring.'
        }
        return descriptions.get(level, 'Assessment completed.')
    
    def _calculate_overall_confidence(self, condition_detection: Dict) -> str:
        """Calculate overall confidence in analysis"""
        findings = condition_detection.get('findings', [])
        
        if not findings:
            return 'low - no specific conditions detected'
        
        confidence_scores = condition_detection.get('confidence_scores', {})
        if confidence_scores:
            avg_confidence = sum(confidence_scores.values()) / len(confidence_scores)
            if avg_confidence > 70:
                return 'moderate-high (visual analysis only)'
            elif avg_confidence > 50:
                return 'moderate (visual analysis only)'
            else:
                return 'low-moderate (visual analysis only)'
        
        return 'moderate (preliminary analysis)'
    
    def _get_detailed_recommendations(self, condition_detection: Dict, severity: Dict, language: str) -> List[str]:
        """
        Generate detailed, context-aware recommendations
        """
        findings = condition_detection.get('findings', [])
        severity_level = severity.get('level', 'minimal')
        
        recommendations = []
        
        # Language-specific recommendations
        if language == 'hindi':
            recommendations.append("🔬 ANALYSIS RESULTS:")
            recommendations.append("")
            
            if not findings:
                recommendations.append("✅ Koi specific concern detect nahi hua")
                recommendations.append("📋 General skin care follow karein")
            else:
                recommendations.append(f"⚠️ Severity Level: {severity_level.upper()}")
                recommendations.append(f"📊 {len(findings)} potential concern(s) detected")
                recommendations.append("")
                
                for i, finding in enumerate(findings, 1):
                    condition = finding.get('condition', 'unknown').replace('_', ' ').title()
                    recommendations.append(f"{i}. {condition}")
                    if 'warning' in finding:
                        recommendations.append(f"   ⚠️ {finding['warning']}")
                
                recommendations.append("")
            
            # Severity-based recommendations
            if severity_level == 'severe':
                recommendations.extend([
                    "🚨 URGENT ACTION REQUIRED:",
                    "• Immediately doctor se milein",
                    "• Emergency mein hospital jaayein",
                    "• Self-medication avoid karein",
                    ""
                ])
            elif severity_level == 'moderate':
                recommendations.extend([
                    "⚠️ RECOMMENDED ACTIONS:",
                    "• 1-2 din mein dermatologist ko dikhayein",
                    "• Affected area ko clean aur dry rakhein",
                    "• Doctor ki advice bina medicine na lein",
                    ""
                ])
            else:
                recommendations.extend([
                    "📋 GENERAL CARE:",
                    "• Area ko saaf aur sukha rakhein",
                    "• Kharab kapde avoid karein",
                    "• Agar condition worsen ho toh doctor se milein",
                    ""
                ])
        
        else:  # English
            recommendations.append("🔬 ANALYSIS RESULTS:")
            recommendations.append("")
            
            if not findings:
                recommendations.append("✅ No specific concerns detected")
                recommendations.append("📋 Continue with general skin care")
            else:
                recommendations.append(f"⚠️ Severity Level: {severity_level.upper()}")
                recommendations.append(f"📊 {len(findings)} potential concern(s) detected")
                recommendations.append("")
                
                for i, finding in enumerate(findings, 1):
                    condition = finding.get('condition', 'unknown').replace('_', ' ').title()
                    confidence = finding.get('confidence', 'unknown')
                    recommendations.append(f"{i}. {condition} (Confidence: {confidence})")
                    if 'warning' in finding:
                        recommendations.append(f"   ⚠️ {finding['warning']}")
                
                recommendations.append("")
            
            # Severity-based recommendations
            if severity_level == 'severe':
                recommendations.extend([
                    "🚨 URGENT ACTION REQUIRED:",
                    "• Seek immediate medical attention",
                    "• Visit emergency if symptoms worsen",
                    "• Avoid self-medication",
                    ""
                ])
            elif severity_level == 'moderate':
                recommendations.extend([
                    "⚠️ RECOMMENDED ACTIONS:",
                    "• Consult a dermatologist within 1-2 days",
                    "• Keep the affected area clean and dry",
                    "• Avoid applying anything without medical advice",
                    ""
                ])
            else:
                recommendations.extend([
                    "📋 GENERAL CARE:",
                    "• Keep area clean and dry",
                    "• Avoid tight or irritating clothing",
                    "• Monitor for changes and consult if worsens",
                    ""
                ])
        
        return recommendations
    
    def _get_next_steps(self, severity: Dict, language: str) -> List[str]:
        """Get actionable next steps based on severity"""
        urgency = severity.get('urgency', 'routine')
        
        if language == 'hindi':
            if urgency == 'high':
                return [
                    "1. Turant doctor se appointment lein",
                    "2. In results ko doctor ko dikhayein",
                    "3. Koi bhi changes monitor karein",
                    "4. Emergency mein 102 ya nearest hospital jaayein"
                ]
            elif urgency == 'medium':
                return [
                    "1. 24-48 ghante mein dermatologist se appointment lein",
                    "2. Image aur analysis report save karein",
                    "3. Daily changes track karein",
                    "4. Agar worsen ho toh immediately help lein"
                ]
            else:
                return [
                    "1. General skin care routine follow karein",
                    "2. Changes monitor karein",
                    "3. Agar 3-4 din mein theek na ho toh doctor se milein",
                    "4. Affected area ko protect karein"
                ]
        else:
            if urgency == 'high':
                return [
                    "1. Schedule immediate doctor appointment",
                    "2. Show these results to your doctor",
                    "3. Monitor for any changes",
                    "4. Go to emergency if symptoms worsen"
                ]
            elif urgency == 'medium':
                return [
                    "1. Schedule dermatologist appointment within 24-48 hours",
                    "2. Save this image and analysis report",
                    "3. Track daily changes",
                    "4. Seek immediate help if condition worsens"
                ]
            else:
                return [
                    "1. Continue general skin care routine",
                    "2. Monitor for changes",
                    "3. Consult doctor if no improvement in 3-4 days",
                    "4. Protect the affected area"
                ]
    
    
    def compare_with_history(self, current_image_hash: str) -> Optional[Dict]:
        """
        Compare current analysis with previous analyses for progress tracking
        """
        if len(self.analysis_history) < 2:
            return None
        
        # Find previous analysis
        previous = None
        for i in range(len(self.analysis_history) - 2, -1, -1):
            if self.analysis_history[i]['image_hash'] != current_image_hash:
                previous = self.analysis_history[i]
                break
        
        if not previous:
            return None
        
        current = self.analysis_history[-1]
        
        # Compare severity
        prev_severity = previous.get('severity', {}).get('score', 0)
        curr_severity = current.get('severity', {}).get('score', 0)
        
        change = curr_severity - prev_severity
        
        if change > 1:
            trend = 'worsening'
        elif change < -1:
            trend = 'improving'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'severity_change': change,
            'previous_date': previous['timestamp'],
            'current_date': current['timestamp'],
            'recommendation': self._get_trend_recommendation(trend)
        }
    
    def _get_trend_recommendation(self, trend: str) -> str:
        """Get recommendation based on condition trend"""
        if trend == 'worsening':
            return "Condition appears to be worsening. Seek medical attention immediately."
        elif trend == 'improving':
            return "Condition shows signs of improvement. Continue current treatment."
        else:
            return "Condition appears stable. Continue monitoring."
    
    def generate_analysis_report(self, analysis: Dict, language: str = 'english') -> str:
        """
        Generate a formatted text report of the analysis
        """
        if not analysis:
            return "No analysis available"
        
        report_lines = []
        
        if language == 'hindi':
            report_lines.extend([
                "=" * 50,
                "📊 MEDICAL IMAGE ANALYSIS REPORT",
                "=" * 50,
                "",
                f"⏰ Analysis Time: {analysis.get('analysis_timestamp', 'N/A')}",
                f"📏 Resolution: {analysis.get('resolution', 'N/A')}",
                f"✅ Quality: {analysis.get('image_quality', 'N/A')}",
                ""
            ])
        else:
            report_lines.extend([
                "=" * 50,
                "📊 MEDICAL IMAGE ANALYSIS REPORT",
                "=" * 50,
                "",
                f"⏰ Analysis Time: {analysis.get('analysis_timestamp', 'N/A')}",
                f"📏 Resolution: {analysis.get('resolution', 'N/A')}",
                f"✅ Quality: {analysis.get('image_quality', 'N/A')}",
                ""
            ])
        
        # Add visual analysis
        if 'visual_analysis' in analysis:
            visual = analysis['visual_analysis']
            report_lines.extend([
                "🔬 VISUAL ANALYSIS:",
                "",
                "Color Metrics:",
                f"  • Redness Score: {visual['color_metrics'].get('redness_score', 0):.1f}/100",
                f"  • Dominant Color: RGB{tuple(visual['color_metrics'].get('dominant_color', [0,0,0]))}",
                "",
                "Texture Metrics:",
                f"  • Texture Type: {visual['texture_metrics'].get('texture_type', 'unknown')}",
                f"  • Smoothness: {visual['texture_metrics'].get('smoothness', 0):.2f}",
                f"  • Edge Density: {visual['texture_metrics'].get('edge_density', 0):.3f}",
                ""
            ])
        
        # Add condition detection
        if 'condition_detection' in analysis:
            findings = analysis['condition_detection'].get('findings', [])
            report_lines.append("🩺 FINDINGS:")
            report_lines.append("")
            if findings:
                for i, finding in enumerate(findings, 1):
                    condition = finding.get('condition', 'unknown').replace('_', ' ').title()
                    confidence = finding.get('confidence', 'unknown')
                    report_lines.append(f"  {i}. {condition}")
                    report_lines.append(f"     Confidence: {confidence}")
                    if 'warning' in finding:
                        report_lines.append(f"     ⚠️  {finding['warning']}")
                    report_lines.append("")
            else:
                report_lines.append("  No specific conditions detected")
                report_lines.append("")
        
        # Add severity
        if 'severity_assessment' in analysis:
            severity = analysis['severity_assessment']
            report_lines.extend([
                "📊 SEVERITY ASSESSMENT:",
                f"  • Level: {severity.get('level', 'unknown').upper()}",
                f"  • Urgency: {severity.get('urgency', 'unknown').upper()}",
                f"  • Score: {severity.get('score', 0)}/{severity.get('max_score', 7)}",
                f"  • {severity.get('description', '')}",
                ""
            ])
        
        # Add recommendations
        if 'recommendations' in analysis:
            report_lines.extend(analysis['recommendations'])
        
        # Add next steps
        if 'next_steps' in analysis:
            report_lines.append("")
            report_lines.append("📝 NEXT STEPS:")
            for step in analysis['next_steps']:
                report_lines.append(f"  {step}")
            report_lines.append("")
        
        # Add disclaimer
        if 'disclaimer' in analysis:
            report_lines.append("")
            report_lines.append(analysis['disclaimer'])
        
        report_lines.extend([
            "",
            "=" * 50,
            "End of Report",
            "=" * 50
        ])
        
        return "\n".join(report_lines)
    
    def _get_general_skin_recommendations(self, language: str) -> List[str]:
        """Get general recommendations for skin issues"""
        recommendations = {
            'hindi': [
                "🔍 Image received. Yahan kuch general guidance hai:",
                "",
                "📋 Basic skin care tips:",
                "• Affected area ko saaf aur sukha rakhein",
                "• Kharaab ya tight kapde avoid karein",
                "• Affected area ko zyada chhuyen nahi",
                "• Hydrated rahein - pani zyada piyein",
                "",
                "⚠️ Doctor se kab milein:",
                "• Agar condition 3-4 din mein behtar na ho",
                "• Agar dard, swelling, ya pus ho",
                "• Agar fever ya infection ke lakshan hon",
                "• Agar condition spread ho rahi ho",
                "",
                "🏥 Professional diagnosis ke liye dermatologist se zaroor milein."
            ],
            'english': [
                "🔍 Image received. Here's some general guidance:",
                "",
                "📋 Basic skin care tips:",
                "• Keep the affected area clean and dry",
                "• Avoid tight or irritating clothing",
                "• Don't scratch or touch the area excessively",
                "• Stay hydrated - drink plenty of water",
                "",
                "⚠️ When to see a doctor:",
                "• If condition doesn't improve in 3-4 days",
                "• If there's pain, swelling, or pus",
                "• If you develop fever or signs of infection",
                "• If the condition is spreading",
                "",
                "🏥 For professional diagnosis, please consult a dermatologist."
            ]
        }
        
        return recommendations.get(language, recommendations['english'])
    
    def _get_disclaimer(self, language: str) -> str:
        """Get medical disclaimer for image analysis"""
        disclaimers = {
            'hindi': """
⚠️ IMPORTANT DISCLAIMER:
Yeh automated image analysis hai aur professional medical diagnosis ka replacement NAHI hai. 
Accurate diagnosis ke liye qualified dermatologist ya doctor se milein.
Emergency mein turant medical help lein.
""",
            'english': """
⚠️ IMPORTANT DISCLAIMER:
This is an automated image analysis and is NOT a replacement for professional medical diagnosis.
Please consult a qualified dermatologist or doctor for accurate diagnosis.
Seek immediate medical help in case of emergency.
"""
        }
        
        return disclaimers.get(language, disclaimers['english'])
    
    def get_image_analysis_instructions(self, language: str) -> str:
        """Get instructions for sending medical images"""
        instructions = {
            'hindi': """
📸 IMAGE ANALYSIS INSTRUCTIONS:

Image bhejne se pehle:
1. ✅ Affected area ka clear photo lein
2. ✅ Achhe lighting mein photo lein
3. ✅ Photo focus mein hona chahiye
4. ✅ Area ko close-up se dikhayein
5. ✅ Multiple angles se photo helpful hai

Supported formats: JPG, PNG, WEBP
Maximum size: 10MB

Privacy: Aapki images secure aur confidential hain.

Image bhejne ke baad main basic guidance provide karunga.
But professional diagnosis ke liye doctor ko zaroor dikhaayein.
""",
            'english': """
📸 IMAGE ANALYSIS INSTRUCTIONS:

Before sending image:
1. ✅ Take a clear photo of the affected area
2. ✅ Ensure good lighting
3. ✅ Photo should be in focus
4. ✅ Show the area in close-up
5. ✅ Multiple angles are helpful

Supported formats: JPG, PNG, WEBP
Maximum size: 10MB

Privacy: Your images are secure and confidential.

After sending the image, I'll provide basic guidance.
However, please consult a doctor for professional diagnosis.
"""
        }
        
        return instructions.get(language, instructions['english'])
    
    def detect_image_request(self, text: str) -> bool:
        """Detect if user wants to send an image"""
        image_keywords = [
            'photo', 'picture', 'image', 'pic', 'photo bhejo', 'image send',
            'tasveer', 'photo dikhao', 'dekhna hai', 'rash dikha', 'skin dikha',
            'फोटो', 'तस्वीर', 'चित्र', 'ছবি', 'புகைப்படம்', 'ఫోటో', 'ਫੋਟੋ', 'ફોટો'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in image_keywords)
    
    def get_common_skin_conditions_info(self, language: str) -> str:
        """Provide information about common skin conditions"""
        info = {
            'hindi': """
📚 COMMON SKIN CONDITIONS:

1. 🔴 Rash (Daad/Kharish)
   - Red, itchy patches
   - Causes: Allergy, infection, heat

2. 🔴 Acne (Muhanse)
   - Pimples, blackheads
   - Common in teenagers

3. 🔴 Eczema (Khujli wali skin)
   - Dry, scaly, itchy skin
   - Chronic condition

4. 🔴 Fungal Infection (Fungal daad)
   - Circular, ring-like patches
   - Spreads easily

5. 🔴 Psoriasis
   - Thick, scaly patches
   - Chronic condition

6. 🔴 Burns
   - Heat, chemical, sun burns
   - Severity varies

Photo bhej kar main basic guidance de sakta hoon.
Lekin doctor se consultation zaroor karein.
""",
            'english': """
📚 COMMON SKIN CONDITIONS:

1. 🔴 Rash
   - Red, itchy patches
   - Causes: Allergy, infection, heat

2. 🔴 Acne
   - Pimples, blackheads
   - Common in teenagers

3. 🔴 Eczema
   - Dry, scaly, itchy skin
   - Chronic condition

4. 🔴 Fungal Infection
   - Circular, ring-like patches
   - Spreads easily

5. 🔴 Psoriasis
   - Thick, scaly patches
   - Chronic condition

6. 🔴 Burns
   - Heat, chemical, sun burns
   - Severity varies

You can send a photo for basic guidance.
However, please consult a doctor for proper diagnosis.
"""
        }
        
        return info.get(language, info['english'])


# Helper function for easy integration
def create_image_analyzer() -> ImageAnalyzer:
    """Factory function to create ImageAnalyzer instance"""
    return ImageAnalyzer()
