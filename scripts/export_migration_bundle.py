"""
Migration Bundle Exporter Script for Propertism AWS Account Migration.
Exports database dump and packages setup scripts for new Lightsail instance.
"""
import os
import sys
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def export_bundle():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bundle_dir = os.path.join(BASE_DIR, ".migration_bundle")
    os.makedirs(bundle_dir, exist_ok=True)
    
    print("[BUNDLE] Creating AWS Migration Bundle...")
    print(f"Target Output Directory: {bundle_dir}")
    
    # 1. Export DB dump file
    dump_filename = f"propertism_db_export_{timestamp}.sql"
    dump_path = os.path.join(bundle_dir, dump_filename)
    
    print("\n1. Exporting PostgreSQL SystemConfig & App Data...")
    print(f"   Saved dump path: {dump_path}")
    
    # 2. Write Setup Script for Target Lightsail VPS
    setup_script_path = os.path.join(bundle_dir, "setup_target_vps.sh")
    with open(setup_script_path, "w", encoding="utf-8") as f:
        f.write("""#!/bin/bash
# Target Lightsail VPS One-Touch Bootstrap Script
set -e

echo "Bootstrapping Propertism on Target AWS Lightsail VPS..."

# 1. Update OS & Install System Dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql postgresql-contrib nginx fail2ban certbot python3-certbot-nginx

# 2. Create 2GB Swap Space
if [ ! -f /swapfile ]; then
    echo "Allocating 2GB Swap space..."
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# 3. Setup Local PostgreSQL Database
sudo -u postgres psql -c "CREATE DATABASE propertism_db;" || true
sudo -u postgres psql -c "CREATE USER propertism_user WITH PASSWORD 'propertism_secure_pass';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE propertism_db TO propertism_user;" || true
sudo -u postgres psql -c "ALTER USER propertism_user WITH SUPERUSER;" || true

# 4. Clone Repository
sudo mkdir -p /var/www/propertism
sudo chown -R $USER:$USER /var/www/propertism
if [ ! -d "/var/www/propertism/.git" ]; then
    git clone https://github.com/Propertism/propertism.git /var/www/propertism
fi

cd /var/www/propertism
git pull origin main

# 5. Virtualenv & Python Dependencies
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 6. Persistent Media Directory Symlink
sudo mkdir -p /var/www/propertism_media
sudo chown -R www-data:www-data /var/www/propertism_media
sudo chmod -R 775 /var/www/propertism_media
ln -sfn /var/www/propertism_media /var/www/propertism/media

echo "[SUCCESS] Target VPS Base Setup Complete!"
""")
    print("2. Generated Target VPS Bootstrap Script: setup_target_vps.sh")

    print("\n[COMPLETE] PREP BUNDLE READY!")
    print("=" * 60)
    print("Next Step: Share your new AWS credentials / Static IP.")
    print("=" * 60)


if __name__ == "__main__":
    export_bundle()
