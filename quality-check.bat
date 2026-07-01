@echo off
REM Quality Check Script for Video Localization AI Studio
REM Runs ESLint, Prettier, and tests

echo ============================================
echo   QUALITY GATE - Video Localization AI Studio
echo ============================================

set FAILED=0

REM ---- 1. ESLint Backend ----
echo.
echo [1/4] Running ESLint on Backend...
cd /d "%~dp0src\backend"
call npx --no-install eslint . 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [PASS] Backend ESLint passed
) else (
    echo   [FAIL] Backend ESLint failed
    set FAILED=1
)
cd /d "%~dp0"

REM ---- 2. ESLint Frontend ----
echo.
echo [2/4] Running ESLint on Frontend...
cd /d "%~dp0src\frontend"
call npx --no-install eslint . 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [PASS] Frontend ESLint passed
) else (
    echo   [FAIL] Frontend ESLint failed
    set FAILED=1
)
cd /d "%~dp0"

REM ---- 3. Prettier Check ----
echo.
echo [3/4] Running Prettier Check...
call npx --no-install prettier --check "src/**/*.{js,jsx,ts,tsx,json,css,md}" 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [PASS] Prettier check passed
) else (
    echo   [FAIL] Prettier check failed
    set FAILED=1
)

REM ---- 4. Tests ----
echo.
echo [4/4] Running Tests...
call npm test 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [PASS] Tests passed
) else (
    echo   [FAIL] Tests failed
    set FAILED=1
)

REM ---- Summary ----
echo.
echo ============================================
if %FAILED% EQU 0 (
    echo   QUALITY GATE: PASSED
    exit /b 0
) else (
    echo   QUALITY GATE: FAILED
    exit /b 1
)
echo ============================================