# Changelog - Username Sniper Bot

All notable changes to this project will be documented in this file.

## [0.5] - 2026-01-07

### 🌟 VIP Membership Program

#### New Features
- **Text Hunt Mode** (VIP Exclusive)
  - UNLIMITED 500-letter custom hunts
  - Optimized for small username patterns
  - No usage limits or cooldowns
  - Instant availability between hunts

- **Enhanced Hunt Quotas** (VIP Users)
  - 10,000 hunts per 3-day cycle
  - Automatic reset on schedule
  - All platforms supported

- **Official X API v2 Integration**
  - Batch username checking (up to 100 usernames per request)
  - VIP users: 100 requests/hour limit
  - Official API endpoint (no IP bans)
  - Automatic logging of available usernames
  - 10x faster checking than single-request method

- **Premium User Interface**
  - Exclusive gold-themed design for VIP members
  - Visual tier differentiation
  - Enhanced feature descriptions
  - Premium help documentation

- **Improved Permission System**
  - Role-based access control
  - Multiple tier support
  - Real-time limit validation

### Improvements
- Streamlined VIP onboarding experience
- Faster cooldown cycles (3 days vs 7 days)
- Enhanced user feedback and status information
- Separated UI/UX for different user tiers
- Comprehensive help system for each tier
- Official API integration for efficient batch checking

---

## [0.4] - 2026-01-07

### Added
- 🎯 **Tiered Hunt Rate Limiting System**
  - Multiple user tier support with different quota levels
  - Automatic quota resets
  - Role-based access control

- 👑 **User Permission Tiers**
  - Owner tier with premium access
  - Whitelisted tier with elevated quotas
  - Standard tier for regular users

- 📊 **Hunt Limit Enforcement**
  - Real-time validation before hunt starts
  - User-friendly status messages
  - Automatic cooldown tracking

- 📈 **Enhanced User Feedback**
  - Tier information in command responses
  - Remaining quota display
  - Clear cooldown countdowns

- 🔔 **Improved Logging**
  - Version information on startup
  - Configuration summary
  - System status reporting

### Changed
- Updated core hunt validation system
- Improved tier detection and assignment
- Enhanced error messaging
- Better user status visibility
- Updated help documentation

---

## [0.3] - Previous Release

### Features
- Multi-platform username availability checking
  - Roblox, Twitter/X, GitHub, TikTok, Discord
- Multiple pattern generation options
- Real-time progress tracking with visual indicators
- Flexible export formats for results
- Discord-native interface with interactive components
- Optimized API rate limiting
- Concurrent request management

---

## Getting Started

### Installation
1. Install required dependencies from requirements.txt
2. Configure your bot token in environment settings
3. Start the bot and use `/snipe` to begin hunting

### Basic Usage
- Run `/snipe` to start a username hunt
- Select your target platforms
- Choose or create username patterns
- Enter desired quantity (based on your tier)
- Export results in preferred format

### Command Reference
- `/snipe` - Start a new hunt session
- `/help` - View detailed feature information
- Select from interactive menus for configuration

---

## Features

### Core Capabilities
- **Multi-Platform Support**: Check availability across major platforms
- **Pattern Generation**: Create custom or use preset patterns
- **Real-Time Progress**: Visual feedback during hunts
- **Flexible Export**: Multiple export formats available

### Tier Benefits
- **Standard Tier**: Basic hunting capabilities with reasonable quotas
- **VIP Tier**: Enhanced quotas and exclusive text hunt mode

---

## Performance & Reliability

- Optimized API request handling
- Rate limiting to prevent platform blocks
- Automatic request batching
- Concurrent user session management
- Graceful error handling
- Official X API v2 integration for batch checking

---

## Support

For questions about features, usage, or technical issues, please refer to the help command or contact support channels.
