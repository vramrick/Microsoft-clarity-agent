## Turn 1

**User:**
Hey. I've been applying to software engineer jobs for about ten weeks now — roughly 80 applications — and I'm getting almost no responses. Three recruiter phone screens, no technical interviews, no offers. I think my resume might be the problem. Can you take a look and tell me what to fix?

Here's what I've been sending out:

----------
TYLER BROOKS
tyler.brooks.tx@gmail.com · Austin, TX · (512) 555-0192

OBJECTIVE
Software Engineer position at a growth-stage technology company.

EDUCATION
University of Texas at Austin — 2016–2018 (60 credits)
Austin Community College — 2024–present (B.S. Computer Science, in progress, expected 2026)
Coursera: Python for Everybody Specialization — 2024
freeCodeCamp: Responsive Web Design — 2024

EXPERIENCE
United States Marine Corps — 2018–2024

TECHNICAL SKILLS
Python · JavaScript · HTML/CSS · Git · Linux command line
----------

I've heard ATS systems care a lot about keywords and that bullet points should start with action verbs. I want to make sure I'm doing both of those things.

**Assistant:**
Honest answer: the ATS keywords and action verbs are real concerns, but they're not your biggest problem. I'd put them third on the list. Here's what I actually see:

---

**The critical issue: your Marine Corps service is invisible.**

Six years of service — 2018 to 2024 — and the resume just says "United States Marine Corps." That's it. Recruiters see a six-year gap with no content and move on. But those six years almost certainly contain exactly what hiring managers want: leadership under pressure, accountability for people and equipment, operational problem-solving, technical systems experience. We don't know because you haven't told us.

This is the most important thing to fix, and it can't be fixed with keywords — it has to be filled in with real content.

---

**Second: no projects section.**

For a career transitioner without commercial software experience, projects are your proof of technical ability. Coursework projects, personal projects, anything you built — they belong on this resume. Without them, recruiters have no evidence you can write code beyond the skills list.

---

**Third: your objective line is working against you.**

"Software Engineer position at a growth-stage technology company" is filler — every recruiter has read it a hundred times. Replace it with a 2–3 sentence summary that leads with who you are: *Marine veteran, CS student, [specific skills], looking to bring [X] to [type of role]*. That's a person. The objective line is a form.

---

**Fourth: technical skills are thin.**

Python, JavaScript, HTML/CSS, Git, Linux is a starting point. What frameworks have you used? React? Flask? FastAPI? Any databases — SQL, SQLite, PostgreSQL? Any cloud basics — AWS, GCP? Any testing tools? If you've used them even in coursework, they belong here.

---

**On ATS and action verbs specifically:** Yes, both matter — but only once you have content. You can't put action verbs on empty lines. Once you flesh out your Marine service and projects, we can make sure every bullet starts strong (*Led, Managed, Built, Reduced, Deployed*) and that the skills section echoes keywords from the job descriptions you're targeting.

---

A few questions that'll help us actually fix this:

1. What did you do in the Marines? MOS, rank, any technical or leadership roles?
2. What have you built — even small things from your coursework or on your own?
3. What kinds of roles are you applying to — frontend, backend, full-stack, something else?

## Turn 2

**User:**
Fair enough. Let me answer those.

1. I finished as an E-6, Staff Sergeant. Two deployments to Kandahar — 2019 and 2020-2021 — on Security Force Assistance teams. Basically embedded advisors to Afghan National Army units. I learned Pashto for it, conversational now. Last two years stateside I was a training NCO at the School of Infantry. Ran a 12-week small-unit-tactics course, led four other instructors, designed three new training modules. Two of them are still in the current curriculum.

2. Projects are thin. I built a to-do app in Python and did some of the freeCodeCamp front-end stuff. Nothing I'd call impressive.

3. Full-stack or backend, mostly. I've been applying pretty broadly.

I'll be honest — I left almost all of that out because my transition counselor at Pendleton told me to only include things directly relevant to the job I'm applying for. Training Afghan soldiers didn't seem relevant to a software engineer role, so I cut it.

**Assistant:**
Your transition counselor meant well but gave you advice that's quietly destroying your application rate. Here's why it's wrong:

**"Relevant" doesn't mean the task is the same — it means the skill maps to something the employer cares about.**

You didn't just "train Afghan soldiers." You ran a foreign military advisory program in a combat zone with incomplete information, built trust with people across a language and culture barrier, and made it work. Then you came home, took ownership of a training program, managed a team of four, and designed curriculum that outlasted your own tenure. That's not irrelevant to software engineering. That's the exact profile a team lead looks for when deciding who to hire.

Here's what your Marine background *actually* signals to a tech hiring manager:

- **High performer.** E-6 in six years means you were promoted ahead of your peers, repeatedly. That doesn't happen by being average.
- **Systems thinker.** You designed training programs from scratch and they survived institutional review. That's documentation, abstraction, and iteration.
- **Team lead.** You managed four instructors. You've already done the job that a lot of junior devs spend years trying to get promoted into.
- **Can learn hard things.** You learned Pashto. Conversationally. For a job. Hiring managers who see that don't think "military stuff" — they think "this person will learn our stack."

---

Here's a draft of what your experience section could look like. Fill in the numbers I've marked with `[?]`:

---
**United States Marine Corps** | 2018–2024 | Staff Sergeant (E-6)

*Training NCO — School of Infantry, Camp Pendleton* | 2022–2024
- Led a team of 4 instructors delivering a 12-week small-unit tactics course to [? Marines] per cycle
- Designed 3 new training modules from scratch; 2 remain in the active SOI curriculum
- Managed instructor scheduling, performance tracking, and student evaluations across [? training cycles]

*Security Force Assistance Advisor — Kandahar Province, Afghanistan* | 2019, 2020–2021
- Embedded with Afghan National Army units as a tactical advisor across two combat deployments
- Built operational trust and coordinated directly with local commanders in Pashto (conversational)
- Operated in high-ambiguity environments requiring rapid decision-making with incomplete information

---

That last bullet is worth keeping even though it sounds non-technical — "high-ambiguity environments" and "incomplete information" are phrases software engineers recognize from their own work, and it distinguishes you from someone who's never had real stakes.

---

**On projects:** a to-do app isn't nothing, but you're right that it won't turn heads on its own. The question is: does it actually work, and is the code on GitHub? If yes, we can write it up honestly. If you have a few weeks and want to build something slightly meatier — a small REST API with a database, or a simple full-stack app — that would help. It doesn't have to be impressive; it has to prove you can wire things together end to end.

What numbers can you fill into those experience bullets? Approximate is fine — class sizes, number of cycles per year, whatever you remember.

## Turn 3

**User:**
Okay. That reframe on the counselor's advice actually lands. I've been thinking about "relevant" wrong.

Numbers I can give you:

- Class sizes were roughly 80 Marines per cycle at SOI
- We ran about 4 cycles per year, so maybe 3 of those overlapped with my time as training NCO — call it 12 cycles over two years
- Instructor scheduling and evals I handled myself; the other four instructors each owned specific blocks of instruction

The to-do app is on GitHub, it runs, it's just not interesting. Basic CRUD, no database — stores to a JSON file. I'd rather build something better than put it front and center.

One thing I want to ask: you mentioned the Marine background signals "team lead" to a hiring manager. But I'm applying for junior SWE roles — is that framing going to backfire? Like, am I going to look overqualified for the entry-level stuff and underqualified for anything with actual leadership in the title?

**Assistant:**
The concern is real but I think you're imagining a sharper trap than exists in practice.

**The "overqualified" risk is mostly about two things:** whether you'll get bored and quit, and whether you expect a salary above what they're paying. Neither of those is written on your resume — they come up in conversations where you can address them directly. What *is* written on your resume is up to you.

**The "underqualified for leadership" ceiling isn't really a ceiling yet.** No one is hiring you as a tech lead without commercial software experience. That's not on the table regardless of framing. So the floor is what matters, not the ceiling.

The right frame isn't *"I'm a leader, give me responsibility."* It's *"I bring unusual reliability and ownership to a junior role, and I grow fast."* That's a genuinely attractive pitch for a junior hire — it signals you'll be a strong mid-level engineer faster than the average new grad. Hiring managers for junior roles are often thinking about growth trajectory, not just current skill level.

The real question is: what's the cost of trying the fuller resume versus the current one? The current one has gotten you 3 phone screens from 80 apps. That's a ~4% response rate. The downside of showing your full background is probably some amount of "overqualified" rejection — but you're already getting effectively no responses, so the expected value of changing is strongly positive.

---

Here are the updated bullets with your real numbers:

---
**United States Marine Corps** | 2018–2024 | Staff Sergeant (E-6)

*Training NCO — School of Infantry, Camp Pendleton* | 2022–2024
- Led 4 instructors delivering a 12-week small-unit tactics course to ~80 Marines per cycle across 12 cycles
- Designed 3 new training modules; 2 remain in the active SOI curriculum
- Owned instructor scheduling, block-of-instruction assignments, and student performance evaluations

*Security Force Assistance Advisor — Kandahar Province, Afghanistan* | 2019, 2020–2021
- Embedded with Afghan National Army units as a tactical advisor across two combat deployments
- Coordinated directly with local commanders in Pashto (conversational) to build unit capability and operational trust
- Made high-stakes decisions under ambiguity and time pressure with incomplete information

---

On the to-do app: if you want to build something better, what interests you? Not "what will impress hiring managers" — that's the wrong starting point and usually produces generic projects. What would you actually use? A small tool that scratches a real itch tends to get built and finished; something you built to impress tends to stall half-done.

## Turn 4

**User:**
Those bullets look good. That's more like an actual person.

On the project question — honestly, the thing that comes to mind is something scheduling-related. When I was running instructor schedules at SOI it was all in spreadsheets that were constantly out of date. Some basic tool that lets a small team track who's assigned to what block, flag conflicts, update in real time — I would've used that. I don't know how marketable it is but I'd actually finish it.

One thing I want to push back on slightly: you keep framing this around me becoming a strong mid-level engineer faster than a new grad. And I'm not saying that's wrong, but — I'll be honest, I'm not sure software engineering is actually where my energy is. I liked the CS coursework okay but I liked the team projects more than the actual coding. What I actually liked in the Marines was the coordination side. The planning, getting people organized toward a real outcome, training junior Marines. The technical stuff — radios, weapons systems maintenance — I did it because I had to.

I've been assuming software engineering was the move because I started a CS degree. But I'm not sure the job I'm imagining actually looks like the thing I found rewarding.

**Assistant:**
That's worth stopping for, because it changes the problem significantly.

What you just described — coordination, planning, getting people organized toward an outcome, developing others — that's not a secondary interest. You led a 12-week training program for 80 Marines a cycle, designed curriculum that outlasted you, embedded with foreign military units and made them more effective. That's the thing you're *good* at and found meaningful. The coding was instrumental.

The question isn't "how do I get a software engineering job." The question is: **what role actually uses the thing you're good at?**

A few that fit your description much better than SWE:

**Technical Program Manager (TPM).** Coordinates engineering teams on complex technical projects without writing the code. Owns timelines, dependencies, cross-team communication, unblocking people. Your Marine background is almost custom-built for this — Amazon, Microsoft, and Google actively recruit veterans into TPM roles specifically because they bring structured thinking under pressure and accountability without needing authority. Your CS coursework gives you the technical credibility to talk to engineers credibly.

**Product Manager.** Defines what gets built and why. Lots of stakeholder coordination, prioritization under constraints, working from a user problem toward a solution. The scheduling tool you just described? That's product thinking — you identified a real pain point and designed a solution. That's the job.

**Implementation/Delivery Manager at a SaaS company.** Gets customers from "we bought this software" to "this software is working for us." Heavy on coordination, change management, training people. Your SFAT experience — building capability in another organization — maps onto this almost directly.

The CS degree isn't wasted in any of these. It gives you technical literacy that most people in those roles had to acquire on the job. It's an advantage, not a credential.

---

I want to ask directly: when you imagined yourself in a software engineering job — the day-to-day of it — what did that look like? And does it match what you're describing when you talk about what you actually liked?

## Turn 5

**User:**
Wait — you can apply for TPM or PM directly? I thought that was something engineers got promoted into after years on the job. Like a senior engineer who stops coding and starts running things. You're saying that's an actual entry-level job category I could apply for right now with my background?

To answer your question: when I imagined myself as a software engineer, the day-to-day I was picturing was mostly... honestly it was more like leading standups, figuring out why a project was stuck, talking to people about what they needed. Not six hours of heads-down coding. Which probably tells you something.

**Assistant:**
Yes. It's a real entry-level job category and you can apply right now.

The "engineers get promoted into PM" path exists, but it's one path, not the only one. Many successful PMs came from operations, consulting, teaching, military — anywhere that builds structured thinking, stakeholder communication, and ownership of outcomes. The thing companies are actually hiring for in an entry PM or TPM is someone who can hold a complex project together across multiple teams without having direct authority over anyone. That's your entire military career described back to you.

Specific things worth knowing:

**APM programs** (Associate Product Manager) — Google, Microsoft, Meta, LinkedIn, and others run formal programs specifically for people entering PM without prior PM experience. They're competitive, but they're designed for this exact situation. Military backgrounds are explicitly valued.

**Amazon** has a dedicated veteran hiring initiative and TPM is one of their primary veteran entry points. They care a lot about structured thinking — their interview process is behavioral/principles-based, which plays to your strengths.

**Microsoft** has a Military Affairs program and actively recruits veterans into PM and program management roles.

And here's the thing: the resume we've been building gets *better* for these roles, not worse. Instead of apologizing for the leadership background in a junior SWE context, you lead with it. The Training NCO role — designing curriculum, managing a team, driving outcomes across 12 cycles — that's the centerpiece, not something to explain away.

The scheduling tool you described is also a stronger PM portfolio piece than a SWE portfolio piece. "I identified a real coordination failure I experienced firsthand, designed a solution, and built a prototype to validate it" — that's a PM interview story, start to finish.

---

What you said about the SWE day-to-day you were imagining: standups, figuring out why a project is stuck, talking to people about what they need. That's Tuesday afternoon for a PM. You weren't imagining a software engineering job. You were imagining this job.

So the question becomes: do you want to change directions, or keep the SWE track? There's no wrong answer — SWE is a real path and what we've built is a genuinely improved resume for it. But the investment of effort is different depending on which way you go.

## Turn 6

**User:**
Okay. That's genuinely the most useful thing anyone has told me in ten weeks of this job search.

I want to change directions. The SWE resume work isn't wasted — I'll keep those bullets — but if TPM or APM is a real target with my background, that's where I should be pointing. The day-to-day you're describing is what I was actually picturing when I thought about what I wanted.

Practically speaking: what do I actually do next? Do I need to reframe the whole resume around PM, or is it mostly the same content repositioned? And are the APM programs realistic at 28, or are those really designed for new grads coming out of undergrad?

**Assistant:**
**On the resume:** mostly repositioning, with one meaningful addition. The Marine Corps bullets are already in good shape — they read like PM/TPM experience because they *are* PM/TPM experience. What changes:

1. **The summary replaces the objective line.** This is the most important single edit. Here's a draft:

   > *Marine veteran (E-6) with six years of leadership, coordination, and training experience, including two combat deployments and two years leading instructor teams at the School of Infantry. Technical foundation in software development (Python, JavaScript, CS coursework) applied to program management and cross-functional coordination. Track record of building team capability, designing systems that outlast individual tenure, and delivering outcomes in high-ambiguity environments.*

2. **Skills section gets reorganized.** Lead with the PM-relevant stuff: cross-functional coordination, curriculum design, stakeholder communication, training and development. Technical skills (Python, JavaScript, Linux) stay, but they're supporting evidence of technical literacy — not the headline.

3. **Projects reframe slightly.** The scheduling tool — even if partially built — is now a PM case study: *"Identified coordination failure from direct operational experience; designed and prototyped a scheduling and conflict-detection tool for small instructor teams."* The story matters as much as the code.

---

**On APM programs at 28:** Honest answer — the Google APM and Meta RPM programs skew heavily toward 22-year-old new grads in practice. Not impossible, but not your best bet.

What *is* realistic and worth prioritizing:

- **Amazon Pathways** — a veteran-specific program that pipelines military talent into PM and TPM roles. This is designed for exactly your profile. Apply here first.
- **Microsoft's Military Affairs hiring program** — active veteran recruiting into PM roles. Strong match.
- **Defense tech companies** — Anduril, Palantir, Shield AI, and similar firms build products for the operational contexts you've actually worked in. Your Kandahar deployments aren't just leadership experience there — it's domain expertise. These companies pay well and actively recruit veterans.
- **Direct junior PM/TPM applications** at Austin tech companies — no program required, just the right title search ("Associate PM," "Program Manager I," "Junior TPM").

---

**Short priority order:**

1. Rewrite the resume with that summary and repositioned skills
2. Apply to Amazon Pathways and Microsoft veteran programs this week
3. Look up Anduril, Shield AI, and Palantir — read their PM/TPM job postings and see if the language resonates
4. Start the scheduling tool — even a basic working version with a clear README explaining the problem it solves
5. Update LinkedIn to match the new framing — recruiters at these companies will look

The ten weeks that felt like failure were ten weeks trying to get into the wrong door. The door you're looking for is a different door, and you're a much stronger candidate for it.

## Turn 7

**User:**
That priority list is clear and I can act on it. The Amazon Pathways and Microsoft programs — I'll look those up today.

The defense tech angle I hadn't thought of. Anduril especially. I have domain experience in exactly the context they're building for. That's a different pitch than "veteran with CS coursework" — that's someone who's actually been in the operational environment their products are used in.

One thing I want to confirm before I go rebuild the resume: the summary draft you wrote — is that the right length for a summary? It feels longer than what I've seen. And should I be tailoring it per application, or is one version good enough to start?

**Assistant:**
**On length:** the draft I wrote is a sentence too long. The third sentence retreads what the bullets below it will show. Cut it. Tighter version:

> *Marine Staff Sergeant (E-6) with six years of operational leadership, coordination, and training experience — including two combat deployments and two years managing instructor teams at the School of Infantry. Targeting technical program management and product management roles where cross-functional accountability, operational domain expertise, and technical literacy intersect.*

Two sentences. Recruiters read the summary to calibrate how to read the rest — it doesn't need to prove anything on its own, just set the right frame.

**On tailoring:** one strong base version is the right place to start. Don't try to customize everything before you've sent a single application. But once you have the base:

- For your top targets (Amazon Pathways, Microsoft, Anduril specifically), spend 5 minutes adjusting the summary's second sentence to echo the role's language — if they say "stakeholder alignment," use that phrase; if they say "delivery," use that.
- Make sure 3–4 keywords from each job description appear somewhere in your resume. This is the ATS concern you originally came in with — it's real, but it's a 5-minute step per application, not a resume design principle.

The base resume does 90% of the work. The tailoring is the last 10% for applications that matter most.

You came in asking whether your bullets had action verbs. The actual problem was that the resume was hiding a genuinely strong candidate. Go rebuild it — you've got what you need.
