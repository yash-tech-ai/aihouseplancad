"""
Comprehensive System Test Suite
Tests all major components and integration
"""
import requests
import json
import time
from pathlib import Path

BASE_URL = 'http://localhost:5000/api'

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}Testing: {name}{Colors.END}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ {message}{Colors.END}")

def test_health_check():
    """Test API health check"""
    print_test("Health Check")

    try:
        response = requests.get(f'{BASE_URL}/health')
        assert response.status_code == 200, "Health check failed"

        data = response.json()
        assert data['status'] == 'healthy', "Service not healthy"

        print_success("Health check passed")
        print_info(f"   Version: {data.get('version', 'N/A')}")
        print_info(f"   Features: {len(data.get('features', {}))} available")
        return True
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

def test_floor_plan_generation():
    """Test AI floor plan generation"""
    print_test("AI Floor Plan Generation")

    try:
        payload = {
            'totalSqFt': 2000,
            'bedrooms': 3,
            'bathrooms': 2.5,
            'style': 'modern',
            'specialRooms': {
                'office': True,
                'garage': True,
                'garage_cars': 2
            }
        }

        print_info("Generating floor plan...")
        response = requests.post(
            f'{BASE_URL}/generate',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )

        assert response.status_code == 200, f"Generation failed: {response.status_code}"

        data = response.json()
        assert data['success'], "Generation not successful"
        assert 'floorPlan' in data, "No floor plan in response"

        floor_plan = data['floorPlan']
        print_success(f"Generated floor plan with {floor_plan['stats']['room_count']} rooms")
        print_info(f"   Total area: {floor_plan['stats']['total_area']:.0f} sq ft")
        print_info(f"   Efficiency: {floor_plan['stats']['efficiency_ratio']:.1f}%")

        # Check validation
        if 'validation' in data:
            validation = data['validation']
            print_info(f"   Compliance: {validation['grade']} ({validation['compliance_score']}/100)")

        return floor_plan
    except Exception as e:
        print_error(f"Generation failed: {str(e)}")
        return None

def test_validation(floor_plan):
    """Test building code validation"""
    print_test("Building Code Validation")

    if not floor_plan:
        print_error("Skipping - no floor plan provided")
        return False

    try:
        response = requests.post(
            f'{BASE_URL}/validate',
            json=floor_plan,
            headers={'Content-Type': 'application/json'}
        )

        assert response.status_code == 200, "Validation request failed"

        data = response.json()
        assert data['success'], "Validation not successful"

        validation = data['validation']
        print_success(f"Validation completed")
        print_info(f"   Grade: {validation['grade']}")
        print_info(f"   Critical violations: {validation['summary']['critical']}")
        print_info(f"   Warnings: {validation['summary']['warnings']}")

        if validation['summary']['critical'] == 0:
            print_success("   No critical violations!")

        return True
    except Exception as e:
        print_error(f"Validation failed: {str(e)}")
        return False

def test_dxf_export(floor_plan):
    """Test DXF export"""
    print_test("DXF Export")

    if not floor_plan:
        print_error("Skipping - no floor plan provided")
        return False

    try:
        response = requests.post(
            f'{BASE_URL}/export/dxf',
            json=floor_plan,
            headers={'Content-Type': 'application/json'}
        )

        assert response.status_code == 200, "DXF export failed"
        assert response.headers['Content-Type'] == 'application/dxf', "Wrong content type"

        file_size = len(response.content)
        print_success(f"DXF file generated ({file_size:,} bytes)")

        # Save file
        output_path = Path('test_output.dxf')
        with open(output_path, 'wb') as f:
            f.write(response.content)

        print_info(f"   Saved to: {output_path.absolute()}")
        return True
    except Exception as e:
        print_error(f"DXF export failed: {str(e)}")
        return False

def test_svg_export(floor_plan):
    """Test SVG export"""
    print_test("SVG Export")

    if not floor_plan:
        print_error("Skipping - no floor plan provided")
        return False

    try:
        response = requests.post(
            f'{BASE_URL}/export/svg',
            json=floor_plan,
            headers={'Content-Type': 'application/json'}
        )

        assert response.status_code == 200, "SVG export failed"

        svg_content = response.text
        assert '<svg' in svg_content, "Invalid SVG content"

        print_success(f"SVG generated ({len(svg_content):,} characters)")

        # Save file
        output_path = Path('test_output.svg')
        with open(output_path, 'w') as f:
            f.write(svg_content)

        print_info(f"   Saved to: {output_path.absolute()}")
        return True
    except Exception as e:
        print_error(f"SVG export failed: {str(e)}")
        return False

def test_analysis(floor_plan):
    """Test comprehensive analysis"""
    print_test("Comprehensive Analysis")

    if not floor_plan:
        print_error("Skipping - no floor plan provided")
        return False

    try:
        response = requests.post(
            f'{BASE_URL}/analyze',
            json=floor_plan,
            headers={'Content-Type': 'application/json'}
        )

        assert response.status_code == 200, "Analysis failed"

        data = response.json()
        assert data['success'], "Analysis not successful"

        print_success("Analysis completed")

        if 'energyEfficiency' in data:
            energy = data['energyEfficiency']
            print_info(f"   Energy Grade: {energy['grade']} ({energy['score']:.1f}/100)")

        if 'recommendations' in data:
            rec_count = len(data['recommendations'])
            print_info(f"   Recommendations: {rec_count}")

        return True
    except Exception as e:
        print_error(f"Analysis failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}AI FLOOR PLAN GENERATOR - SYSTEM TEST SUITE{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

    print_info("Starting tests...")
    print_info(f"Target API: {BASE_URL}")

    results = {}
    floor_plan = None

    # Test 1: Health Check
    results['health'] = test_health_check()

    if results['health']:
        # Test 2: Generation
        floor_plan = test_floor_plan_generation()
        results['generation'] = floor_plan is not None

        # Test 3: Validation
        results['validation'] = test_validation(floor_plan)

        # Test 4: DXF Export
        results['dxf_export'] = test_dxf_export(floor_plan)

        # Test 5: SVG Export
        results['svg_export'] = test_svg_export(floor_plan)

        # Test 6: Analysis
        results['analysis'] = test_analysis(floor_plan)
    else:
        print_error("Health check failed - skipping remaining tests")

    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}TEST SUMMARY{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASSED{Colors.END}" if result else f"{Colors.RED}FAILED{Colors.END}"
        print(f"  {test_name.replace('_', ' ').title()}: {status}")

    print(f"\n{Colors.BLUE}Results: {passed}/{total} tests passed{Colors.END}")

    if passed == total:
        print(f"\n{Colors.GREEN}✓ ALL TESTS PASSED! System is working correctly.{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.RED}✗ Some tests failed. Please review the errors above.{Colors.END}\n")
        return 1

if __name__ == '__main__':
    import sys

    print("\nWaiting for server to start...")
    time.sleep(2)

    try:
        sys.exit(run_all_tests())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Test suite failed: {str(e)}{Colors.END}\n")
        sys.exit(1)
