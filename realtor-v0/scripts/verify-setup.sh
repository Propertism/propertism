#!/bin/bash

echo "🔍 Verifying Chennai Realtor Monorepo Setup..."
echo ""

# Check root structure
echo "✅ Checking root structure..."
if [ -f "package.json" ] && [ -d "shared" ] && [ -d "realtor-web" ] && [ -d "realtor-mobile" ]; then
    echo "   ✓ Root structure correct"
else
    echo "   ✗ Root structure incomplete"
    exit 1
fi

# Check shared code
echo "✅ Checking shared code..."
if [ -f "shared/types/index.ts" ] && [ -f "shared/utils/formatPriceINR.ts" ] && [ -f "shared/services/api.ts" ]; then
    echo "   ✓ Shared code present"
else
    echo "   ✗ Shared code missing"
    exit 1
fi

# Check Django backend
echo "✅ Checking Django backend..."
if [ -f "realtor-web/manage.py" ] && [ -f "realtor-web/requirements.txt" ]; then
    echo "   ✓ Django files present"
else
    echo "   ✗ Django files missing"
    exit 1
fi

# Check React PWA
echo "✅ Checking React PWA..."
if [ -f "realtor-web/uilayers/package.json" ] && [ -f "realtor-web/uilayers/vite.config.ts" ]; then
    echo "   ✓ React PWA files present"
else
    echo "   ✗ React PWA files missing"
    exit 1
fi

# Check React Native mobile
echo "✅ Checking React Native mobile..."
if [ -f "realtor-mobile/package.json" ] && [ -f "realtor-mobile/app.json" ]; then
    echo "   ✓ Mobile app files present"
else
    echo "   ✗ Mobile app files missing"
    exit 1
fi

# Check documentation
echo "✅ Checking documentation..."
if [ -f "README.md" ] && [ -f "SETUP_GUIDE.md" ] && [ -f "QUICK_START.md" ]; then
    echo "   ✓ Documentation complete"
else
    echo "   ✗ Documentation incomplete"
    exit 1
fi

echo ""
echo "🎉 Setup verification complete!"
echo ""
echo "Next steps:"
echo "1. yarn install"
echo "2. cd realtor-web && pip install -r requirements.txt"
echo "3. cd realtor-web && python manage.py migrate"
echo "4. yarn dev"
echo ""
