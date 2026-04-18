from __future__ import annotations

from datetime import date
from typing import Any

from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'consumer-rights-hub-demo-secret'

CATEGORY_CONTENT: dict[str, dict[str, Any]] = {
    'shopping': {
        'title': 'Online Shopping Disputes',
        'route': 'shopping',
        'short': 'Comprehensive support for resolving online shopping issues including counterfeit products, refund denials, and order discrepancies.',
        'common_issues': [
            {'title': 'Counterfeit or Fake Products', 'text': 'Received items that do not match authenticity claims or brand standards.', 'slug': 'shopping-counterfeit-products'},
            {'title': 'Refund or Return Denial', 'text': 'Seller refuses legitimate refund or return requests within policy period.', 'slug': 'shopping-refund-return-denial'},
            {'title': 'Order Mismatch', 'text': 'Received different items, wrong sizes, colours, or specifications.', 'slug': 'shopping-order-mismatch'},
            {'title': 'Damaged or Defective Items', 'text': 'Products arrived damaged or stopped working within warranty period.', 'slug': 'shopping-damaged-or-defective-items'},
        ],
        'rights_cards': [
            {'title': 'Right to Return (7-14 Days)', 'text': 'Many online purchases can be returned within the advertised period, and faulty goods may qualify for stronger remedies.', 'slug': 'shopping-right-to-return'},
            {'title': 'Right to Accurate Information', 'text': 'Sellers must provide truthful product descriptions, pricing, and delivery information.', 'slug': 'shopping-right-to-accurate-information'},
            {'title': 'Right to Quality Goods', 'text': 'Products must be of satisfactory quality, fit for purpose, and match their description.', 'slug': 'shopping-right-to-quality-goods'},
        ],
        'evidence_required': [
            'Order confirmation and receipt',
            'Product photos showing defects or discrepancies',
            'Communication records with the seller',
            'Payment proof and transaction details',
        ],
        'evidence_helpful': [
            'Screenshots of the product listing',
            'Packaging and shipping labels',
            'Expert opinions for counterfeit claims',
            'Comparison with authentic products',
        ],
        'resource_page': 'resource-shopping',
        'apply_label': 'Start Rights Protection Process',
        'secondary_label': 'Contact Support',
    },
    'fraud': {
        'title': 'Fraud & Information Leakage',
        'route': 'fraud',
        'short': 'Immediate assistance for online fraud, identity theft, unauthorised charges, and data breaches.',
        'emergency_steps': [
            ('Secure Your Accounts Immediately', 'Change passwords of affected accounts and enable two-factor authentication on all financial accounts.'),
            ('Contact Your Bank or Card Issuer', 'Report unauthorised charges immediately and request a card freeze or replacement if necessary.'),
            ('Document Everything', 'Take screenshots of suspicious messages, transactions, and communication. Save all evidence.'),
            ('Report to Authorities', 'File a report with the relevant authority and keep case numbers for reference.'),
        ],
        'common_issues': [
            {'title': 'Phishing Scams', 'text': 'Fake emails or texts pretending to be from legitimate companies requesting personal information.', 'slug': 'fraud-phishing-scams'},
            {'title': 'Identity Theft', 'text': 'Unauthorised use of your personal information to open accounts or make purchases.', 'slug': 'fraud-identity-theft'},
            {'title': 'Payment Fraud', 'text': 'Unauthorised charges on credit cards, digital wallets, or bank accounts.', 'slug': 'fraud-payment-fraud'},
            {'title': 'Data Breaches', 'text': 'Personal information exposed through company security failures or hacking.', 'slug': 'fraud-data-breaches'},
        ],
        'tips_left': [
            'Never share passwords or PINs with anyone',
            'Use strong, unique passwords for each account',
            'Enable two-factor authentication wherever possible',
            'Monitor bank statements and credit reports regularly',
        ],
        'tips_right': [
            'Urgent requests for personal or financial information',
            'Suspicious links or attachments in emails',
            'Offers that seem too good to be true',
            'Pressure to act immediately without verification',
        ],
        'resource_page': 'resource-fraud',
        'apply_label': 'Start Rights Protection Process',
        'secondary_label': 'Emergency Support',
    },
    'subscriptions': {
        'title': 'Subscription & Auto-Renewal Issues',
        'route': 'subscriptions',
        'short': 'Help with unwanted charges, difficult cancellations, hidden fees, and managing recurring payments.',
        'common_issues': [
            {'title': 'Unwanted Auto-Renewal', 'text': 'Subscriptions automatically renew without clear notice or easy cancellation options.', 'slug': 'subscriptions-auto-renewal'},
            {'title': 'Hidden or Increased Fees', 'text': 'Unexpected price increases or additional charges not disclosed during sign-up.', 'slug': 'subscriptions-hidden-fees'},
            {'title': 'Difficult Cancellation', 'text': 'Complex cancellation processes or customer service refusing legitimate requests.', 'slug': 'subscriptions-difficult-cancellation'},
            {'title': 'Free Trial Traps', 'text': 'Free trials converting to paid subscriptions without adequate warning or consent.', 'slug': 'subscriptions-free-trial-traps'},
        ],
        'rights_cards': [
            {'title': 'Right to Clear Terms', 'text': 'Companies must clearly disclose subscription terms, renewal dates, and pricing before you agree.', 'slug': 'knowledge-subscription-management'},
            {'title': 'Right to Cancel Easily', 'text': 'Cancellation should be as simple as signing up, and recent charges may be reversible in some situations.', 'slug': 'subscriptions-difficult-cancellation'},
            {'title': 'Right to Renewal Notices', 'text': 'Companies should warn users before charging for renewals or major price increases.', 'slug': 'subscriptions-auto-renewal'},
        ],
        'guide_left': [
            'Locate your subscription in the account settings or billing section',
            'Follow the cancellation process and save confirmation emails',
            'If unable to cancel online, contact customer service in writing',
            'Monitor your next billing cycle to confirm cancellation',
        ],
        'guide_right': [
            'Charged after a cancellation request',
            'No renewal notice provided before the charge',
            'Price increased without notification',
            'Cancellation process was unavailable',
        ],
        'resource_page': 'resource-subscriptions',
        'apply_label': 'Apply for Rights Protection',
        'secondary_label': 'Get Human Help',
    },
}

KNOWLEDGE_ALERTS = [
    ('New Email Phishing Campaign Targeting Online Shoppers', 'Fake shipping notifications claiming delivery issues. Do not click suspicious links.', 'Apr 10, 2026', 'High'),
    ('Cryptocurrency Investment Scam on Social Media', 'Fraudulent investment schemes promising unrealistic returns. Verify all investment opportunities.', 'Apr 8, 2026', 'Critical'),
    ('Impersonation of Government Agencies', 'Scammers posing as authorities and demanding immediate payment. Official agencies do not request payment by surprise phone calls.', 'Apr 3, 2026', 'High'),
]

KNOWLEDGE_TOPICS = [
    {
        'title': 'Consumer Rights',
        'summary': 'Understanding your return rights and warranties.',
        'items': ['What to do when a seller refuses a refund', 'Product quality standards and your rights'],
        'slug': 'knowledge-consumer-rights',
    },
    {
        'title': 'Fraud Prevention',
        'summary': 'How to spot phishing scams and protect your personal information online.',
        'items': ['Protecting your personal information online', "What to do if you've been scammed"],
        'slug': 'knowledge-fraud-prevention',
    },
    {
        'title': 'Subscription Management',
        'summary': 'How to cancel unwanted subscriptions and dispute hidden fees.',
        'items': ['Understanding auto-renewal risks', 'Getting refunds for unauthorised charges'],
        'slug': 'knowledge-subscription-management',
    },
]

SUCCESS_CASES = [
    {
        'id': 1,
        'tag': 'Shopping',
        'badge': 'Full Refund',
        'title': 'Received Full Refund for Counterfeit Designer Handbag',
        'summary': 'Ordered a designer handbag that turned out to be fake. Seller initially refused the refund, but the case succeeded after evidence and escalation.',
        'amount': '$450',
        'type': 'Full Refund',
        'days': '12 days',
        'likes': 142,
        'comments': 23,
        'helpful': 68,
        'story': [
            'I ordered a handbag that was advertised as an authentic designer item, but as soon as it arrived I could tell the stitching, logo placement, and packaging were wrong.',
            'I immediately saved screenshots of the product listing, my payment confirmation, and several close-up photos comparing the bag with authentic reference images.',
            'When the seller refused to refund me, I organised all of the evidence into one clear timeline and submitted it through the complaint process.',
            'After I escalated the case with that evidence pack, the refund was finally approved and I received the full amount back within 12 days.',
        ],
        'comment_threads': [
            ('Mia', 'Keeping the listing screenshots made a huge difference in my own case too.'),
            ('Daniel', 'This story helped me understand what evidence to collect first.'),
            ('Ava', 'The timeline idea is really useful. I usually forget to record when each step happened.'),
            ('Noah', 'I had a similar counterfeit issue and the packaging photos ended up being very important.'),
            ('Chloe', 'This makes me feel less nervous about pushing back when a seller says no.'),
            ('Ethan', 'Organising the evidence before escalating seems like the smartest part here.'),
        ],
    },
    {
        'id': 2,
        'tag': 'Fraud',
        'badge': 'Chargeback Success',
        'title': 'Recovered $800 from Investment Scam',
        'summary': 'The user was misled by a fake cryptocurrency platform and later recovered the transferred funds through a dispute and fraud report.',
        'amount': '$800',
        'type': 'Chargeback Success',
        'days': '21 days',
        'likes': 256,
        'comments': 45,
        'helpful': 176,
        'story': [
            'I found what looked like a legitimate cryptocurrency investment platform through a social media advertisement and put in money before realising something was wrong.',
            'At first the dashboard looked convincing, but when I tried to withdraw my funds the requests kept failing and support stopped responding properly.',
            'I documented every transfer, screenshot, message, and wallet reference I could find, then contacted my bank and filed a fraud report straight away.',
            'The chargeback process did not move quickly at first, but once I submitted a clear evidence timeline and the fraud reference number, the bank reversed the payment successfully.',
        ],
        'comment_threads': [
            ('Sarah', 'The timeline format is a great idea for scam reports.'),
            ('Leo', 'Seeing the bank dispute route spelled out clearly gives me a better plan.'),
            ('Grace', 'I wish I had documented the wallet address earlier in my own case.'),
            ('Lucas', 'This is a good reminder to act quickly with the bank instead of waiting for the platform to reply.'),
            ('Isla', 'The first-person detail makes this much easier to relate to.'),
            ('Henry', 'Thanks for mentioning that the first bank response was not the final result.'),
        ],
    },
    {
        'id': 3,
        'tag': 'Subscription',
        'badge': 'Refund + Cancellation',
        'title': 'Canceled Gym Membership and Got 3 Months Refunded',
        'summary': 'The service used hidden cancellation requirements, but written proof of repeated attempts led to a refund and final cancellation.',
        'amount': '$180',
        'type': 'Refund + Cancellation',
        'days': '8 days',
        'likes': 98,
        'comments': 17,
        'helpful': 62,
        'story': [
            'I tried to cancel my gym membership through the online portal, but every attempt redirected me to a broken support form instead of completing the cancellation.',
            'After that kept happening, I switched to email and attached screenshots showing every failed cancellation attempt and the dates they happened.',
            'In my message, I asked the provider to treat my first cancellation attempt as the effective date rather than the later email date.',
            'A few days later they confirmed the membership was closed and refunded three months of charges that should never have gone through.',
        ],
        'comment_threads': [
            ('Olivia', 'Written cancellation attempts are so important.'),
            ('James', 'This convinced me to stop relying on phone calls only.'),
            ('Zoe', 'I had almost the same issue with a streaming service. Screenshots helped me too.'),
            ('William', 'Using the first cancellation date as the reference point is a really strong move.'),
            ('Lily', 'This is exactly why I now save every confirmation page before closing a tab.'),
            ('Jack', 'It helps a lot to see a success story for subscription disputes.'),
            ('Sophie', 'I like that the story explains both the failed portal and the follow-up email.'),
        ],
    },
]

SUPPORT_OPTIONS = [
    ('Live Chat Support', 'Get instant help from our AI assistant or connect with a human agent for complex issues.', 'Start Chat', 'Currently available'),
    ('Phone Support', 'Speak directly with a consumer rights specialist who can guide you through your case.', 'Call Support', 'Mon-Fri 9 AM-5 PM'),
    ('Legal Advisory', 'Schedule a consultation with our legal advisers for complex cases requiring professional guidance.', 'Schedule Consultation', 'Free for active cases'),
]

SUPPORT_FAQS = [
    ('How do I track my case status?', 'Open the Progress Inquiry dashboard to view the latest updates.'),
    ('What evidence do I need to submit?', 'Receipts, screenshots, communication records, invoices, product photos, and bank transaction details are all helpful.'),
    ('How long does resolution take?', 'Simple cases may resolve within 7-14 days, while fraud or subscription disputes can take longer depending on the merchant response.'),
    ('Can I get a refund for my case?', 'That depends on the issue type and evidence provided. The platform will guide you toward the most appropriate outcome, such as refund, replacement, or cancellation.'),
]

FAQS = [
    ('What is the typical timeframe for resolving a consumer dispute?', 'Most cases are resolved within 14-30 days, depending on complexity and merchant responsiveness.'),
    ('Do I need a lawyer to file a consumer rights complaint?', 'No, this platform helps you navigate the process without legal representation for most standard cases.'),
    ('Can I get a refund if I simply changed my mind?', 'For online purchases, the return window depends on the seller policy and the condition of the goods, while faulty goods may qualify for stronger remedies.'),
    ('What evidence do I need to support my claim?', 'Order confirmations, receipts, product photos, communication records, and payment proof are most helpful.'),
]

INFO_PAGES: dict[str, dict[str, Any]] = {
    'shopping-counterfeit-products': {
        'heading': 'Counterfeit or Fake Products',
        'description': 'What to do when an online order is advertised as genuine but arrives as a fake or imitation item.',
        'bullets': ['Keep the original listing, receipt, and payment confirmation.', 'Photograph the item, packaging, labels, and obvious differences.', 'Request a refund in writing and state that the item does not match the description.', 'Escalate through your payment provider or consumer regulator if the seller refuses.'],
        'links': [('ACCC: consumer guarantees', 'https://www.accc.gov.au/consumers/buying-products-and-services/consumer-rights-and-guarantees'), ('NSW Fair Trading: shopping and refunds', 'https://www.fairtrading.nsw.gov.au/buying-products-and-services')],
    },
    'shopping-refund-return-denial': {
        'heading': 'Refund or Return Denial',
        'description': 'How to respond when a seller refuses a return or refund that should be allowed under policy or consumer law.',
        'bullets': ['Save screenshots of the advertised return period.', 'Submit your refund request through traceable channels such as email or in-app chat.', 'State the order number, delivery date, and why the goods fail to match the contract.', 'Keep a dated timeline in case you need to escalate.'],
        'links': [('ACCC: refunds and returns', 'https://www.accc.gov.au/consumers/problem-with-a-product-or-service-you-bought/refunds-and-returns')],
    },
    'shopping-order-mismatch': {
        'heading': 'Order Mismatch',
        'description': 'Steps to take if you receive the wrong colour, size, model, or specification.',
        'bullets': ['Photograph the delivered item next to the invoice or packing slip.', 'Compare the received item with the listing description and keep screenshots.', 'Ask for replacement or refund depending on whether you still want the item.', 'Do not discard packaging until the dispute is resolved.'],
        'links': [('NSW Fair Trading: goods not as described', 'https://www.fairtrading.nsw.gov.au/buying-products-and-services/repairs,-replacements-and-refunds')],
    },
    'shopping-damaged-or-defective-items': {
        'heading': 'Damaged or Defective Items',
        'description': 'Evidence and next steps when goods arrive damaged or stop working soon after purchase.',
        'bullets': ['Record the fault as soon as possible using photos or short videos.', 'Note when the issue first appeared and whether normal use was involved.', 'Ask for repair, replacement, or refund depending on the seriousness of the fault.', 'Keep warranty documents and service responses together in one place.'],
        'links': [('ACCC: repairs, replacements, and refunds', 'https://www.accc.gov.au/consumers/problem-with-a-product-or-service-you-bought/repair-replace-refund-cancel')],
    },
    'shopping-right-to-return': {
        'heading': 'Right to Return',
        'description': 'A summary of return expectations for online purchases and what proof helps support a return request.',
        'bullets': ['Return rights depend on the merchant policy and whether the goods are faulty or misdescribed.', 'Save the advertised policy at the time of purchase because terms may change later.', 'When goods are faulty, consumer guarantees can apply even if a store says "no refunds".'],
        'links': [('ACCC: consumer guarantees overview', 'https://www.accc.gov.au/consumers/buying-products-and-services/consumer-rights-and-guarantees')],
    },
    'shopping-right-to-accurate-information': {
        'heading': 'Right to Accurate Information',
        'description': 'Consumers should be able to rely on truthful listings, pricing, shipping claims, and seller representations.',
        'bullets': ['Take screenshots of the listing, including title, price, specifications, and delivery estimate.', 'Misleading advertising can support a refund, chargeback, or complaint to a regulator.', 'Ask the seller to explain any mismatch between the listing and the delivered product.'],
        'links': [('ACCC: false or misleading claims', 'https://www.accc.gov.au/business/advertising-and-promotions/false-or-misleading-claims')],
    },
    'shopping-right-to-quality-goods': {
        'heading': 'Right to Quality Goods',
        'description': 'Goods should be fit for purpose, acceptable in quality, and consistent with what was sold.',
        'bullets': ['Describe the failure in practical terms: broken, unsafe, unusable, or not durable.', 'Include when the item was purchased and how soon the fault appeared.', 'For serious faults, consumers can usually choose a refund or replacement.'],
        'links': [('ACCC: acceptable quality', 'https://www.accc.gov.au/consumers/problem-with-a-product-or-service-you-bought/repair-replace-refund-cancel')],
    },
    'fraud-phishing-scams': {
        'heading': 'Phishing Scams',
        'description': 'How to spot impersonation emails, texts, and fake login pages before they cause damage.',
        'bullets': ['Avoid clicking links in urgent messages asking you to verify payment or account details.', 'Check the sender address carefully and compare it with the legitimate organisation.', 'Report the message and change passwords if you entered credentials.'],
        'examples': [
            ('Fake bank security alert', 'You receive a text saying your bank account has been frozen and you must click a link immediately to verify your identity. The link leads to a page that looks like your bank login screen.'),
            ('Parcel delivery problem message', 'You get an email claiming your package cannot be delivered unless you pay a small redelivery fee. The payment page asks for card details and personal information.'),
            ('University or workplace account warning', 'An email says your school or work account will be disabled unless you confirm your password. The sender name looks familiar, but the email address and link domain are slightly different.'),
        ],
        'links': [('Australian Cyber Security Centre: phishing', 'https://www.cyber.gov.au/learn-basics/explore-basics/watch-out-threats/phishing')],
    },
    'fraud-identity-theft': {
        'heading': 'Identity Theft',
        'description': 'Immediate actions when someone uses your details to open accounts or make purchases.',
        'bullets': ['Contact your bank, card issuer, and key service providers straight away.', 'Place alerts where available and monitor for new statements or logins.', 'Keep a record of all case numbers, support references, and disputed transactions.'],
        'examples': [
            ('Credit card opened in your name', 'You receive a letter welcoming you to a new credit card account you never applied for. Soon after, collection notices begin arriving for unpaid charges.'),
            ('Phone plan created with stolen ID', 'A scammer uses your licence, passport, or leaked personal details to sign up for a mobile plan, and you only discover it when the bill arrives.'),
            ('Online shopping account takeover', 'A fraudster logs into one of your existing shopping accounts, changes the contact details, and places orders using your saved payment method.'),
        ],
        'links': [('IDCARE support services', 'https://www.idcare.org/')],
    },
    'fraud-payment-fraud': {
        'heading': 'Payment Fraud',
        'description': 'What to do after unauthorised card, wallet, or bank account transactions.',
        'bullets': ['Freeze the affected card or account as soon as you spot suspicious activity.', 'List each unauthorised transaction with amount, date, and merchant reference.', 'Ask your bank about chargeback, dispute, and replacement card options.'],
        'examples': [
            ('Unfamiliar small card charges', 'Your statement shows several small transactions from online merchants you do not recognise. These test charges are often used before larger fraudulent purchases.'),
            ('Digital wallet payments you did not approve', 'You receive notifications from a payment app for purchases or transfers that you never authorised, even though your phone is still with you.'),
            ('Bank transfer scam after fake customer support call', 'Someone pretending to be from your bank tells you your account is under attack and instructs you to move money into a so-called safe account, which is actually controlled by the scammer.'),
        ],
        'links': [('eSafety: online shopping scams', 'https://www.esafety.gov.au/key-topics/scams')],
    },
    'fraud-data-breaches': {
        'heading': 'Data Breaches',
        'description': 'How to respond when a company exposes your personal information through a security incident.',
        'bullets': ['Read the breach notice carefully to confirm what data was exposed.', 'Change affected passwords and turn on two-factor authentication.', 'Watch for suspicious contact attempts that use the leaked information.'],
        'examples': [
            ('Retail website account leak', 'A shopping platform notifies you that names, email addresses, and password hashes may have been exposed after a system intrusion.'),
            ('Health or insurance record exposure', 'A company reports that uploaded documents containing address details, identification numbers, or claim records were accessed by an unauthorised party.'),
            ('Follow-up scams after a breach', 'Shortly after a publicised data breach, you receive very convincing calls or emails that mention real personal details taken from the leaked data.'),
        ],
        'links': [('OAIC: data breach response', 'https://www.oaic.gov.au/privacy/notifiable-data-breaches')],
    },
    'subscriptions-auto-renewal': {
        'heading': 'Unwanted Auto-Renewal',
        'description': 'Evidence and escalation tips for services that renew without clear notice or consent.',
        'bullets': ['Save the sign-up page, pricing, and any renewal notice you received.', 'Record the date you attempted cancellation and the method you used.', 'Check whether the service made cancellation harder than sign-up.'],
        'links': [('ACCC consumer guidance', 'https://www.accc.gov.au/consumers')],
    },
    'subscriptions-hidden-fees': {
        'heading': 'Hidden or Increased Fees',
        'description': 'How to challenge price increases or add-on fees that were not clearly disclosed.',
        'bullets': ['Compare your first invoice with the current charge and note the difference.', 'Look for any notice email that mentioned a price change or updated terms.', 'Request a refund if the increase was applied without fair notice.'],
        'links': [('ACCC: pricing and advertising', 'https://www.accc.gov.au/business/pricing')],
    },
    'subscriptions-difficult-cancellation': {
        'heading': 'Difficult Cancellation',
        'description': 'What to document when a provider buries or blocks cancellation steps.',
        'bullets': ['Take screenshots of every cancellation screen or error message.', 'Use written channels if the website fails or support is unavailable.', 'Keep proof of every attempt so you can dispute later charges.'],
        'links': [('NSW Fair Trading', 'https://www.fairtrading.nsw.gov.au/buying-products-and-services')],
    },
    'subscriptions-free-trial-traps': {
        'heading': 'Free Trial Traps',
        'description': 'How to respond when a free trial turns into a paid subscription without adequate notice.',
        'bullets': ['Check whether the trial end date and first paid billing date were clearly shown.', 'Cancel in writing immediately and request reversal of the first charge if needed.', 'Keep confirmation pages and all reminder emails for evidence.'],
        'links': [('ACCC advertising guidance', 'https://www.accc.gov.au/business/advertising-and-promotions')],
    },
    'knowledge-consumer-rights': {
        'heading': 'Consumer Rights Basics',
        'description': 'A quick guide to refunds, warranties, and what to collect before escalating a dispute.',
        'bullets': ['Consumer guarantees can still apply even if a seller posts a strict refund policy.', 'Receipts, screenshots, delivery notices, and communication records make cases much stronger.', 'It helps to ask for a specific outcome: refund, replacement, repair, or cancellation.'],
        'links': [('ACCC consumer rights guide', 'https://www.accc.gov.au/consumers/buying-products-and-services/consumer-rights-and-guarantees')],
    },
    'knowledge-fraud-prevention': {
        'heading': 'Fraud Prevention',
        'description': 'Practical steps to reduce the risk of phishing, impersonation, and payment scams.',
        'bullets': ['Use strong unique passwords and enable two-factor authentication.', 'Slow down when a message creates urgency around payments or account security.', 'Verify suspicious messages with the organisation through official channels.'],
        'links': [('Australian Cyber Security Centre', 'https://www.cyber.gov.au/')],
    },
    'knowledge-subscription-management': {
        'heading': 'Subscription Management',
        'description': 'How to track renewal dates, store cancellation proof, and dispute unwanted recurring charges.',
        'bullets': ['Keep confirmation emails and a note of every billing cycle.', 'Cancel early when possible and save the final confirmation screen.', 'Dispute charges quickly if billing continues after cancellation.'],
        'links': [('Moneysmart', 'https://moneysmart.gov.au/')],
    },
    'resource-shopping': {
        'heading': 'Shopping Regulations and Resources',
        'description': 'Useful external resources for online shopping disputes, returns, and faulty products.',
        'bullets': ['Use these links when you need official wording, regulatory guidance, or complaint escalation contacts.'],
        'links': [('ACCC consumer rights and guarantees', 'https://www.accc.gov.au/consumers/buying-products-and-services/consumer-rights-and-guarantees'), ('NSW Fair Trading buying products and services', 'https://www.fairtrading.nsw.gov.au/buying-products-and-services')],
    },
    'resource-fraud': {
        'heading': 'Fraud Reporting Resources',
        'description': 'Official organisations that can help with identity theft, data breaches, and online scams.',
        'bullets': ['Keep screenshots, case references, and transaction details ready before contacting these organisations.'],
        'links': [('ReportCyber', 'https://www.cyber.gov.au/report-and-recover/report'), ('IDCARE', 'https://www.idcare.org/'), ('OAIC data breaches', 'https://www.oaic.gov.au/privacy/notifiable-data-breaches')],
    },
    'resource-subscriptions': {
        'heading': 'Subscription Rules and Resources',
        'description': 'Links for learning about ongoing charges, cancellation, and misleading pricing practices.',
        'bullets': ['Review the official guidance before contacting the merchant so you know what to ask for.'],
        'links': [('ACCC consumer guidance', 'https://www.accc.gov.au/consumers'), ('NSW Fair Trading', 'https://www.fairtrading.nsw.gov.au/')],
    },
}

CONSULTATION_SLOTS = [
    ('Mon-Fri', '9:00 AM - 5:00 PM', 'Legal intake clinic'),
    ('Mon-Fri', '9:00 AM - 5:00 PM', 'Consumer dispute consultation'),
    ('24/7', 'Available anytime', 'Fraud recovery support'),
]

DOWNLOADS = [
    ('Consumer Rights Guide', 'PDF 2.5 MB'),
    ('Dispute Letter Template', 'DOCX 4.5 KB'),
    ('Evidence Checklist', 'PDF 1.1 MB'),
    ('Legal Resources Directory', 'PDF 3.2 MB'),
]

BROWSING_HISTORY = [
    'Consumer Rights Guide - 2 days ago',
    'Success Cases - Shopping Disputes - 3 days ago',
    'Fraud Prevention Tips - 1 week ago',
]


def get_user() -> dict[str, Any] | None:
    return session.get('user')


def set_user(name: str, email: str) -> None:
    session['user'] = {'name': name, 'email': email, 'phone': '0400 000 000', 'verified': True}


def seed_cases() -> list[dict[str, Any]]:
    return [
        {
            'case_id': 'CR-2026-0412',
            'category': 'Shopping',
            'category_class': 'shopping',
            'status': 'In Progress',
            'progress': 68,
            'submitted': '2026-04-08',
            'estimated': '2026-04-22',
            'amount': '$249.99',
            'label': 'Shopping',
            'timeline': [
                ('Submitted', 'Apr 8, 2026'),
                ('Under Review', 'Apr 9, 2026'),
                ('Merchant Contacted', 'Apr 10, 2026'),
                ('Response Pending', 'Expected Apr 18'),
                ('Resolution', 'Expected Apr 22'),
            ],
        },
        {
            'case_id': 'CR-2026-0305',
            'category': 'Subscription',
            'category_class': 'subscriptions',
            'status': 'Pending',
            'progress': 22,
            'submitted': '2026-04-05',
            'estimated': '2026-04-20',
            'amount': '$19.99',
            'label': 'Subscription',
            'timeline': [
                ('Submitted', 'Apr 5, 2026'),
                ('Under Review', 'Expected Apr 16'),
                ('Company Contacted', 'TBD'),
                ('Response Pending', 'TBD'),
                ('Resolution', 'TBD'),
            ],
        },
        {
            'case_id': 'CR-2026-0228',
            'category': 'Fraud',
            'category_class': 'fraud',
            'status': 'Resolved',
            'progress': 100,
            'submitted': '2026-02-28',
            'estimated': '2026-03-08',
            'amount': '$350.00',
            'label': 'Fraud',
            'timeline': [
                ('Submitted', 'Feb 28, 2026'),
                ('Evidence Verified', 'Mar 1, 2026'),
                ('Bank Contacted', 'Mar 2, 2026'),
                ('Chargeback Approved', 'Mar 5, 2026'),
                ('Resolved', 'Mar 8, 2026'),
            ],
        },
    ]


def get_cases() -> list[dict[str, Any]]:
    cases = session.get('cases')
    if not cases:
        cases = seed_cases()
        session['cases'] = cases
    return cases


def case_amount_for_category(category: str) -> str:
    return {'shopping': '$249.99', 'subscriptions': '$19.99', 'fraud': '$350.00'}.get(category, '$99.00')


def add_case(category: str, issue_name: str, issue_detail: str, evidence_name: str | None) -> dict[str, Any]:
    cases = get_cases()
    new_id = f'CR-2026-{len(cases) + 1001}'
    new_case = {
        'case_id': new_id,
        'category': category.title() if category != 'subscriptions' else 'Subscription',
        'category_class': category,
        'status': 'Submitted',
        'progress': 10,
        'submitted': str(date.today()),
        'estimated': str(date.today()),
        'amount': case_amount_for_category(category),
        'label': category.title() if category != 'subscriptions' else 'Subscription',
        'issue_name': issue_name,
        'issue_detail': issue_detail,
        'evidence_name': evidence_name or 'No file attached',
        'timeline': [
            ('Submitted', 'Today'),
            ('Under Review', 'Expected soon'),
            ('Evidence Check', 'Pending'),
            ('Merchant Contacted', 'Pending'),
            ('Resolution', 'Pending'),
        ],
    }
    cases.insert(0, new_case)
    session['cases'] = cases
    return new_case


def get_story_or_none(story_id: int) -> dict[str, Any] | None:
    return next((story for story in SUCCESS_CASES if story['id'] == story_id), None)


@app.context_processor
def inject_global_data() -> dict[str, Any]:
    return {
        'current_user': get_user(),
        'support_options': SUPPORT_OPTIONS,
    }


@app.route('/')
def home():
    return render_template('home.html', page_title='Consumer Rights Platform')


@app.route('/about')
def about():
    return render_template('about.html', page_title='About Consumer Rights Hub')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    mode = request.args.get('mode', 'login')
    if request.method == 'POST':
        form_mode = request.form.get('mode', 'login')
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        name = request.form.get('full_name', '').strip() or 'John Smith'
        if not email or not password:
            flash('Please complete all required fields.', 'error')
            return redirect(url_for('auth', mode=form_mode))
        set_user(name, email)
        flash(f'Welcome, {name}. You are now signed in to the prototype.', 'success')
        return redirect(url_for('home'))
    return render_template('auth.html', page_title='Sign In / Register', mode=mode)


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been signed out from the prototype.', 'success')
    return redirect(url_for('home'))


@app.route('/shopping')
def shopping():
    return render_template('category.html', page_title=CATEGORY_CONTENT['shopping']['title'], category=CATEGORY_CONTENT['shopping'])


@app.route('/fraud')
def fraud():
    return render_template('category_fraud.html', page_title=CATEGORY_CONTENT['fraud']['title'], category=CATEGORY_CONTENT['fraud'])


@app.route('/subscriptions')
def subscriptions():
    return render_template('category_subscriptions.html', page_title=CATEGORY_CONTENT['subscriptions']['title'], category=CATEGORY_CONTENT['subscriptions'])


@app.route('/knowledge')
def knowledge():
    return render_template(
        'knowledge.html',
        page_title='Rights Knowledge & Fraud Prevention',
        alerts=KNOWLEDGE_ALERTS,
        faqs=FAQS,
        knowledge_topics=KNOWLEDGE_TOPICS,
    )


@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        flash('Your message has been sent to the support team. A human adviser will follow up soon.', 'success')
        return redirect(url_for('support'))
    return render_template(
        'support.html',
        page_title='Human Support',
        support_faqs=SUPPORT_FAQS,
        consultation_slots=CONSULTATION_SLOTS,
    )


@app.route('/community')
def community():
    selected = request.args.get('cat', 'all').lower()
    query_text = request.args.get('q', '').strip()
    category_filtered = SUCCESS_CASES if selected == 'all' else [case for case in SUCCESS_CASES if case['tag'].lower() == selected]
    if query_text:
        query_lower = query_text.lower()
        filtered = [
            case
            for case in category_filtered
            if query_lower in case['title'].lower()
            or query_lower in case['summary'].lower()
            or query_lower in case['tag'].lower()
        ]
    else:
        filtered = category_filtered
    counts = {
        'all': len(SUCCESS_CASES),
        'shopping': sum(1 for case in SUCCESS_CASES if case['tag'].lower() == 'shopping'),
        'fraud': sum(1 for case in SUCCESS_CASES if case['tag'].lower() == 'fraud'),
        'subscription': sum(1 for case in SUCCESS_CASES if case['tag'].lower() == 'subscription'),
    }
    return render_template(
        'community.html',
        page_title='Community Success Cases',
        success_cases=filtered,
        counts=counts,
        selected_filter=selected,
        search_query=query_text,
    )


@app.route('/community/story/<int:story_id>')
def story_detail(story_id: int):
    story = get_story_or_none(story_id)
    if story is None:
        flash('That story could not be found.', 'error')
        return redirect(url_for('community'))
    return render_template('story_detail.html', page_title=story['title'], story=story)


@app.route('/progress')
def progress():
    cases = get_cases()
    resolved = sum(1 for case in cases if case['status'].lower() == 'resolved')
    in_progress = sum(1 for case in cases if case['status'].lower() == 'in progress')
    pending = sum(1 for case in cases if case['status'].lower() in {'submitted', 'pending'})
    summary = {'pending': pending or 1, 'in_progress': 2, 'resolved': 5}
    max_value = max(summary.values()) if summary else 1
    chart = {
        'pending': max(44, round(summary['pending'] / max_value * 180)),
        'in_progress': max(44, round(summary['in_progress'] / max_value * 180)),
        'resolved': max(44, round(summary['resolved'] / max_value * 180)),
    }
    return render_template(
        'dashboard.html',
        page_title='Case Progress Dashboard',
        cases=cases,
        summary=summary,
        chart=chart,
    )


@app.route('/personal-center')
def personal_center():
    cases = get_cases()
    user = get_user() or {'name': 'John Smith', 'email': 'john.smith@email.com', 'phone': '0400 000 000', 'verified': True}
    stats = {
        'total': len(cases),
        'resolved': sum(1 for case in cases if case['status'].lower() == 'resolved'),
        'success_rate': '100%' if cases else '0%',
    }
    activities = [
        ('Case CR-2026-0412 updated to In Progress', 'Apr 10, 2026, 2:30 PM'),
        ('New message from support team', 'Apr 8, 2026, 11:15 AM'),
        ('Submitted case CR-2026-0305', 'Apr 5, 2026, 4:20 PM'),
    ]
    return render_template(
        'personal_center.html',
        page_title='Personal Center',
        user=user,
        cases=cases,
        stats=stats,
        downloads=DOWNLOADS,
        activities=activities,
        history=BROWSING_HISTORY,
    )


@app.route('/info/<slug>')
def info_page(slug: str):
    page = INFO_PAGES.get(slug)
    if page is None:
        flash('That detail page is not available right now.', 'error')
        return redirect(url_for('home'))
    return render_template(
        'info_page.html',
        page_title=page['heading'],
        heading=page['heading'],
        description=page['description'],
        bullets=page['bullets'],
        examples=page.get('examples', []),
        links=page['links'],
    )


@app.route('/complaint/start/<category>')
def complaint_start(category: str):
    if category not in CATEGORY_CONTENT:
        flash('That category is not available in this prototype.', 'error')
        return redirect(url_for('home'))
    session['complaint_category'] = category
    session['complaint_form'] = {}
    return redirect(url_for('complaint_step1'))


@app.route('/complaint/step-1', methods=['GET', 'POST'])
def complaint_step1():
    category = session.get('complaint_category', 'shopping')
    form_data = session.get('complaint_form', {})
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        if not name or not phone or not address:
            flash('Please complete all contact details before continuing.', 'error')
        else:
            form_data.update({'name': name, 'phone': phone, 'address': address})
            session['complaint_form'] = form_data
            return redirect(url_for('complaint_step2'))
    return render_template('complaint_step1.html', page_title='Rights Protection Form - Step 1', category=CATEGORY_CONTENT[category], form_data=form_data)


@app.route('/complaint/step-2', methods=['GET', 'POST'])
def complaint_step2():
    category = session.get('complaint_category', 'shopping')
    form_data = session.get('complaint_form', {})
    if request.method == 'POST':
        issue_name = request.form.get('issue_name', '').strip()
        issue_detail = request.form.get('issue_detail', '').strip()
        if not issue_name or not issue_detail:
            flash('Please provide the issue name and details before continuing.', 'error')
        else:
            form_data.update({'issue_name': issue_name, 'issue_detail': issue_detail})
            session['complaint_form'] = form_data
            return redirect(url_for('complaint_step3'))
    return render_template('complaint_step2.html', page_title='Rights Protection Form - Step 2', category=CATEGORY_CONTENT[category], form_data=form_data)


@app.route('/complaint/step-3', methods=['GET', 'POST'])
def complaint_step3():
    category = session.get('complaint_category', 'shopping')
    form_data = session.get('complaint_form', {})
    if request.method == 'POST':
        evidence_name = request.form.get('evidence_name', '').strip()
        uploaded_files = [file for file in request.files.getlist('evidence_file') if file and file.filename]
        if uploaded_files:
            file_names = ', '.join(file.filename for file in uploaded_files)
            evidence_name = evidence_name or file_names
        if not evidence_name:
            flash('Please add at least one supporting document name or choose a file.', 'error')
        else:
            form_data.update({'evidence_name': evidence_name})
            session['complaint_form'] = form_data
            created = add_case(
                category=category,
                issue_name=form_data.get('issue_name', 'Consumer Rights Case'),
                issue_detail=form_data.get('issue_detail', ''),
                evidence_name=evidence_name,
            )
            session['last_case_id'] = created['case_id']
            return redirect(url_for('complaint_success'))
    return render_template('complaint_step3.html', page_title='Rights Protection Form - Step 3', category=CATEGORY_CONTENT[category], form_data=form_data)


@app.route('/complaint/success')
def complaint_success():
    last_case_id = session.get('last_case_id')
    return render_template('complaint_success.html', page_title='Complaint Submitted', last_case_id=last_case_id)


@app.route('/case/<case_id>')
def case_detail(case_id: str):
    cases = get_cases()
    case = next((item for item in cases if item['case_id'] == case_id), None)
    if case is None:
        flash('The requested case was not found.', 'error')
        return redirect(url_for('progress'))
    return render_template('case_detail.html', page_title=f'Case {case_id}', case=case)


if __name__ == '__main__':
    app.run(debug=True)
