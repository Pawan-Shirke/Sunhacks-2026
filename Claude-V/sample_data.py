"""
Sample datasets from RBI, SEBI, and MCA for demonstration.
In production these are fetched live; here we provide rich mock data.
"""

SAMPLE_REGULATIONS = [
    {
        "id": "RBI-2024-001",
        "source": "RBI",
        "title": "Master Direction — Know Your Customer (KYC) Amendment 2024",
        "date": "2024-11-15",
        "category": "Banking / KYC",
        "risk": "High",
        "summary": (
            "The Reserve Bank of India has issued an amendment to its Master Direction on KYC, "
            "mandating that all regulated entities must re-verify customer documents using Aadhaar-based "
            "eKYC for accounts opened before 2020. Additionally, beneficial ownership declarations are now "
            "mandatory for all corporate accounts above ₹10 lakh. Entities must comply within 90 days of "
            "circular publication. Non-compliance may attract penalties under Section 11(1)(b)(ii) of the "
            "Prevention of Money Laundering Act."
        ),
        "diff": "+ eKYC re-verification mandatory for pre-2020 accounts\n+ Beneficial ownership declaration for corporate accounts > ₹10L\n- Removed: Self-declaration waiver for existing KYC-compliant customers\n+ New: 90-day compliance deadline",
        "full_text": (
            "RBI/2024-25/001 Master Direction – Know Your Customer (KYC) Direction, 2016 (Updated 2024)\n\n"
            "1. Introduction\nIn exercise of powers conferred under Section 35A and 56 of the Banking Regulation Act, "
            "1949, the Reserve Bank of India hereby amends the Master Direction on KYC as follows:\n\n"
            "2. Key Amendments\n"
            "2.1 All Regulated Entities (REs) shall re-verify customer documents via Aadhaar-based eKYC for "
            "accounts opened before 01 January 2020, within 90 days of this circular.\n"
            "2.2 Beneficial Ownership: For all corporate accounts with transaction limits above ₹10,00,000, "
            "a fresh Beneficial Ownership (BO) declaration shall be obtained from the account holder.\n"
            "2.3 Video KYC: REs may also use Video-based Customer Identification Process (V-CIP) as an "
            "alternative to in-person verification for re-KYC.\n"
            "2.4 Penalties: Non-compliance will be treated as a violation of the Prevention of Money Laundering "
            "Act and may attract penalties up to ₹1 crore per instance.\n\n"
            "3. Effective Date: This amendment is effective 90 days from the date of issue.\n"
            "4. Previous circular RBI/2020-21/KYC/35 stands superseded to the extent of conflict."
        ),
        "url": "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12345"
    },
    {
        "id": "SEBI-2024-002",
        "source": "SEBI",
        "title": "SEBI Circular: Enhanced Disclosure Requirements for IPO Filings",
        "date": "2024-10-28",
        "category": "Capital Markets / IPO",
        "risk": "High",
        "summary": (
            "SEBI has revised its ICDR Regulations to require enhanced disclosures in Draft Red Herring "
            "Prospectus (DRHP) filings. Companies must now disclose all related-party transactions for the "
            "past 5 years (up from 3 years), provide a detailed risk stratification matrix, and include "
            "ESG (Environmental, Social, Governance) reporting for companies with turnover above ₹500 crore. "
            "Merchant bankers must certify the completeness of disclosures under their own liability."
        ),
        "diff": "+ Related-party disclosure window extended from 3 to 5 years\n+ ESG reporting mandatory for turnover > ₹500 Cr\n+ Merchant banker certification under personal liability\n- Removed: Simplified disclosure option for SME-IPOs below ₹50 Cr",
        "full_text": (
            "SEBI/HO/CFD/DIL/CIR/2024/002\n\nSubject: Amendments to SEBI (Issue of Capital and Disclosure "
            "Requirements) Regulations, 2018 – Enhanced Disclosure in IPO Filings\n\n"
            "1. Background: In view of recent concerns regarding completeness of information in IPO prospectuses, "
            "SEBI has reviewed its disclosure framework and proposes the following amendments.\n\n"
            "2. Related Party Transactions: The look-back period for RPT disclosure in DRHP is extended from "
            "3 years to 5 years immediately preceding the date of filing.\n\n"
            "3. ESG Disclosures: Issuers with annual turnover exceeding ₹500 crore must include a Business "
            "Responsibility and Sustainability Report (BRSR) in the DRHP.\n\n"
            "4. Merchant Banker Responsibility: Lead managers must certify, under their own liability, that "
            "all information in the DRHP is complete, accurate, and not misleading.\n\n"
            "5. Effective Date: Applicable to all DRHPs filed on or after 01 January 2025."
        ),
        "url": "https://www.sebi.gov.in/legal/circulars/2024/sebi-circular-002.html"
    },
    {
        "id": "MCA-2024-003",
        "source": "MCA",
        "title": "Companies (Amendment) Rules 2024 — Annual Filing Compliance",
        "date": "2024-09-10",
        "category": "Corporate Compliance",
        "risk": "Medium",
        "summary": (
            "The Ministry of Corporate Affairs has amended the Companies (Accounts) Rules to introduce "
            "stricter timelines and digital filing requirements. All companies must now file AOC-4 and MGT-7 "
            "within 60 days of the AGM (reduced from 60 to 45 days for listed companies). "
            "XBRL tagging is now mandatory for all public companies irrespective of turnover. "
            "The amendment also introduces e-CSR-1 form for companies spending above ₹50 lakh on CSR."
        ),
        "diff": "+ AOC-4 filing deadline reduced to 45 days for listed companies\n+ XBRL mandatory for ALL public companies (no turnover threshold)\n+ New e-CSR-1 form for CSR spends > ₹50L\n- Removed: Physical filing option for certain forms",
        "full_text": (
            "G.S.R. (E).— In exercise of the powers conferred by sub-sections (1) and (3) of section 129 and "
            "sub-section (3) of section 137 of the Companies Act, 2013, the Central Government hereby makes "
            "the following rules to amend the Companies (Accounts) Rules, 2014.\n\n"
            "Rule 12 Filing of Financial Statements:\n"
            "(a) Every listed company shall file its financial statements in Form AOC-4 within 45 days of "
            "the AGM.\n"
            "(b) Every public company shall mandatorily tag financial data using XBRL (eXtensible Business "
            "Reporting Language), regardless of paid-up share capital or turnover.\n\n"
            "Rule 8A CSR Reporting:\n"
            "Companies spending ₹50 lakh or more on CSR activities shall file Form e-CSR-1 with the "
            "Designated National CSR Hub, Ministry of Corporate Affairs, within 30 days of completion.\n\n"
            "Effective Date: 01 October 2024."
        ),
        "url": "https://www.mca.gov.in/MinistryV2/notification-detail.html?id=2024-003"
    },
    {
        "id": "RBI-2024-004",
        "source": "RBI",
        "title": "Prudential Framework for Resolution of Stressed Assets — Updated Guidelines",
        "date": "2024-08-22",
        "category": "Banking / NPA",
        "risk": "High",
        "summary": (
            "RBI has updated its Prudential Framework for Resolution of Stressed Assets, extending the "
            "Inter-Creditor Agreement (ICA) signing deadline from 30 to 45 days after classification as SMA-2. "
            "Banks are now required to provision 35% (up from 20%) for accounts under resolution beyond 180 days. "
            "Additionally, all lenders must implement a real-time SMA reporting system integrated with CRILC by "
            "March 2025."
        ),
        "diff": "+ ICA deadline extended from 30 to 45 days post-SMA-2\n+ Provision requirement increased from 20% to 35% (beyond 180 days)\n+ Real-time CRILC integration mandatory by March 2025\n- Removed: 60-day grace period for restructuring proposals",
        "full_text": (
            "RBI/2024-25/DBOD/BP.BC/004\n\nSubject: Prudential Framework for Resolution of Stressed Assets – Revised\n\n"
            "Section 1: Inter-Creditor Agreement\nThe timeline for signing the Inter-Creditor Agreement (ICA) "
            "is extended to 45 calendar days from the date of classification of the account as SMA-2.\n\n"
            "Section 2: Provisioning Norms\nFor accounts where resolution plan implementation remains pending "
            "beyond 180 days from the date of agreement, lenders shall make additional provisions raising the "
            "total provision to 35% of the outstanding amount (previously 20%).\n\n"
            "Section 3: CRILC Reporting\nAll scheduled commercial banks shall implement real-time reporting "
            "to Central Repository of Information on Large Credits (CRILC) by 31 March 2025. Failure to "
            "integrate shall be subject to supervisory action."
        ),
        "url": "https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12400"
    },
    {
        "id": "SEBI-2024-005",
        "source": "SEBI",
        "title": "SEBI Cybersecurity & Cyber Resilience Framework for Market Infrastructure Institutions",
        "date": "2024-07-05",
        "category": "Cybersecurity / Technology",
        "risk": "High",
        "summary": (
            "SEBI has issued a comprehensive Cybersecurity and Cyber Resilience Framework (CSCRF) applicable "
            "to all Market Infrastructure Institutions (MIIs), Qualified RTA, Depository Participants, "
            "and Stock Brokers above a defined threshold. Entities must appoint a CISO, conduct quarterly "
            "vulnerability assessments, and report all cyber incidents to SEBI within 6 hours. "
            "A 3-year technology roadmap must be submitted by December 2024."
        ),
        "diff": "+ CISO appointment mandatory for all covered entities\n+ Cyber incident reporting within 6 hours (was 24 hours)\n+ Quarterly VAPT assessments mandatory\n+ 3-year tech roadmap submission by Dec 2024\n- Removed: Annual self-certification option",
        "full_text": (
            "SEBI/HO/MRD/MRD-PoD-1/P/CIR/2024/005\n\n"
            "Subject: Cybersecurity and Cyber Resilience Framework (CSCRF) for SEBI Regulated Entities\n\n"
            "1. Scope: This circular applies to: (a) Market Infrastructure Institutions (Stock Exchanges, "
            "Clearing Corporations, Depositories); (b) Qualified Registrar and Transfer Agents (QRTAs); "
            "(c) Depository Participants and Stock Brokers with client base > 50,000.\n\n"
            "2. Governance: Every covered entity must appoint a Chief Information Security Officer (CISO) "
            "who shall report directly to the Board/MD & CEO.\n\n"
            "3. Incident Reporting: All material cyber incidents (unauthorized access, data breach, ransomware) "
            "shall be reported to SEBI within 6 hours of detection.\n\n"
            "4. Vulnerability Assessment: Covered entities shall conduct VAPT (Vulnerability Assessment and "
            "Penetration Testing) at least once per quarter by a CERT-In empanelled auditor.\n\n"
            "5. Technology Roadmap: A 3-year technology and cybersecurity roadmap must be submitted to SEBI "
            "by 31 December 2024."
        ),
        "url": "https://www.sebi.gov.in/legal/circulars/2024/sebi-cscrf-005.html"
    },
    {
        "id": "MCA-2024-006",
        "source": "MCA",
        "title": "Insolvency and Bankruptcy Code — Pre-Packaged Insolvency Amendment",
        "date": "2024-06-15",
        "category": "Insolvency / Restructuring",
        "risk": "Medium",
        "summary": (
            "MCA has expanded the Pre-Packaged Insolvency Resolution Process (PPIRP) to cover MSMEs with "
            "defaults up to ₹10 crore (up from ₹1 crore). The process timeline is shortened from 120 to "
            "90 days. Financial creditors must submit Expression of Interest within 15 days. Resolution "
            "plans with haircuts exceeding 60% require approval of 90% of the CoC."
        ),
        "diff": "+ PPIRP default threshold raised to ₹10 Cr (was ₹1 Cr)\n+ Resolution timeline reduced from 120 to 90 days\n+ EoI submission window: 15 days from public announcement\n+ Haircuts > 60% need 90% CoC approval (was 75%)",
        "full_text": (
            "Ministry of Corporate Affairs, Government of India\n\n"
            "Notification: Insolvency and Bankruptcy (Amendment) Rules, 2024\n\n"
            "G.S.R. – The Central Government hereby amends the Insolvency and Bankruptcy Board of India "
            "(Pre-packaged Insolvency Resolution Process) Regulations, 2021:\n\n"
            "1. Default Threshold: The minimum default threshold for initiating PPIRP under Section 54A "
            "is revised to ₹10,00,00,000 (Ten Crore Rupees).\n\n"
            "2. Timeline: The maximum period for completion of the pre-packaged insolvency resolution process "
            "is reduced from 120 days to 90 days.\n\n"
            "3. Expression of Interest: Financial creditors shall submit their EoI to the Resolution "
            "Professional within 15 days of the public announcement.\n\n"
            "4. CoC Voting Threshold: Resolution plans proposing a haircut exceeding 60% of admitted claims "
            "shall require approval by at least 90% voting share of the Committee of Creditors."
        ),
        "url": "https://www.mca.gov.in/MinistryV2/notification-detail.html?id=2024-006"
    },
]

SAMPLE_POLICIES = [
    {
        "id": "POL-KYC-001",
        "title": "Customer KYC and Onboarding Policy",
        "text": (
            "This policy governs the Know Your Customer (KYC) procedures for all customer onboarding at "
            "RegTech Financial Services Pvt Ltd. All new customers must submit valid government ID (Aadhaar, "
            "PAN, Passport or Voter ID) along with proof of address. KYC is verified within 24 hours of "
            "submission. For corporate accounts, the beneficial ownership structure must be disclosed. "
            "The KYC team is responsible for periodic refresh of customer data every 2 years for low-risk "
            "customers and annually for high-risk customers. Video KYC is supported for individuals who "
            "cannot visit in person."
        ),
        "department": "Compliance",
        "last_updated": "2023-04-01"
    },
    {
        "id": "POL-LOAN-002",
        "title": "Loan Origination and Approval Policy",
        "text": (
            "Loan applications are processed as follows: (1) Customer submits application with income proof "
            "and KYC documents. (2) Credit team assesses CIBIL score, ITR, and bank statements. (3) Loans "
            "up to ₹50,000 are pre-approved digitally. (4) Loans above ₹50,000 require manual credit review. "
            "(5) All loan agreements must include an arbitration clause (Clause 3.1) and interest disclosure "
            "per RBI guidelines. (6) Disbursement is within 3 working days of approval. Prepayment penalties "
            "are capped at 2% as per RBI fair practices code."
        ),
        "department": "Credit",
        "last_updated": "2023-07-15"
    },
    {
        "id": "POL-IPO-003",
        "title": "Capital Market and IPO Compliance Policy",
        "text": (
            "For any proposed public issue of securities, the Company Secretary and CFO must ensure: "
            "(1) Draft Red Herring Prospectus (DRHP) is reviewed by Legal for completeness; (2) Related-party "
            "transactions for the past 3 years are disclosed; (3) Material litigation disclosures are current. "
            "The merchant banker must be notified of all material changes post-DRHP filing. SEBI observations "
            "must be responded to within the statutory 30-day window. The Board must approve the final "
            "prospectus before filing with the RoC."
        ),
        "department": "Legal / Finance",
        "last_updated": "2022-11-20"
    },
    {
        "id": "POL-NPA-004",
        "title": "Non-Performing Asset (NPA) Management Policy",
        "text": (
            "Accounts are classified as Special Mention Accounts (SMA) based on days past due: SMA-0 "
            "(1-30 days), SMA-1 (31-60 days), SMA-2 (61-90 days). Upon SMA-2 classification, the Credit "
            "Risk team initiates resolution discussions with the borrower. An Inter-Creditor Agreement (ICA) "
            "is sought from consortium members within 30 days. Provisioning follows RBI guidelines: 5% for "
            "substandard, 15–40% for doubtful, 100% for loss assets. Resolution plans must be approved by "
            "the Credit Committee within 90 days."
        ),
        "department": "Credit Risk",
        "last_updated": "2023-01-10"
    },
    {
        "id": "POL-CYBER-005",
        "title": "Cybersecurity and Information Security Policy",
        "text": (
            "The Company adopts ISO/IEC 27001 standards for information security management. Key controls: "
            "(1) Penetration testing twice a year by external auditor; (2) All cyber incidents reported to "
            "the CISO within 24 hours; (3) Annual security awareness training for all employees; "
            "(4) Critical systems use multi-factor authentication; (5) Customer data is encrypted at rest "
            "(AES-256) and in transit (TLS 1.3). The CISO submits a quarterly security report to the Board. "
            "Business continuity and disaster recovery tests are conducted annually."
        ),
        "department": "IT Security",
        "last_updated": "2023-06-30"
    },
    {
        "id": "POL-CSR-006",
        "title": "Corporate Social Responsibility (CSR) Policy",
        "text": (
            "As per Section 135 of the Companies Act, 2013, the Company spends a minimum of 2% of average "
            "net profit of the preceding 3 financial years on CSR activities. The CSR Committee, comprising "
            "3 directors including 1 Independent Director, approves projects annually. Focus areas: "
            "education, healthcare, rural development. Annual CSR report is included in the Board's Report. "
            "Unspent CSR amount is transferred to Schedule VII funds within 6 months of year-end. "
            "Projects are monitored quarterly by the CSR Committee."
        ),
        "department": "Corporate Affairs",
        "last_updated": "2023-03-15"
    },
    {
        "id": "POL-MSME-007",
        "title": "MSME Lending and Recovery Policy",
        "text": (
            "The Company provides working capital and term loans to MSME borrowers registered under the "
            "MSMED Act. Loan processing follows a simplified credit appraisal for limits up to ₹2 crore. "
            "In case of default, the Company prefers resolution over litigation for MSME accounts. "
            "Recovery proceedings under SARFAESI are initiated only for accounts with defaults above ₹5 lakh "
            "and overdue beyond 180 days. For pre-packaged insolvency cases, the Company participates as a "
            "financial creditor and files its claim with the Resolution Professional within 15 days."
        ),
        "department": "MSME Finance",
        "last_updated": "2022-08-01"
    },
    {
        "id": "POL-AML-008",
        "title": "Anti-Money Laundering (AML) and CFT Policy",
        "text": (
            "The Company complies with the Prevention of Money Laundering Act, 2002 and RBI's AML guidelines. "
            "All cash transactions above ₹10 lakh are reported to the Financial Intelligence Unit (FIU-IND) "
            "as Cash Transaction Reports (CTR). Suspicious transactions are reported as Suspicious Transaction "
            "Reports (STR) within 7 days of detection. The AML Officer conducts periodic training. "
            "Customer risk categorization (Low/Medium/High) determines KYC refresh frequency. "
            "Politically Exposed Persons (PEPs) are subject to enhanced due diligence."
        ),
        "department": "Compliance",
        "last_updated": "2023-09-01"
    },
]

# FAQ and Q&A dataset for chatbot
REGULATORY_QA = [
    {
        "q": "What are the RBI KYC requirements for 2024?",
        "a": (
            "Under RBI's 2024 KYC amendment, all regulated entities must:\n"
            "1. Re-verify pre-2020 accounts via Aadhaar eKYC within 90 days\n"
            "2. Obtain Beneficial Ownership declarations for corporate accounts > ₹10L\n"
            "3. Offer Video KYC (V-CIP) as an alternative to in-person verification\n"
            "4. Non-compliance attracts penalties up to ₹1 crore per instance under PMLA"
        )
    },
    {
        "q": "What is SEBI's new IPO disclosure requirement?",
        "a": (
            "SEBI's 2024 ICDR amendment requires:\n"
            "1. Related-party transaction disclosure extended to 5 years (from 3)\n"
            "2. Mandatory ESG/BRSR reporting for companies with turnover > ₹500 Cr\n"
            "3. Merchant bankers must certify DRHP completeness under personal liability\n"
            "Applicable to all DRHPs filed from 01 January 2025."
        )
    },
    {
        "q": "What are the MCA annual filing deadlines?",
        "a": (
            "Under the 2024 MCA amendment:\n"
            "• Listed companies: AOC-4 filing within 45 days of AGM\n"
            "• Unlisted companies: AOC-4 within 60 days of AGM\n"
            "• MGT-7 (Annual Return): within 60 days of AGM for all\n"
            "• XBRL tagging: mandatory for ALL public companies\n"
            "• New e-CSR-1 form required for CSR spends > ₹50 lakh"
        )
    },
    {
        "q": "What does SEBI's cybersecurity framework require?",
        "a": (
            "SEBI's CSCRF 2024 mandates:\n"
            "1. Appointment of a CISO reporting to Board/MD\n"
            "2. Cyber incident reporting within 6 hours\n"
            "3. Quarterly VAPT by CERT-In empanelled auditor\n"
            "4. 3-year technology roadmap submission by Dec 2024\n"
            "Applies to Stock Exchanges, Clearing Corporations, Depositories, QRTAs, DPs, and brokers with > 50,000 clients."
        )
    },
    {
        "q": "How has the NPA resolution framework changed?",
        "a": (
            "RBI's 2024 stressed asset framework update:\n"
            "1. ICA signing deadline extended to 45 days post-SMA-2\n"
            "2. Provisioning increased to 35% for accounts >180 days in resolution\n"
            "3. Real-time CRILC integration mandatory by March 2025\n"
            "Grace period for restructuring proposals has been removed."
        )
    },
    {
        "q": "What is the PPIRP threshold for MSMEs?",
        "a": (
            "Under the 2024 IBC amendment:\n"
            "• Default threshold for PPIRP raised from ₹1 Cr to ₹10 Cr\n"
            "• Resolution timeline reduced from 120 to 90 days\n"
            "• Haircuts > 60% now require 90% CoC approval\n"
            "• Expression of Interest must be filed within 15 days"
        )
    },
    {
        "q": "What penalties apply for non-compliance?",
        "a": (
            "Key penalty provisions across regulators:\n"
            "• RBI KYC: Up to ₹1 crore per instance (PMLA)\n"
            "• SEBI IPO: Merchant banker liability for DRHP deficiencies\n"
            "• MCA filing defaults: Late fee + adjudication under Companies Act\n"
            "• SEBI Cyber: Supervisory action including suspension of operations\n"
            "• IBC violations: Contempt proceedings before NCLT"
        )
    },
]
