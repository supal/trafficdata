# Traffic MCP Server - Quick Reference

## 1️⃣ Configuration File Location

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

---

## 2️⃣ Configuration Content

Copy and paste this into your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "traffic": {
      "command": "node",
      "args": [
        "/Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server/dist/server.js"
      ],
      "env": {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_USER": "postgres",
        "DB_PASSWORD": "your_password_here",
        "DB_NAME": "traffic_data"
      }
    }
  }
}
```

**Update `DB_PASSWORD` with your actual PostgreSQL password!**

---

## 3️⃣ Setup Steps

1. **Find or create the config file** at the location above
2. **Paste the configuration** with your database credentials
3. **Restart Claude Desktop** (close and reopen)
4. **Verify** tools appear in Claude
5. **Test** by asking Claude to use a traffic tool

---

## 4️⃣ Quick Verification

### Open terminal and run:

```bash
# Check server file exists
ls /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server/dist/server.js

# Verify database connection
psql -U postgres -d traffic_data -c "SELECT COUNT(*) FROM traffic_data;"

# Validate config (should show no errors)
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool
```

---

## 5️⃣ Test in Claude

Ask Claude any of these:

- "Show me traffic statistics"
- "Get the latest 50 traffic records"
- "What's the traffic on road E4?"
- "Compare speeds for different vehicle types"
- "Show traffic data from Jan 1-4, 2026"

---

## 6️⃣ Troubleshooting

| Issue | Solution |
|-------|----------|
| Tools not showing | Restart Claude Desktop |
| Database connection error | Check credentials in config file |
| "Cannot find module" error | Verify path is absolute (not relative) |
| JSON error in config | Use JSON validator or correct syntax |
| PostgreSQL not running | Start PostgreSQL: `brew services start postgresql` |

---

## 7️⃣ Available Tools

```
✓ get_all_traffic_data          - Fetch traffic records
✓ get_traffic_by_location       - Search by county/road/point
✓ get_traffic_by_date_range     - Filter by dates
✓ get_traffic_by_road           - Filter by road number
✓ get_traffic_by_county         - Filter by county
✓ get_traffic_by_measurement_point - Filter by measurement point
✓ get_traffic_statistics        - Get comprehensive stats
✓ get_vehicle_counts_comparison - Compare vehicle counts
✓ get_speeds_comparison         - Compare speeds by type
```

---

## 8️⃣ If Something Goes Wrong

```bash
# Rebuild the server
cd /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server
npm run build

# Run tests
npm test

# Run server manually to see errors
node dist/server.js
```

---

**That's it!** You're ready to use traffic data in Claude. 🚀
