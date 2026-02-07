import json
import httpx
from openai import AsyncOpenAI
from sqlalchemy.orm import Session
from . import schemas, models, database
from .config import settings

class AIService:
    def __init__(self):
        # Initialize OpenAI client (supports OpenAI, DeepSeek, Moonshot, etc.)
        # If Base URL is empty, it defaults to OpenAI
        if settings.LLM_API_KEY and settings.LLM_API_KEY != "sk-...":
            # Use custom httpx client to bypass system proxy issues if needed
            http_client = httpx.AsyncClient(trust_env=False)
            
            self.client = AsyncOpenAI(
                api_key=settings.LLM_API_KEY,
                base_url=settings.LLM_BASE_URL if settings.LLM_BASE_URL else None,
                http_client=http_client
            )
        else:
            self.client = None

    def search_context(self, question: str, db: Session, limit: int = 3) -> str:
        """
        Simple keyword search in crawled data.
        In a real production system, this should be Vector Search (RAG).
        """
        # Split question into keywords (very naive)
        keywords = [k for k in question.split() if len(k) > 1]
        if not keywords:
            keywords = [question]
            
        results = []
        for kw in keywords:
            # Search in title or content
            items = db.query(models.CrawledData).filter(
                (models.CrawledData.title.contains(kw)) | 
                (models.CrawledData.content.contains(kw))
            ).limit(limit).all()
            results.extend(items)
        
        # Deduplicate results by ID
        unique_results = {r.id: r for r in results}.values()
        
        # Format context
        context_str = ""
        for i, item in enumerate(list(unique_results)[:limit]):
            context_str += f"Source {i+1} ({item.title}):\n{item.content[:500]}...\n\n"
            
        return context_str

    async def get_answer_stream(self, question: str, db: Session):
        # 1. Search local context
        context = self.search_context(question, db)
        
        # Yield sources first
        yield json.dumps({"type": "sources", "content": ["本地数据库 + DeepSeek-R1"]}, ensure_ascii=False) + "\n"

        # 2. If no client configured
        if not self.client:
            mock_answer = f"[System] AI API未配置。请在后台配置 API Key。\n\n本地搜索到的相关信息:\n{context if context else '无'}"
            # Simulate streaming
            for chunk in mock_answer.split():
                yield json.dumps({"type": "answer", "content": chunk + " "}, ensure_ascii=False) + "\n"
                await asyncio.sleep(0.05)
            return

        # 3. Call LLM with stream=True
        try:
            system_prompt = f"""
            你是一个专业的考研咨询助手，拥有丰富的考研政策、院校信息和复习规划知识。
            你的目标是为用户提供清晰、准确、有深度且排版精美的回答。

            ### 回答要求：
            1. **格式规范**：必须使用 Markdown 格式。
               - 使用清晰的标题（##, ###）分层级。
               - 关键信息使用**加粗**。
               - 列表项使用 - 或 1. 符号。
               - 代码或特定术语使用 `代码块`。
            2. **内容结构**：
               - **核心结论**：开头直接给出明确的回答或总结。
               - **详细分析**：结合参考资料和通用知识进行深度解析。
               - **建议/规划**：如果适用，给出具体的复习或择校建议。
            3. **参考资料使用**：
               - 以下提供了本地数据库的搜索结果（参考资料）。
               - 请优先基于参考资料回答。
               - 如果参考资料不足，请**务必**利用你的通用大模型知识进行补充，确保回答完整。
               - 如果参考资料完全不相关，请忽略它，直接使用通用知识回答。

            ### 本地参考资料：
            {context}
            """
            
            stream = await self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    yield json.dumps({"type": "answer", "content": content}, ensure_ascii=False) + "\n"
            
        except Exception as e:
            yield json.dumps({"type": "error", "content": f"[Error] 调用 AI 服务失败: {str(e)}"}, ensure_ascii=False) + "\n"

ai_service = AIService()
