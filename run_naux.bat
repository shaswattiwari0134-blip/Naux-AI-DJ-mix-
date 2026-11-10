@echo off
echo ========================================================
echo   Starting NAUX Local Party DJ Server on http://localhost:3000
echo ========================================================
echo.
echo Opening http://localhost:3000/naux_party_clone.html in your browser...
start http://localhost:3000/naux_party_clone.html
echo.
echo Press Ctrl+C in this terminal window to stop the server anytime.
echo.
python -m http.server 3000

