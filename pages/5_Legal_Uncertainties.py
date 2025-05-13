import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Legal Uncertainties | Social Media Auditing Workshop",
    page_icon="🔍",
    layout="wide"
)

st.title("5. Legal Uncertainties")
st.subheader("Navigating the legal tensions in platform auditing")

# Introduction to legal uncertainties
st.markdown("""
Platform auditing exists at the intersection of multiple legal frameworks that can sometimes 
be in tension with one another. Researchers must navigate these uncertainties when designing 
and implementing their auditing methods.

This section explores key legal uncertainties that arise when conducting platform audits, particularly 
when using alternative methods like scraping or sock puppets.
""")


# Legal uncertainties framework
st.header("Key Legal Tensions in Platform Auditing")

st.markdown("""
The following areas represent significant legal uncertainties that researchers 
must consider when designing platform audits:
""")

# Terms of Service & Automated Behavior
with st.expander("A. Terms of Service & Automated Behavior", expanded=True):
    st.subheader("Terms of Service & Automated Behavior")
    
    st.markdown("""
    ### Uncertainty
    
    Most platform Terms of Service (ToS) explicitly prohibit:
    - Automated access to platform services
    - Creating accounts for research purposes
    - Scraping public-facing content
    - Reverse engineering platform algorithms
    
    However, these provisions may conflict with legitimate research interests and other legal frameworks.
    
    ### Legal Questions
    
    - Are ToS provisions that broadly prohibit research legally enforceable?
    - Can platforms use ToS violations to block legitimate research?
    - How do courts balance contract law against research interests?
    - Could violating ToS trigger other legal issues (e.g., CFAA in the US)?
    
    ### Current Research Approaches
    
    1. **DSA Framework Reliance**: Focusing on officially sanctioned research methods under DSA Article 40
    2. **Scraping Limitation**: Limiting scraping to minimal data necessary for research
    3. **Institutional Authorization**: Conducting research under institutional approval (university IRB)
    4. **Public Interest Defense**: Preparing public interest justifications for ToS violations
    5. **Technical Obfuscation**: Designing systems that minimize detection of automated behavior
    
    ### Case Precedents
    
    - **HiQ Labs v. LinkedIn**: US case suggesting scraping publicly available data may not violate CFAA
    - **Van Buren v. United States**: Narrowed CFAA interpretation regarding "exceeding authorized access"
    """)

# GDPR & Personal Data Scraping
with st.expander("B. GDPR & Scraping Personal Data", expanded=True):
    st.subheader("GDPR & Scraping Personal Data")
    
    st.markdown("""
    ### Uncertainty
    
    The General Data Protection Regulation (GDPR) requires a legal basis for processing personal data,
    which may conflict with scraping methods that collect personal data from platforms.
    
    ### Legal Questions
    
    - Can researchers rely on "legitimate interests" as a legal basis for scraping personal data?
    - How does the research exemption in GDPR Article 89 apply to platform auditing?
    - What anonymization standards must be met when publishing scraped data?
    - Who is the data controller when researchers scrape platform data?
    
    ### Current Research Approaches
    
    1. **Anonymization Protocols**: Implementing robust anonymization before analysis
    2. **Data Minimization**: Collecting only necessary personal data for research purposes
    3. **Legitimate Interest Assessment**: Documenting public interest justification
    4. **Research Exemption Documentation**: Formally invoking Article 89 research provisions
    5. **Transparency Notices**: Creating research-specific privacy statements
    
    ### Similar Challenges
    
    **Internet Archive (Archive.org) Case Study**
    
    The Internet Archive faces similar challenges when archiving web content:
    - Must balance preservation goals against copyright and privacy concerns
    - Implements "robots.txt" respecting policies and takedown procedures
    - Provides opt-out mechanisms for content owners
    - Has established "legitimate archival purpose" arguments
    """)

# Computer Fraud and Abuse Act
with st.expander("C. Computer Fraud and Abuse Act (US) / Cybercrime Laws (EU)", expanded=False):
    st.subheader("Computer Fraud and Abuse Act (US) / Cybercrime Laws (EU)")
    
    st.markdown("""
    ### Uncertainty
    
    Laws like the US Computer Fraud and Abuse Act (CFAA) and similar cybercrime laws in the EU
    prohibit unauthorized access to computer systems, raising questions about the legality of
    certain research methods.
    
    ### Legal Questions
    
    - Does automated access to platforms constitute "unauthorized access"?
    - Can ToS violations trigger criminal liability under these laws?
    - How do courts distinguish between malicious hacking and legitimate research?
    - Do research exemptions exist in these frameworks?
    
    ### Current Research Approaches
    
    1. **Legal Consultation**: Seeking specialized legal advice before conducting research
    2. **Documentation**: Maintaining detailed records of research methods and decisions
    3. **Institutional Approval**: Securing formal institutional approval for methods
    4. **Transparency**: Being open about research methods with platforms when possible
    5. **Jurisdictional Considerations**: Understanding different interpretations across jurisdictions
    
    ### Recent Developments
    
    - **Van Buren v. United States (2021)**: US Supreme Court narrowed CFAA interpretation
    - **EU Cybercrime Convention**: Ongoing discussions about research exemptions
    - **CNIL (France) Guidelines**: Provides some guidance on scraping for research
    """)

# Sock Puppet Risks
with st.expander("D. Misuse of SOAP & Ethical Concerns", expanded=False):
    st.subheader("Misuse of SOAP & Ethical Concerns")
    
    st.markdown("""
    ### Uncertainty
    
    Sock Puppet Auditing Protocol (SOAP) methods involve creating simulated user accounts, which
    raises specific legal and ethical concerns beyond traditional scraping.
    
    ### Legal Questions
    
    - Does creating fictitious accounts constitute identity fraud?
    - Can sock puppet interactions violate integrity of service provisions?
    - How does platform manipulation differ legally from observation?
    - What liability exists if sock puppets generate or amplify harmful content?
    
    ### Current Research Approaches
    
    1. **Minimalist Interaction**: Limiting sock puppet activities to passive observation when possible
    2. **Careful Documentation**: Recording all automated activities for transparency
    3. **Content Policies**: Establishing strict policies against harmful content generation
    4. **Disclosure Timing**: Planning appropriate disclosure of methods after research
    5. **Research Controls**: Implementing safeguards against unintended consequences
    
    ### Illegal Content Concerns
    
    A particular concern with SOAP methods is the potential exposure to illegal content:
    
    - Research sock puppets may be algorithmically recommended illegal content
    - Possession or viewing of certain content may create legal liability
    - Reporting obligations may exist for certain types of content
    - Platform manipulation could inadvertently amplify harmful material
    
    **Research safeguards include:**
    
    - Content filtering systems for high-risk categories
    - Clear protocols for reporting illegal content
    - Limitations on certain research topics
    - Collaboration with legal authorities when necessary
    """)

# Legal Risk Assessment Framework
st.header("Assessing Legal Risk in Research Methods")

# Create a risk matrix
risk_data = {
    "Method": [
        "DSA Ads Repository Analysis",
        "Transparency Database Review",
        "Research API Access",
        "GDPR Data Donation Analysis",
        "Public Profile Scraping",
        "Automated Content Scraping",
        "Sock Puppet Implementation (Passive)",
        "Sock Puppet Implementation (Active)"
    ],
    "ToS Risk": [
        "Very Low",
        "Very Low",
        "Very Low",
        "Low",
        "Medium",
        "High",
        "High",
        "Very High"
    ],
    "GDPR Risk": [
        "Very Low",
        "Very Low",
        "Low",
        "Low",
        "Medium",
        "High",
        "Medium",
        "High"
    ],
    "CFAA/Cybercrime Risk": [
        "Very Low",
        "Very Low",
        "Very Low",
        "Very Low",
        "Low-Medium",
        "Medium-High",
        "Medium",
        "High"
    ],
    "Ethical Concerns": [
        "Very Low",
        "Very Low",
        "Low",
        "Low",
        "Low-Medium",
        "Medium",
        "Medium-High",
        "High"
    ]
}

risk_df = pd.DataFrame(risk_data)

# Display the risk matrix
st.subheader("Legal Risk Matrix by Research Method")
st.dataframe(risk_df, use_container_width=True)

# Risk mitigation strategies
st.header("Risk Mitigation Strategies")

st.markdown("""
### Approaches to Reducing Legal Uncertainty

Researchers can take several steps to mitigate legal risks while conducting platform audits:
""")

mitigation_strategies = {
    "Legal Consultation": "Engage with legal experts specializing in digital research methods",
    "Research Design": "Design studies to minimize legal exposure while maintaining validity",
    "Documentation": "Maintain detailed records of decision-making processes and justifications",
    "Institutional Approval": "Secure formal ethics approval from research institutions",
    "Transparency": "Be open about methods where possible without compromising research",
    "Data Protection": "Implement robust data anonymization and security measures",
    "Multi-method Approach": "Combine higher and lower risk methods to validate findings",
    "Jurisdictional Considerations": "Account for legal differences across jurisdictions",
    "Collaboration": "Partner with platforms where possible to reduce adversarial dynamics"
}

col1, col2 = st.columns(2)

for i, (strategy, description) in enumerate(mitigation_strategies.items()):
    if i < len(mitigation_strategies) // 2:
        with col1:
            st.markdown(f"**{strategy}**: {description}")
    else:
        with col2:
            st.markdown(f"**{strategy}**: {description}")


# Recent case studies
st.header("Recent Legal Precedents in Platform Research")

st.markdown("""
Several recent cases have helped clarify the legal landscape for researchers:
""")

cases = [
    {
        "Case": "HiQ Labs v. LinkedIn (US)",
        "Year": "2022",
        "Significance": "Suggested that scraping publicly available data may not violate the Computer Fraud and Abuse Act (CFAA)",
        "Impact": "Potentially limited platforms' ability to use CFAA to block research scraping of public data"
    },
    {
        "Case": "Van Buren v. United States (US)",
        "Year": "2021",
        "Significance": "Narrowed the interpretation of 'exceeding authorized access' under CFAA",
        "Impact": "Reduced risk that ToS violations alone could trigger CFAA liability"
    },
    {
        "Case": "Clearview AI regulatory actions (EU)",
        "Year": "2021-2023",
        "Significance": "Multiple EU data protection authorities ruled against facial recognition database built on scraped images",
        "Impact": "Established limits on bulk scraping of personal data, even from public sources"
    }
]

cases_df = pd.DataFrame(cases)
st.dataframe(cases_df, use_container_width=True)

# Conclusion
st.header("Balancing Research Needs with Legal Compliance")

st.markdown("""
### Moving Forward with Platform Auditing Research

The legal landscape for platform auditing is complex and evolving. As researchers navigate these uncertainties:

1. **Document your decision-making process** thoroughly
2. **Consider a mixed-methods approach** that combines official and alternative data sources
3. **Stay informed about legal developments** in this rapidly changing field
4. **Engage with the broader research community** to establish best practices
5. **Advocate for clearer legal frameworks** that protect legitimate research

The tension between the need for platform accountability and existing legal frameworks will continue 
to evolve as cases work their way through courts and policymakers respond to emerging research needs.
""")

# Discussion prompt
st.header("Workshop Discussion")

st.markdown("""
### Discussion Question

Given these legal uncertainties, how should researchers balance methodological needs against legal risks? 
What responsibility do platforms have to facilitate independent research beyond minimum compliance?
""")

discussion_response = st.text_area(
    "Share your thoughts on balancing research needs with legal compliance:",
    height=150
)

# Navigation buttons
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    prev_button = st.button("← Previous: Alternative Tools")
    if prev_button:
        st.switch_page("pages/4_SOAP_and_Scraping.py")

with col2:
    next_button = st.button("Next: Reflections & Wrap-up →")
    if next_button:
        st.switch_page("pages/6_Conclusion.py")