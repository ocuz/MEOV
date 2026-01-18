# X API v2 Official Integration - v0.5

## 🚀 Official X API Batch Username Checking

This bot now supports **official X API v2 batch checking** for efficient, high-speed username sniping on Twitter/X.

---

## 📊 Why X API v2 Is Better

### Efficiency Comparison

| Method | Usernames/Request | Speed | Accuracy | Rate Limit |
|--------|---|---|---|---|
| **Official X API v2** | 100 | Very Fast | Official API | 100/hour (VIP) |
| **Single Checks** | 1 | Slow | Good | 100/minute (old) |
| **Manual Scraping** | 1 | Slow | Poor | IP Bans |

### Key Advantages
✅ Check **100 usernames in a single request**  
✅ Stay under rate limits with batch processing  
✅ Official API endpoint (no IP bans)  
✅ Accurate availability detection  
✅ Automatic logging of available usernames  
✅ Special handling for banned accounts  

---

## 🔑 Setup Instructions

### Step 1: Get X API Bearer Token

1. Go to [X Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create/select your project and app
3. Navigate to **Keys and tokens**
4. Generate/copy your **Bearer Token**
   - Look for "Bearer Token" under "Authentication Tokens"
   - Format: `AAAAAxxxxxxxxxxxxxxxxxxxxxxxxx...`

### Step 2: Add to .env File

```bash
nano .env
```

Add this line:
```env
X_BEARER_TOKEN=AAAAAxxxxxxxxxxxxxxxxxxxxxxxxx_your_token_here
```

### Step 3: Restart Bot

```bash
python discord_bot.py
```

You should see:
```
🔌 X API v2 Integration: ENABLED (Official batch checking)
📊 VIP Twitter Limit: 100 requests/hour (batch mode)
```

---

## 🎯 How It Works

### API Response Parsing

The X API returns a single response with two key sections:

```json
{
  "data": [
    {"id": "12345", "username": "available_user"}  // TAKEN usernames
  ],
  "errors": [
    {"title": "Not Found Error", "value": "available"}  // AVAILABLE usernames
  ]
}
```

**Our Logic:**
- Username in `data` array → **TAKEN** (status: 1)
- Username in `errors` with "Not Found Error" → **AVAILABLE** (status: 0)
- Banned/suspended accounts → Appear as "Not Found" (can't register)

---

## 📈 VIP Rate Limiting

### For VIP Users Using X API Batch Mode

```
Limit: 100 requests per hour
With 100 usernames per request = 10,000 usernames/hour
```

**Example:**
```
Hour 0:00 → Send batch of 100 names (1/100 requests used)
Hour 0:05 → Send batch of 100 names (2/100 requests used)
Hour 0:10 → Send batch of 100 names (3/100 requests used)
...
Hour 0:59 → Send batch of 100 names (100/100 requests used)
Hour 1:00 → Counter resets, new batch allowed ✅
```

---

## 🔍 How to Use X API Batch Checking

### For Developers (Python)

```python
# Check batch of usernames
usernames = ["username1", "username2", ..., "username100"]
results = await UsernameChecker.chk_twitter_batch(usernames, user_id)

# Results format: {username: status}
# 0 = Available
# 1 = Taken
# None = Error
```

### For VIP Users (Discord Bot)

When a VIP user runs `/snipe` with Twitter/X platform:

1. Bot detects VIP status
2. Checks 100-request/hour limit
3. Uses batch API endpoint
4. Returns results for up to 100 usernames
5. Logs available names to `available_usernames.txt`

---

## 📊 Token Tier Limits

### Free Tier
- **Very limited** - Not recommended for sniping
- Gets blocked quickly

### Basic Tier ($100/month)
- **10,000 requests/month**
- With batch checking: **1,000,000 usernames/month**
- Recommended for regular VIP users

### Pro Tier ($5,000/month)
- **500,000 requests/month**
- With batch checking: **50,000,000 usernames/month**
- For enterprise/high-volume snipers

---

## 🛡️ Rate Limit Handling

### Automatic Rate Limit Enforcement

```python
if request_count > VIP_TWITTER_MAX_REQUESTS_PER_HOUR:
    return "❌ Twitter X API Rate Limit: You can do X more requests this hour"
```

### Hour Reset Logic

```
Timer tracks: last_request_timestamp
When: (now - last_request) >= 3600 seconds
Then: Counter resets automatically
```

---

## 📝 Available Usernames Logging

### Automatic File Logging

When available usernames are found, they're logged to:
```
available_usernames.txt
```

**Format:**
```
username1
username2
username3
...
```

One username per line, ready to snipe!

---

## ⚡ Performance Metrics

### Without X API (Old Method)
- 1 username per request
- 100 requests/minute = 6,000 usernames/hour
- Subject to IP bans

### With X API Batch (New Method)
- 100 usernames per request
- 100 requests/hour = 10,000 usernames/hour (VIP)
- Official endpoint (no IP bans)

### Efficiency Gain
**~67% faster** checking on same rate limit!

---

## 🔧 Technical Details

### New Classes

#### `TwitterXAPIChecker`
```python
check_vip_twitter_rate_limit(user_id, request_count)
  → (allowed: bool, message: str, remaining: int)

batch_check_twitter_usernames(usernames, bearer_token)
  → {username: status}

log_available_usernames(available_list, filename)
  → Async file logging
```

### New Configuration Variables

```python
X_BEARER_TOKEN = ""           # X API Bearer Token
X_API_ENDPOINT = "https://api.twitter.com/2/users/by"
X_BATCH_SIZE = 100            # Max per request
VIP_TWITTER_MAX_REQUESTS_PER_HOUR = 100
VIP_TWITTER_COOLDOWN_MINUTES = 60

vip_twitter_rate_limit = {}   # Tracks per-hour requests
```

### Updated Functions

```python
chk_twitter()          # Now supports user_id and use_x_api params
chk_twitter_batch()    # New batch checking method
```

---

## 🚨 Error Handling

### Scenario 1: No Bearer Token
```
Status: DISABLED
Message: ⚠️ X API v2 Token not configured
Fallback: Single-check method only
```

### Scenario 2: Rate Limit Exceeded
```
Status: BLOCKED
Message: ❌ You can do X more requests this hour. Resets in Ym
Action: User must wait for hour to reset
```

### Scenario 3: API Error (429 Too Many Requests)
```
Status: SKIPPED
Action: Request returns None (error status)
Behavior: Graceful degradation
```

### Scenario 4: Network Error
```
Status: TIMEOUT
Action: Request returns None for all usernames
Behavior: Can retry in next batch
```

---

## 📚 X API Documentation

- **Official Docs**: [X API v2 Users Endpoint](https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by)
- **Authentication**: [Bearer Token Setup](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens)
- **Rate Limits**: [X API Rate Limits](https://developer.twitter.com/en/docs/twitter-api/rate-limits)

---

## 💡 Usage Examples

### Example 1: Batch Check 100 Names

```python
usernames = ["abc", "def", "ghi", ..., "xyz"]  # 100 names

results = await UsernameChecker.chk_twitter_batch(
    usernames, 
    user_id=123456789
)

# Results: {
#   "abc": 0,     # Available
#   "def": 1,     # Taken
#   "ghi": None,  # Error/timeout
#   ...
# }
```

### Example 2: Check Rate Limit Before Request

```python
user_id = 123456789
allowed, msg, remaining = TwitterXAPIChecker.check_vip_twitter_rate_limit(
    user_id,
    request_count=1
)

if allowed:
    print(f"✅ Request allowed. {remaining} requests remaining this hour")
else:
    print(f"❌ {msg}")
```

### Example 3: Auto Logging Available Names

```python
available = ["name1", "name2", "name3"]
await TwitterXAPIChecker.log_available_usernames(available)
# Writes to available_usernames.txt
```

---

## 🎁 VIP Benefits with X API

| Feature | Standard | VIP |
|---------|----------|-----|
| Batch Checking | ❌ | ✅ 100/request |
| Per-Hour Limit | N/A | ✅ 100 requests |
| Auto Logging | ❌ | ✅ Yes |
| Priority | None | High |

---

## 📱 Command Integration

When VIP user runs `/snipe` with Twitter selected:

```
Bot detects:
✅ User is VIP
✅ Platform is Twitter/X
✅ X_BEARER_TOKEN is configured

Bot actions:
✅ Shows 100 username form
✅ Validates against 100-request/hour limit
✅ Sends batch check to X API
✅ Logs available names to file
✅ Returns results instantly
```

---

## 🔐 Security Notes

- Bearer Token is stored in `.env` (not in code)
- Token not logged to console
- Only VIP users can use batch method
- Rate limits prevent abuse
- Official API (no IP ban risk)

---

## 📞 Troubleshooting

### Issue: X API Integration Not Showing

**Solution**: Add `X_BEARER_TOKEN` to .env and restart bot
```
🔌 X API v2 Integration: ENABLED
```

### Issue: Rate Limit Errors

**Solution**: Ensure VIP user, check hour reset, wait for cooldown

### Issue: No Available Names Logging

**Solution**: Check `available_usernames.txt` permissions, verify X API key

### Issue: "Invalid Bearer Token"

**Solution**: 
1. Go to X Developer Portal
2. Get fresh Bearer Token
3. Update .env
4. Restart bot

---

## 🚀 Next Steps

1. ✅ Get X API Bearer Token from Developer Portal
2. ✅ Add to .env: `X_BEARER_TOKEN=...`
3. ✅ Restart bot
4. ✅ VIP users can now batch check 100 names/request
5. ✅ Available names auto-logged to `available_usernames.txt`

---

**Version**: 0.5  
**Status**: ✅ X API v2 Integration Active  
**VIP Limit**: 100 requests/hour (10,000 usernames/hour)  
**Official API**: ✅ Fully Integrated

Enjoy official batch checking! 🎉
