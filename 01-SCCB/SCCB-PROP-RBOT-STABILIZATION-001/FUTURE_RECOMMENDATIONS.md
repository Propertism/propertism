# Future Recommendations - realBOT Stabilization

Following the implementation review of SCCB-PROP-RBOT-STABILIZATION-001, we propose the following guidelines for future development:

## 1. Suggestion Chip Definition Management
- Suggestion chips and their corresponding actions are currently loaded from database definitions that fallback to hardcoded entries in `suggestions_config.py`.
- **Recommendation**: Provide a unified Admin dashboard or spreadsheet import capability for marketing teams to easily define and update suggestion labels, icons, target actions, and priority scoring without developer involvement.

## 2. Advanced Multi-Channel Handover
- Currently, when human handover is requested, the admin receives an email or WhatsApp containing a direct link to resume the chat session on their device.
- **Recommendation**: Build a unified Agent Console using React that supports real-time WebSocket connection state updates. This will allow multiple advisors to collaborate, assign active tickets, and view active chat sessions dynamically with instant notifications.

## 3. Real-Time Chat Archival Policies
- Chats are currently archived instantly when the client closes the sliding panel or clears the chat.
- **Recommendation**: Implement a background task (e.g. Celery beat or a cron management task) that periodically scans active `RealBotSession` records that have been idle/inactive for a specific threshold (e.g., 30 minutes) and archives them automatically under `closure_reason='timeout'`.
