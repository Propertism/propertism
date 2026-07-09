# SCCB-PROP-RBOT-STABILIZATION-001: realBOT Stabilization & Enhancements

## Problem Statement & Requirements
The following feedback and requests were collated for stabilization:
1. After selecting the Country chip, still the phone number is being asked (retrospective validation & country-aware extraction).
2. The spaces/padding across the client chat and the bot chat should be reduced for a tighter, cleaner look.
3. Suggestion Chips should trigger their appropriate actions (URLs, phone call, whatsapp, clear chat, etc.) instead of just sending text as a user message.
4. Inquiry forms submission fails at times (NoneType fields in database creation), and the inquiry mail content still carries technical details (attribution, session IDs) not relevant to the customer.
5. Handover "Talk to Advisor" requires the admin to be notified via email or whatsapp with a link to open the chat on phone/desktop and continue.
6. Ending the chat (close button, end session, clear chat) should save the chat history to a django model containing date, start/end time, duration, and transcripts.
7. The django model UI in admin must be wrapped in a React component resembling the realBOT chat bubble UI.
8. Customize the mobile number prompt to "Please share your mobile number." only.
