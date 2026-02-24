@echo off
echo Starting Local Tunnel for SignAI Backend...
echo ------------------------------------------
echo 1. Ensure your backend is running separately (py -3.8 final_backend.py)
echo 2. This tunnel will provide a public URL for your Vercel frontend.
echo ------------------------------------------
npx localtunnel --port 5000
pause
