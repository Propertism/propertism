import random

def generate_post(platform, intent, geo):
    """
    Rule-based generator for real estate content targeting NRIs.
    Focus: Selling property in Chennai.
    Removed branding ties to Propertism.
    """
    platform = platform.lower()
    intent = intent.upper()
    geo = geo or "USA"
    
    # Templates for Selling Chennai properties for NRIs in the USA
    templates = {
        "linkedin": [
            {
                "headline": "Maximize Your Chennai Property Assets: Strategic Insights for {geo}-based NRIs",
                "body": "For many {geo}-based professionals, managing or deciding to sell property in Chennai can be a complex logistical challenge. Current market indicators show a strong surge in demand for premium residential zones.\n\nOur team specializes in helping the {geo} diaspora navigate the complete lifecycle of property divestment—from valuation to legal clearance—without requiring you to travel.\n\nIf you are looking to sell property in Chennai this quarter, we provide the quiet authority and precision you need.",
                "cta": "Reply 'SELL' or DM for a confidential consultation.",
                "hashtags": "#ChennaiRealEstate #NRIInvestment #PropertyManagement #SellProperty #USAtoChennai"
            },
            {
                "headline": "Liquidity & Legacy: Why NRIs in the {geo} are choosing to divest now.",
                "body": "The Chennai real estate landscape is shifting. For NRIs living in the {geo}, the current exchange rate paired with local demand spikes presents a unique window to sell property in Chennai and maximize returns.\n\nWe provide end-to-end support for {geo} residents, ensuring transparency and structural integrity in every transaction.",
                "cta": "Interested in a valuation? Comment 'SELL' below.",
                "hashtags": "#RealEstateChennai #NRIExitStrategy #USA #Chennai #InvestmentBanking"
            }
        ],
        "facebook": [
            {
                "headline": "🏠 Calling all Chennai NRIs in the {geo}! Thinking of selling?",
                "body": "We know how hard it is to manage your ancestral home or investment apartment in Chennai when you're thousands of miles away in the {geo}.\n\nDon't let your property sit vacant or incur maintenance headaches. The Chennai market is HOT right now, and motivated buyers are looking for homes just like yours! We handle everything locally so you don't have to fly down.",
                "cta": "Message us 'SELL' to get a free market estimate today! 📩",
                "hashtags": "#ChennaiNRIs #USA #ChennaiRealEstate #SellHome #HomeSellingTips"
            },
            {
                "headline": "Turning your Chennai Property into Dollars? 💵✈️",
                "body": "If you're an NRI in the {geo} holding on to property in Chennai, now might be the perfect time to sell property in Chennai. We've helped dozens of families in the {geo} transition their assets smoothly with zero stress.\n\nReady to see what your Chennai home is worth today?",
                "cta": "Click 'Learn More' or DM us 'SELL' to start the conversation!",
                "hashtags": "#ChennaiToUSA #NRILife #ChennaiHomes #PropertySale #SellWithConfidence"
            }
        ],
        "whatsapp": [
            {
                "body": "*URGENT for NRIs in {geo}: Sell Property in Chennai*\n\nHi! We're seeing huge demand for properties in Chennai. If you're based in the {geo} and looking to sell property in Chennai, we can handle the entire process for you remotely.\n\n✅ Legal Help\n✅ Documentation\n✅ Direct Buyers\n\nReply *SELL* to this message to get details!",
                "cta": "",
                "hashtags": ""
            },
            {
                "body": "📢 *Attention {geo} NRIs*\n\nPlanning to sell your Chennai house or plot? Avoid the travel stress. We specialize in assisting {geo}-based owners with seamless sales in Chennai.\n\nReply *SELL* for a quick callback.",
                "cta": "",
                "hashtags": ""
            }
        ]
    }

    # Fallback platform
    if platform not in templates:
        platform = "linkedin"

    selected_template = random.choice(templates[platform])
    
    # Compose text
    if platform == "whatsapp":
        generated_text = selected_template["body"].format(geo=geo)
    else:
        generated_text = f"{selected_template['headline'].format(geo=geo)}\n\n{selected_template['body'].format(geo=geo)}\n\n{selected_template['cta']}\n\n{selected_template['hashtags']}"

    return generated_text
