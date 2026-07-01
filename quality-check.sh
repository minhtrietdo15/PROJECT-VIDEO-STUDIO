#!/bin/bash
# Quality Check Script for Video Localization AI Studio
# Runs ESLint, Prettier, and tests

echo "============================================"
echo "  QUALITY GATE - Video Localization AI Studio"
echo "============================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILED=0

# ---- 1. ESLint Backend ----
echo -e "\n${YELLOW}[1/4] Running ESLint on Backend...${NC}"
cd src/backend
npx eslint . --ext .js,.jsx,.ts,.tsx 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✓ Backend ESLint passed${NC}"
else
    echo -e "${RED}  ✗ Backend ESLint failed${NC}"
    FAILED=1
fi
cd ../..

# ---- 2. ESLint Frontend ----
echo -e "\n${YELLOW}[2/4] Running ESLint on Frontend...${NC}"
cd src/frontend
npx eslint . --ext .js,.jsx,.ts,.tsx 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✓ Frontend ESLint passed${NC}"
else
    echo -e "${RED}  ✗ Frontend ESLint failed${NC}"
    FAILED=1
fi
cd ../..

# ---- 3. Prettier Check ----
echo -e "\n${YELLOW}[3/4] Running Prettier Check...${NC}"
npx prettier --check "src/**/*.{js,jsx,ts,tsx,json,css,md}" 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✓ Prettier check passed${NC}"
else
    echo -e "${RED}  ✗ Prettier check failed${NC}"
    FAILED=1
fi

# ---- 4. Tests ----
echo -e "\n${YELLOW}[4/4] Running Tests...${NC}"
npm test 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}  ✓ Tests passed${NC}"
else
    echo -e "${RED}  ✗ Tests failed${NC}"
    FAILED=1
fi

# ---- Summary ----
echo -e "\n============================================"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}  QUALITY GATE: PASSED ✓${NC}"
    exit 0
else
    echo -e "${RED}  QUALITY GATE: FAILED ✗${NC}"
    exit 1
fi
echo "============================================"