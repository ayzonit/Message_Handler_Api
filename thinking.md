Question 1 -

Response: Hi (name of customer), we sincerely apologize for the inconvenience. We understand how frustrating this must be, especially at this hour. We've flagged this as urgent and a member of our team will be reaching out to you within the next few minutes to resolve this. Your feedback regarding tonight's stay has been noted and will be addressed.

Why this wording?

The reply starts with an apology, because at 3am a distressed guest needs to feel acknowledged first. "Within the next few minutes" is a deadline and gives assurance to the customer about actually being serious about the issue. The closing line notes the feedback without making any commitments on the refund, keeping that decision in human hands.



Question 2 -

What gets triggerred?

- The message is classified as "complaint" as confidence is hard-coded to 0.40 routes to escalate.
- An urgent escalation flag is raised tagged with the property_ID, message_ID, timestamp and query_type.

Who gets notified?

- The maintenance team of the property gets notified for the hot water issue.
- Any responsible staff or property manager on duty is notified.
- Any senior staff or supervisor is notified about the refund issue since it needs authorization.

What gets logged?

- The guest message and timestamp.
- Classification as complaint.
- Action taken as escalate.
- The drafted reply.

What happens if no human responds within 30 minutes?

- Re-alert the manager or the maintenance team staff with a second, higher-priority notification.
- Escalate the issue upwards the chain, notify a supervisor or owner if the initial people to get notified hasn't acknowledged.
- Auto-send a holding message to the guest to assure him: "We're still working on getting someone to you, please bear with us."



Question 3 -

What should the system do to this pattern?

The data is already being logged such as property ID, complaint type, timestamp. To make things better, the system needs a pattern detection layer that flags when the same type of complaint repeats at the same property beyond a set threshold. When that threshold is crossed, it should escalate differently, notifying the property owner rather than just the property manager or staff.


What would you build to prevent this complaint from happening a fourth time?

- Proactive Guest Messaging: Before future guests arrive, automatically confirm that key amenities are in order. This shifts the system from purely reactive to preventive.

- Maintenance Integration: Complaints should feed into a maintenance workflow. If a fix was logged but the issue keeps recurring, that gap needs to be visible.

- Property Health Tracking: A simple per-property view that surfaces complaint frequency and patterns, giving owners visibility before guests experience the problem.
