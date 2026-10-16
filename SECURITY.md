# Exposed credentials remediation

The previous public history contained embedded API-Football and Telegram bot credentials. **Removing them from source does not revoke them or erase prior commits.**

1. Immediately revoke/rotate the exposed API-Football API key in its provider dashboard.
2. Regenerate the exposed Telegram bot token using BotFather, then update any other services that use that bot.
3. In GitHub repository Settings → Secrets and variables → Actions, add `API_FOOTBALL_KEY`, `TELEGRAM_BOT_TOKEN`, and `TELEGRAM_CHAT_ID` using newly issued values. Do not share the values in chat, issues, screenshots, or commits.
4. Configure any other hosting service using the Streamlit app to provide `API_FOOTBALL_KEY` in its private environment settings.
5. Review and clean the public Git commit history with appropriate GitHub support or a planned history rewrite. This PR does not rewrite history.
6. Verify GitHub Actions and Telegram deliveries with the replacement credentials before retiring previous workflows.

This branch intentionally has no auto-deployment. **Merging without configuring secrets will cause scheduled notifications to stop.**
