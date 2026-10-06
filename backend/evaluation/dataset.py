# backend/evaluation/dataset.py

EVALUATION_DATASET = [

    {
        "id": "RET-001",
        "question": "What is the return window for electronics?",
        "expected_answer": (
            "Electronics can be returned within 15 calendar days, "
            "provided they are unused or have a confirmed functional defect."
        ),
        "expected_document": "refund_policy.pdf",
        "expected_document_id": "RET-002",
    },

    {
        "id": "RET-002",
        "question": (
            "How long are refunds normally processed after a return "
            "is accepted?"
        ),
        "expected_answer": (
            "Approved refunds are normally processed within 5-7 business "
            "days after the return is accepted."
        ),
        "expected_document": "refund_policy.pdf",
        "expected_document_id": "RET-002",
    },

    {
        "id": "RET-003",
        "question": "What is the return window for furniture?",
        "expected_answer": (
            "Furniture has a 10 calendar day return window, "
            "and the product should be in its original condition."
        ),
        "expected_document": "refund_policy.pdf",
        "expected_document_id": "RET-002",
    },

    {
        "id": "RET-004",
        "question": "Can a damaged or defective item be replaced?",
        "expected_answer": (
            "Replacement may be offered when an item is damaged, "
            "defective, or incorrectly shipped."
        ),
        "expected_document": "refund_policy.pdf",
        "expected_document_id": "RET-002",
    },

    {
        "id": "WAR-001",
        "question": "What is the standard warranty period for laptops?",
        "expected_answer": (
            "Laptops have a standard warranty period of 2 years "
            "covering manufacturing defects and covered hardware failures."
        ),
        "expected_document": "warranty_policy.pdf",
        "expected_document_id": "WAR-004",
    },

    {
        "id": "WAR-002",
        "question": "What is the warranty period for accessories?",
        "expected_answer": (
            "Accessories have a standard warranty period of 1 year "
            "for manufacturing defects."
        ),
        "expected_document": "warranty_policy.pdf",
        "expected_document_id": "WAR-004",
    },

    {
        "id": "WAR-003",
        "question": "What can exclude warranty coverage?",
        "expected_answer": (
            "Damage caused by misuse, unauthorized modification, "
            "or accidental impact may be excluded from warranty coverage."
        ),
        "expected_document": "warranty_policy.pdf",
        "expected_document_id": "WAR-004",
    },

    {
        "id": "SAL-001",
        "question": (
            "What information should sales recommendations not fabricate?"
        ),
        "expected_answer": (
            "Sales recommendations should not fabricate stock levels, "
            "discounts, delivery dates, or customer history."
        ),
        "expected_document": "sales_guidelines.pdf",
        "expected_document_id": "SAL-005",
    },

    {
        "id": "EMP-001",
        "question": (
            "How many days per week can employees work remotely "
            "with manager approval?"
        ),
        "expected_answer": (
            "Employees can work remotely up to 2 days per week "
            "with manager approval."
        ),
        "expected_document": "employee_handbook.pdf",
        "expected_document_id": "EMP-006",
    },

    {
        "id": "EMP-002",
        "question": (
            "How should AI-generated output be treated when a human "
            "approval step is required?"
        ),
        "expected_answer": (
            "AI-generated output should be treated as a draft "
            "when a human approval step is required."
        ),
        "expected_document": "employee_handbook.pdf",
        "expected_document_id": "EMP-006",
    },
]