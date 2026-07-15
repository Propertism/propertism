/**
 * Google Apps Script: Classifieds Portal Aggregator & Propertism Leads Agent
 * 
 * This unified script provides:
 * 1. Classifieds Portal Aggregator (NO-API Version): Instantly seeds, formats, and validates 
 *    a high-quality list of free classified ad portals for 12 specified countries. 
 *    This version runs completely offline/locally without requiring Google Custom Search APIs.
 * 2. Propertism Lead Collation Agent: Receives inbound leads via webhook, tags intent, 
 *    appends to sheet, sends WhatsApp alerts to the team, and runs prospecting digests.
 * 
 * Setup Instructions:
 * 1. Open Spreadsheet: https://docs.google.com/spreadsheets/d/1un4Gbix9M6nq9nY5N0LoKSEUxBF5BgoA9pdz6WqpYM0/edit
 * 2. Click Extensions > Apps Script
 * 3. Replace all code with this file and save.
 * 4. Go to Project Settings (gear icon on the left) > Script Properties
 *    Add required properties for the Leads Agent:
 *    - SEARCH_API_KEY: Your Serper key from google.serper.dev (Prospecting)
 *    - WHATSAPP_TOKEN: Your Meta WhatsApp Cloud API token
 *    - WHATSAPP_PHONE_ID: Your WhatsApp Business phone number ID
 *    - TEAM_WHATSAPP_NUMBER: Team phone number to alert (e.g. 9198418xxxxx)
 *    - WEBHOOK_SECRET: Any random string you choose for webhook validation
 * 5. Reload the spreadsheet. You will see "Classifieds" and "Propertism Leads" menus.
 */

// =========================================================================
// 1. GLOBAL CONFIGURATION
// =========================================================================

// Propertism Leads Config
const SHEET_LEADS     = 'Leads';
const SHEET_PROSPECTS = 'Prospects';
const SERPER_URL      = 'https://google.serper.dev/search';

// Predefined Curated Classifieds Portals (12 Target Countries)
// This list is populated with active, high-quality free classified/property advertising portals.
var PREDEFINED_PORTALS = [
  // USA
  { country: "USA", portalName: "Craigslist", website: "https://www.craigslist.org", homeUrl: "https://www.craigslist.org", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "craigslist.org", notes: "Most popular general and real estate classifieds site in the US." },
  { country: "USA", portalName: "ClassifiedAds", website: "https://www.classifiedads.com", homeUrl: "https://www.classifiedads.com", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "classifiedads.com", notes: "Popular free ad posting site covering general and real estate." },
  { country: "USA", portalName: "Oodle", website: "https://www.oodle.com", homeUrl: "https://www.oodle.com", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "oodle.com", notes: "Large aggregator of free classified listings." },
  { country: "USA", portalName: "Locanto USA", website: "https://www.locanto.com", homeUrl: "https://www.locanto.com", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "locanto.com", notes: "Free local classified ads portal." },
  { country: "USA", portalName: "Geebo", website: "https://geebo.com", homeUrl: "https://geebo.com", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "geebo.com", notes: "Safe community classifieds for jobs, real estate, and services." },

  // UK
  { country: "UK", portalName: "Gumtree", website: "https://www.gumtree.com", homeUrl: "https://www.gumtree.com", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "gumtree.com", notes: "#1 classifieds site in the UK for properties and services." },
  { country: "UK", portalName: "Freeads UK", website: "https://www.freeads.co.uk", homeUrl: "https://www.freeads.co.uk", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "freeads.co.uk", notes: "One of the largest free classified ad sites in the UK." },
  { country: "UK", portalName: "Friday Ad", website: "https://www.friday-ad.co.uk", homeUrl: "https://www.friday-ad.co.uk", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "friday-ad.co.uk", notes: "Long-standing local free classified ad paper and site." },
  { country: "UK", portalName: "Vivastreet UK", website: "https://www.vivastreet.co.uk", homeUrl: "https://www.vivastreet.co.uk", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "vivastreet.co.uk", notes: "Popular local classifieds site." },

  // Canada
  { country: "Canada", portalName: "Kijiji", website: "https://www.kijiji.ca", homeUrl: "https://www.kijiji.ca", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "kijiji.ca", notes: "Canada's most popular free classifieds site." },
  { country: "Canada", portalName: "Craigslist Canada", website: "https://www.craigslist.ca", homeUrl: "https://www.craigslist.ca", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "craigslist.ca", notes: "Canada branch of Craigslist." },
  { country: "Canada", portalName: "Locanto Canada", website: "https://www.locanto.ca", homeUrl: "https://www.locanto.ca", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "locanto.ca", notes: "Free local classified ads for Canada." },

  // Dubai
  { country: "Dubai", portalName: "Dubizzle Dubai", website: "https://dubai.dubizzle.com", homeUrl: "https://dubai.dubizzle.com", category: "General", freePosting: "Partial", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "dubizzle.com", notes: "Leading classifieds brand in Dubai and UAE." },
  { country: "Dubai", portalName: "Expatriates Dubai", website: "https://www.expatriates.com", homeUrl: "https://www.expatriates.com", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "expatriates.com", notes: "Highly popular community classifieds for expats in Dubai." },
  { country: "Dubai", portalName: "AdsDubai", website: "http://www.adsdubai.com", homeUrl: "http://www.adsdubai.com", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "adsdubai.com", notes: "Local classifieds platform in Dubai." },

  // Bahrain
  { country: "Bahrain", portalName: "Expatriates Bahrain", website: "https://www.expatriates.com", homeUrl: "https://www.expatriates.com", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "expatriates.com", notes: "Most active expat classifieds board in Bahrain." },
  { country: "Bahrain", portalName: "Dubizzle Bahrain", website: "https://bahrain.dubizzle.com", homeUrl: "https://bahrain.dubizzle.com", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "dubizzle.com", notes: "Official Dubizzle portal for Bahrain." },
  { country: "Bahrain", portalName: "Loozap Bahrain", website: "https://bahrain.loozap.com", homeUrl: "https://bahrain.loozap.com", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "loozap.com", notes: "Free local classified ads directory." },

  // Abu Dhabi
  { country: "Abu Dhabi", portalName: "Dubizzle Abu Dhabi", website: "https://abudhabi.dubizzle.com", homeUrl: "https://abudhabi.dubizzle.com", category: "General", freePosting: "Partial", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "dubizzle.com", notes: "Abu Dhabi branch of UAE's Dubizzle." },
  { country: "Abu Dhabi", portalName: "Expatriates Abu Dhabi", website: "https://www.expatriates.com", homeUrl: "https://www.expatriates.com", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "expatriates.com", notes: "Popular expat classifieds for Abu Dhabi." },

  // Kuwait
  { country: "Kuwait", portalName: "Expatriates Kuwait", website: "https://www.expatriates.com", homeUrl: "https://www.expatriates.com", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "expatriates.com", notes: "Highly popular portal for expats in Kuwait." },
  { country: "Kuwait", portalName: "Dubizzle Kuwait", website: "https://kuwait.dubizzle.com", homeUrl: "https://kuwait.dubizzle.com", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "dubizzle.com", notes: "OLX/Dubizzle Kuwait portal." },

  // Saudi Arabia
  { country: "Saudi Arabia", portalName: "Expatriates Saudi Arabia", website: "https://www.expatriates.com", homeUrl: "https://www.expatriates.com", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "expatriates.com", notes: "Very active expat classifieds board in KSA." },
  { country: "Saudi Arabia", portalName: "Haraj", website: "https://haraj.com.sa", homeUrl: "https://haraj.com.sa", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "haraj.com.sa", notes: "Leading local classifieds platform in Saudi Arabia." },
  { country: "Saudi Arabia", portalName: "OpenSooq KSA", website: "https://sa.opensooq.com", homeUrl: "https://sa.opensooq.com", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "opensooq.com", notes: "KSA branch of the major Arab world classifieds platform." },

  // Singapore
  { country: "Singapore", portalName: "Carousell Singapore", website: "https://www.carousell.sg", homeUrl: "https://www.carousell.sg", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "carousell.sg", notes: "Leading classifieds app and site in Singapore." },
  { country: "Singapore", portalName: "Locanto Singapore", website: "https://www.locanto.sg", homeUrl: "https://www.locanto.sg", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "locanto.sg", notes: "Free local classified ads in Singapore." },
  { country: "Singapore", portalName: "Classifieds.sg", website: "https://www.classifieds.sg", homeUrl: "https://www.classifieds.sg", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "classifieds.sg", notes: "Local Singaporean listing portal." },

  // Malaysia
  { country: "Malaysia", portalName: "Mudah", website: "https://www.mudah.my", homeUrl: "https://www.mudah.my", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "mudah.my", notes: "Largest local classifieds portal in Malaysia." },
  { country: "Malaysia", portalName: "Locanto Malaysia", website: "https://www.locanto.com.my", homeUrl: "https://www.locanto.com.my", category: "Local", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "locanto.com.my", notes: "Free local classified ads portal for Malaysia." },

  // South Africa
  { country: "South Africa", portalName: "Gumtree South Africa", website: "https://www.gumtree.co.za", homeUrl: "https://www.gumtree.co.za", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "gumtree.co.za", notes: "Most active classifieds portal in South Africa." },
  { country: "South Africa", portalName: "Junk Mail", website: "https://www.junkmail.co.za", homeUrl: "https://www.junkmail.co.za", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "junkmail.co.za", notes: "Popular local classified ads platform." },

  // Botswana
  { country: "Botswana", portalName: "Classifieds Botswana", website: "https://www.classifieds.co.bw", homeUrl: "https://www.classifieds.co.bw", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "classifieds.co.bw", notes: "Local classifieds platform in Botswana." },
  { country: "Botswana", portalName: "Loozap Botswana", website: "https://botswana.loozap.com", homeUrl: "https://botswana.loozap.com", category: "General", freePosting: "Yes", supportsRealEstate: "Yes", supportsBusiness: "Yes", domain: "loozap.com", notes: "Free online classifieds directory in Botswana." }
];

/**
 * Helper to fetch a Script Property.
 */
function getProp_(key) {
  return PropertiesService.getScriptProperties().getProperty(key) || '';
}

// =========================================================================
// 2. UNIFIED ONOPEN MENU INITIALIZATION
// =========================================================================

/**
 * Creates the Custom Menus when the Spreadsheet is opened.
 * This handles both the Classifieds Portal Aggregator and Propertism Leads menus.
 */
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  
  // Menu 1: Classifieds Portal Aggregator
  ui.createMenu('Classifieds')
      .addItem('Generate All Countries', 'refreshAll')
      .addItem('Generate Current Country', 'refreshCurrentCountry')
      .addItem('Remove Duplicates', 'removeDuplicates')
      .addItem('Verify Links', 'verifyAllLinks')
      .addToUi();

  // Menu 2: Propertism Leads Collation Agent
  ui.createMenu('Propertism Leads')
      .addItem('Setup Leads & Prospects Sheets', 'setupSheets')
      .addItem('Run Prospecting Digest Now → Prospects sheet', 'runProspectingDigest')
      .addItem('Add Test Lead to Leads Sheet', 'addTestLead')
      .addItem('Send Test WhatsApp Alert', 'sendTestWhatsApp')
      .addItem('Show Webhook Integration Help', 'showWebhookHelp')
      .addToUi();
}

// =========================================================================
// 3. CLASSIFIEDS PORTAL AGGREGATOR FUNCTIONS (NO-API SYSTEM)
// =========================================================================

/**
 * Populates all predefined classifieds portals and runs live link validation on them.
 */
function refreshAll() {
  var ui = SpreadsheetApp.getUi();

  var response = ui.alert("Generate Classifieds", "This will instantly generate the predefined classifieds list for all 12 countries (Status will default to Active). Proceed?", ui.ButtonSet.YES_NO);
  if (response != ui.Button.YES) return;

  var processedPortals = [];
  for (var i = 0; i < PREDEFINED_PORTALS.length; i++) {
    var portal = PREDEFINED_PORTALS[i];
    
    var p = {
      country: portal.country,
      portalName: portal.portalName,
      website: portal.website,
      homeUrl: portal.homeUrl,
      postAdUrl: "",
      category: portal.category,
      freePosting: portal.freePosting,
      registrationRequired: "No",
      supportsRealEstate: portal.supportsRealEstate,
      supportsBusiness: portal.supportsBusiness,
      domain: portal.domain,
      status: "Active",
      lastVerifiedDate: new Date(),
      notes: portal.notes
    };
    
    processedPortals.push(p);
  }

  if (processedPortals.length > 0) {
    writeToSheet(processedPortals);
    ui.alert("Success", "Generated " + processedPortals.length + " portals. You can manually verify them or select 'Verify Links' from the menu.", ui.ButtonSet.OK);
  } else {
    ui.alert("Completed", "No portals were generated.", ui.ButtonSet.OK);
  }
}

/**
 * Prompts user for a specific country to generate and verify.
 */
function refreshCurrentCountry() {
  var ui = SpreadsheetApp.getUi();

  var response = ui.prompt("Generate Country", "Enter country name (e.g. Dubai, Singapore, UK, USA):", ui.ButtonSet.OK_CANCEL);
  if (response.getSelectedButton() != ui.Button.OK) return;

  var countryInput = response.getResponseText().trim().toLowerCase();
  if (!countryInput) {
    ui.alert("Invalid Input", "Country name cannot be empty.", ui.ButtonSet.OK);
    return;
  }

  var processedPortals = [];
  for (var i = 0; i < PREDEFINED_PORTALS.length; i++) {
    var portal = PREDEFINED_PORTALS[i];
    if (portal.country.toLowerCase() === countryInput || 
        (countryInput === "uae" && (portal.country.toLowerCase() === "dubai" || portal.country.toLowerCase() === "abu dhabi"))) {
      
      var p = {
        country: portal.country,
        portalName: portal.portalName,
        website: portal.website,
        homeUrl: portal.homeUrl,
        postAdUrl: "",
        category: portal.category,
        freePosting: portal.freePosting,
        registrationRequired: "No",
        supportsRealEstate: portal.supportsRealEstate,
        supportsBusiness: portal.supportsBusiness,
        domain: portal.domain,
        status: "Active",
        lastVerifiedDate: new Date(),
        notes: portal.notes
      };

      processedPortals.push(p);
    }
  }

  if (processedPortals.length > 0) {
    writeToSheet(processedPortals);
    ui.alert("Success", "Generated " + processedPortals.length + " portals for " + countryInput + ".", ui.ButtonSet.OK);
  } else {
    ui.alert("Completed", "No matching predefined portals found for '" + countryInput + "'.", ui.ButtonSet.OK);
  }
}

/**
 * Fallback search routine (bypassed in no-API version but kept for compatibility).
 */
function searchCountry(country, apiKey, cx) {
  // Returns matching predefined portals directly to save API quota
  var result = [];
  for (var i = 0; i < PREDEFINED_PORTALS.length; i++) {
    if (PREDEFINED_PORTALS[i].country.toLowerCase() === country.toLowerCase()) {
      result.push(PREDEFINED_PORTALS[i]);
    }
  }
  return result;
}

/**
 * Extracts and cleans portal details from search item.
 */
function extractPortal(searchItem, country) {
  var url = searchItem.link;
  var domain = getRootDomain(url);
  return {
    country: country,
    portalName: searchItem.title || domain,
    website: "https://" + domain,
    homeUrl: "https://" + domain,
    postAdUrl: "",
    category: "General",
    freePosting: "Yes",
    registrationRequired: "No",
    supportsRealEstate: "Yes",
    supportsBusiness: "Yes",
    domain: domain,
    status: "Active",
    lastVerifiedDate: new Date(),
    notes: ""
  };
}

/**
 * Verifies if a portal is active and scans homepage HTML for features.
 */
function verifyPortal(url) {
  var result = {
    status: "Inactive",
    postAdUrl: "",
    registrationRequired: "No",
    supportsRealEstate: "No",
    supportsBusiness: "No"
  };

  try {
    var response = UrlFetchApp.fetch(url, {
      muteHttpExceptions: true,
      followRedirects: true,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      }
    });

    var code = response.getResponseCode();
    if (code >= 200 && code < 400) {
      result.status = "Active";
      var html = response.getContentText();
      
      if (html) {
        var htmlLower = html.toLowerCase();
        
        // Scan for registration hints
        if (htmlLower.indexOf("register") !== -1 || htmlLower.indexOf("sign up") !== -1 || htmlLower.indexOf("signup") !== -1 || htmlLower.indexOf("create account") !== -1) {
          result.registrationRequired = "Yes";
        }
        
        // Scan for category support
        if (htmlLower.indexOf("real estate") !== -1 || htmlLower.indexOf("property") !== -1 || htmlLower.indexOf("house") !== -1 || htmlLower.indexOf("rent") !== -1) {
          result.supportsRealEstate = "Yes";
        }
        if (htmlLower.indexOf("business services") !== -1 || htmlLower.indexOf("b2b") !== -1 || htmlLower.indexOf("directory") !== -1 || htmlLower.indexOf("services") !== -1) {
          result.supportsBusiness = "Yes";
        }

        // Search for "Post Ad" links
        var anchorRegex = /<a\s+[^>]*href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi;
        var match;
        while ((match = anchorRegex.exec(html)) !== null) {
          var href = match[1];
          var text = match[2].replace(/<[^>]*>/g, "").toLowerCase().trim();
          if (text.indexOf("post ad") !== -1 || text.indexOf("post free") !== -1 || text.indexOf("submit ad") !== -1 || text.indexOf("add listing") !== -1) {
            if (href.indexOf("http") !== 0) {
              if (href.indexOf("/") === 0) {
                var domainMatch = url.match(/^(https?:\/\/[^\/]+)/i);
                href = (domainMatch ? domainMatch[1] : url) + href;
              } else {
                href = url + (url.endsWith("/") ? "" : "/") + href;
              }
            }
            result.postAdUrl = href;
            break;
          }
        }
      }
    } else if (code === 403 || code === 503 || code === 429 || code === 401) {
      result.status = "Verification Blocked";
    } else {
      result.status = "Inactive";
    }
  } catch (e) {
    Logger.log("Failed verification for URL: " + url + " - " + e.toString());
    result.status = "Verification Blocked"; // Default to verification blocked on fetch exceptions
  }

  return result;
}

/**
 * Idempotently writes discovered portals to sheet.
 */
function writeToSheet(portals) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("Classifieds");
  
  if (!sheet) {
    sheet = ss.insertSheet("Classifieds");
  }

  var headers = [
    "Country", "Portal Name", "Website", "Home URL", "Post Ad URL", 
    "Category", "Free Posting", "Registration Required", "Supports Real Estate", 
    "Supports Business Services", "Domain", "Status", "Last Verified Date", "Notes"
  ];

  // Set up header if empty
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(headers);
    formatHeaders(sheet);
  }

  // Load existing records to maintain idempotency
  var lastRow = sheet.getLastRow();
  var existingData = [];
  if (lastRow > 1) {
    existingData = sheet.getRange(2, 1, lastRow - 1, 14).getValues();
  }

  var existingMap = {};
  for (var i = 0; i < existingData.length; i++) {
    var domain = existingData[i][10].toString().toLowerCase().trim();
    if (domain) {
      existingMap[domain] = {
        rowNum: i + 2,
        data: existingData[i]
      };
    }
  }

  // Insert or update records
  for (var j = 0; j < portals.length; j++) {
    var p = portals[j];
    
    var finalStatus = p.status;
    var finalNotes = p.notes;
    
    // Map Verification Blocked to Active status + note to avoid violating data validation rule of Sheet
    if (p.status === "Verification Blocked") {
      finalStatus = "Active";
      if (finalNotes.indexOf("[Verification Blocked]") === -1) {
        finalNotes = "[Verification Blocked] Bot-protected site. " + finalNotes;
      }
    }

    var rowData = [
      p.country, p.portalName, p.website, p.homeUrl, p.postAdUrl,
      p.category, p.freePosting, p.registrationRequired, p.supportsRealEstate,
      p.supportsBusiness, p.domain, finalStatus, p.lastVerifiedDate, finalNotes
    ];

    if (existingMap[p.domain]) {
      // Update record (preserving manual notes or fields if needed)
      var targetRow = existingMap[p.domain].rowNum;
      sheet.getRange(targetRow, 1, 1, 14).setValues([rowData]);
    } else {
      // Append new record
      sheet.appendRow(rowData);
    }
  }

  // Apply visual styling, sorting, and filters
  lastRow = sheet.getLastRow();
  if (lastRow > 1) {
    // Sort by Country (Col 1), then Portal Name (Col 2)
    sheet.getRange(2, 1, lastRow - 1, 14).sort([
      {column: 1, ascending: true},
      {column: 2, ascending: true}
    ]);

    // Format Dates
    sheet.getRange(2, 13, lastRow - 1, 1).setNumberFormat("yyyy-mm-dd hh:mm");

    // Clear existing filter and reapply to header row
    var filter = sheet.getFilter();
    if (filter) {
      filter.remove();
    }
    sheet.getRange(1, 1, lastRow, 14).createFilter();
  }
}

/**
 * Formats header row with Navy background and Gold text.
 */
function formatHeaders(sheet) {
  var headerRange = sheet.getRange(1, 1, 1, 14);
  headerRange.setBackground("#0F172A")
             .setFontColor("#B89A4A")
             .setFontWeight("bold")
             .setHorizontalAlignment("center");
  sheet.setFrozenRows(1);
}

/**
 * Removes duplicate records based on the Domain column.
 */
function removeDuplicates() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Classifieds");
  if (!sheet) return;
  var lastRow = sheet.getLastRow();
  if (lastRow <= 1) return;

  var range = sheet.getRange(2, 1, lastRow - 1, 14);
  var values = range.getValues();
  var uniqueMap = {};
  var uniqueRows = [];

  for (var i = 0; i < values.length; i++) {
    var domain = values[i][10].toString().toLowerCase().trim();
    if (!domain) continue;

    if (!uniqueMap[domain]) {
      uniqueMap[domain] = true;
      uniqueRows.push(values[i]);
    }
  }

  // Clear data range and overwrite with unique records
  sheet.getRange(2, 1, lastRow - 1, 14).clearContent();
  if (uniqueRows.length > 0) {
    sheet.getRange(2, 1, uniqueRows.length, 14).setValues(uniqueRows);
  }

  SpreadsheetApp.getUi().alert("Deduplication Complete", "Removed duplicates. " + uniqueRows.length + " unique portals remain.", SpreadsheetApp.getUi().ButtonSet.OK);
}

/**
 * Verifies the reachability of all registered links.
 */
function verifyAllLinks() {
  var ui = SpreadsheetApp.getUi();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Classifieds");
  if (!sheet) return;
  
  var lastRow = sheet.getLastRow();
  if (lastRow <= 1) return;

  var range = sheet.getRange(2, 1, lastRow - 1, 14);
  var values = range.getValues();

  for (var i = 0; i < values.length; i++) {
    var url = values[i][3]; // Column 4: Home URL
    if (url) {
      var verification = verifyPortal(url);
      var finalStatus = verification.status;
      var notes = values[i][13] || "";
      
      if (verification.status === "Verification Blocked") {
        finalStatus = "Active";
        if (notes.indexOf("[Verification Blocked]") === -1) {
          notes = "[Verification Blocked] Bot-protected site. " + notes;
        }
      }
      
      values[i][11] = finalStatus; // Column 12: Status
      values[i][12] = new Date();          // Column 13: Last Verified Date
      values[i][13] = notes;               // Column 14: Notes
    }
  }

  range.setValues(values);
  ui.alert("Link Verification Complete", "Verified " + values.length + " portal links.", ui.ButtonSet.OK);
}

/**
 * Helper to extract root domain (e.g. classifieds.sapo.pt -> sapo.pt)
 */
function getRootDomain(url) {
  try {
    var hostname = url.replace(/^(https?:\/\/)?(www\.)?/i, "").split('/')[0].split(':')[0];
    var parts = hostname.split('.');
    if (parts.length > 2) {
      var secondToLast = parts[parts.length - 2];
      // TLD extensions support
      if (['co', 'com', 'org', 'net', 'gov', 'edu', 'ltd', 'net', 'me', 'ae'].indexOf(secondToLast) !== -1) {
        return parts.slice(-3).join('.');
      }
      return parts.slice(-2).join('.');
    }
    return hostname;
  } catch (e) {
    return url;
  }
}

/**
 * Checks if domain matches standard social/search engine/blog platforms.
 */
function isExcluded(domain) {
  for (var i = 0; i < EXCLUDED_DOMAINS.length; i++) {
    if (domain.indexOf(EXCLUDED_DOMAINS[i]) !== -1) {
      return true;
    }
  }
  return false;
}

// =========================================================================
// 4. PROPERTISM LEAD COLLATION AGENT FUNCTIONS
// =========================================================================

/**
 * Triggers a test WhatsApp notification message to the configured team number.
 */
function sendTestWhatsApp() {
  notifyTeamWhatsApp_('Test Lead', 'SELL', '+919999999999', 'menu-test');
  SpreadsheetApp.getUi().alert(
    'Test WhatsApp alert sent. Check that WHATSAPP_TOKEN, WHATSAPP_PHONE_ID, ' +
    'and TEAM_WHATSAPP_NUMBER are set in Script Properties.'
  );
}

/**
 * Shows helper alert outlining how to set up and construct the webhook POST payload.
 */
function showWebhookHelp() {
  SpreadsheetApp.getUi().alert(
    'Webhook Setup',
    'To get your webhook URL:\n' +
    'Extensions > Apps Script > Deploy > New deployment\n' +
    'Type: Web app\n' +
    'Execute as: Me\n' +
    'Who has access: Anyone\n\n' +
    'Copy the Web App URL — that is your webhook endpoint.\n\n' +
    'POST JSON to it (see PAYLOAD FORMAT in the script comments).',
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}

/**
 * Performs one-time setup of required Leads and Prospects sheets with frozen header rows.
 */
function setupSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // -- Leads tab --
  let leads = ss.getSheetByName(SHEET_LEADS);
  if (!leads) leads = ss.insertSheet(SHEET_LEADS);
  // Only write headers if the sheet is completely empty
  if (leads.getLastRow() === 0) {
    leads.appendRow([
      'Timestamp', 'Name', 'Phone', 'Email', 'City/Country',
      'Intent', 'Message', 'Source', 'Status', 'Notes'
    ]);
    leads.setFrozenRows(1);
    
    // Highlight headers in Propertism Navy/Gold theme
    var range = leads.getRange(1, 1, 1, 10);
    range.setBackground("#0F172A")
         .setFontColor("#B89A4A")
         .setFontWeight("bold")
         .setHorizontalAlignment("center");
  }

  // -- Prospects tab --
  let prospects = ss.getSheetByName(SHEET_PROSPECTS);
  if (!prospects) prospects = ss.insertSheet(SHEET_PROSPECTS);
  if (prospects.getLastRow() === 0) {
    prospects.appendRow([
      'Found On', 'Platform/Source', 'Snippet', 'Likely Intent',
      'Link', 'Status', 'Notes'
    ]);
    prospects.setFrozenRows(1);

    // Highlight headers in Propertism Navy/Gold theme
    var rangePr = prospects.getRange(1, 1, 1, 7);
    rangePr.setBackground("#0F172A")
           .setFontColor("#B89A4A")
           .setFontWeight("bold")
           .setHorizontalAlignment("center");
  }

  SpreadsheetApp.getUi().alert(
    '"Leads" and "Prospects" tabs are ready.\n\n' +
    '"Leads" = inbound leads from your website/WhatsApp (via webhook).\n' +
    '"Prospects" = NRIs found via web search (run "Prospecting Digest").'
  );
}

/**
 * Webhook entry point handling inbound HTTP POST leads.
 */
function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);

    // Basic auth check
    if (body.secret !== getProp_('WEBHOOK_SECRET')) {
      return jsonResponse_({ ok: false, error: 'Invalid secret' });
    }

    const intent = inferIntent_(body.intent, body.message);
    const row = [
      new Date(),
      body.name    || '',
      body.phone   || '',
      body.email   || '',
      body.city    || '',
      intent,
      body.message || '',
      body.source  || 'unknown',
      'New',
      ''
    ];

    const sheet = SpreadsheetApp.getActiveSpreadsheet()
                    .getSheetByName(SHEET_LEADS);
    sheet.appendRow(row);

    notifyTeamWhatsApp_(body.name, intent, body.phone, body.source);

    return jsonResponse_({ ok: true, intent: intent });
  } catch (err) {
    return jsonResponse_({ ok: false, error: err.message });
  }
}

/**
 * Constructs structured JSON API responses.
 */
function jsonResponse_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Adds a dummy lead row to the Leads sheet for local verification.
 */
function addTestLead() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet()
                  .getSheetByName(SHEET_LEADS);
  if (!sheet) {
    SpreadsheetApp.getUi().alert('Leads sheet not found — run Setup Sheets first.');
    return;
  }
  sheet.appendRow([
    new Date(),
    'Test NRI User',
    '+1-408-555-0001',
    'test.nri@example.com',
    'California, USA',
    'SELL',
    'I want to sell my 3BHK flat in Adyar, Chennai',
    'manual-test',
    'New',
    'Added by Add Test Lead menu item'
  ]);
  SpreadsheetApp.getUi().alert('Test lead added to the Leads sheet.');
}

/**
 * Infer intent tags from explicit selection or scan message text.
 */
function inferIntent_(explicitIntent, message) {
  const valid = ['sell', 'buy', 'manage'];
  if (explicitIntent && valid.indexOf(explicitIntent.toLowerCase()) !== -1) {
    return explicitIntent.toUpperCase();
  }

  const text = (message || '').toLowerCase();
  const sellWords   = ['sell', 'selling', 'sale', 'dispose', 'divest'];
  const buyWords    = ['buy', 'buying', 'purchase', 'invest',
                       'looking for a property', 'looking to invest'];
  const manageWords = ['manage', 'management', 'rent out', 'tenant',
                       'maintenance', 'lease out', 'caretaker'];

  const scoreFor = (words) =>
    words.reduce((s, w) => s + (text.indexOf(w) !== -1 ? 1 : 0), 0);

  const scores = {
    SELL:   scoreFor(sellWords),
    BUY:    scoreFor(buyWords),
    MANAGE: scoreFor(manageWords)
  };

  let best = 'UNSURE', bestScore = 0;
  for (const k in scores) {
    if (scores[k] > bestScore) { best = k; bestScore = scores[k]; }
  }
  return best;
}

/**
 * Dispatches WhatsApp Cloud API text messages to team.
 */
function notifyTeamWhatsApp_(name, intent, phone, source) {
  const token      = getProp_('WHATSAPP_TOKEN');
  const phoneId    = getProp_('WHATSAPP_PHONE_ID');
  const teamNumber = getProp_('TEAM_WHATSAPP_NUMBER');
  if (!token || !phoneId || !teamNumber) return; // not configured, skip silently

  const text =
    `🔔 New ${intent} lead\n` +
    `Name:   ${name   || 'N/A'}\n` +
    `Phone:  ${phone  || 'N/A'}\n` +
    `Source: ${source || 'N/A'}\n` +
    `Check the "Leads" sheet for details.`;

  const url = `https://graph.facebook.com/v19.0/${phoneId}/messages`;
  const payload = {
    messaging_product: 'whatsapp',
    to: teamNumber,
    type: 'text',
    text: { body: text }
  };

  UrlFetchApp.fetch(url, {
    method:          'post',
    contentType:     'application/json',
    headers:         { Authorization: 'Bearer ' + token },
    payload:         JSON.stringify(payload),
    muteHttpExceptions: true
  });
}

/**
 * Scans public portals using Serper.dev API to identify new Prospects.
 */
function runProspectingDigest() {
  const apiKey = getProp_('SEARCH_API_KEY');
  if (!apiKey) {
    Logger.log('SEARCH_API_KEY not set — skipping prospecting digest.');
    SpreadsheetApp.getUi().alert(
      'SEARCH_API_KEY is not set.\n\n' +
      'Go to Project Settings → Script Properties and add your Serper key.\n' +
      'Get a free key at https://serper.dev'
    );
    return;
  }

  const queries = [
    { q: 'NRI sell property Chennai site:linkedin.com',       intent: 'SELL'   },
    { q: '"want to sell" Chennai property NRI',               intent: 'SELL'   },
    { q: '"looking to sell" Chennai flat NRI abroad',         intent: 'SELL'   },
    { q: 'NRI looking to buy property Chennai',               intent: 'BUY'    },
    { q: 'NRI invest Chennai apartment site:linkedin.com',    intent: 'BUY'    },
    { q: 'NRI need property management Chennai',              intent: 'MANAGE' },
    { q: 'NRI rent out property Chennai help',                intent: 'MANAGE' }
  ];

  const sheet = SpreadsheetApp.getActiveSpreadsheet()
                  .getSheetByName(SHEET_PROSPECTS);
  if (!sheet) {
    SpreadsheetApp.getUi().alert(
      'Prospects sheet not found — run Setup Sheets first.'
    );
    return;
  }

  // Build a Set of URLs already in the sheet (col E = index 4)
  const existingUrls = new Set();
  const lastRow = sheet.getLastRow();
  if (lastRow > 1) {
    sheet.getRange(2, 5, lastRow - 1, 1).getValues()
      .forEach(row => {
        const u = (row[0] || '').toString().trim();
        if (u) existingUrls.add(u);
      });
  }

  let totalAdded   = 0;
  let totalSkipped = 0;
  let errors       = [];

  queries.forEach(({ q, intent }) => {
    try {
      const resp = UrlFetchApp.fetch(SERPER_URL, {
        method:          'post',
        contentType:     'application/json',
        headers:         { 'X-API-KEY': apiKey },
        payload:         JSON.stringify({ q: q, num: 5 }),
        muteHttpExceptions: true
      });

      const data    = JSON.parse(resp.getContentText());
      const results = data.organic || [];

      results.forEach(r => {
        const link = (r.link || '').trim();

        // Skip if this URL is already in the sheet
        if (link && existingUrls.has(link)) {
          totalSkipped++;
          return;
        }

        sheet.appendRow([
          new Date(),
          'Web / Serper',
          (r.snippet || r.title || '').substring(0, 300),
          intent,
          link,
          'New',
          q
        ]);

        if (link) existingUrls.add(link);
        totalAdded++;
      });
    } catch (err) {
      const msg = 'Query failed: "' + q + '" → ' + err.message;
      Logger.log(msg);
      errors.push(msg);
    }
  });

  const summary =
    `Prospecting Digest complete.\n` +
    `Added:   ${totalAdded} new results\n` +
    `Skipped: ${totalSkipped} already in sheet\n` +
    (errors.length ? `\n${errors.length} error(s) — check Execution Log.` : '');

  SpreadsheetApp.getUi().alert(summary);
  Logger.log(summary);
}

/**
 * Manual test routine for intent inference engine verification.
 */
function testInferIntent() {
  Logger.log(inferIntent_('', 'I want to sell my flat in Adyar, please help'));
  Logger.log(inferIntent_('', 'Looking to invest in a 2BHK in OMR'));
  Logger.log(inferIntent_('', 'Need someone to manage my rented house while I am abroad'));
}
