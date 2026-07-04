<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Astra (Platform Owner-Propertism)
Reviewed By: Viji (Product Owner & Final Decision Authority)
Created By: Astra
Created On: 2026-07-04 18:36:00
Last Updated By: Astra
Last Updated On: 2026-07-04 18:36:00
Searchtag: SCCB-PROP-M2.X-COMM-001-06-CHANGE-SUMMARY
-->

# SCCB-PROP-M2.X-COMM-001-06
## Change Summary

**Status:** COMPLETED  
**Version:** 1.0  
**Repository:** Propertism  
**Date:** July 04, 2026  

---

## 1. File Modification Log

The following files were added/modified during the framework implementation:

| Action | File | Description |
| :--- | :--- | :--- |
| **[MODIFY]** | [settings.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/realtor_project/settings.py) | Registered new installed app `communications`. |
| **[MODIFY]** | [urls.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/realtor_project/urls.py) | Mapped prefix `/api/v1/communications/` to router. |
| **[MODIFY]** | [views.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/content/views.py) | Refactored `send_rfq_notification` and `newsletter_subscribe` to use `AcknowledgementService.send`. |
| **[NEW]** | [models.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/communications/models.py) | DB models (Templates, Channels, Types, Deliveries, Retry). |
| **[NEW]** | [providers.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/communications/providers.py) | Transport wrappers for SMTP, WhatsApp, and SMS stub. |
| **[NEW]** | [dispatcher.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/communications/dispatcher.py) | Background ThreadPoolExecutor asynchronous dispatcher. |
| **[NEW]** | [services.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/communications/services.py) | Gateway services layer. |
| **[NEW]** | [views.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/communications/views.py) | REST API endpoints. |
| **[NEW]** | [serializers.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/communications/serializers.py) | Serialization rules. |
| **[NEW]** | [urls.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/communications/urls.py) | Endpoint routing mapping. |
| **[NEW]** | [admin.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/communications/admin.py) | Django Admin panel config. |
| **[NEW]** | [process_communications_queue.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/communications/management/commands/process_communications_queue.py) | Outbox background worker command. |
| **[NEW]** | [tests.py](file:///d:/viji/viji-olivine/03rolledout/01propertism/communications/tests.py) | Unit and API test cases. |

---

***
*Maintained by Astra | 2026-07-04 18:36 IST*
