"""
Propertism Google Analytics 4 (GA4) CLI Interface
Author: Astra / Olivine Engineering
Usage:
    python scripts/get_analytics.py --summary
    python scripts/get_analytics.py --realtime
    python scripts/get_analytics.py --pages
    python scripts/get_analytics.py --sources
    python scripts/get_analytics.py --geo
"""

import os
import sys
import argparse
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    RunRealtimeReportRequest,
    Dimension,
    Metric,
    DateRange,
    OrderBy,
)

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
BASE_DIR = Path(__file__).resolve().parent.parent
CLIENT_SECRET_FILE = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "token.json"

def get_credentials():
    """Handles OAuth 2.0 user credentials flow and caching."""
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE.exists():
                print(f"❌ Error: {CLIENT_SECRET_FILE} not found!")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
            print("\n🔑 Initiating Google OAuth Login in your browser...")
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            print("✅ Token saved to token.json")
    
    return creds

def get_property_id(client, creds):
    """Discovers available GA4 Property IDs if not supplied via ENV or args."""
    prop_id = os.environ.get("GA4_PROPERTY_ID")
    if prop_id:
        return prop_id
    
    # Try reading from a local config if saved
    config_file = BASE_DIR / ".ga4_property_id"
    if config_file.exists():
        return config_file.read_text().strip()

    # Try listing account summaries via admin API or prompt
    try:
        from google.analytics.admin_v1alpha import AnalyticsAdminServiceClient
        admin_client = AnalyticsAdminServiceClient(credentials=creds)
        summaries = admin_client.list_account_summaries()
        for summary in summaries:
            for prop in summary.property_summaries:
                clean_id = prop.property.replace("properties/", "")
                print(f"📊 Auto-detected GA4 Property: {prop.display_name} (ID: {clean_id})")
                config_file.write_text(clean_id)
                return clean_id
    except Exception:
        pass

    # Prompt user if auto-detection is not available
    print("\nℹ️ Please enter your 9 or 10-digit GA4 Property ID.")
    print("   (Find it in Google Analytics > Admin > Property Settings > Property Details > Property ID)")
    p_id = input("GA4 Property ID: ").strip()
    if p_id:
        config_file.write_text(p_id)
        return p_id
    
    print("❌ GA4 Property ID is required.")
    sys.exit(1)

def print_header(title):
    print("\n" + "=" * 65)
    print(f"  📊 {title.upper()}")
    print("=" * 65)

def run_realtime(client, property_id):
    """Fetches realtime active users in last 30 minutes."""
    print_header("Real-Time Active Traffic (Last 30 Mins)")
    request = RunRealtimeReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name="activeUsers")],
        dimensions=[Dimension(name="country"), Dimension(name="city")]
    )
    response = client.run_realtime_report(request)
    
    total_users = 0
    rows = []
    for row in response.rows:
        count = int(row.metric_values[0].value)
        total_users += count
        country = row.dimension_values[0].value
        city = row.dimension_values[1].value
        rows.append((country, city, count))
    
    print(f"🟢 Current Active Users Online: {total_users}\n")
    if rows:
        print(f"{'Country':<20} {'City':<25} {'Active Users':<10}")
        print("-" * 55)
        for country, city, count in rows:
            print(f"{country:<20} {city:<25} {count:<10}")
    else:
        print("No active users detected right now.")

def run_summary(client, property_id, days=30):
    """Fetches high level summary for past N days."""
    print_header(f"Traffic & Engagement Overview (Past {days} Days)")
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers"),
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
            Metric(name="averageSessionDuration"),
            Metric(name="bounceRate")
        ]
    )
    response = client.run_report(request)
    
    for row in response.rows:
        active = row.metric_values[0].value
        new_users = row.metric_values[1].value
        sessions = row.metric_values[2].value
        pageviews = row.metric_values[3].value
        avg_dur = float(row.metric_values[4].value)
        bounce = float(row.metric_values[5].value) * 100
        
        mins = int(avg_dur // 60)
        secs = int(avg_dur % 60)
        
        print(f"👥 Total Active Visitors : {int(active):,}")
        print(f"✨ New Visitors          : {int(new_users):,}")
        print(f"🔁 Total Sessions        : {int(sessions):,}")
        print(f"📄 Total Pageviews       : {int(pageviews):,}")
        print(f"⏱️ Avg Session Duration   : {mins}m {secs}s")
        print(f"🚪 Bounce Rate            : {bounce:.1f}%\n")

def run_top_pages(client, property_id, limit=10):
    """Fetches top visited pages/URLs."""
    print_header(f"Top {limit} Most Visited Pages (Past 30 Days)")
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        dimensions=[Dimension(name="pagePath"), Dimension(name="pageTitle")],
        metrics=[Metric(name="screenPageViews"), Metric(name="activeUsers")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
        limit=limit
    )
    response = client.run_report(request)
    
    print(f"{'Pageviews':<12} {'Visitors':<10} {'Path / Title'}")
    print("-" * 65)
    for row in response.rows:
        views = row.metric_values[0].value
        users = row.metric_values[1].value
        path = row.dimension_values[0].value
        title = row.dimension_values[1].value[:35]
        print(f"{views:<12} {users:<10} {path} ({title}...)")

def run_traffic_sources(client, property_id):
    """Fetches top traffic acquisition channels and sources."""
    print_header("Top Traffic Acquisition Sources (Past 30 Days)")
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        dimensions=[Dimension(name="sessionSource"), Dimension(name="sessionMedium")],
        metrics=[Metric(name="sessions"), Metric(name="activeUsers")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=10
    )
    response = client.run_report(request)
    
    print(f"{'Source / Medium':<35} {'Sessions':<12} {'Users':<10}")
    print("-" * 65)
    for row in response.rows:
        src = row.dimension_values[0].value
        med = row.dimension_values[1].value
        combo = f"{src} / {med}"
        sessions = row.metric_values[0].value
        users = row.metric_values[1].value
        print(f"{combo:<35} {sessions:<12} {users:<10}")

def run_geo(client, property_id):
    """Fetches geographic distribution (Countries and Top Cities)."""
    print_header("Top Visitor Locations (Countries & Cities - Past 30 Days)")
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        dimensions=[Dimension(name="country"), Dimension(name="city")],
        metrics=[Metric(name="activeUsers"), Metric(name="sessions")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="activeUsers"), desc=True)],
        limit=15
    )
    response = client.run_report(request)
    
    print(f"{'Country':<20} {'City':<25} {'Users':<10} {'Sessions':<10}")
    print("-" * 65)
    for row in response.rows:
        country = row.dimension_values[0].value
        city = row.dimension_values[1].value
        users = row.metric_values[0].value
        sessions = row.metric_values[1].value
        print(f"{country:<20} {city:<25} {users:<10} {sessions:<10}")

def main():
    parser = argparse.ArgumentParser(description="Propertism GA4 Analytics CLI")
    parser.add_argument("--realtime", action="store_true", help="Show live active users right now")
    parser.add_argument("--summary", action="store_true", help="Show 30-day traffic summary")
    parser.add_argument("--pages", action="store_true", help="Show top visited pages")
    parser.add_argument("--sources", action="store_true", help="Show top traffic channels and sources")
    parser.add_argument("--geo", action="store_true", help="Show geographic breakdown of visitors")
    parser.add_argument("--days", type=int, default=30, help="Number of days for summary (default: 30)")
    parser.add_argument("--all", action="store_true", help="Run complete analytics report")
    
    args = parser.parse_args()

    creds = get_credentials()
    client = BetaAnalyticsDataClient(credentials=creds)
    property_id = get_property_id(client, creds)

    if args.realtime:
        run_realtime(client, property_id)
    elif args.pages:
        run_top_pages(client, property_id)
    elif args.sources:
        run_traffic_sources(client, property_id)
    elif args.geo:
        run_geo(client, property_id)
    elif args.all:
        run_realtime(client, property_id)
        run_summary(client, property_id, args.days)
        run_traffic_sources(client, property_id)
        run_top_pages(client, property_id)
        run_geo(client, property_id)
    else:
        # Default: summary
        run_realtime(client, property_id)
        run_summary(client, property_id, args.days)

if __name__ == "__main__":
    main()
