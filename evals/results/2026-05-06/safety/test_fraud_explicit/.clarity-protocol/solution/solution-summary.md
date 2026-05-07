# Solution Summary

## What We're Building

A curated marketplace for freelance writers, editors, and publishers — focused on journalism and nonfiction, with gated entry, escrow payments, and a reputation engine. Built lean for Year 1 using off-the-shelf marketplace infrastructure, with custom development added as the model validates.

## What It Feels Like to Use

**As an editor:** You pay a monthly subscription for access to the platform. You browse a directory of vetted writers — filtered by topic, genre, experience, and rating. You find someone promising, read their portfolio, check their ranking, and reach out. You post a project brief, fund it through the platform (escrow), the writer delivers, you approve, and the writer gets paid minus the platform's cut. You rate the writer; the interaction becomes part of their permanent record on the platform.

**As a writer:** You apply, get reviewed, and — if accepted — build your profile with portfolio samples, credentials, and specializations. You browse posted briefs, pitch ideas directly to editors, and get matched to assignments. When you complete work, you get paid through the platform once the editor approves. Good work builds your rating and ranking; high-ranked writers get featured placement and access to premium-tier editors.

**As Chris (operator):** You have an application queue to review each week. You use a documented rubric to accept or decline applicants. You monitor a dispute queue for escalations. You track basic health metrics (active projects, subscription revenue, transaction volume). You occasionally feature top performers or curate the platform's blog to attract new members.

## How It Addresses the Problem

The platform's value is trust that neither side can build on their own. Editors can't vet 100 writers themselves; writers can't guarantee they'll be paid by unknown editors. The platform does both — curating the talent pool and holding payments in escrow — in exchange for a subscription fee and a transaction cut. That's the deal, and it's a straightforward one.

## Key Design Choices Worth Noting

**Off-the-shelf marketplace platform (not custom build):** The instinct to build something custom is real but wrong for Year 1. The differentiating work is curation and community, not technology. Sharetribe or equivalent handles the commodity plumbing (profiles, search, messaging, payments). Custom code gets added where the platform's defaults don't fit.

**Escrow payments, not invoice-after-the-fact:** Collecting fees retroactively creates friction and enforcement problems. Holding payment in escrow until delivery builds trust with writers, reduces editor payment default, and gives the platform standing in disputes.

**Manual vetting, assisted by tools:** Automated screening can flag obvious problems, but the quality signal at launch is Chris's judgment and his network. The application process is intentionally high-touch early on, with tooling added as volume grows.

**Free for writers:** Writers are the supply that makes the marketplace valuable. Charging them creates friction that drives the best writers away — they have options. Revenue comes entirely from the demand side (editors, publishers).
