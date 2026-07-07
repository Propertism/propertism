# M2.10 Future Recommendations & Backlog

These items represent future enhancements for the **Conversation Memory & Context Management** module. They are non-blocking and preserved here for subsequent development cycles.

---

## 1. Context Namespaces
Introduce logical namespaces such as:
- `Session`
- `Inquiry`
- `Service`
- `Knowledge`
- `Navigation`
- `User`

This will simplify variable scoping and partition data access as the conversational capability scale grows.

---

## 2. Context Locks
Allow selected variables or scopes to become read-only or "locked" once validated.
* *Example workflow:* After an Inquiry is successfully submitted, lock the corresponding inquiry context keys so they cannot be overwritten during the remaining session duration unless explicitly cleared by the framework.

---

## 3. Context Snapshots
Support named state checkpoints to enable rollbacks or multi-step form resumption:
- `Before Inquiry`
- `After Inquiry`
- `Before Navigation`

Allows debug engines or conversational flow rules to safely undo topic switches.

---

## 4. Context Events
Publish lifecycle signals to Django's signal framework or event dispatchers to enable decoupling:
- `context_created`
- `context_updated`
- `topic_changed`
- `topic_restored`
- `context_cleared`

---

## 5. Memory Policies
Extend TTL controls by mapping specific keys to lifecycle policies:
- `Session Only` (clear when window closes/session logs out)
- `Expire After 30 Minutes` (sliding time-to-live)
- `Expire After Submission` (garbage collect once lead is created)
- `Manual Clear Only`

---

## 6. Context Schema Registry
Instead of allowing arbitrary unstructured context variables, establish a declarative Registry of supported keys, declaring data types, default values, and description text. This enhances schema governance and system transparency.

---

## 7. Context Visualization
Develop an administrative dashboard view displaying real-time tracking for active sessions:
- Current Topic
- Topic Stack
- Active Variables
- Outstanding Fields
- Active Intents, Services, and Inquiry links

---

## 8. Context Replay
Build a diagnostic replay engine that reads sequential transition traces from `ContextUpdateLog` to recreate step-by-step customer session trajectories, simplifying debug operations for support desks.
