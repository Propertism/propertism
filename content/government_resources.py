"""Tamil Nadu government property services resources configuration."""

GOVERNMENT_RESOURCE_CATEGORIES = [
    {
        "id": "land-records",
        "title": "Land Records & Ownership Verification",
        "description": "Official services to verify land ownership, view extracts, A-Register, and maps.",
        "services": [
            {
                "id": "verify-patta-chitta",
                "title": "Verify Patta/Chitta",
                "description": "Verify the authenticity of Patta/Chitta land record extracts online.",
                "url": "https://eservices.tn.gov.in/eservices_html/index.html",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "verify"
            },
            {
                "id": "view-patta-chitta-extract",
                "title": "View Patta/Chitta Extract",
                "description": "View and print Patta/Chitta land record details.",
                "url": "https://eservices.tn.gov.in/eservices_html/index.html",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "doc"
            },
            {
                "id": "view-a-register-extract",
                "title": "View A-Register Extract",
                "description": "Access land survey numbers, classification, and tax details.",
                "url": "https://eservices.tn.gov.in/eservices_html/index.html",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "table"
            },
            {
                "id": "download-fmb-sketch",
                "title": "Download FMB Sketch",
                "description": "Download Field Measurement Book (FMB) sketches of property survey lines.",
                "url": "https://eservices.tn.gov.in/eservices_html/index.html",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "map"
            },
            {
                "id": "view-patta-order-copy",
                "title": "View Patta Order Copy",
                "description": "Retrieve copies of land transfer/modification orders.",
                "url": "https://eservices.tn.gov.in/eservices_html/index.html",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "file-text"
            },
            {
                "id": "check-patta-transfer-status",
                "title": "Check Patta Transfer Status",
                "description": "Monitor the real-time status of land ownership transfer applications.",
                "url": "https://eservices.tn.gov.in/eservices_html/index.html",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "clock"
            },
            {
                "id": "view-urban-tslr-extract",
                "title": "View Urban TSLR Extract",
                "description": "Retrieve Town Survey Land Register (TSLR) extracts for urban properties.",
                "url": "https://eservices.tn.gov.in/eservices_html/index.html",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "building"
            },
            {
                "id": "verify-land-classification",
                "title": "Verify Government/Private Land Classification",
                "description": "Check whether land is classified as Government (Poramboke) or Private.",
                "url": "https://eservices.tn.gov.in/eservices_html/index.html",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "shield"
            }
        ]
    },
    {
        "id": "registration-encumbrance",
        "title": "Registration & Encumbrance Services",
        "description": "Official services for property transaction registration history and guideline values.",
        "services": [
            {
                "id": "encumbrance-certificate-search",
                "title": "Encumbrance Certificate Search",
                "description": "Search and download transaction history and debt encumbrance certificates.",
                "url": "https://tnreginet.gov.in/portal/",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "search"
            },
            {
                "id": "guideline-value-search",
                "title": "Guideline Value Search",
                "description": "Find official government valuation rates for properties in Tamil Nadu.",
                "url": "https://tnreginet.gov.in/portal/",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "trending-up"
            },
            {
                "id": "registration-department-services",
                "title": "Registration Department Services",
                "description": "Access documentation checklists, fee estimators, and registration portal tools.",
                "url": "https://tnreginet.gov.in/portal/",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "briefcase"
            }
        ]
    },
    {
        "id": "property-tax-civic",
        "title": "Property Tax & Civic Services",
        "description": "Official utility and tax portals for properties within municipal limits.",
        "services": [
            {
                "id": "chennai-corporation-property-tax-portal",
                "title": "Chennai Corporation Property Tax Portal",
                "description": "Pay property tax and check payment status under Greater Chennai Corporation.",
                "url": "https://onlinepayment.chennaicorporation.gov.in/",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "credit-card"
            },
            {
                "id": "water-tax-sewerage-services",
                "title": "Water Tax / Sewerage Services",
                "description": "Pay water and sewerage taxes online via CMWSSB portal.",
                "url": "https://chennaimetrowater.tn.gov.in/",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "droplet"
            }
        ]
    },
    {
        "id": "utility-ownership-support",
        "title": "Utility & Ownership Support Services",
        "description": "Curated supporting services designed for future utility expansion.",
        "services": [
            {
                "id": "tangedco-electricity-billing",
                "title": "TANGEDCO Electricity Billing",
                "description": "Pay electricity bills and check usage details online for Tamil Nadu.",
                "url": "https://www.tangedco.org/",
                "badge": "Official Tamil Nadu Government Service",
                "icon": "zap"
            }
        ]
    }
]
