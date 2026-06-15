"""
Management command: seed_knowledge_hub_phase_a

Seeds 10 foundational NRI Knowledge Hub articles as BlogPost records.
Safe to run multiple times — skips slugs that already exist.

Usage:
    python manage.py seed_knowledge_hub_phase_a
    python manage.py seed_knowledge_hub_phase_a --publish
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from content.models import BlogPost

ARTICLES = [
    {
        "slug": "nri-property-management-chennai-complete-guide",
        "title": "NRI Property Management in Chennai: Complete Guide",
        "category": "nri",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "A complete guide for NRIs managing property in Chennai from abroad. "
            "Covers tenant management, maintenance, legal compliance, and choosing "
            "a reliable local property manager."
        ),
        "content": """Managing property in Chennai from abroad is one of the most common challenges NRIs face. Distance creates dependency on informal networks, delayed updates, and unverified execution. This guide explains how NRI property management works in practice and what to look for in a local partner.

<h2>Why NRI Property Management is Different</h2>

Resident property owners can visit their property, speak to tenants directly, and respond to maintenance issues the same day. NRIs cannot. Every task — from collecting rent to approving a repair — requires a trusted local point of contact who acts with accountability.

The core challenge is not finding people to help. It is finding a structured system that keeps your property productive, legally compliant, and well-maintained without requiring your constant involvement.

<h2>What a Property Manager Does for NRIs</h2>

A professional NRI property manager in Chennai handles the following on your behalf:

<strong>Tenant Management:</strong> Sourcing verified tenants, conducting background checks, preparing rental agreements, and managing move-in and move-out processes.

<strong>Rent Collection and Remittance:</strong> Collecting rent on schedule, following up on delays, and transferring funds to your account with documentation.

<strong>Property Inspections:</strong> Conducting periodic inspections — typically quarterly — and sending photo or video reports so you can verify the property condition remotely.

<strong>Maintenance Coordination:</strong> Managing repairs using a verified vendor network. Approving costs within agreed limits and escalating larger decisions to the owner.

<strong>Legal and Compliance Tracking:</strong> Ensuring property tax is paid, rental agreements are registered where required, and documentation is current.

<h2>How to Choose a Property Manager in Chennai</h2>

The most important factor is accountability. Ask any prospective manager:

- How do you report to owners? How frequently?
- What is your process for tenant disputes?
- How do you handle maintenance approvals above a set limit?
- Do you provide documented rent receipts and maintenance records?

A manager who cannot answer these clearly is not running a structured operation.

<h2>Common Mistakes NRI Property Owners Make</h2>

<strong>Relying on relatives:</strong> Well-meaning relatives often lack the time, tools, or authority to manage property professionally. This leads to deferred maintenance and undocumented tenancies.

<strong>Choosing the lowest-cost manager:</strong> Low fees often reflect low service levels. An underpaid manager will deprioritise your property when issues arise.

<strong>No written agreements:</strong> Verbal arrangements with tenants or managers create disputes. Every relationship must be documented.

<strong>Infrequent communication:</strong> Owners who go months without updates lose track of their property's condition and occupancy status.

<h2>NRI Property Management in Chennai: Propertism's Approach</h2>

Propertism manages NRI-owned properties in Chennai through a structured process: tenant sourcing, documented rent operations, scheduled inspections, maintenance coordination, and regular owner reporting. All activity is logged and communicated so you always know the status of your property.

<h2>Frequently Asked Questions</h2>

<strong>Can I manage my Chennai property without visiting India?</strong>
Yes. With a structured local management partner, most NRI property owners successfully manage their properties without visiting India for years. Critical decisions can be made remotely with proper documentation.

<strong>How often should I receive property reports?</strong>
Monthly rent confirmation and quarterly inspection reports are a reasonable baseline. Higher-value properties or those with active maintenance issues warrant more frequent updates.

<strong>What happens if my tenant stops paying rent?</strong>
A professional manager follows a documented escalation process: reminder, formal notice, and legal action if required. You should never find out about a non-paying tenant weeks after the problem started.

<strong>Do I need to give power of attorney to my property manager?</strong>
Not always. Most routine management tasks do not require POA. However, for property sale, certain registrations, or legal proceedings, a limited POA may be necessary.

If you own property in Chennai and are managing it from abroad, <a href="/chennai/nri-property-management/">explore how Propertism's NRI property management service works</a> or <a href="/contact/">speak to our advisory team</a>.
""",
    },
    {
        "slug": "how-nris-can-sell-property-in-india-from-abroad",
        "title": "How NRIs Can Sell Property in India from Abroad",
        "category": "nri",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "Step-by-step guide for NRIs selling property in India without travelling. "
            "Covers valuation, buyer coordination, documentation, power of attorney, "
            "and tax obligations."
        ),
        "content": """Selling property in India as an NRI involves more steps than a typical domestic sale. Documentation requirements, tax obligations, and the practical challenge of coordinating buyers from abroad make the process complex without a structured local partner. This guide covers the complete process.

<h2>Step 1: Property Valuation</h2>

Before listing, establish a realistic price band. An NRI who has not visited their property recently often overestimates its market value based on outdated comparisons. A local advisor who knows current buyer demand in your area will give you a more accurate picture.

Key factors affecting valuation in Chennai:
- Location and micro-market demand
- Property condition and pending repairs
- Documentation completeness (title, encumbrance, tax receipts)
- Current inventory levels in the locality

<h2>Step 2: Documentation Preparation</h2>

Incomplete documentation is the most common cause of NRI property sale delays. Before listing, verify you have:

- Original title deed or sale deed
- Encumbrance certificate (minimum last 30 years)
- Latest property tax receipts
- Khata / Patta certificate (applicable in Tamil Nadu)
- Identity documents (passport, PAN card, OCI card if applicable)
- No-objection certificates if the property has a loan

If any document is missing or requires correction, address it before finding a buyer.

<h2>Step 3: Buyer Coordination Without Travelling</h2>

NRIs do not need to visit India to find and qualify buyers. A local execution partner handles:

- Property listings and marketing
- Coordinating and attending buyer visits
- Filtering serious inquiries from speculative ones
- Negotiation within agreed parameters
- Sharing verified buyer updates with you remotely

<h2>Step 4: Legal and Registration Process</h2>

The sale deed registration requires the seller to be present, or to authorise a representative through a registered Power of Attorney (POA). Most NRI sellers complete this step by:

1. Executing a POA in the country of residence (notarised and apostilled)
2. Having the POA registered in India
3. The authorised representative attending registration on the seller's behalf

<h2>Step 5: Tax Obligations for NRI Sellers</h2>

NRIs selling property in India are subject to capital gains tax:

- <strong>Long-term capital gains (LTCG):</strong> Property held over 24 months. Taxed at 20% with indexation benefit (or 12.5% without indexation under the 2024 amendment).
- <strong>Short-term capital gains (STCG):</strong> Property held under 24 months. Taxed at applicable income tax slab rate.

The buyer is also required to deduct TDS at 20% (for LTCG) or 30% (for STCG) on the sale value before paying the NRI seller. Plan for this before pricing the transaction.

<h2>Repatriation of Sale Proceeds</h2>

NRIs can repatriate sale proceeds outside India subject to FEMA rules. Generally, up to USD 1 million per financial year from property sale proceeds can be repatriated after payment of applicable taxes and submission of a CA certificate in Form 15CB.

<h2>Frequently Asked Questions</h2>

<strong>Can I sell my property in India without visiting?</strong>
Yes. With a registered POA and a structured local partner, NRIs complete property sales in India entirely remotely.

<strong>How long does NRI property sale typically take in Chennai?</strong>
From listing to registration, 3–6 months is a realistic timeline for a well-priced, fully-documented property in Chennai. Incomplete documentation or unrealistic pricing extends this.

<strong>Do I pay tax in India and in my country of residence?</strong>
India taxes the capital gain. Your country of residence may also tax it, but India has Double Taxation Avoidance Agreements (DTAA) with most countries where NRIs reside, which prevents double taxation.

To start the process, <a href="/chennai/nri-sell-property/">explore our NRI property sale support for Chennai</a> or <a href="/contact/">speak to our team</a>.
""",
    },
    {
        "slug": "power-of-attorney-for-nris-complete-guide",
        "title": "Power of Attorney for NRIs: Complete Guide",
        "category": "legal",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "Everything NRIs need to know about Power of Attorney for property in India. "
            "Types of POA, how to execute from abroad, registration requirements, and risks to avoid."
        ),
        "content": """Power of Attorney (POA) is one of the most important legal instruments available to NRIs managing or selling property in India. When executed correctly, it allows a trusted representative to act on your behalf for specific property transactions without requiring your physical presence in India.

<h2>What is a Power of Attorney?</h2>

A Power of Attorney is a legal document that authorises another person (the attorney or agent) to perform specified legal acts on your behalf. For NRI property owners, it is commonly used to:

- Register a sale deed on the owner's behalf
- Execute a rental agreement
- Apply for property-related documents
- Manage maintenance approvals and vendor payments
- Handle property tax and municipal compliance

<h2>Types of POA for NRI Property</h2>

<strong>General Power of Attorney (GPA):</strong> Grants broad authority to the agent to handle multiple tasks. Use with caution — a GPA given to the wrong person creates significant risk.

<strong>Specific / Limited Power of Attorney (SPA):</strong> Authorises the agent to perform only defined tasks (e.g., sell one specific property, register one specific agreement). This is the safer option for most NRI transactions.

<strong>Irrevocable POA:</strong> Cannot be cancelled once granted. Only use this when explicitly required by a transaction structure — not for routine management.

<h2>How NRIs Execute a POA from Abroad</h2>

The process has four steps:

<strong>Step 1 — Draft the POA</strong>
The document must be drafted clearly with the specific powers granted, the property details, and the agent's identity. Use a qualified lawyer in India to draft it.

<strong>Step 2 — Execute Before a Notary in Your Country of Residence</strong>
Sign the POA before a notary public in the country where you reside.

<strong>Step 3 — Apostille the Document</strong>
Countries that are signatories to the Hague Apostille Convention (USA, UK, UAE, Singapore, Australia, Canada) can apostille the POA. An apostille certifies the notary's authority and makes the document valid in India.

For countries not in the Hague Convention, the document must be attested by the Indian Embassy or Consulate.

<strong>Step 4 — Register in India</strong>
Once received in India, the POA must typically be registered at the Sub-Registrar's office to be used for property transactions. Stamp duty applies.

<h2>Who Should You Give POA To?</h2>

This is the most critical decision. A misused POA can result in your property being sold without your knowledge or agreement. Choose:

- A close family member with a clear understanding of the specific authority granted
- A registered professional with documented accountability
- Always use a specific/limited POA rather than a general one

<h2>Common POA Mistakes NRIs Make</h2>

- Granting GPA when SPA is sufficient
- Using templates from the internet that miss required clauses
- Not registering the POA, making it inadmissible for property registration
- Giving POA to someone without a written agreement on their role and limits
- Not cancelling POA when no longer needed

<h2>Frequently Asked Questions</h2>

<strong>Is a notarised POA enough or does it need to be registered in India?</strong>
For property transactions (sale, purchase, lease registration), the POA must be registered in India. Notarisation alone is not sufficient.

<strong>Can I cancel a POA once I have given it?</strong>
Yes, unless it is explicitly irrevocable. To cancel, execute a revocation deed and ensure the agent is notified in writing. Register the revocation if the original was registered.

<strong>Does my POA agent have to pay capital gains tax on my behalf?</strong>
No. Tax liability remains with the property owner, not the agent. The agent executes the transaction; tax obligations are the owner's responsibility.

For guidance on POA in the context of a Chennai property sale, <a href="/chennai/nri-sell-property/">see our NRI sell property service</a> or <a href="/chennai/nri-property-legal-support/">explore legal support options</a>.
""",
    },
    {
        "slug": "how-to-verify-property-documents-chennai",
        "title": "How to Verify Property Documents in Chennai",
        "category": "legal",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "A practical guide to verifying property documents before buying or selling in Chennai. "
            "Covers title deed, encumbrance certificate, Patta, tax receipts, and approval documents."
        ),
        "content": """Property document verification is the most important step in any Chennai property transaction. Incomplete, encumbered, or disputed documents are the leading cause of failed sales and buyer disputes. This guide covers what to check and where to check it.

<h2>Why Document Verification Matters for NRIs</h2>

NRIs buying or selling property in Chennai often complete transactions remotely. This makes document verification even more important — you cannot walk through the property registry or verify physical documents yourself. A structured document check protects your transaction.

<h2>Key Documents to Verify</h2>

<h3>1. Title Deed (Sale Deed)</h3>
The title deed establishes legal ownership. Verify:
- The seller's name matches the registered owner
- A clear chain of ownership with no gaps
- No disputes or court orders attached to the property
- Deed is registered at the Sub-Registrar's office

<h3>2. Encumbrance Certificate (EC)</h3>
An EC from the Sub-Registrar's office records all registered transactions against a property for a specified period. It reveals:
- Mortgages or loans on the property
- Previous sale transactions
- Any registered disputes

Request an EC for a minimum of 30 years. Ideally, trace back to when the property was first sold from a government or approved layout.

<h3>3. Patta (Tamil Nadu)</h3>
Patta is the revenue record that establishes land ownership in Tamil Nadu. It is maintained by the Tahsildar's office. Verify that:
- Patta is in the current owner's name
- Patta details match the sale deed (extent, survey number)
- No joint-patta disputes exist

NRIs can check Patta status online through the Tamil Nadu government's e-services portal.

<h3>4. Property Tax Receipts</h3>
Verify that property tax is paid up to date with the Greater Chennai Corporation (GCC) or relevant municipal body. Unpaid tax becomes the buyer's liability after purchase.

<h3>5. Approved Building Plan</h3>
For built properties, check that the building plan was approved by the Chennai Metropolitan Development Authority (CMDA) or Chennai Corporation, and that the construction conforms to the approved plan.

<h3>6. Occupancy Certificate</h3>
For apartments and newly built structures, an Occupancy Certificate (OC) confirms the building was constructed as approved and is fit for occupation.

<h2>Where to Verify Documents in Chennai</h2>

| Document | Verification Source |
|---|---|
| Sale Deed | Sub-Registrar's office (by survey number) |
| Encumbrance Certificate | Sub-Registrar's office or online via TNREGINET |
| Patta | Tahsildar's office or TN e-services portal |
| Property Tax | GCC portal or local municipal office |
| Building Approval | CMDA or Chennai Corporation records |

<h2>Frequently Asked Questions</h2>

<strong>Can I verify property documents in Chennai online?</strong>
Some documents, including EC and Patta, can be checked online. Title deed registration details are available on TNREGINET. Full verification still requires physical document review for a complete picture.

<strong>How far back should an EC go?</strong>
A minimum of 30 years. For older properties, go back to the first registered transaction or to a government land grant if available.

<strong>What if the Patta is not in the seller's name?</strong>
This is a red flag. Insist on Patta transfer before completing the purchase, or verify the specific reason through a qualified local property lawyer.

For property verification support in Chennai, <a href="/chennai/nri-property-legal-support/">see our NRI legal support service</a> or <a href="/contact/">speak to our team</a>.
""",
    },
    {
        "slug": "patta-transfer-process-explained",
        "title": "Patta Transfer Process Explained for NRIs",
        "category": "legal",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "Step-by-step guide to Patta transfer in Tamil Nadu for NRIs. "
            "What Patta is, why it matters, and how to transfer it after buying or inheriting property."
        ),
        "content": """Patta is one of the most important land records in Tamil Nadu. For NRIs buying, selling, or inheriting property in Chennai or elsewhere in Tamil Nadu, understanding Patta and how to transfer it is essential.

<h2>What is Patta?</h2>

Patta (also called Adangal) is an official revenue record maintained by the Tamil Nadu government's Revenue Department. It records:
- The name of the landowner (pattedar)
- Survey number and sub-division number
- Extent of land (in hectares or cents)
- Land use classification (dry, wet, or garden land)

Patta is the government's recognition of who owns a piece of land. It is separate from the registered sale deed but both must be consistent.

<h2>Why Patta Transfer Matters</h2>

After a property is purchased or inherited, the Patta must be updated to reflect the new owner's name. If Patta remains in the previous owner's name:
- Future sale complications arise
- Mutations and tax records may not update correctly
- Government land acquisition compensation may be paid to the wrong party
- Bank loans against the property become difficult

<h2>When to Transfer Patta</h2>

Patta transfer is required after:
- Purchase of land or independent house (after sale deed registration)
- Inheritance of property (after obtaining legal heir certificate or probate)
- Gift deed registration
- Partition deed registration

<h2>Patta Transfer Process in Tamil Nadu</h2>

<strong>Step 1: Prepare Documents</strong>
- Registered sale deed / gift deed / partition deed
- Previous Patta (in seller's/previous owner's name)
- Latest property tax receipt
- Encumbrance certificate
- Identity proof (passport for NRIs)

<strong>Step 2: Submit Application</strong>
Submit Form 1 (application for Patta transfer) at the Tahsildar's office of the taluk where the property is located. NRIs can submit through an authorised representative using POA.

Online applications can be submitted through the Tamil Nadu e-Sevai portal or Common Service Centres (CSC).

<strong>Step 3: Field Inspection</strong>
The Revenue Inspector may conduct a field inspection to verify the property details match records.

<strong>Step 4: Patta Issued</strong>
After verification, the updated Patta is issued in the new owner's name. Processing typically takes 30–60 days.

<h2>Patta Transfer for Inherited Property</h2>

For inherited property, the process requires additional documents:
- Death certificate of the previous owner
- Legal heir certificate (issued by the Tahsildar) or succession certificate (court-issued)
- Affidavit from legal heirs

NRIs inheriting property in Chennai should initiate Patta transfer promptly after obtaining the legal heir certificate.

<h2>Frequently Asked Questions</h2>

<strong>Can NRIs apply for Patta transfer without visiting India?</strong>
Yes. An authorised representative with a registered POA can submit the application and attend any field inspection on your behalf.

<strong>Is Patta required to sell property in Tamil Nadu?</strong>
While a sale can technically proceed without Patta in the buyer's name, buyers are advised not to purchase property where Patta has not been transferred to the seller's name. It creates downstream complications.

<strong>What is the difference between Patta and Chitta?</strong>
Patta records ownership. Chitta (Adangal) records cultivation and land classification details. Both are maintained by the Revenue Department and are often verified together.

For help managing Patta transfer for NRI-owned property in Tamil Nadu, <a href="/chennai/nri-property-legal-support/">explore our legal support service</a> or <a href="/contact/">contact us</a>.
""",
    },
    {
        "slug": "encumbrance-certificate-guide-for-nris",
        "title": "Encumbrance Certificate Guide for NRIs",
        "category": "legal",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "What an Encumbrance Certificate is, why NRIs need it before buying or selling property "
            "in India, how to obtain it, and what to look for."
        ),
        "content": """An Encumbrance Certificate (EC) is one of the most important documents in any Indian property transaction. For NRIs buying, selling, or using property as collateral, understanding the EC is essential.

<h2>What is an Encumbrance Certificate?</h2>

An Encumbrance Certificate is an official document issued by the Sub-Registrar's office that records all registered transactions on a specific property over a defined period. It shows:

- Sale deeds registered on the property
- Mortgages or loans registered against it
- Gift deeds, partition deeds, lease deeds
- Any court-ordered attachments or charges

An EC proves that a property is free from registered financial and legal liabilities for the period it covers.

<h2>Why NRIs Need an EC</h2>

<strong>Before buying:</strong> An EC confirms there are no outstanding loans, mortgages, or disputes on the property you are purchasing.

<strong>Before selling:</strong> Buyers and their lawyers will request an EC as standard due diligence. Having it ready speeds up the transaction.

<strong>For home loans:</strong> Banks require EC before approving loans against property.

<strong>For legal heir transfer:</strong> EC is required during Patta transfer and mutation after inheritance.

<h2>Types of EC</h2>

<strong>Form 15:</strong> Issued when there are encumbrances (transactions registered) on the property during the requested period.

<strong>Form 16 (Nil Encumbrance Certificate):</strong> Issued when there are no registered transactions on the property during the requested period.

<h2>How to Obtain an EC in Tamil Nadu</h2>

<strong>Online (TNREGINET):</strong>
1. Visit tnreginet.gov.in
2. Select "Encumbrance Certificate" under services
3. Enter property details (district, registration office, survey number, and period)
4. Pay the prescribed fee online
5. Download the EC or collect from the Sub-Registrar's office

<strong>Offline:</strong>
Submit Form 22 at the Sub-Registrar's office with property details and the period for which EC is required. Processing takes 3–7 working days.

NRIs can apply online or through an authorised representative.

<h2>How to Read an EC</h2>

When you receive an EC, check:

- Is every transaction in the chain accounted for? The EC should show the history of how the current owner acquired the property.
- Are there any mortgage entries that have not been discharged?
- Is there a court attachment or order affecting the property?
- Is the period covered adequate? Request a minimum of 30 years.

If the EC shows a mortgage, verify it has been officially discharged (a release deed registered at the Sub-Registrar's office).

<h2>Frequently Asked Questions</h2>

<strong>How many years of EC should I request?</strong>
Request a minimum of 30 years. For older properties, request from the date of the earliest available transaction.

<strong>Does an EC guarantee clear title?</strong>
No. An EC only records registered transactions. Unregistered agreements, oral arrangements, or disputes not yet reflected in registered records will not appear. Title verification requires additional steps.

<strong>Can the EC be obtained online for Chennai properties?</strong>
Yes. EC for properties in Tamil Nadu can be obtained through TNREGINET without visiting the Sub-Registrar's office.

For property document support in Chennai, <a href="/chennai/nri-property-legal-support/">see our NRI legal support service</a> or <a href="/contact/">speak to our advisory team</a>.
""",
    },
    {
        "slug": "property-tax-guide-chennai-nris",
        "title": "Property Tax Guide for Chennai NRIs",
        "category": "legal",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "How property tax works in Chennai for NRI-owned properties. "
            "How to pay, check dues, update records, and avoid penalties while living abroad."
        ),
        "content": """Property tax in Chennai is levied by the Greater Chennai Corporation (GCC) on all buildings and land within its jurisdiction. For NRIs, staying current with property tax is both a legal obligation and a practical necessity for clean documentation when selling or transferring property.

<h2>Who Levies Property Tax in Chennai?</h2>

The Greater Chennai Corporation (GCC) levies and collects property tax for properties within the Chennai city limits. For properties in areas administered by the Chennai Metropolitan Development Authority (CMDA) outside GCC limits, the respective local body (municipality or town panchayat) is responsible.

<h2>How Property Tax is Calculated</h2>

Chennai property tax is calculated based on the Annual Value (AV) of the property, which depends on:
- Built-up area
- Location and zone classification
- Age of the building
- Use (residential or commercial)

The tax rate is a percentage of the Annual Value. Residential properties typically attract lower rates than commercial ones.

<h2>How NRIs Can Pay Property Tax</h2>

<strong>Online payment (recommended for NRIs):</strong>
- Visit the GCC online portal (chennaicorporation.gov.in)
- Enter the Assessment Number or Door Number
- View outstanding dues and pay using net banking, UPI, or card

<strong>Through a representative:</strong>
NRIs can authorise a family member or property manager to pay property tax on their behalf. A POA is not required for tax payments — the authorised person simply uses the assessment number to pay.

<h2>Checking Property Tax Dues</h2>

Use the GCC portal to check outstanding dues at any time. NRIs should verify:
- That tax is paid in the current owner's name (not a previous owner)
- That there are no arrears from previous years
- That the property details (address, area) in GCC records match actual property details

Discrepancies in area or classification should be corrected before selling the property.

<h2>Property Tax and Property Sale</h2>

Buyers request proof of paid property tax as standard due diligence. Before listing a property for sale:
- Ensure all property tax arrears are cleared
- Obtain a tax payment receipt for at least the last 3 years
- If property tax records show an incorrect name or area, initiate a correction before listing

<h2>Consequences of Non-Payment</h2>

Unpaid property tax accrues penalty interest. The GCC can:
- Attach and auction the property for recovery of dues
- Issue notices that complicate future transactions

For NRIs who have been abroad for extended periods, checking for arrears is the first step.

<h2>Frequently Asked Questions</h2>

<strong>Can I pay Chennai property tax from abroad?</strong>
Yes. The GCC online portal accepts payments via net banking and international cards. NRIs regularly pay property tax online without assistance.

<strong>Will unpaid property tax affect my property sale?</strong>
Yes. Buyers and their lawyers will verify tax payment records. Significant arrears must be cleared before the sale proceeds.

<strong>How do I update property tax records to my name after purchase?</strong>
Submit a mutation application to the GCC with the registered sale deed, previous tax receipt, and identity proof. Online mutation is available on the GCC portal.

For help managing property tax compliance and documentation for your Chennai property, <a href="/chennai/nri-property-management/">see our property management service</a> or <a href="/contact/">contact us</a>.
""",
    },
    {
        "slug": "capital-gains-tax-property-sale-nris",
        "title": "Capital Gains Tax on Property Sale for NRIs",
        "category": "legal",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "How capital gains tax applies when NRIs sell property in India. "
            "LTCG, STCG, TDS obligations for buyers, exemptions, and repatriation rules."
        ),
        "content": """Capital gains tax is a critical consideration for every NRI selling property in India. Understanding how it is calculated, what obligations it creates, and what exemptions may apply will directly affect your net sale proceeds.

<h2>What is Capital Gains Tax on Property?</h2>

When you sell a property for more than its cost of acquisition (adjusted for improvements and inflation), the profit is a capital gain. Capital gains on property sales are taxable in India regardless of whether the seller is a resident or NRI.

<h2>Long-Term vs Short-Term Capital Gains</h2>

<strong>Long-Term Capital Gain (LTCG):</strong> Applies when the property has been held for more than 24 months. As of the Finance Act 2024, LTCG is taxed at 12.5% without the benefit of indexation, or 20% with indexation — whichever the taxpayer chooses (for properties acquired before July 23, 2024).

<strong>Short-Term Capital Gain (STCG):</strong> Applies when the property has been held for 24 months or less. Taxed at the applicable income tax slab rate of the seller.

<h2>TDS on NRI Property Sales</h2>

This is where NRI property sales differ critically from resident sales. Under Section 195 of the Income Tax Act, the buyer is required to deduct TDS before paying the NRI seller:

- LTCG: 20% TDS on sale value (plus applicable surcharge and cess)
- STCG: 30% TDS on sale value (plus applicable surcharge and cess)

The buyer must deduct this TDS, deposit it with the government, and issue Form 16A to the seller. The NRI can then file an income tax return and claim a refund if the actual tax liability is lower.

<h2>Lower TDS Deduction Certificate</h2>

If the actual capital gains tax liability is lower than the TDS rate, NRIs can apply to the Income Tax Officer for a Lower Deduction Certificate under Section 197. This allows the buyer to deduct TDS at a lower rate.

<h2>Capital Gains Exemptions Available to NRIs</h2>

<strong>Section 54:</strong> LTCG exemption if the proceeds are reinvested in a new residential property in India within specified timelines (purchase within 1 year before or 2 years after sale; construction within 3 years).

<strong>Section 54EC:</strong> LTCG exemption if proceeds (up to ₹50 lakhs) are invested in specified bonds (NHAI, RECL) within 6 months of sale.

<h2>Repatriation of Sale Proceeds</h2>

After paying applicable taxes, NRIs can repatriate sale proceeds subject to FEMA regulations. Generally:
- Up to USD 1 million per financial year from property sale proceeds
- Requires a CA certificate in Form 15CB certifying tax compliance
- Bank submits Form 15CA before remitting funds

<h2>DTAA — Avoiding Double Taxation</h2>

India has Double Taxation Avoidance Agreements with most countries where NRIs reside (USA, UK, UAE, Singapore, Canada, Australia). Under DTAA provisions, tax paid in India on capital gains can typically be credited against tax payable in the country of residence, preventing double taxation.

<h2>Frequently Asked Questions</h2>

<strong>Does the buyer always have to deduct TDS when buying from an NRI?</strong>
Yes, unless the NRI has obtained a Lower Deduction Certificate from the Income Tax Officer. Failure to deduct TDS makes the buyer liable for the tax amount.

<strong>What happens if my actual tax liability is lower than TDS deducted?</strong>
File an income tax return in India for the year of sale and claim the excess TDS as a refund. This requires a PAN card.

<strong>Do NRIs need a PAN card to sell property in India?</strong>
Yes. PAN is required for property transactions above ₹10 lakhs and for filing tax returns to claim TDS refunds.

For guidance on the sale process for your Chennai property, <a href="/chennai/nri-sell-property/">see our NRI sell property service</a> or <a href="/chennai/nri-capital-gains/">explore capital gains guidance</a>.
""",
    },
    {
        "slug": "tenant-management-guide-overseas-property-owners",
        "title": "Tenant Management Guide for Overseas Property Owners",
        "category": "tenant",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "How NRIs can manage tenants effectively from abroad. "
            "Covers tenant screening, rental agreements, rent collection, disputes, and move-out."
        ),
        "content": """Managing tenants from abroad is one of the most operationally demanding aspects of NRI property ownership. Without a structured system, rent delays, tenant disputes, and undocumented tenancies become difficult to resolve from a distance. This guide covers the complete tenant management lifecycle for overseas property owners.

<h2>Tenant Sourcing and Screening</h2>

The quality of the tenant you place determines the quality of the tenancy. A rushed or unverified placement is a common source of later problems.

<strong>Background verification:</strong> At minimum, verify employment or income (salary slips, employment letter, or business documents), identity (Aadhaar, passport), and previous rental history (contact previous landlord where possible).

<strong>Reference checks:</strong> Speak to or request references from the tenant's employer or previous landlord.

<strong>Credit behaviour signals:</strong> Does the tenant pay their advance promptly? Do they negotiate aggressively on deposit? Early signals of financial reliability matter.

<h2>Rental Agreement Essentials</h2>

Every tenancy must be backed by a written rental agreement. Key terms to include:

- Monthly rent amount and due date
- Security deposit amount and conditions for deduction
- Lease duration and renewal terms
- Maintenance responsibilities (what the tenant covers, what the owner covers)
- Restrictions on subletting or commercial use
- Notice period for termination by either party
- Utilities responsibility

In Tamil Nadu, rental agreements for 12 months or more should be registered at the Sub-Registrar's office. Unregistered agreements for longer periods have limited legal enforceability.

<h2>Rent Collection for NRI Landlords</h2>

Establishing a reliable rent collection mechanism is critical when you are abroad:

- Direct bank transfer is the safest and most documentable method
- Request digital payment receipts or bank transfer acknowledgements monthly
- Agree upfront that rent is due on a specific date (e.g., 5th of each month)
- Build in an escalation process for delays: reminder on day 6, formal notice on day 15

If using a property manager, confirm how rent is remitted to you and what documentation you receive.

<h2>Property Inspections During Tenancy</h2>

NRI owners often go years without inspecting their property. This allows maintenance issues to accumulate and gives tenants scope to make unauthorised modifications. Establish:

- Quarterly inspections with photo/video reports sent to you
- A pre-vacation inspection when the tenancy ends
- Any identified maintenance items addressed and documented

<h2>Handling Tenant Disputes from Abroad</h2>

Common disputes involve rent arrears, property damage, and refusal to vacate. The process:

1. Attempt resolution through a documented written request
2. Issue a formal notice through your property manager or lawyer
3. Escalate to the appropriate legal process if unresolved (Rent Control Act procedures in Tamil Nadu)

Do not allow disputes to escalate silently. Set escalation timelines in advance with your property manager.

<h2>Move-Out and Deposit Settlement</h2>

When a tenant vacates:
- Conduct a move-out inspection with photos before returning the deposit
- Deduct documented repair costs for damages beyond normal wear and tear
- Return the balance deposit within the agreed timeline (typically 15–30 days after move-out)
- Obtain a written no-dues confirmation from the tenant

<h2>Frequently Asked Questions</h2>

<strong>Can I rent out my property in Chennai without visiting India?</strong>
Yes. With a professional property manager handling sourcing, screening, agreement, and ongoing operations, NRIs routinely manage tenanted properties without visiting India.

<strong>How do I ensure my tenant pays rent on time when I am abroad?</strong>
Set up a direct bank transfer mandate, establish clear due dates, and ensure your property manager follows a documented escalation process for late payments.

<strong>What is the security deposit standard in Chennai?</strong>
In Chennai, the advance deposit (often called kaanom or advance) for residential properties is typically 6–10 months' rent, significantly higher than in other Indian cities. Confirm the deposit terms in writing before finalising a tenant.

For NRI rental management in Chennai, <a href="/chennai/nri-rental-management/">see our rental management service</a> or <a href="/contact/">speak to our team</a>.
""",
    },
    {
        "slug": "nri-property-maintenance-checklist",
        "title": "NRI Property Maintenance Checklist",
        "category": "maintenance",
        "author": "Propertism Advisory Team",
        "excerpt": (
            "A practical property maintenance checklist for NRIs managing Chennai property from abroad. "
            "Covers vacant property care, scheduled inspections, preventive maintenance, and vendor management."
        ),
        "content": """Property maintenance is the most neglected aspect of NRI property ownership — until something goes wrong. A vacant or poorly-maintained property deteriorates faster than an occupied one, and deferred maintenance compounds into expensive repairs. This checklist gives NRI property owners a structured approach to protecting their asset from abroad.

<h2>Vacant Property Maintenance</h2>

Vacant properties are more vulnerable than occupied ones. Without regular occupancy, issues like seepage, electrical faults, pest infestations, and structural deterioration go unnoticed.

<strong>Monthly checks for vacant properties:</strong>
- Open all windows and doors for ventilation
- Run all water outlets (taps, flush tanks, drainage) to prevent pipe blockages and stagnation
- Check for water seepage in walls, ceilings, and bathrooms
- Inspect for pest activity (termites, rodents, dampness-related growth)
- Verify all electrical switches and circuit breakers are functional
- Check locks and security systems

<h2>Annual Maintenance Tasks</h2>

These should be scheduled once a year regardless of occupancy:

- <strong>Waterproofing inspection:</strong> Check terrace, external walls, and bathroom tiles for cracks or seepage. Repair before monsoon season.
- <strong>Electrical check:</strong> Have a qualified electrician inspect wiring, distribution boards, and earthing.
- <strong>Plumbing check:</strong> Inspect all pipes, tanks (overhead and sump), and drainage lines for blockages or leaks.
- <strong>Exterior painting:</strong> Repaint exterior surfaces every 3–5 years to prevent moisture infiltration.
- <strong>Pest control treatment:</strong> Annual preventive pest control, particularly for termites in wood-framed structures.

<h2>Monsoon Preparation (Pre-June Checklist)</h2>

Chennai experiences heavy monsoon rains. Before the season:

- Clear roof drains, gutters, and drainage pipes
- Inspect terrace waterproofing and reseal cracks
- Check window seals and door frames for gaps
- Verify boundary wall integrity
- Ensure sump and overhead tank connections are sealed

<h2>Maintenance for Tenanted Properties</h2>

Tenants are responsible for day-to-day cleanliness and minor wear-and-tear maintenance (replacing bulbs, cleaning drains). Owner responsibilities typically include:

- Structural repairs
- Plumbing and electrical failures not caused by tenant misuse
- Appliance repairs if included in the lease
- Building exterior maintenance

Define these in the rental agreement to avoid disputes.

<h2>Vendor Management for NRIs</h2>

NRIs cannot supervise vendors directly. Without oversight, maintenance work may be substandard, overpriced, or incomplete.

Best practices:
- Use a property manager with a pre-verified vendor network
- Require photo/video documentation before and after repairs
- Set approval limits (e.g., your manager can approve repairs up to ₹5,000 without consultation; above that, they must notify you)
- Request itemised bills, not lump-sum quotes

<h2>Emergency Maintenance Protocol</h2>

Establish in advance what constitutes an emergency and how it is handled:
- Burst pipe or flooding: Immediate action without owner approval
- Electrical fault: Immediate action
- Break-in or security breach: Immediate action + police report
- Significant structural damage: Notify owner within 24 hours before proceeding

<h2>Frequently Asked Questions</h2>

<strong>How often should an NRI property be inspected?</strong>
Monthly for vacant properties; quarterly for tenanted properties. Video inspections sent to the owner after each visit.

<strong>What is the most common maintenance issue in Chennai NRI properties?</strong>
Water seepage and terrace waterproofing failures. Chennai's monsoons and aging construction make this the most frequent and costly maintenance item for NRI-owned properties.

<strong>Can I approve maintenance remotely?</strong>
Yes. A good property manager sends documented quotes and photos for your approval before proceeding on non-emergency repairs above your agreed threshold.

For professional property maintenance support in Chennai, <a href="/chennai/nri-property-maintenance/">see our maintenance service</a> or <a href="/contact/">contact our team</a>.
""",
    },
]


class Command(BaseCommand):
    help = "Seed Knowledge Hub Phase-A articles as BlogPost records (skips existing slugs)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--publish",
            action="store_true",
            help="Mark all seeded articles as published (default: draft)",
        )

    def handle(self, *args, **options):
        publish = options["publish"]
        created_count = skipped = 0

        for data in ARTICLES:
            post, is_new = BlogPost.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "category": data["category"],
                    "author": data["author"],
                    "excerpt": data["excerpt"],
                    "content": data["content"],
                    "is_published": publish,
                    "published_date": timezone.now(),
                }
            )

            if not is_new:
                if publish:
                    post.is_published = True
                    post.published_date = timezone.now()
                    post.save(update_fields=["is_published", "published_date"])
                    self.stdout.write(self.style.SUCCESS(f"  PUBLISHED (updated): {data['slug']}"))
                else:
                    self.stdout.write(f"  SKIP (exists): {data['slug']}")
                skipped += 1
            else:
                status = "PUBLISHED" if publish else "DRAFT"
                self.stdout.write(self.style.SUCCESS(f"  {status}: {data['slug']}"))
                created_count += 1

        self.stdout.write(f"\nDone. Created: {created_count}  Skipped: {skipped}")
        if not publish:
            self.stdout.write("Re-run with --publish to mark all as published.")
