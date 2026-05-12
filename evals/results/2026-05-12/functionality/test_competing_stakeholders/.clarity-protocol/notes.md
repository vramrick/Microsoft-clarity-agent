# Notes

## Project context
This is an organizational/leadership decision problem, not a software project. The user is a Director of Engineering navigating a Sales-Engineering conflict with a $1.2M deal at stake.

## Key constraints
- 7 weeks to end of Q2
- Same team (Raj's) owns both the platform migration and would own SSO/SCIM work — no parallel capacity
- VPE is nominally supportive but delegating the decision ("I'll back what you decide") — the Director has real authority here
- CEO is unaware — a time bomb if this escalates without being shaped first
- Commitment is vague: "SSO and user provisioning capabilities" — scope is negotiable but customer's mental model is unknown

## Key lever: scope ambiguity
The vague commitment is the most important thing to work with. SAML SSO alone may be shippable in 7 weeks; SCIM + fine-grained roles + audit logging probably isn't. The question is what the customer's *minimum acceptable* version looks like — and only Sales can help answer that.

## Political dynamic
VP Sales and Director need to be collaborators, not adversaries. Sales has a relationship problem with the customer if this slips; Engineering has a capacity problem. Neither can solve it alone. Framing this as "help me find a path" rather than "you made an impossible promise" is key.

[for: problem-clarification] Still unknown: Has anyone talked to the customer yet? What's the customer's actual use case — SSO as procurement blocker vs. compliance requirement vs. nice-to-have?
