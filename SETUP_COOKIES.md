# Setup YouTube Cookies (Option 2)

## Step 1: Export Cookies from Browser

### Method A: Using Browser Extension (Easiest)
1. Install extension:
   - **Chrome**: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - **Firefox**: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. Go to **youtube.com** and login to your account
3. Click the extension icon
4. Click "Export" → Save as `cookies.txt`

### Method B: Using yt-dlp (Alternative)
```bash
# On your local machine
yt-dlp --cookies-from-browser chrome --cookies cookies.txt https://youtube.com
```

## Step 2: Add Cookies to Render

### Option A: Via GitHub (Recommended)
```bash
# Copy your cookies.txt to project folder
cp ~/Downloads/cookies.txt .

# Add to git (it's in .gitignore for security)
git add -f cookies.txt

# Commit and push
git commit -m "Add YouTube cookies"
git push
```

### Option B: Via Render Environment Variable
1. Go to Render Dashboard → Your Service
2. Environment → Add Secret File
3. Key: `COOKIES_FILE`
4. Upload your `cookies.txt`
5. Redeploy

## Step 3: Test
```bash
curl -X POST "https://your-app.onrender.com/download" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://youtube.com/watch?v=VIDEO_ID"}'
```

---

# Setup Proxy (Option 3)

## Free Proxy Services
- **ProxyScrape**: https://proxyscrape.com/free-proxy-list
- **Free Proxy List**: https://free-proxy-list.net

## Paid Proxy Services (Recommended for Production)
- **BrightData**: https://brightdata.com (Residential proxies)
- **Smartproxy**: https://smartproxy.com
- **Oxylabs**: https://oxylabs.io

## Add Proxy to Render

1. Go to Render Dashboard → Your Service
2. Environment → Add Environment Variable
3. Key: `PROXY_URL`
4. Value: `http://username:password@proxy-server:port`
   - Example: `http://user:pass@proxy.example.com:8080`
   - Or: `socks5://proxy.example.com:1080`
5. Save and Redeploy

## Test with Proxy
Your API will automatically use the proxy if `PROXY_URL` is set.

---

# Which Option to Choose?

- **Cookies**: Free, works well, needs renewal every few months
- **Proxy**: Costs money, more reliable, better for production

**Recommendation**: Start with cookies, upgrade to proxy if needed.
