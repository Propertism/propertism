"""
chat/services_config.py — M2.5 Service Coverage Framework Seed configuration.
Defines profiles for all 14 Propertism offerings.
Loaded into the database via the seed_services management command.
"""

SEED_SERVICES = [
    {
        'name': 'Buy Property',
        'category': 'Property Acquisition',
        'short_description': 'End-to-end property buying advisory in Chennai.',
        'detailed_description': 'Assists buyers from sourcing to registration, ensuring zero-risk title ownership.',
        'business_objective': 'Facilitate secure property purchases with legal validation and fair valuation.',
        'target_audience': 'Homebuyers, first-time investors, and overseas purchasers.',
        'eligibility': 'Minimum budget of ₹30 Lakhs; proof of funding or bank pre-approval.',
        'required_inputs': 'PAN Card, Aadhaar Card, Income Proof, Bank Statement (last 6 months).',
        'advisory_content': {
            'overview': 'Our property acquisition service covers sourcing, pricing evaluation, and full title verification.',
            'benefits': 'Ensures legal clarity, uncovers hidden risks, negotiates lower prices, and guides registration.',
            'process': '1. Sourcing → 2. Verification → 3. Viewing → 4. Price Negotiation → 5. Agreement → 6. Registration',
            'pricing': '1% of purchase value + GST as advisory commission.',
            'limitations': 'We do not support layout transactions that lack CMDA/DTCP approval.'
        },
        'faqs': [
            {'q': 'What is the commission?', 'a': 'We charge 1% of the final sale value as our service fee.'},
            {'q': 'Do you check land approval status?', 'a': 'Yes, we only facilitate CMDA/DTCP approved layout properties.'}
        ],
        'knowledge_references': 'buy property, buying guide',
        'related_services': ['SRV000005', 'SRV000006', 'SRV000007'],
        'call_to_actions': [
            {'label': 'Schedule Viewing', 'action': 'property_viewing'},
            {'label': 'Submit Inquiry', 'action': 'inquiry_creation'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'},
            {'type': 'whatsapp', 'value': '+918667020798'}
        ],
        'escalation_rules': {
            'level_1': 'RealBot Advisor',
            'level_2': 'Property Acquisition Manager'
        },
        'navigation_links': [
            {'label': 'Buy Property Portal', 'url': '/services/buy-property/'}
        ],
        'display_priority': 1
    },
    {
        'name': 'Sell Property',
        'category': 'Property Divestment',
        'short_description': 'Professional property selling and valuation services.',
        'detailed_description': 'Guides sellers in pricing, marketing, and closing property sales securely.',
        'business_objective': 'Maximize asset divestment realization within a fixed legal timeframe.',
        'target_audience': 'Individual owners, NRI sellers, and commercial asset managers.',
        'eligibility': 'Clear ownership title deeds; property located within Chennai metropolitan limits.',
        'required_inputs': 'Original Title Deed, Parent Documents, Patta Extract, Encumbrance Certificate.',
        'advisory_content': {
            'overview': 'Our sell property services include listing curation, valuation checks, and seller legal guidance.',
            'benefits': 'Reaches premium vetted buyers, avoids undervalued sales, and structures escrow safety.',
            'process': '1. Valuation → 2. Listing Curation → 3. Buyer Sourcing → 4. Agreement → 5. Transfer & Closure',
            'pricing': '1.5% of sale value + GST as divestment service fee.',
            'limitations': 'We do not list properties under active litigation or without clear title flow.'
        },
        'faqs': [
            {'q': 'How long does a sale take?', 'a': 'Average closure time ranges from 60 to 90 days for clear title assets.'},
            {'q': 'Do you charge listing fees?', 'a': 'Listing is free. We only charge upon successful closure.'}
        ],
        'knowledge_references': 'sell property, listing process',
        'related_services': ['SRV000001', 'SRV000003'],
        'call_to_actions': [
            {'label': 'Request Valuation', 'action': 'inquiry_creation'},
            {'label': 'Talk to Advisor', 'action': 'human_assistance'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'},
            {'type': 'whatsapp', 'value': '+918667020798'}
        ],
        'escalation_rules': {
            'level_1': 'RealBot Advisor',
            'level_2': 'Divestment Lead'
        },
        'navigation_links': [
            {'label': 'Sell Property Portal', 'url': '/services/sell-property/'}
        ],
        'display_priority': 2
    },
    {
        'name': 'Rental Income Management',
        'category': 'Property Operations',
        'short_description': 'End-to-end rental management for residential landlords.',
        'detailed_description': 'Handles tenant vetting, lease execution, rent collection, and maintenance.',
        'business_objective': 'Secure stable tenancy cashflow and maintain property value.',
        'target_audience': 'Individual owners, NRI landlords, and multi-unit investors.',
        'eligibility': 'Clear ownership deed; ready-to-move property in clean condition.',
        'required_inputs': 'Ownership Deed, Tax Receipt, Electricity Bill, Keys / Access codes.',
        'advisory_content': {
            'overview': 'Ensures your property delivers stable yield without the administrative burden.',
            'benefits': 'Tenant verification, automated collections, digital receipts, and vendor management.',
            'process': '1. Inspection → 2. Tenant Search → 3. Verification → 4. Lease Sign-off → 5. Monthly Management',
            'pricing': 'Service charge of 1 month rent per tenant sourcing or 8.33% of monthly rent.',
            'limitations': 'Maintenance costs exceeding ₹10,000 require landlord sign-off.'
        },
        'faqs': [
            {'q': 'How do you vet tenants?', 'a': 'We conduct background checks, verify employee IDs, and file police reports.'},
            {'q': 'Who handles repairs?', 'a': 'Propertism coordinates vendors. Cost is deducted from rent with approval.'}
        ],
        'knowledge_references': 'rental management, landlord guide',
        'related_services': ['SRV000007', 'SRV000002'],
        'call_to_actions': [
            {'label': 'Request Tenant Sourcing', 'action': 'inquiry_creation'},
            {'label': 'Speak to Manager', 'action': 'human_assistance'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'},
            {'type': 'whatsapp', 'value': '+918667020798'}
        ],
        'escalation_rules': {
            'level_1': 'RealBot Advisor',
            'level_2': 'Rental Desk Lead'
        },
        'navigation_links': [
            {'label': 'Property Management Portal', 'url': '/services/property-management/'}
        ],
        'display_priority': 3
    },
    {
        'name': 'Land / Plot Services',
        'category': 'Property Acquisition',
        'short_description': 'Assistance in layout acquisition and title clearances.',
        'detailed_description': 'Helps acquire residential layout plots and structures legal clearances.',
        'business_objective': 'Mitigate litigation risk in layout plot purchases in Chennai.',
        'target_audience': 'Individual land buyers, builders, and long-term land investors.',
        'eligibility': 'Verification of layout layout approvals (CMDA/DTCP/RERA).',
        'required_inputs': 'Layout plan, survey numbers, FMB sketches, parent documents.',
        'advisory_content': {
            'overview': 'Land purchase assistance, survey evaluation, and boundary markings.',
            'benefits': 'Protects against double registrations, confirms exact GPS boundary, and verifies approvals.',
            'process': '1. Survey Check → 2. Parent Title Review → 3. EC Verification → 4. Registration Guide',
            'pricing': 'Flat advisory fee of ₹25,000 for verification or 1% commission on buying.',
            'limitations': 'We do not facilitate purchase of agricultural lands or unapproved layouts.'
        },
        'faqs': [
            {'q': 'What is CMDA?', 'a': 'Chennai Metropolitan Development Authority, the regulatory layout planning body.'},
            {'q': 'Do you check land boundaries?', 'a': 'Yes, we coordinate surveyor visits to match FMB records.'}
        ],
        'knowledge_references': 'land purchase, plots chennai',
        'related_services': ['SRV000001', 'SRV000010', 'SRV000011'],
        'call_to_actions': [
            {'label': 'Check Plot Status', 'action': 'inquiry_creation'},
            {'label': 'Talk to Advisor', 'action': 'human_assistance'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'}
        ],
        'escalation_rules': {
            'level_1': 'RealBot Advisor',
            'level_2': 'Land & Plot Team Lead'
        },
        'navigation_links': [
            {'label': 'Plots Portal', 'url': '/services/land-plots/'}
        ],
        'display_priority': 4
    },
    {
        'name': 'Property Search',
        'category': 'Property Sourcing',
        'short_description': 'Browse and filter available properties matching your budget.',
        'detailed_description': 'Accesses Propertism’s curated verified listing portfolio in Chennai.',
        'business_objective': 'Match requirements to pre-vetted available residential inventory.',
        'target_audience': 'Active property searchers, homebuyers, and renters.',
        'eligibility': 'Vetted location preference and active purchase timeframe.',
        'required_inputs': 'Preferred Location, Budget, Property Config (BHK), Ready-to-move status.',
        'advisory_content': {
            'overview': 'Curated property search covering ECR, OMR, and central Chennai regions.',
            'benefits': 'No spam listings, verified legal checklist for each asset, and direct builder rates.',
            'process': '1. Set Budget & Location → 2. Receive Matches → 3. Shortlist → 4. Arrange Viewings',
            'pricing': 'Free property search, advisory fee only paid upon successful buying closure.',
            'limitations': 'Search inventory is limited to properties carrying legal vetting approval.'
        },
        'faqs': [
            {'q': 'Are all listings verified?', 'a': 'Yes, each listing must pass our internal 24-point legal title checklist.'},
            {'q': 'Do you charge search fees?', 'a': 'No, searching our inventory database is entirely free.'}
        ],
        'knowledge_references': 'property listings, search inventory',
        'related_services': ['SRV000001', 'SRV000006'],
        'call_to_actions': [
            {'label': 'Search Villas', 'action': 'property_search'},
            {'label': 'Search Apartments', 'action': 'property_search'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'},
            {'type': 'whatsapp', 'value': '+918667020798'}
        ],
        'escalation_rules': {
            'level_1': 'RealBot Advisor',
            'level_2': 'Sales Lead'
        },
        'navigation_links': [
            {'label': 'Browse Properties', 'url': '/properties/'}
        ],
        'display_priority': 5
    },
    {
        'name': 'Property Viewing',
        'category': 'Property Sourcing',
        'short_description': 'Schedule guided site visits with property advisors.',
        'detailed_description': 'Coordinates and facilitates on-site property walkthroughs with legal experts.',
        'business_objective': 'Deliver immersive, advisory-led viewing walkthroughs to prospective buyers.',
        'target_audience': 'Buyers ready to visit shortlisted properties.',
        'eligibility': 'Completed property search phase or direct listing query.',
        'required_inputs': 'Selected Property ID, Preferred Viewing Date & Time, Contact Details.',
        'advisory_content': {
            'overview': 'Guided property viewing with a dedicated Propertism consultant.',
            'benefits': 'Detailed structural inspection, neighborhood overview, and builder verification checks.',
            'process': '1. Select Listing → 2. Propose Slots → 3. Confirm Advisor Availability → 4. Site Walkthrough',
            'pricing': 'First 3 site viewings are free; subsequent viewings require travel reimbursement deposit.',
            'limitations': 'Site viewings must be scheduled at least 24 hours in advance.'
        },
        'faqs': [
            {'q': 'Are site visits free?', 'a': 'Yes, the first 3 viewings are completely free of cost.'},
            {'q': 'Can we visit on Sunday?', 'a': 'Yes, viewing slots are available on Sundays with advance notice.'}
        ],
        'knowledge_references': 'site visit, property viewing schedule',
        'related_services': ['SRV000005', 'SRV000001'],
        'call_to_actions': [
            {'label': 'Schedule Site Visit', 'action': 'inquiry_creation'},
            {'label': 'Call Support', 'action': 'phone_call'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'}
        ],
        'escalation_rules': {
            'level_1': 'RealBot Advisor',
            'level_2': 'Viewing Desk Coordinator'
        },
        'navigation_links': [
            {'label': 'Contact for Viewing', 'url': '/contact/'}
        ],
        'display_priority': 6
    },
    {
        'name': 'NRI Assist',
        'category': 'NRI Services',
        'short_description': 'Comprehensive NRI real estate advisory and compliance desk.',
        'detailed_description': 'Specialized support for overseas investors in acquisition, management, and tax.',
        'business_objective': 'Ensure FEMA and RBI compliance for non-resident property transactions.',
        'target_audience': 'Non-Resident Indians (NRIs), OCIs, and PIO holders.',
        'eligibility': 'Valid NRI / OCI status; NRE / NRO bank account setup.',
        'required_inputs': 'Passport Copy, OCI Card (if applicable), PAN Card, NRO Account details.',
        'advisory_content': {
            'overview': 'End-to-end support handling property transactions in Chennai on behalf of NRI clients.',
            'benefits': 'POA assistance, RBI compliance reviews, FEMA tax filings, and NRO repatriation guidance.',
            'process': '1. Compliance Check → 2. Search / Divestment → 3. POA Registration → 4. Transaction Audit',
            'pricing': 'Advisory retainer starting from ₹50,000 + transaction-specific fees.',
            'limitations': 'NRIs cannot buy agricultural land or plantation property in India.'
        },
        'faqs': [
            {'q': 'Can NRIs buy property in India?', 'a': 'Yes, residential and commercial properties are allowed. Agricultural land is prohibited.'},
            {'q': 'How do I transfer sale proceeds abroad?', 'a': 'Repatriation is allowed up to $1M per financial year from NRO accounts with Form 15CA/CB.'}
        ],
        'knowledge_references': 'nri investment, repatriation fema',
        'related_services': ['SRV000001', 'SRV000003'],
        'call_to_actions': [
            {'label': 'Talk to NRI Desk', 'action': 'human_assistance'},
            {'label': 'Submit Compliance Query', 'action': 'inquiry_creation'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'},
            {'type': 'whatsapp', 'value': '+918667020798'}
        ],
        'escalation_rules': {
            'level_1': 'RealBot Advisor',
            'level_2': 'NRI Service Director'
        },
        'navigation_links': [
            {'label': 'NRI Assist Portal', 'url': '/services/nri/'}
        ],
        'display_priority': 7
    },
    {
        'name': 'Resource Hub',
        'category': 'Resource Directory',
        'short_description': 'Access property guides, blogs, and market insights.',
        'detailed_description': 'Read curated articles and expert analyses on property regulations and market updates.',
        'business_objective': 'Provide educational resources to facilitate informed property decisions.',
        'target_audience': 'General public, buyers, sellers, and landlords.',
        'eligibility': 'Open access for all platform visitors.',
        'required_inputs': 'None.',
        'advisory_content': {
            'overview': 'Library of articles covering legal document guides, NRI investment checklists, and ECR market news.',
            'benefits': 'Free expert advice, zero-commercial bias, and structured legal summaries.',
            'process': 'Select category → Browse articles → View article.',
            'pricing': 'Free open resource portal.',
            'limitations': 'Content is educational only and does not constitute formal legal binding counsel.'
        },
        'faqs': [
            {'q': 'How often is content updated?', 'a': 'New guides and market reports are published weekly.'},
            {'q': 'Can I request a topic?', 'a': 'Yes, you can suggest a topic by writing to our email desk.'}
        ],
        'knowledge_references': 'resource articles, guide portal',
        'related_services': ['SRV000009'],
        'call_to_actions': [
            {'label': 'Read NRI Guides', 'action': 'navigation_card'},
            {'label': 'Browse Legal Guides', 'action': 'navigation_card'}
        ],
        'contact_channels': [],
        'escalation_rules': {},
        'navigation_links': [
            {'label': 'Resource Hub Portal', 'url': '/resource-hub/'}
        ],
        'display_priority': 8
    },
    {
        'name': 'Useful Links',
        'category': 'Resource Directory',
        'short_description': 'Directory of external government portals and property utilities.',
        'detailed_description': 'Quick links to TNREGINET, GCC Property Tax, Patta Chitta, and EC Portals.',
        'business_objective': 'Centralize all key government land and property links in one place.',
        'target_audience': 'Property owners and prospective buyers doing self-verification.',
        'eligibility': 'Open access portal.',
        'required_inputs': 'None.',
        'advisory_content': {
            'overview': 'Verified external links to official land registration and valuation portals.',
            'benefits': 'Instant access without searching, direct links to government domains, and security checks.',
            'process': 'Identify required utility → Click navigation link.',
            'pricing': 'Free utility index.',
            'limitations': 'External sites are governed by respective authorities; we are not responsible for downtime.'
        },
        'faqs': [
            {'q': 'What links are included?', 'a': 'We list TNREGINET, Patta Chitta download, and GCC Tax links.'}
        ],
        'knowledge_references': 'useful links, government portal links',
        'related_services': ['SRV000008', 'SRV000010', 'SRV000011', 'SRV000012'],
        'call_to_actions': [
            {'label': 'TNREGINET Portal', 'action': 'navigation_card'},
            {'label': 'Patta Chitta Portal', 'action': 'navigation_card'}
        ],
        'contact_channels': [],
        'escalation_rules': {},
        'navigation_links': [
            {'label': 'Useful Links Directory', 'url': '/useful-links/'}
        ],
        'display_priority': 9
    },
    {
        'name': 'Patta / Chitta Extract',
        'category': 'Document Retrieval',
        'short_description': 'Verify and download Patta Chitta land ownership records.',
        'detailed_description': 'Guidance on retrieving and reading land registration Patta/Chitta documents.',
        'business_objective': 'Facilitate land record authentication to prevent layout transaction fraud.',
        'target_audience': 'Land buyers, sellers, and property title evaluators.',
        'eligibility': 'Requires valid District, Taluk, and Survey/Subdivision numbers.',
        'required_inputs': 'District Name, Taluk Name, Village Name, Survey Number, Subdivision Number.',
        'advisory_content': {
            'overview': 'Step-by-step assistance in downloading the Patta/Chitta copy from the e-Services portal.',
            'benefits': 'Confirms government land records, validates owner name, and verifies boundary limits.',
            'process': '1. Choose Taluk/Village → 2. Input Survey Details → 3. Generate Extract → 4. Match with Deed',
            'pricing': 'Free for self-download. Professional legal verification report: ₹5,000.',
            'limitations': 'Some layouts might have outdated digital survey mappings requiring manual sub-registrar checks.'
        },
        'faqs': [
            {'q': 'What is Patta?', 'a': 'Patta is the legal document issued by the government proving land ownership.'},
            {'q': 'What is Chitta?', 'a': 'Chitta is land record details containing classification, size, and owner share.'}
        ],
        'knowledge_references': 'patta chitta verification, land record tn',
        'related_services': ['SRV000004', 'SRV000011'],
        'call_to_actions': [
            {'label': 'Open Government Portal', 'action': 'navigation_card'},
            {'label': 'Request Legal Review', 'action': 'inquiry_creation'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'}
        ],
        'escalation_rules': {
            'level_1': 'RealBot Advisor',
            'level_2': 'Legal Consultant'
        },
        'navigation_links': [
            {'label': 'TN Government e-Services Portal', 'url': 'https://eservices.tn.gov.in/'}
        ],
        'display_priority': 10
    },
    {
        'name': 'Encumbrance Search',
        'category': 'Document Retrieval',
        'short_description': 'Verify property history and liability encumbrances.',
        'detailed_description': 'Help in searching, downloading, and translating property Encumbrance Certificates (EC).',
        'business_objective': 'Ensure properties are clear of undisclosed loans, mortgages, and litigation.',
        'target_audience': 'Buyers, financial underwriters, and legal evaluators.',
        'eligibility': 'Requires exact sub-registrar office jurisdiction and survey numbers.',
        'required_inputs': 'Sub-registrar Jurisdiction, Survey Number, Plot Number (if layout), Search Period (years).',
        'advisory_content': {
            'overview': 'Searches and generates property transactions registry record for up to 30 years.',
            'benefits': 'Unveils bank loans, reveals double sales, registers mortgage releases, and tracks clear ownership.',
            'process': '1. Select Registry Office → 2. Enter Survey Details → 3. Submit EC Search → 4. Evaluate Transactions',
            'pricing': 'Government search fee varies (₹1 to ₹200). Propertism full search service: ₹2,500.',
            'limitations': 'Encumbrances not registered with sub-registrars (e.g., family agreements) do not appear on EC.'
        },
        'faqs': [
            {'q': 'What is EC?', 'a': 'Encumbrance Certificate lists all recorded transaction history of a property.'},
            {'q': 'How many years search is safe?', 'a': 'We recommend running a minimum 30-year encumbrance search for safety.'}
        ],
        'knowledge_references': 'encumbrance certificate check, ec search tn',
        'related_services': ['SRV000010', 'SRV000001'],
        'call_to_actions': [
            {'label': 'Access TNREGINET EC', 'action': 'navigation_card'},
            {'label': 'Get EC Review Service', 'action': 'inquiry_creation'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'}
        ],
        'escalation_rules': {
            'level_1': 'RealBot Advisor',
            'level_2': 'Legal Desk Lead'
        },
        'navigation_links': [
            {'label': 'TNREGINET Official Portal', 'url': 'https://tnreginet.gov.in/'}
        ],
        'display_priority': 11
    },
    {
        'name': 'GCC Property Tax',
        'category': 'Document Retrieval',
        'short_description': 'Verify and pay Greater Chennai Corporation property tax.',
        'detailed_description': 'Guidance on looking up tax records, calculating tax dues, and completing online payments.',
        'business_objective': 'Ensure zero property tax liabilities at the time of property registration.',
        'target_audience': 'Property owners in Chennai and prospective buyers checking dues.',
        'eligibility': 'Valid GCC Zone, Ward, and Bill numbers.',
        'required_inputs': 'Zone Number, Ward Number, Bill Number, Sub-registrar Jurisdiction.',
        'advisory_content': {
            'overview': 'Guidance on paying municipal tax and verifying tax assessment details under Chennai limits.',
            'benefits': 'Prevents municipal attachment actions, confirms name in tax logs, and satisfies sale checklist.',
            'process': '1. Input Bill Number → 2. Review Dues → 3. Pay via Online Portal → 4. Save Assessment Bill',
            'pricing': 'Free guidance. Online transaction charges apply as per bank payment gateways.',
            'limitations': 'Out-of-court tax disputes must be cleared directly at respective ward offices.'
        },
        'faqs': [
            {'q': 'How do I pay GCC property tax online?', 'a': 'Visit GCC payment portal, enter zone/ward/bill number, pay via UPI/Card.'},
            {'q': 'What happens if dues are unpaid?', 'a': 'GCC levies a monthly penalty of 1% simple interest on unpaid tax dues.'}
        ],
        'knowledge_references': 'property tax chennai, gcc tax dues',
        'related_services': ['SRV000009', 'SRV000003'],
        'call_to_actions': [
            {'label': 'Pay GCC Property Tax', 'action': 'navigation_card'},
            {'label': 'Check Dues Portal', 'action': 'navigation_card'}
        ],
        'contact_channels': [],
        'escalation_rules': {},
        'navigation_links': [
            {'label': 'GCC Property Tax Portal', 'url': 'https://chennaicorporation.gov.in/'}
        ],
        'display_priority': 12
    },
    {
        'name': 'General Advisory',
        'category': 'Customer Advisory',
        'short_description': 'General real estate queries and consultancy.',
        'detailed_description': 'Advises users on real estate procedures, legal issues, or platform tools.',
        'business_objective': 'Deliver premium initial consulting and educate first-time buyers.',
        'target_audience': 'General users seeking broad property market guidance.',
        'eligibility': 'Open access.',
        'required_inputs': 'Name, contact detail, general query description.',
        'advisory_content': {
            'overview': ' broad-spectrum advisory covering legal verification, price analysis, and locality insights.',
            'benefits': 'Unbiased second opinion, expert localized expertise, and protection against overpricing.',
            'process': '1. Ask Query → 2. RealBot Search → 3. Optional Expert Escalation',
            'pricing': 'Initial chat consulting is free. Written advisory reports: ₹5,000.',
            'limitations': 'Advisory is information-only and does not guarantee financial outcomes.'
        },
        'faqs': [
            {'q': 'Do you charge for initial advisory?', 'a': 'No, basic realBOT query advisory is entirely free.'}
        ],
        'knowledge_references': 'general advisory, chennai real estate',
        'related_services': ['SRV000014', 'SRV000001'],
        'call_to_actions': [
            {'label': 'Talk to expert', 'action': 'human_assistance'},
            {'label': 'Ask FAQ', 'action': 'faq'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'},
            {'type': 'whatsapp', 'value': '+918667020798'}
        ],
        'escalation_rules': {
            'level_1': 'RealBot Advisor',
            'level_2': 'Principal Advisor'
        },
        'navigation_links': [],
        'display_priority': 13
    },
    {
        'name': 'Contact Advisory',
        'category': 'Customer Advisory',
        'short_description': 'Connect directly with Propertism advisors and experts.',
        'detailed_description': 'Escalation desk to book consultations, schedule office visits, or report issues.',
        'business_objective': 'Provide direct escalation channels to support user enquiries.',
        'target_audience': 'Users ready to schedule calls or start transaction negotiations.',
        'eligibility': 'Open access escalation pathways.',
        'required_inputs': 'Name, Contact Number, Preferred communication channel, Topic.',
        'advisory_content': {
            'overview': 'Provides phone, email, WhatsApp, and office location coordinates.',
            'benefits': 'Instantly talk to a human expert, resolve complex issues, and book office visits.',
            'process': '1. Select Channel → 2. Initiate Call / Chat → 3. Dedicated expert handles query',
            'pricing': 'Free client assistance channels.',
            'limitations': 'Human support channels are active Monday-Saturday, 9:00 AM to 6:00 PM IST.'
        },
        'faqs': [
            {'q': 'When are phone lines open?', 'a': 'Our phone support desk operates Mon-Sat 9 AM to 6 PM IST.'}
        ],
        'knowledge_references': 'contact details, support hours',
        'related_services': ['SRV000013', 'SRV000006'],
        'call_to_actions': [
            {'label': 'Call Desk Now', 'action': 'phone_call'},
            {'label': 'Message WhatsApp', 'action': 'whatsapp'}
        ],
        'contact_channels': [
            {'type': 'phone', 'value': '+91 86670 20798'},
            {'type': 'whatsapp', 'value': '+918667020798'},
            {'type': 'email', 'value': 'info@propertism.in'}
        ],
        'escalation_rules': {
            'level_1': 'Customer Support Agent',
            'level_2': 'Operations Manager'
        },
        'navigation_links': [
            {'label': 'Contact Directory Page', 'url': '/contact/'}
        ],
        'display_priority': 14
    }
]
