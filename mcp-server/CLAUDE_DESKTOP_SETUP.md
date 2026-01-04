# Traffic MCP Server - Claude Desktop Setup Guide

A complete guide to integrate the Traffic Data MCP Server with Claude Desktop application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Setup](#quick-setup)
3. [Configuration Details](#configuration-details)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Using the Server](#using-the-server)

---

## Prerequisites

Before setting up the MCP server with Claude Desktop, ensure you have:

- ✅ Claude Desktop installed ([download here](https://claude.ai/download))
- ✅ Node.js 18+ installed
- ✅ PostgreSQL database running with `traffic_data` table
- ✅ MCP server built (`npm run build` completed)
- ✅ Database credentials configured in `.env` file

### Check Your Setup

```bash
# Verify Node.js
node --version

# Verify MCP server files exist
ls -la /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server/dist/server.js

# Verify .env is configured
cat /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server/.env
```

---

## Quick Setup

### Step 1: Locate Claude Desktop Config Directory

Claude Desktop stores configuration in your user directory:

```bash
# macOS
open ~/Library/Application\ Support/Claude/

# Linux
~/.config/Claude/

# Windows
%APPDATA%\Claude\
```

### Step 2: Create or Edit `claude_desktop_config.json`

Create the file at:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration:

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

### Step 3: Restart Claude Desktop

1. Close Claude Desktop completely
2. Reopen Claude Desktop
3. The server should connect automatically

---

## Configuration Details

### Environment Variables

The MCP server needs these environment variables to connect to PostgreSQL:

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `DB_HOST` | localhost | Yes | PostgreSQL server hostname |
| `DB_PORT` | 5432 | Yes | PostgreSQL port number |
| `DB_USER` | postgres | Yes | Database username |
| `DB_PASSWORD` | (empty) | Yes | Database password |
| `DB_NAME` | traffic_data | Yes | Database name |

### Configuration File Location

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

You can open it directly:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

Or use PowerShell:
```powershell
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

---

## Complete Example Configuration

Here's a complete `claude_desktop_config.json` with the traffic server and optional other servers:

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
        "DB_PASSWORD": "your_secure_password",
        "DB_NAME": "traffic_data",
        "NODE_ENV": "production"
      }
    }
  }
}
```

---

## Verification

### Step 1: Check Server Status

After restarting Claude Desktop, verify the server is connected:

1. Open Claude Desktop
2. Start a conversation
3. Look for the **🔧 Tools** icon or **@** symbol
4. You should see "traffic" listed as an available tool

### Step 2: Test a Tool

In Claude, type:

```
Use the traffic tool to get all traffic statistics
```

Claude will call `get_traffic_statistics` and return the results.

### Step 3: View Server Logs

To check if the server is running, you can monitor the logs:

```bash
# In a terminal, run the server directly to see logs
cd /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server
node dist/server.js
```

You should see:
```
🚀 Starting Traffic MCP Server...
✓ Connected to PostgreSQL database
✓ MCP Server is running and connected to database
```

---

## Troubleshooting

### Issue 1: Server Not Appearing in Claude

**Symptoms:** Tools don't show up in Claude Desktop

**Solutions:**

1. **Restart Claude Desktop**
   ```bash
   # Close all Claude windows
   # Reopen Claude Desktop
   ```

2. **Check config file exists**
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. **Verify the server path is correct**
   ```bash
   ls -la /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server/dist/server.js
   ```

4. **Check JSON syntax** - Use an online JSON validator to verify the config file

### Issue 2: Database Connection Error

**Symptoms:** Server starts but can't connect to database

**Solutions:**

1. **Verify PostgreSQL is running**
   ```bash
   psql -U postgres -d traffic_data -c "SELECT COUNT(*) FROM traffic_data;"
   ```

2. **Check credentials in `.env`**
   ```bash
   cat /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server/.env
   ```

3. **Update config with correct credentials**
   ```json
   "env": {
     "DB_HOST": "localhost",
     "DB_PORT": "5432",
     "DB_USER": "your_username",
     "DB_PASSWORD": "your_password",
     "DB_NAME": "traffic_data"
   }
   ```

4. **Test connection manually**
   ```bash
   cd /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server
   npm test
   ```

### Issue 3: "Server does not support tools" Error

**Symptoms:** Server runs but Claude says tools aren't supported

**Solutions:**

1. **Rebuild the server**
   ```bash
   cd /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server
   npm run build
   ```

2. **Restart Claude Desktop**

3. **Check server.js is properly compiled**
   ```bash
   head -20 /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server/dist/server.js
   ```

### Issue 4: "Cannot find module" Error

**Symptoms:** Error says Node can't find the server.js file

**Solutions:**

1. **Verify file exists**
   ```bash
   ls -la /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server/dist/server.js
   ```

2. **Use absolute path** (not relative path) in config

3. **Check Node path**
   ```bash
   which node
   ```
   Should show: `/opt/homebrew/bin/node` or similar

### Issue 5: Port Already in Use

**Symptoms:** "Address already in use" error

**Solutions:**

1. **The MCP server doesn't use a port** - it uses stdio communication, so this shouldn't happen

2. **If you see this, check for**:
   - Old server processes running
   ```bash
   ps aux | grep "node.*server.js"
   killall node
   ```

---

## Using the Server

### Available Tools in Claude

Once configured, you can use these tools in Claude:

#### 1. Get All Traffic Data
```
Ask Claude: "Show me the latest 50 traffic records"
Claude will use: get_all_traffic_data with limit: 50
```

#### 2. Search by Location
```
Ask Claude: "What's the traffic on road E4?"
Claude will use: get_traffic_by_location with location: "E4"
```

#### 3. Search by Date Range
```
Ask Claude: "Show traffic data from Jan 1-4, 2026"
Claude will use: get_traffic_by_date_range
```

#### 4. Get Statistics
```
Ask Claude: "Give me traffic statistics"
Claude will use: get_traffic_statistics
```

#### 5. Compare Vehicle Types
```
Ask Claude: "Compare speeds for different vehicle types"
Claude will use: get_speeds_comparison
```

#### 6. Filter by County
```
Ask Claude: "What's the traffic in Stockholm county?"
Claude will use: get_traffic_by_county with county: "Stockholm"
```

#### 7. Filter by Road
```
Ask Claude: "Show data for road number 3"
Claude will use: get_traffic_by_road with road_number: "3"
```

### Example Conversations

#### Example 1: Analyze Peak Traffic Times
```
You: "Analyze the traffic patterns from Jan 1-4 and tell me when speeds 
     were highest for passenger cars"

Claude will:
1. Call get_traffic_by_date_range(2026-01-01, 2026-01-04)
2. Call get_speeds_comparison()
3. Analyze and provide insights
```

#### Example 2: Compare Vehicle Types
```
You: "What's the difference in speeds between heavy vehicles with and 
     without trailers?"

Claude will:
1. Call get_vehicle_counts_comparison()
2. Call get_speeds_comparison()
3. Compare and explain the differences
```

#### Example 3: Regional Analysis
```
You: "Which county has the most traffic, and what are the speeds there?"

Claude will:
1. Call get_traffic_statistics()
2. Call get_traffic_by_county() for top counties
3. Provide regional analysis
```

---

## Advanced Configuration

### Multiple Environment Configurations

If you need different configurations for development/production:

```json
{
  "mcpServers": {
    "traffic-prod": {
      "command": "node",
      "args": ["/path/to/traffic/mcp-server/dist/server.js"],
      "env": {
        "DB_HOST": "prod-db.example.com",
        "DB_PORT": "5432",
        "DB_USER": "prod_user",
        "DB_PASSWORD": "prod_password",
        "DB_NAME": "traffic_data_prod"
      }
    },
    "traffic-dev": {
      "command": "node",
      "args": ["/path/to/traffic/mcp-server/dist/server.js"],
      "env": {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_USER": "postgres",
        "DB_PASSWORD": "dev_password",
        "DB_NAME": "traffic_data_dev"
      }
    }
  }
}
```

### Using .env File Instead

Alternatively, you can skip the `env` section and rely on the `.env` file:

```json
{
  "mcpServers": {
    "traffic": {
      "command": "node",
      "args": [
        "/Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server/dist/server.js"
      ]
    }
  }
}
```

Then edit the `.env` file with your credentials:
```bash
cd /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server
nano .env
# Update DB_PASSWORD and other credentials
```

---

## Testing Before Production

### Test 1: Run Server Manually
```bash
cd /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server
npm run build
node dist/server.js
```

You should see:
```
🚀 Starting Traffic MCP Server...
✓ Connected to PostgreSQL database
✓ MCP Server is running and connected to database
```

### Test 2: Run Tests
```bash
cd /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server
npm test
```

### Test 3: Verify Config Syntax
```bash
# Validate JSON
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool
```

---

## Updating the Server

When you update the MCP server code:

```bash
cd /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server

# Pull latest changes
git pull

# Install dependencies
npm install

# Rebuild
npm run build

# Restart Claude Desktop
# (Close and reopen)
```

---

## System Requirements

- **macOS**: 10.15+ (Intel or Apple Silicon)
- **Linux**: Ubuntu 18.04+, Fedora 30+
- **Windows**: Windows 10+
- **Node.js**: 18.0.0 or higher
- **PostgreSQL**: 12.0+
- **RAM**: 512MB minimum, 1GB recommended
- **Disk**: 100MB for server + dependencies

---

## Additional Resources

- [Claude Desktop Documentation](https://support.anthropic.com)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Node.js Documentation](https://nodejs.org/en/docs/)

---

## Support

### Check Server Status
```bash
# View running processes
ps aux | grep "node.*server.js"

# Check logs (if running in foreground)
cd /Users/arif.ahsan/Documents/GitHub/trafficdata/mcp-server
node dist/server.js
```

### Common Commands

```bash
# Rebuild server
npm run build

# Run tests
npm test

# Start server in development
npm run dev

# Watch mode (auto-compile)
npm run watch
```

---

## Checklist

Before considering your setup complete:

- [ ] Node.js 18+ installed
- [ ] PostgreSQL running with `traffic_data` table
- [ ] `.env` file configured with correct credentials
- [ ] Server built successfully (`npm run build`)
- [ ] `claude_desktop_config.json` created with correct paths
- [ ] Claude Desktop restarted
- [ ] Traffic tools visible in Claude
- [ ] Can successfully call a tool (e.g., `get_traffic_statistics`)
- [ ] Database returns real data

---

**Setup Complete!** 🎉

Your Traffic MCP Server is now integrated with Claude Desktop. Start using the tools in your conversations!
