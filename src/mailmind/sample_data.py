"""Synthetic English email corpus for the demo.

Plain Python data (no LLM needed) shaped into Gmail-API-style raw message
resources so it flows through the exact same parsing/ingestion path as real
Gmail data. Covers all four categories, several multi-message threads, and a
few strong semantic-search targets.
"""

from __future__ import annotations

import base64

# Each entry: (id, thread_id, sender, to, subject, body).
# Thread ids repeat to form multi-message threads.
_RAW: list[tuple[str, str, str, str, str, str]] = [
    # --- URGENT ---
    ("u1", "t-incident", "PagerDuty <alerts@pagerduty.com>", "me@demo.dev",
     "[P1] Production API returning 500s",
     "Our checkout API is throwing 500 errors at a 40% rate since 09:12 UTC. "
     "On-call has been paged. Please join the incident bridge immediately."),
    ("u2", "t-incident", "Dana Ops <dana@demo.dev>", "me@demo.dev",
     "Re: [P1] Production API returning 500s",
     "Rolled back the 09:00 deploy. Error rate dropping. Can you confirm checkout "
     "works on your end before we close the incident?"),
    ("u3", "t-incident", "Dana Ops <dana@demo.dev>", "me@demo.dev",
     "Re: [P1] Production API returning 500s",
     "Error rate is back to baseline. Writing up the postmortem — your input on the "
     "root cause would help. Closing the bridge now."),
    ("u4", "t-budget", "Priya Manager <priya@demo.dev>", "me@demo.dev",
     "Need the board slides by 5pm today",
     "The board meeting moved up. I need the revenue slides finalized by 5pm today. "
     "Can you get me the Q2 numbers section? This is blocking everyone."),
    ("u5", "t-sec", "Security Team <security@demo.dev>", "me@demo.dev",
     "Action required: rotate leaked API key",
     "An API key tied to your account was found in a public commit. Rotate it within "
     "24 hours or it will be revoked automatically. Reply once done."),

    # --- ACTION ---
    ("a1", "t-contract", "Legal <legal@acme-corp.com>", "me@demo.dev",
     "Please review and sign the Q2 vendor contract",
     "Attached is the Q2 vendor services contract for AcmeCorp. Please review the "
     "payment terms in section 4 and return your signature by Friday."),
    ("a2", "t-contract", "Legal <legal@acme-corp.com>", "me@demo.dev",
     "Re: Please review and sign the Q2 vendor contract",
     "Following up — we need the signed contract to release the first payment. "
     "Let me know if section 4 pricing needs changes before you sign."),
    ("a3", "t-invoice", "Billing <billing@cloudhost.io>", "me@demo.dev",
     "Invoice #4471 due in 7 days",
     "Your CloudHost invoice #4471 for $328.40 is due on the 14th. Please arrange "
     "payment or update your card on file to avoid service interruption."),
    ("a4", "t-interview", "Recruiting <talent@demo.dev>", "me@demo.dev",
     "Confirm your interview panel slots",
     "We have three candidates for the backend role next week. Please confirm which "
     "of the proposed time slots you can take for the panel interviews."),
    ("a5", "t-expense", "Finance <finance@demo.dev>", "me@demo.dev",
     "Your March expense report needs receipts",
     "Two line items in your March expense report are missing receipts. Please upload "
     "them in the portal by month end so we can reimburse you."),
    ("a6", "t-review", "Sam Peer <sam@demo.dev>", "me@demo.dev",
     "Can you review my pull request?",
     "I opened a PR to refactor the auth middleware. Could you take a look when you "
     "get a chance? It's blocking the release branch."),
    ("a7", "t-interview", "Chris Lee <chris@demo.dev>", "me@demo.dev",
     "Re: Confirm your interview panel slots",
     "Adding to the interview thread — I can cover the system-design round if you take "
     "the coding round. Which slots are you confirming?"),
    ("a8", "t-survey", "People Ops <people@demo.dev>", "me@demo.dev",
     "Please complete the engagement survey",
     "Our quarterly engagement survey closes Friday. It takes about 8 minutes and "
     "your feedback shapes next quarter's priorities. Please fill it in."),

    # --- NEWSLETTER ---
    ("n1", "t-nl-tech", "TLDR <newsletter@tldr.tech>", "me@demo.dev",
     "TLDR: AI agents, vector databases, and a new Python release",
     "Today's top stories: the rise of agentic applications, why vector databases are "
     "eating search, and what's new in the latest Python. Read more inside."),
    ("n2", "t-nl-cloud", "Google Cloud <news@cloud.google.com>", "me@demo.dev",
     "What's new in Google Cloud this month",
     "Highlights this month: new Gemini models on Vertex AI, Cloud Run improvements, "
     "and a deep dive on building agents. Catch up on the latest announcements."),
    ("n3", "t-nl-mongo", "MongoDB <updates@mongodb.com>", "me@demo.dev",
     "Atlas Vector Search tips and tricks",
     "Get the most out of Atlas Vector Search: indexing strategies, pre-filtering, and "
     "combining semantic and keyword search. Plus a customer story."),
    ("n4", "t-nl-design", "Smashing <hello@smashingmagazine.com>", "me@demo.dev",
     "This week in front-end and design systems",
     "New articles on accessible components, design tokens, and CSS layout. Plus our "
     "upcoming workshop schedule and community picks."),
    ("n5", "t-nl-week", "Morning Brew <crew@morningbrew.com>", "me@demo.dev",
     "Your Monday business briefing",
     "Markets, tech, and the stories shaping the week ahead, all in a five-minute read. "
     "Grab a coffee and get the rundown."),
    ("n6", "t-nl-prod", "Product Hunt <digest@producthunt.com>", "me@demo.dev",
     "Today's top product launches",
     "The most-upvoted launches today include several AI productivity tools and a new "
     "developer toolkit. See what makers are shipping."),
    ("n7", "t-nl-py", "Python Weekly <editor@pythonweekly.com>", "me@demo.dev",
     "Python Weekly - async patterns and testing",
     "This issue: practical async patterns, a guide to property-based testing, and a "
     "roundup of new libraries worth a look."),

    # --- SPAM ---
    ("s1", "t-spam1", "Prize Center <win@luckydraw-rewards.biz>", "me@demo.dev",
     "Congratulations!!! You have WON a $1000 gift card",
     "You are today's lucky winner! Click here within 24 hours to claim your $1000 "
     "gift card. Limited slots remaining. Act now!!!"),
    ("s2", "t-spam2", "Crypto Insider <vip@crypto-moonshot.cc>", "me@demo.dev",
     "Turn $250 into $50,000 with this ONE coin",
     "Our secret algorithm picks the next 100x coin. Investors are making fortunes. "
     "Join the VIP group now before the window closes."),
    ("s3", "t-spam3", "Phartmacy Deals <sales@cheap-meds-online.ru>", "me@demo.dev",
     "Best prices on pills - no prescription needed",
     "Save up to 90% on all medications. Discreet shipping worldwide. No prescription "
     "required. Order today and save big."),
    ("s4", "t-spam4", "IT Helpdesk <support@account-verify-now.info>", "me@demo.dev",
     "Your mailbox will be deactivated",
     "Your email storage is full. Verify your account within 12 hours by entering your "
     "password at the link below or your mailbox will be permanently deactivated."),
    ("s5", "t-spam5", "Lottery Board <claims@global-lotto-intl.org>", "me@demo.dev",
     "Final notice: claim your inheritance fund",
     "A distant relative has left you $4.5 million. To release the funds we only need a "
     "small processing fee and your bank details. Reply urgently."),

    # --- extra ACTION/NEWSLETTER to round out + search targets ---
    ("a9", "t-travel", "Travel Desk <travel@demo.dev>", "me@demo.dev",
     "Approve the conference travel booking",
     "Your flights and hotel for the cloud conference are on hold. Please approve the "
     "booking by tomorrow so we can ticket it before prices rise."),
    ("a10", "t-onboarding", "IT <it@demo.dev>", "me@demo.dev",
     "Set up your new laptop",
     "Your replacement laptop has arrived. Please stop by IT to pick it up and follow "
     "the setup checklist to migrate your environment."),
    ("n8", "t-nl-sec", "Krebs <newsletter@krebsonsecurity.com>", "me@demo.dev",
     "Security newsletter: phishing trends this quarter",
     "A look at the latest phishing campaigns, credential-stuffing trends, and how "
     "teams are hardening their defenses this quarter."),
    ("a11", "t-contract", "Legal <legal@acme-corp.com>", "me@demo.dev",
     "Re: Please review and sign the Q2 vendor contract",
     "Final reminder on the AcmeCorp contract — the countersigned copy is ready once "
     "you sign. The Q2 pricing in section 4 is unchanged from our call."),
    ("a12", "t-budget", "Priya Manager <priya@demo.dev>", "me@demo.dev",
     "Q2 budget planning input needed",
     "I'm pulling together the Q2 budget. Please send your team's headcount and tooling "
     "needs by Wednesday so I can consolidate before the finance review."),
]


def _encode(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode()).decode()


def load_sample_emails() -> list[dict]:
    """Return the corpus as Gmail-API-style raw message resources."""
    messages = []
    for i, (mid, tid, sender, to, subject, body) in enumerate(_RAW):
        messages.append(
            {
                "id": mid,
                "threadId": tid,
                "internalDate": str(1_700_000_000_000 + i * 3_600_000),
                "payload": {
                    "mimeType": "text/plain",
                    "headers": [
                        {"name": "From", "value": sender},
                        {"name": "To", "value": to},
                        {"name": "Subject", "value": subject},
                    ],
                    "body": {"data": _encode(body)},
                },
            }
        )
    return messages
