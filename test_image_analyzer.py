# -*- coding: utf-8 -*-
"""
Test script to verify image analyzer is working correctly
"""

import os
import sys

print("=" * 60)
print("Testing Image Analyzer Dependencies and Functionality")
print("=" * 60)

# Test 1: Check imports
print("\n1. Checking imports...")
try:
    from PIL import Image
    print("   ✅ PIL (Pillow) imported successfully")
except ImportError as e:
    print(f"   ❌ PIL import failed: {e}")
    sys.exit(1)

try:
    import numpy as np
    print("   ✅ NumPy imported successfully")
except ImportError as e:
    print(f"   ❌ NumPy import failed: {e}")
    sys.exit(1)

try:
    from src.image_analyzer import ImageAnalyzer
    print("   ✅ ImageAnalyzer imported successfully")
except ImportError as e:
    print(f"   ❌ ImageAnalyzer import failed: {e}")
    sys.exit(1)

# Test 2: Create analyzer instance
print("\n2. Creating ImageAnalyzer instance...")
try:
    analyzer = ImageAnalyzer()
    print("   ✅ ImageAnalyzer instance created successfully")
except Exception as e:
    print(f"   ❌ Failed to create ImageAnalyzer: {e}")
    sys.exit(1)

# Test 3: Create a simple test image
print("\n3. Creating test image...")
try:
    # Create a simple 200x200 red image (simulating redness/inflammation)
    test_img = Image.new('RGB', (200, 200), color=(255, 100, 100))
    
    # Save to bytes
    import io
    img_byte_arr = io.BytesIO()
    test_img.save(img_byte_arr, format='JPEG')
    image_data = img_byte_arr.getvalue()
    
    print(f"   ✅ Test image created ({len(image_data)} bytes)")
except Exception as e:
    print(f"   ❌ Failed to create test image: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Validate image
print("\n4. Testing image validation...")
try:
    is_valid, message, metadata = analyzer.validate_image(image_data, 'image/jpeg')
    if is_valid:
        print(f"   ✅ Image validation passed: {message}")
        print(f"   📊 Metadata: {metadata}")
    else:
        print(f"   ❌ Image validation failed: {message}")
except Exception as e:
    print(f"   ❌ Validation error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Analyze skin condition
print("\n5. Testing skin condition analysis...")
try:
    result = analyzer.analyze_skin_condition(image_data, language='english')
    
    if result['success']:
        print("   ✅ Analysis successful!")
        analysis = result['analysis']
        print(f"   📊 Image quality: {analysis.get('image_quality', 'N/A')}")
        print(f"   🔍 Findings: {len(analysis['condition_detection']['findings'])} potential concerns")
        print(f"   ⚠️ Severity: {analysis['severity_assessment'].get('level', 'N/A')}")
        print(f"   📋 Recommendations: {len(analysis['recommendations'])} items")
    else:
        print(f"   ❌ Analysis failed: {result['error']}")
except Exception as e:
    print(f"   ❌ Analysis error: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Test with Hindi language
print("\n6. Testing with Hindi language...")
try:
    result = analyzer.analyze_skin_condition(image_data, language='hindi')
    
    if result['success']:
        print("   ✅ Hindi analysis successful!")
    else:
        print(f"   ❌ Hindi analysis failed: {result['error']}")
except Exception as e:
    print(f"   ❌ Hindi analysis error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
