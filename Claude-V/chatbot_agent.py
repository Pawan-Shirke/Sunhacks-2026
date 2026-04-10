"""
Chatbot Agent — RAG-based Q&A chatbot for regulatory queries.
Uses ChromaDB + LLM if available; falls back to keyword-matched Q&A dataset.
"""
import os
from data.sample_data import REGULATORY_QA, SAMPLE_REGULATIONS
from agents.kb_agent import query_policies

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

_llm = None
_langchain_available = False

def _init_llm():
    global _llm, _langchain_available
    if not OPENAI_API_KEY:
        return
    try:
        from langchain_openai import ChatOpenAI
        _llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.3,
            openai_api_key=OPENAI_API_KEY
        )
        _langchain_available = True
    except Exception as e:
        print(f"[ChatbotAgent] LLM init: {e}")

_init_llm()


def _find_best_qa(query: str) -> str | None:
    """Find best matching Q&A from dataset using keyword overlap."""
    query_words = set(query.lower().split())
    best_score = 0
    best_answer = None
    for qa in REGULATORY_QA:
        q_words = set(qa["q"].lower().split())
        overlap = len(query_words & q_words)
        if overlap > best_score:
            best_score = overlap
            best_answer = qa["a"]
    if best_score >= 2:
        return best_answer
    return None


def _find_relevant_regs(query: str) -> list:
    """Find regulations relevant to the query."""
    query_lower = query.lower()
    relevant = []
    for reg in SAMPLE_REGULATIONS:
        score = sum(
            1 for word in query_lower.split()
            if word in reg["title"].lower() or word in reg["summary"].lower()
        )
        if score > 0:
            relevant.append((score, reg))
    relevant.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in relevant[:3]]


def chat_with_bot(user_message: str, history: list = None) -> str:
    """
    Process a user message and return a chatbot response.
    Uses RAG: retrieves relevant regulations + policies, then generates response.
    """
    # ── Try LLM + RAG ─────────────────────────────────────────────────────────
    if _langchain_available and _llm:
        try:
            from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

            # Retrieve context
            policy_hits = query_policies(user_message, k=3)
            reg_hits = _find_relevant_regs(user_message)

            context_parts = []
            for h in policy_hits:
                context_parts.append(f"[Internal Policy — {h['title']}]: {h['text'][:300]}")
            for r in reg_hits:
                context_parts.append(f"[{r['source']} Regulation — {r['title']}]: {r['summary'][:300]}")
            context = "\n\n".join(context_parts) if context_parts else "No specific context found."

            system_msg = SystemMessage(content=(
                "You are RegIntel AI, an expert regulatory compliance assistant specializing in Indian "
                "financial regulations: RBI, SEBI, and MCA. You have access to the latest regulatory "
                "circulars and internal policy documents. Answer questions clearly, accurately, and "
                "in a helpful, professional tone. Use bullet points where appropriate. Always mention "
                "relevant regulation names/IDs when citing rules.\n\n"
                f"Relevant context from our knowledge base:\n{context}"
            ))
            messages = [system_msg]
            if history:
                for msg in history[:-1]:
                    if msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        messages.append(AIMessage(content=msg["content"]))
            messages.append(HumanMessage(content=user_message))

            response = _llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"[ChatbotAgent] LLM error: {e}")

    # ── Fallback: Q&A dataset lookup ─────────────────────────────────────────
    qa_answer = _find_best_qa(user_message)
    if qa_answer:
        return qa_answer

    # ── Fallback: regulation search ───────────────────────────────────────────
    rel_regs = _find_relevant_regs(user_message)
    if rel_regs:
        reg = rel_regs[0]
        return (
            f"📋 **{reg['source']} — {reg['title']}** ({reg['date']})\n\n"
            f"{reg['summary']}\n\n"
            f"**Risk Level:** {reg['risk']} | **Category:** {reg['category']}\n\n"
            "💡 *For detailed analysis, use the Analysis Engine tab.*"
        )

    # ── Generic fallback ──────────────────────────────────────────────────────
    keywords = user_message.lower()
    if any(k in keywords for k in ["rbi", "reserve bank", "banking"]):
        return (
            "The Reserve Bank of India (RBI) regularly issues Master Directions, circulars, and "
            "notifications covering banking regulation, KYC, NPA management, digital payments, and "
            "monetary policy. Our system tracks all new RBI publications. Could you specify which "
            "aspect of RBI regulation you'd like to know more about?"
        )
    elif any(k in keywords for k in ["sebi", "securities", "market", "ipo", "stock"]):
        return (
            "SEBI regulates India's capital markets including stock exchanges, IPOs, mutual funds, "
            "and broker-dealer activities. Recent key circulars cover IPO disclosures, cybersecurity "
            "for market infrastructure, and ESG reporting. What specific SEBI regulation can I help with?"
        )
    elif any(k in keywords for k in ["mca", "ministry", "company", "filing", "roc", "director"]):
        return (
            "The Ministry of Corporate Affairs (MCA) administers the Companies Act, 2013 and "
            "related rules. Key compliance areas include annual filings (AOC-4, MGT-7), CSR "
            "reporting, insolvency proceedings, and director KYC. Which MCA compliance topic "
            "are you looking for guidance on?"
        )
    else:
        return (
            "I can help with questions about **RBI**, **SEBI**, and **MCA** regulations, including:\n\n"
            "• KYC and AML compliance requirements\n"
            "• IPO and capital market disclosures\n"
            "• Annual filing deadlines and procedures\n"
            "• NPA/stressed asset management\n"
            "• Cybersecurity frameworks\n"
            "• Insolvency and bankruptcy proceedings\n\n"
            "Please ask your specific question and I'll provide the most relevant guidance!"
        )
