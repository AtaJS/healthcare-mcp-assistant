"""
Healthcare data for MCP tools.
Each dictionary represents a different data source that will become an MCP tool.
"""

# Tool 1: FAQ Database
FAQ_DATA = {
    "what are your hours": "Monday-Friday 8AM-6PM, Saturday 9AM-2PM. Closed Sundays.",
    "hours": "Monday-Friday 8AM-6PM, Saturday 9AM-2PM. Closed Sundays.",
    "do you accept insurance": "Yes, we accept Blue Cross Blue Shield, Aetna, UnitedHealthcare, and Cigna.",
    "insurance": "Yes, we accept Blue Cross Blue Shield, Aetna, UnitedHealthcare, and Cigna.",
    "where are you located": "123 Medical Plaza, Boston MA 02101",
    "location": "123 Medical Plaza, Boston MA 02101",
    "address": "123 Medical Plaza, Boston MA 02101",
    "how do i schedule": "Call us at 555-1234 or use the patient portal at portal.healthcareplus.com",
    "schedule": "Call us at 555-1234 or use the patient portal at portal.healthcareplus.com",
    "appointment": "Call us at 555-1234 or use the patient portal at portal.healthcareplus.com",
    "covid test": "Yes, rapid COVID tests are available Monday-Friday without appointment.",
    "covid": "Yes, rapid COVID tests are available Monday-Friday without appointment.",
    "cancellation policy": "Please cancel at least 24 hours in advance to avoid a $50 fee.",
    "cancel": "Please cancel at least 24 hours in advance to avoid a $50 fee.",
    "parking": "Free parking is available in Lot B behind the main building.",
    "telehealth": "Yes, telehealth appointments are available for follow-ups and consultations.",
    "lab services": "We offer blood work, X-rays, and ultrasound services on-site.",
    "labs": "We offer blood work, X-rays, and ultrasound services on-site.",
    "children": "We treat patients ages 12 and older.",
    "kids": "We treat patients ages 12 and older.",
    "age": "We treat patients ages 12 and older."
}

# Tool 2: Appointment Lookup
APPOINTMENTS = {
    "APT-101": {
        "patient": "John Doe",
        "doctor": "Dr. Smith",
        "date": "December 10, 2025",
        "time": "10:00 AM",
        "status": "confirmed",
        "reason": "Annual checkup"
    },
    "APT-102": {
        "patient": "Jane Doe",
        "doctor": "Dr. Johnson",
        "date": "December 12, 2025",
        "time": "2:00 PM",
        "status": "pending confirmation",
        "reason": "Follow-up consultation"
    },
    "APT-103": {
        "patient": "Bob Wilson",
        "doctor": "Dr. Lee",
        "date": "December 15, 2025",
        "time": "9:00 AM",
        "status": "confirmed",
        "reason": "Flu symptoms"
    },
    "APT-104": {
        "patient": "Alice Brown",
        "doctor": "Dr. Smith",
        "date": "December 18, 2025",
        "time": "11:00 AM",
        "status": "cancelled",
        "reason": "Annual physical"
    },
    "APT-105": {
        "patient": "Charlie Davis",
        "doctor": "Dr. Johnson",
        "date": "December 20, 2025",
        "time": "3:00 PM",
        "status": "confirmed",
        "reason": "Blood pressure check"
    }
}

# Tool 3: Lab Results Lookup
LAB_RESULTS = {
    "LAB-201": {
        "patient": "John Doe",
        "test_type": "Complete Blood Panel",
        "ordered_date": "December 1, 2025",
        "status": "ready",
        "urgent": False,
        "result_summary": "All values within normal range"
    },
    "LAB-202": {
        "patient": "Jane Doe",
        "test_type": "Chest X-Ray",
        "ordered_date": "December 3, 2025",
        "status": "ready",
        "urgent": True,
        "result_summary": "Abnormal findings - doctor will contact you"
    },
    "LAB-203": {
        "patient": "Bob Wilson",
        "test_type": "COVID-19 PCR Test",
        "ordered_date": "December 5, 2025",
        "status": "processing",
        "urgent": False,
        "result_summary": "Results expected within 24 hours"
    },
    "LAB-204": {
        "patient": "Alice Brown",
        "test_type": "Abdominal Ultrasound",
        "ordered_date": "November 28, 2025",
        "status": "ready",
        "urgent": False,
        "result_summary": "No abnormalities detected"
    },
    "LAB-205": {
        "patient": "Charlie Davis",
        "test_type": "Lipid Panel",
        "ordered_date": "December 6, 2025",
        "status": "processing",
        "urgent": False,
        "result_summary": "Results expected by December 9"
    }
}

# Tool 4: Doctor Directory
DOCTORS = {
    "Dr. Smith": {
        "full_name": "Dr. Sarah Smith",
        "specialty": "Family Medicine",
        "available_days": ["Monday", "Wednesday", "Friday"],
        "accepting_new_patients": True,
        "languages": ["English", "Spanish"],
        "years_experience": 15
    },
    "Dr. Johnson": {
        "full_name": "Dr. Michael Johnson",
        "specialty": "Internal Medicine",
        "available_days": ["Tuesday", "Thursday"],
        "accepting_new_patients": False,
        "languages": ["English"],
        "years_experience": 22
    },
    "Dr. Lee": {
        "full_name": "Dr. Emily Lee",
        "specialty": "Pediatrics",
        "available_days": ["Monday", "Tuesday", "Wednesday"],
        "accepting_new_patients": True,
        "languages": ["English", "Chinese", "French"],
        "years_experience": 8
    }
}