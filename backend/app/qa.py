from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .config import get_settings
from .vectorstore import similarity_search

SYSTEM = """You are a helpful assistant. Answer the user's question using ONLY the
provided context. If the answer is not in the context, say you don't know.
Cite sources inline like [source: filename].

Context:
{context}
"""

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("human", "{question}"),
])


def answer(question: str) -> dict:
    settings = get_settings()
    docs = similarity_search(question)
    context = "\n\n".join(f"[source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}" for d in docs)
    llm = ChatOpenAI(model=settings.chat_model, api_key=settings.openai_api_key, temperature=0)
    msg = PROMPT.format_messages(context=context, question=question)
    resp = llm.invoke(msg)
    return {
        "answer": resp.content,
        "sources": [
            {"source": d.metadata.get("source", "unknown"), "snippet": d.page_content[:200]}
            for d in docs
        ],
    }