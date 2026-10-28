# Legal, licensing, and release-readiness checklist

**Review date:** 2026-10-28  
**Jurisdictional starting point:** Nigeria, with other jurisdictions potentially relevant if the software is distributed or used elsewhere.

This document is a practical issue-spotting checklist, **not legal advice and not a guarantee against claims, regulatory action, or liability**. A Nigerian lawyer familiar with software, intellectual property, product liability, and any relevant health/scientific regulation should review the intended distribution and use before public release.

## Current high-priority findings

- **No project licence has been selected.** A public GitHub repository is not automatically open-source licensed. GitHub explains that without a licence, default copyright rules apply and others generally do not receive permission to reproduce, distribute, or create derivatives. Do not add MIT, Apache, GPL, or another licence until the owner deliberately chooses it and confirms rights to all contributed material.
- **The package metadata contains a placeholder licence.** `pyproject.toml` says `License not yet selected`. That is not a real licence grant and should be removed until an actual choice is made.
- **Third-party rights are not yet documented comprehensively.** Check the licence and attribution requirements for each dependency, dataset, structure image, copied code fragment, and generated asset. Retain required notices. Do not assume that public availability means unrestricted redistribution.
- **The archived app presents outputs as organ damage and lethality estimates.** A disclaimer alone does not establish that these outputs are scientifically valid, safe, lawful, or free of liability. The implementation has not been independently validated.
- **The archive contains high-hazard chemical records and parameters.** Decide, with qualified legal and safety review, what data is appropriate to publish in a public repository. The current audit does not certify that public release is risk-free.
- **No user-data workflow has been documented.** If the app collects or stores identifiable user data, logs, device identifiers, or information linked to people in a deployment, assess the Nigeria Data Protection Act 2023 and any other applicable privacy laws. If it remains a local, offline educational tool and does not process personal data, a privacy notice may not be needed for that use—but verify the actual data flows.

## Documents to prepare before distribution

### 1. Intellectual property and software licensing

- [ ] Choose the intended licence (proprietary, permissive open source, copyleft, or another reviewed arrangement).
- [ ] Add the actual `LICENSE` file and update `pyproject.toml` only after the decision is made.
- [ ] Confirm that all contributors have the right to contribute the code and that any third-party code is compatible with the chosen licence.
- [ ] Add `THIRD_PARTY_NOTICES.md` when the actual dependency and asset inventory is confirmed.
- [ ] Record the origin, licence, retrieval date, and permitted use for external datasets and structure images.
- [ ] Do not distribute bundled executables until their bundled libraries and notices have been audited.

### 2. Scientific integrity and safety

- [ ] State the intended users and intended educational/research use.
- [ ] Remove or clearly segregate unverified parameter defaults; label synthetic data as synthetic.
- [ ] Document equations, assumptions, units, data provenance, uncertainty, and validation limitations.
- [ ] Have a qualified toxicologist/pharmacometrics reviewer examine any scientific claims before a release describes outputs as predictive.
- [ ] Do not market the tool as clinical decision support or use it to make treatment decisions without the appropriate evidence and regulatory review.
- [ ] Define an incident-reporting process for harmful misuse, incorrect output, or a discovered data defect.
- [ ] Keep emergency-exposure guidance separate from the simulation; direct users to qualified emergency services rather than model outputs.

### 3. Privacy and security

- [ ] Inventory every data flow: local files, network requests, telemetry, crash logs, saved scenarios, and external APIs.
- [ ] If personal data is processed, document the purpose, lawful basis, retention, access, deletion, security controls, and any sharing or cross-border transfers.
- [ ] Provide an accurate privacy notice if required by the actual data processing.
- [ ] Do not store API keys, tokens, or secrets in source control.
- [ ] Enable private vulnerability reporting if appropriate, and publish a security contact or reporting route.
- [ ] Scan release artifacts for bundled secrets and unintended personal data.

### 4. Distribution and user-facing terms

- [ ] Identify whether distribution is free, paid, academic, commercial, or bundled with a service.
- [ ] Have counsel assess whether consumer-protection, product-safety, health-software, export-control, or other sector-specific requirements apply to the actual functionality and distribution.
- [ ] Use clear versioning, release notes, support contact, and a process to withdraw a defective release.
- [ ] Use terms and disclaimers drafted for the actual use case and jurisdiction; do not rely on boilerplate as a substitute for safety, evidence, or compliance.
- [ ] Avoid claims such as “accurate,” “predicts lethality,” “clinically validated,” or “safe” unless independently supported and legally reviewed.

## Primary and official references

1. **GitHub Docs — Licensing a repository:** explains the effect of choosing or not choosing a licence.  
   https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
2. **Choose a License — No License:** plain-language explanation of default copyright when no licence is supplied.  
   https://choosealicense.com/no-permission/
3. **Nigerian Copyright Commission — Copyright Act, 2022:** official source for the Nigerian copyright statute.  
   https://copyright.gov.ng/CopyrightAct/
4. **Nigeria Data Protection Commission — Nigeria Data Protection Act, 2023:** official Act and resources.  
   https://ndpc.gov.ng/download/nigeria-data-protection-act-2023
5. **Federal Competition and Consumer Protection Commission — Resources & Library:** official source for the Federal Competition and Consumer Protection Act 2018 and related materials.  
   https://fccpc.gov.ng/resources-library/
6. **RDKit — project licence:** RDKit states that its code is released under a BSD licence. Check the exact version and notices for the version distributed with the app.  
   https://github.com/rdkit/rdkit/blob/master/license.txt

## What this checklist cannot establish

Completing the boxes does not guarantee immunity from lawsuits or regulatory action. Applicability depends on actual functionality, claims, data sources, distribution model, users, and jurisdiction. Get qualified legal advice before commercial release or any release that makes real-world toxicological claims.
