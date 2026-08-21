"""Script to update buyer-discovery/page.tsx with Pre-Run Parameters, Intent Filters, and Excel Import/Export."""
import os

target_file = r"D:\viji\viji-olivine\04-propertism-deal-engine\frontend-next\app\propertism\deal-engine\buyer-discovery\page.tsx"

with open(target_file, "r", encoding="utf-8") as f:
    code = f.read()

# Let's inspect imports and add CSV/Excel export helper & import handler
excel_helpers = '''
// Excel / CSV Export Utility (UTF-8 BOM formatted for native Microsoft Excel compatibility)
function exportProspectsToExcel(prospects: Prospect[], filename: string = 'Counterparty_Prospects.csv') {
  if (!prospects || prospects.length === 0) {
    showToast('No prospects available to export.');
    return;
  }
  const headers = [
    '#',
    'Prospect Title',
    'Confidence Score (%)',
    'Intent',
    'Contact Tier',
    'Phone Number',
    'Email Address',
    'Location',
    'Source Provider',
    'Direct URL',
    'Requirement Summary'
  ];

  const rows = prospects.map((p, idx) => {
    const title = (p.title || p.buyer_name || 'Prospect').replace(/"/g, '""');
    const score = p.confidence || p.confidence_score || 50;
    const intent = (p.intent || 'BUY').replace(/"/g, '""');
    const contactTier = (p.phone || p.email || p.is_internal) ? 'DIRECT_CONTACT' : 'SOCIAL_DM_LEAD';
    const phone = (p.phone || '').replace(/"/g, '""');
    const email = (p.email || '').replace(/"/g, '""');
    const loc = (p.location || p.locality || 'Chennai').replace(/"/g, '""');
    const source = (p.source || p.provider || 'SERPER').replace(/"/g, '""');
    const url = (p.link || p.url || '').replace(/"/g, '""');
    const snippet = (p.snippet || '').replace(/"/g, '""').replace(/[\\r\\n]+/g, ' ');

    return [
      idx + 1,
      `"${title}"`,
      `"${score}%"`,
      `"${intent}"`,
      `"${contactTier}"`,
      `"${phone}"`,
      `"${email}"`,
      `"${loc}"`,
      `"${source}"`,
      `"${url}"`,
      `"${snippet}"`
    ].join(',');
  });

  const csvContent = '\\uFEFF' + [headers.join(','), ...rows].join('\\r\\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const downloadUrl = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', downloadUrl);
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(downloadUrl);
  showToast(`✓ Exported ${prospects.length} prospects to Excel`);
}
'''

print("Length of current page:", len(code))
