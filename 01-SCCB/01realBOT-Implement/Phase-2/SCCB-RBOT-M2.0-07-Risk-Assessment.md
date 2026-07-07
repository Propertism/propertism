<!-- OLIVINE-PLATFORM-META -->
<!--
Issued By: Antigravity (Authorized Execution Agent)
Reviewed By: Mindra (Final Review Authority)
Product Approval: Viji (Product Owner & Final Decision Authority)
Created By: Antigravity
Created On: 2026-07-05 14:40:00
Last Updated By: Antigravity
Last Updated On: 2026-07-05 14:40:00
Searchtag: SCCB-RBOT-M2.0-07-Risk-Assessment
-->

# SCCB-RBOT-M2.0 - Risk Assessment
## Technical, Migration, and Operational Risk Log with Rollback Protocols

---

## 1. Risk Evaluation Registry

The following table logs identified risks associated with integrating the realBOT platform:

| Risk ID | Description | Impact | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **R-01** | **Network Latency or Endpoint Timeout:** Calls to realBOT API from Propertism proxy gateway slow down responses. | High | Medium | 1. Implement strict connection timeouts (e.g., 5 seconds).<br>2. Fall back to local warning toasts or "Offline Advisor Desk" messaging if the endpoint times out. |
| **R-02** | **Widget Load Blocker:** Slow loading of external JavaScript widget blocks page interactions. | Medium | Low | 1. Add `async` and `defer` attributes to the loader script tags.<br>2. Lazy-load the widget iframe only after the user clicks the FAB. |
| **R-03** | **Data Loss During Model Migration:** Purging the local database tables deletes session histories. | Low | Low | 1. Take a full PostgreSQL backup (`pg_dump`) prior to deploying database migrations.<br>2. Keep local models in place (deprecated status) during Phase M2.1-M2.4, and run the drop table script only when integration is stable. |
| **R-04** | **JWT Signature Handshake Failure:** Expired keys or config mismatches block authentication. | High | Low | 1. Rigorous automated tests verifying key exchange signature validation.<br>2. Support API-key stubs for server-to-server operations during network failures. |
| **R-05** | **CORS and Origin Restrictions:** Browsers block requests to the realBOT script. | High | Medium | 1. Register proper origin whitelist mappings on both domains.<br>2. Ensure the CloudFront forwarding configuration propagates headers. |

---

## 2. Transition Rollback Protocols

To minimize production downtime, a two-level rollback strategy must be implemented in the codebase:

### Level 1: Configuration-Based Fallback Toggle
*   **Implementation:** Introduce a boolean configuration flag `REALBOT_INTEGRATION_ENABLED` (via settings or environment variables).
*   **Fallback Logic:**
    ```python
    # chat/views.py - Proxy gateway controller
    from django.conf import settings
    from django.http import JsonResponse

    def init_session(request):
        if not getattr(settings, 'REALBOT_INTEGRATION_ENABLED', False):
            # Fall back to offline advisory desk response
            return JsonResponse({
                "success": True,
                "session_id": "offline-fallback",
                "messages": [{
                    "id": "fallback-msg",
                    "sender": "assistant",
                    "text": "Our AI advisory desk is currently undergoing scheduled maintenance. Please submit an offline inquiry form or try again later.",
                    "metadata": { "chips": ["Submit Query"] }
                }]
            })
        # Normal proxy request to realBOT API
        return proxy_to_realbot(request)
    ```

### Level 2: Deployment Reversion
*   **Trigger:** System-wide server crashes, unresolvable CORS blocks, or memory leaks on production launch.
*   **Procedure:**
    1.  Revert the main git branch to the previous stable release commit (e.g., `git revert` or checking out the tag prior to integration).
    2.  CI/CD automatically builds and deploys the working version.
    3.  Confirm static files and database migrations are restored.

---
*Maintained by Antigravity | 2026-07-05 14:40:10 IST*
