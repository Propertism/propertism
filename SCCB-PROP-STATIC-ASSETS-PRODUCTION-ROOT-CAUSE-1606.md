# SCCB-PROP-STATIC-ASSETS-PRODUCTION-ROOT-CAUSE-1606

**Date**: June 16, 2026
**Status**: Root Cause Identified
**Severity**: HIGH — Production frontend broken (HTML loads, CSS/JS/images 404)

---

## 1. Symptom Confirmation

```
$ curl -sI https://www.propertism.in/
→ HTTP/1.1 200 OK  (HTML loads)

$ curl -sI https://www.propertism.in/static/css/propertism-styles.css
→ HTTP/1.1 404 Not Found  (CSS returns 404)
```

All static assets (CSS, JS, images) return 404. HTML renders unstyled.

---

## 2. Investigation Results

### 2.1 STATIC_URL / STATIC_ROOT (settings.py — Line 247-249)

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

**Verdict: ✅ Correct.** No issue here.

### 2.2 WhiteNoise Middleware (settings.py — Line 162)

```python
'whitenoise.middleware.WhiteNoiseMiddleware',
```

**Verdict: ✅ Present and correctly positioned** after SecurityMiddleware.

### 2.3 Nginx Configuration (`.platform/nginx/nginx.conf` — Line 24-28)

```nginx
location /static/ {
    alias /var/app/current/staticfiles/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

**Verdict: ✅ Correct.** Nginx is configured to serve `/static/` from `/var/app/current/staticfiles/`.

### 2.4 `.ebextensions/01_django.config` — Container Command

```yaml
container_commands:
  01_collectstatic:
    command: "python manage.py collectstatic --noinput --clear"
```

**Verdict: ⚠️ Present but problematic.** The `--clear` flag deletes the entire `staticfiles/` directory before recreating it. This command runs during the **build phase** (PostBuildEbExtension), not during config-deploy.

### 2.5 Postdeploy Hook (`.platform/hooks/postdeploy/00_collectstatic_current.sh`)

**Verdict: ✅ Correct.** This hook runs `collectstatic --noinput --clear` as the `webapp` user and sets proper permissions. It runs during `app-deploy` lifecycle.

---

## 3. ROOT CAUSE: Config-Deploy Wipes staticfiles/

### Timeline of Failure

| Time | Event | Details |
|------|-------|---------|
| 06:43:12 | **app-deploy succeeds** | Postdeploy hook creates `/var/app/current/staticfiles/` with 228 files |
| 06:48:14 | **config-deploy triggered** | EB applies configuration changes (likely from `.ebextensions` or environment update) |
| 06:48:21 | **`Removing /var/app/current/`** | EB **deletes the entire `/var/app/current/` directory** |
| 06:48:21 | **`Renaming /var/app/staging/ to /var/app/current/`** | EB replaces with fresh staging bundle (which does NOT contain `staticfiles/`) |
| 06:48:24 | **config-deploy completes** | No postdeploy hooks run for config-deploy (`No hooks found in .platform/confighooks/postdeploy/`) |

### Why This Happens

1. **`staticfiles/` is excluded from the build bundle** — The `build-eb-bundle.ps1` script explicitly excludes `staticfiles/` from the deployment ZIP (line 55: `"staticfiles"` in `$excludedDirectories`).

2. **`staticfiles/` is created at runtime** by the postdeploy hook `00_collectstatic_current.sh`.

3. **Config-deploy does NOT run postdeploy hooks** — EB's `config-deploy` lifecycle only runs hooks from `.platform/confighooks/postdeploy/`, which does not exist.

4. **Config-deploy does NOT run container_commands** — The `PostBuildEbExtension` (which executes `.ebextensions` container_commands) only runs during `app-deploy`, not `config-deploy`.

### The Chain of Events

```
app-deploy:
  ├── PostBuildEbExtension → container_commands (01_collectstatic runs)
  ├── Swap /var/app/staging/ → /var/app/current/
  └── PostDeployHooks → 00_collectstatic_current.sh creates staticfiles/ ✅

config-deploy (triggered by env config change):
  ├── Remove /var/app/current/  ← DELETES staticfiles/
  ├── Rename /var/app/staging/ → /var/app/current/  ← No staticfiles/ in bundle
  ├── No PostBuildEbExtension  ← container_commands NOT executed
  └── No confighooks/postdeploy/  ← staticfiles/ NOT recreated ❌
```

---

## 4. Contributing Factors

### 4.1 `--clear` Flag in Container Command

The `01_collectstatic` container command uses `--clear` which deletes the entire `staticfiles/` directory before recreating it. This was failing intermittently during the build phase (multiple `Command 01_collectstatic failed` errors in cfn-init.log at 06:30, 06:31, 06:33, 06:37) before finally succeeding at 06:42:59.

### 4.2 Missing confighooks Directory

There is no `.platform/confighooks/postdeploy/` directory. The postdeploy hooks only run during `app-deploy`, not during `config-deploy`.

### 4.3 `aws:elasticbeanstalk:environment:proxy:staticfiles` Setting

The `.ebextensions/01_django.config` also contains:
```yaml
aws:elasticbeanstalk:environment:proxy:staticfiles:
    /static: staticfiles
```

This setting tells EB's proxy to serve `/static` from `staticfiles`, but this is **overridden** by the custom `.platform/nginx/nginx.conf` which has its own `/static/` location block. This creates a potential conflict.

---

## 5. Recommended Minimal Fix

### Option A (Recommended): Add confighooks/postdeploy for collectstatic

Create `.platform/confighooks/postdeploy/00_collectstatic_current.sh` — a symlink or copy of the existing postdeploy hook:

```bash
#!/bin/bash
set -euo pipefail

if [ -f /opt/elasticbeanstalk/deployment/env ]; then
    set -a
    . /opt/elasticbeanstalk/deployment/env || true
    set +a
fi

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-realtor_project.settings}"
export PYTHONPATH="/var/app/current:${PYTHONPATH:-}"

STATIC_ROOT="/var/app/current/staticfiles"
PYTHON_BIN=$(echo /var/app/venv/*/bin/python)

mkdir -p "$STATIC_ROOT"
chown -R webapp:webapp "$STATIC_ROOT"
chmod 775 "$STATIC_ROOT"

sudo -u webapp env \
    DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
    PYTHONPATH="$PYTHONPATH" \
    "$PYTHON_BIN" /var/app/current/manage.py collectstatic --noinput --clear

chown -R webapp:webapp "$STATIC_ROOT"
find "$STATIC_ROOT" -type d -exec chmod 755 {} \;
find "$STATIC_ROOT" -type f -exec chmod 644 {} \;
```

This ensures `collectstatic` runs during **both** `app-deploy` and `config-deploy` lifecycles.

### Option B (Alternative): Remove `--clear` from container_command

Change the container command to not use `--clear`:
```yaml
01_collectstatic:
    command: "python manage.py collectstatic --noinput"
```

This prevents the directory from being wiped during the build phase, but doesn't fix the config-deploy issue.

### Option C (Quick Fix): Run collectstatic manually on production

```bash
sudo -u webapp /var/app/venv/staging-LQM1lest/bin/python /var/app/current/manage.py collectstatic --noinput --clear
```

This is a temporary fix until the next deployment.

---

## 6. Verification

After applying the fix:
1. Deploy a config change (or trigger config-deploy)
2. Verify: `curl -I https://www.propertism.in/static/css/propertism-styles.css` → `200 OK`
3. Verify: `ls -la /var/app/current/staticfiles/` exists with CSS/JS/images

---

## 7. Summary

| Check | Status |
|-------|--------|
| STATIC_URL/STATIC_ROOT | ✅ Correct |
| WhiteNoise middleware | ✅ Present |
| collectstatic in deployment | ✅ Present (postdeploy hook) |
| Nginx /static/ config | ✅ Correct |
| **Config-deploy preserves staticfiles** | **❌ BROKEN — Root Cause** |
| confighooks/postdeploy/ | ❌ Missing — needs creation |
| Build bundle includes staticfiles | ❌ Correctly excluded (runtime-generated) |

**Root Cause**: EB `config-deploy` lifecycle wipes `/var/app/current/` and replaces it with the staging bundle (which excludes `staticfiles/`). The postdeploy hook that recreates `staticfiles/` only runs during `app-deploy`, not `config-deploy`. The fix is to add a `confighooks/postdeploy` hook that runs `collectstatic` during config-deploy as well.
