# Legal & Regulatory Compliance Framework: "काम मिलेगा" (Kaam Milega)

This document details the regulatory compliance architecture implemented in "काम मिलेगा" to operate in full accordance with Indian statutes.

---

## 1. Child & Adolescent Labour (Prohibition and Regulation) Act, 1986 (Amended 2016)

### Legal Mandate
* Prohibition of employment of children (under 14) and adolescents (14 to 18) in hazardous occupations and processes, including building and construction work, brick kilns, and manual excavation.

### Platform Implementation
1. **Frontend Age Gate**: Calculates exact age from year of birth. If `< 18`, registration is hard-blocked with an audio warning.
2. **Mandatory Declaration**: Workers must confirm `declared_age_18_plus = 1`.
3. **Backend API Barrier**: `api.py` asserts `birth_year <= (current_year - 18)`. Violation yields `HTTP 403 Forbidden` (`UNDERAGE_REGISTRATION_PROHIBITED`).
4. **Employer Disclaimer**: Employers must accept a non-underage hiring clause before posting jobs.
5. **Direct Reporting Flag**: One-tap reporting category for "कम उम्र / बाल श्रम का संदेह" immediately hides profiles for investigation.

---

## 2. Digital Personal Data Protection Act, 2023 (DPDP Act)

### Legal Mandate
* Lawful processing of digital personal data based on informed, unambiguous consent, with clear data principal rights (access, correction, erasure).

### Platform Implementation
1. **Notice & Granular Consent**: Bilingual notice displayed before onboarding and on the homepage.
2. **Data Minimization**: Only essential operational data is collected. No biometric data, financial accounts, or unnecessary identifiers.
3. **Zero Raw Aadhaar Storage**: Strictly compliant with the Aadhaar (Targeted Delivery of Financial and Other Subsidies, Benefits and Services) Act, 2016. The platform does not collect, scan, or store 12-digit Aadhaar numbers. Verification is decentralized through local Panchayat and peer endorsement.
4. **Right to Erasure ("डेटा हटाएं")**: Self-serve profile deletion permanently removes personal details and soft-deletes records.
5. **Grievance Redressal**: Mandatory Grievance Officer email and physical address published.

---

## 3. Information Technology Act, 2000 & Intermediary Guidelines (2021)

### Legal Mandate
* Safe harbour protection under Section 79 for intermediaries that do not initiate, select the receiver, or modify information transmitted.

### Platform Implementation
1. **Terms of Service**: Explicit notice that "काम मिलेगा" is an intermediary and not an employer or labor contractor.
2. **Due Diligence**: Takedown mechanism within 24 hours upon receiving complaints or legal notices.
3. **Audit Trail**: Secure contact interaction logging (`contact_logs`) for dispute resolution.

---

## 4. Minimum Wages Act, 1948 & Fair Trade

### Platform Implementation
* Platform displays wage guidance aligned with State Minimum Wage standards for skilled, semi-skilled, and unskilled rural labor.
* Digital "काम की पर्ची" (Work Slip) generator records agreed wage rates to prevent underpayment and extortion.
* Zero commission deducted from worker wages.
