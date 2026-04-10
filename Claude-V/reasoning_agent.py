"""
Reasoning Agent — LangChain-powered LLM analysis of regulatory changes.
Uses OpenAI GPT-4 if API key is set; falls back to template-based analysis.
"""
import os
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ─── Try LangChain ────────────────────────────────────────────────────────────
_langchain_available = False
_llm = None

def _init_langchain():
    global _langchain_available, _llm
    if not OPENAI_API_KEY:
        print("[ReasoningAgent] No OPENAI_API_KEY set. Using template fallback.")
        return
    try:
        from langchain_openai import ChatOpenAI
        _llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.2,
            openai_api_key=OPENAI_API_KEY
        )
        _langchain_available = True
        print("[ReasoningAgent] LangChain + GPT-4 initialized.")
    except Exception as e:
        print(f"[ReasoningAgent] LangChain init failed: {e}")


_init_langchain()


def _run_llm(prompt: str) -> str:
    """Run a prompt through the LLM if available."""
    if _langchain_available and _llm:
        try:
            from langchain_core.messages import HumanMessage
            response = _llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            print(f"[ReasoningAgent] LLM call failed: {e}")
    return None


# ─── Template-based fallback analyses ────────────────────────────────────────
def _template_impact(changes: str, context: str) -> str:
    """Heuristic impact analysis when LLM is unavailable."""
    # Detect risk keywords
    high_keywords = ["mandatory", "penalty", "penalt", "non-compliance", "crore", "prohibited", "liable", "enforcement"]
    med_keywords = ["amendment", "revised", "updated", "extended", "deadline", "threshold"]

    text_lower = changes.lower()
    risk = "Low"
    if any(k in text_lower for k in high_keywords):
        risk = "High"
    elif any(k in text_lower for k in med_keywords):
        risk = "Medium"

    # Detect affected areas
    area_map = {
        "KYC": ["kyc", "know your customer", "aadhaar", "identity", "verification"],
        "Loan Processing": ["loan", "credit", "disbursement", "npa", "sma"],
        "IPO / Capital Markets": ["ipo", "sebi", "drhp", "prospectus", "shares", "securities"],
        "Cybersecurity": ["cyber", "ciso", "vapt", "incident", "data breach", "it security"],
        "Filing / Compliance": ["filing", "aoc", "mgt", "annual return", "xbrl", "mca"],
        "Insolvency": ["insolvency", "iba", "ppirp", "nclt", "resolution", "creditor"],
        "AML / CFT": ["aml", "money laundering", "fiu", "suspicious", "ctr", "str"],
    }
    affected = [area for area, keywords in area_map.items()
                if any(k in text_lower for k in keywords)]
    if not affected:
        affected = ["General Compliance"]

    return (
        f"**1. What Changed**\n{changes[:400]}...\n\n"
        f"**2. Affected Business Areas**\n" +
        "\n".join(f"• {a}" for a in affected) +
        f"\n\n**3. Risk Level: `{risk}`**\n"
        f"{'Significant regulatory changes requiring immediate action.' if risk == 'High' else 'Moderate changes that need policy review within 30-60 days.'}\n\n"
        "**4. Recommended Actions**\n"
        "• Review and update the relevant internal policy documents\n"
        "• Brief the compliance team on these changes\n"
        "• Update internal SOPs within 30 days\n"
        "• Consult legal counsel if penalties are involved\n"
        "• Train relevant staff on the new requirements"
    )


def _template_amendment(changes: str) -> str:
    """Template-based draft amendment."""
    return (
        "**Proposed Policy Amendment (Draft)**\n\n"
        "Pursuant to the latest regulatory update, the following amendments are proposed:\n\n"
        "1. **Section [X] — Compliance Requirements**: Update to reflect the new mandatory requirements "
        "as specified in the regulatory circular. The existing provision is hereby replaced with: "
        "*'All regulated activities shall comply with the requirements set forth in the regulatory "
        "circular within the specified timeline.'*\n\n"
        "2. **Section [Y] — Penalties**: Add the following: *'Non-compliance with the above requirements "
        "shall attract penalties as prescribed by the relevant regulatory authority.'*\n\n"
        "3. **Effective Date**: This amendment takes effect from the date of board approval, and in any "
        "case no later than the deadline specified in the regulatory circular.\n\n"
        "_Note: This draft requires review by Legal Counsel and Compliance Head before adoption._"
    )


def _template_explain(changes: str) -> str:
    """Plain-language explanation template."""
    return (
        "**In Simple Terms** 💡\n\n"
        "The regulator has made some important updates to the rules. Here's what it means for you:\n\n"
        "🔹 **What's new**: There are some new requirements that businesses in this sector must follow.\n\n"
        "🔹 **Why it matters**: These changes help ensure that companies operate fairly, transparently, "
        "and in the interest of customers and the economy.\n\n"
        "🔹 **What you need to do**: Review your current processes and make sure they align with these "
        "new rules. If you're unsure, speak to your compliance team or a legal advisor.\n\n"
        "🔹 **Deadline**: Check the specific circular for the compliance timeline — typically 30 to 90 days.\n\n"
        "_💬 Need more details? Ask our chatbot!_"
    )


# ─── Public API ───────────────────────────────────────────────────────────────
def analyze_change(changes: str, company_context: str = "") -> str:
    """
    Analyze regulatory change and return structured impact analysis.
    Uses LLM if available, else template fallback.
    """
    prompt = (
        f"You are a senior Indian regulatory compliance expert.\n\n"
        f"A regulatory change has been detected:\n{changes}\n\n"
        f"Company context: {company_context}\n\n"
        f"Provide a structured analysis:\n"
        f"1. What changed in the regulation?\n"
        f"2. Which business areas or policies are affected?\n"
        f"3. Risk level (High/Medium/Low) with justification.\n"
        f"4. Recommended actions or amendments.\n\n"
        f"Format your response clearly with numbered sections."
    )
    result = _run_llm(prompt)
    return result if result else _template_impact(changes, company_context)


def draft_amendment(changes: str) -> str:
    """
    Draft a policy amendment based on regulatory change.
    """
    prompt = (
        f"You are a legal drafting assistant specializing in Indian corporate and financial regulations.\n\n"
        f"Based on this regulatory change:\n{changes}\n\n"
        f"Draft a formal policy amendment clause that a company can adopt. "
        f"Keep the language precise, formal, and actionable. Include a proposed effective date."
    )
    result = _run_llm(prompt)
    return result if result else _template_amendment(changes)


def simple_explain(changes: str) -> str:
    """
    Explain the regulatory change in plain, simple language.
    """
    prompt = (
        f"Explain the following regulatory change in simple, plain English for "
        f"a non-legal, non-technical business person:\n\n{changes}\n\n"
        f"Use bullet points. Keep it short and practical. Start with 'In simple terms...'."
    )
    result = _run_llm(prompt)
    return result if result else _template_explain(changes)
