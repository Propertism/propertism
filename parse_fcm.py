import json
from collections import Counter

with open('fcm_models.json') as f:
    data = json.load(f)

print(f'Total models catalogued: {len(data)}')
print()

# Count by tier
tiers = Counter(m.get('tier','?') for m in data)
print('Models by Tier:')
for t in ['S+','S','A+','A','B','C']:
    if tiers.get(t):
        print(f'  {t}: {tiers[t]}')
print()

# Count by provider
providers = Counter(m.get('provider','?') for m in data)
print('Models by Provider:')
for p, c in providers.most_common():
    print(f'  {p}: {c}')
print()

# Top healthy models
healthy = [m for m in data if m.get('status') == 'up' and m.get('verdict') not in ['Overloaded','Pending']]
healthy.sort(key=lambda x: x.get('latestPing',99999))
print(f'Healthy models: {len(healthy)}')
print()
print('Top 10 Fastest Healthy Models:')
for m in healthy[:10]:
    label = m.get('label','?')
    provider = m.get('provider','?')
    tier = m.get('tier','?')
    ping = m.get('latestPing','?')
    swe = m.get('sweScore','-')
    ctx = m.get('context','-')
    verdict = m.get('verdict','?')
    print(f'  #{m["rank"]} {label:35s} | {provider:15s} | Tier: {tier:4s} | Ping: {str(ping):>5}ms | SWE: {str(swe):>6s} | Ctx: {str(ctx):>6s} | {verdict}')

print()
print('Top S+ Tier Models (all statuses):')
splus = [m for m in data if m.get('tier') == 'S+']
for m in splus:
    label = m.get('label','?')
    provider = m.get('provider','?')
    ping = m.get('latestPing','?')
    swe = m.get('sweScore','-')
    ctx = m.get('context','-')
    status = m.get('status','?')
    verdict = m.get('verdict','?')
    print(f'  #{m["rank"]} {label:35s} | {provider:15s} | Ping: {str(ping):>5}ms | SWE: {str(swe):>6s} | Ctx: {str(ctx):>6s} | Status: {status:10s} | {verdict}')
