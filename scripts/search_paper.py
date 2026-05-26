"""
wechat-paper-synthesizer / search_paper.py
v1.0 - 多源论文解读文章搜索 + 去重 + 元数据导出

首选通道：搜狗微信搜索（sogou_weixin_search），覆盖微信公众号深度解读。
Skill 主工作流中会配合 WebSearch 补充搜狐、澎湃、腾讯新闻等全网中文内容。

用法:
    python search_paper.py --paper-title "论文标题" --paper-authors "作者" \
        --paper-journal "期刊" --paper-year 2026 \
        [--output results.json] [--max-results 10]

或直接编辑脚本中的 PAPER_CONFIG 字典后运行。
"""
import json
import sys
import argparse
from typing import Optional

# 尝试导入 weixin-search-mcp
try:
    from weixin_search_mcp.tools.weixin_search import sogou_weixin_search
    HAS_WEIXIN_SEARCH = True
except ImportError:
    HAS_WEIXIN_SEARCH = False
    print("[WARN] weixin-search-mcp 未安装。将跳过搜狗搜索，请手动提供文章列表。")


def build_search_queries(paper_title: str, authors: str, journal: str,
                         year: str, chinese_field: str = "",
                         paper_type: str = "论文") -> list[str]:
    """
    根据论文元数据构造 4-5 组中文搜索关键词。
    参考 references/search_queries.md 的构造策略。
    """
    # 提取英文标题关键词（取前2-3个有辨识度的词）
    title_words = [w for w in paper_title.split() if len(w) > 3][:3]
    title_kw = " ".join(title_words)

    # 提取作者姓氏
    author_surname = authors.split(",")[0].strip().split()[-1] if authors else ""

    queries = []

    # 策略一：原文精确匹配
    if journal and title_kw:
        queries.append(f'"{journal}" "{title_kw}" {year} 解读')
    if journal and chinese_field:
        queries.append(f'"{journal}" "{title_words[0]}" {chinese_field} 综述')

    # 策略二：作者驱动
    if author_surname and chinese_field:
        queries.append(f'"{author_surname}" "{chinese_field}" "{journal}" {paper_type}')

    # 策略三：中文泛化 — 需由调用方提供 chinese_keywords
    # 策略四：长尾 — 需由调用方提供

    # 如果策略三四未覆盖，用原文标题作为兜底
    if len(queries) < 3:
        queries = [
            f"{journal} {title_kw} {year} 解读 公众号",
            f"{author_surname} {chinese_field} {paper_type}",
            title_kw,
        ]

    return queries


def search_sogou(queries: list[str], page: int = 1) -> dict[str, dict]:
    """通过搜狗微信搜索多组关键词，按标题去重返回。
    这是多源搜索管道中的首选通道。Skill 主工作流会配合 WebSearch 补充全网内容。"""
    if not HAS_WEIXIN_SEARCH:
        print("[SKIP] 搜狗搜索不可用")
        return {}

    all_articles = {}
    for query in queries:
        print(f"  搜索: {query}")
        try:
            results = sogou_weixin_search(query, page=page)
            count = len(results)
            new_count = 0
            for r in results:
                title = r.get("title", "").strip()
                if title and title not in all_articles:
                    all_articles[title] = {
                        "title": title,
                        "description": r.get("description", ""),
                        "publish_time": r.get("publish_time", ""),
                        "source_query": query,
                    }
                    new_count += 1
            print(f"    共 {count} 条，新增 {new_count} 条")
        except Exception as e:
            print(f"    出错: {e}")

    print(f"\n  去重总计: {len(all_articles)} 篇")
    return all_articles


def filter_relevant(articles: dict, paper_title: str, authors: str = "",
                    journal: str = "", min_relevance: float = 0.3) -> dict:
    """
    简单相关性过滤：标题包含论文核心词的比例。
    返回过滤后的文章字典。
    """
    # 构造核心词集合
    core_words = set()
    for word in paper_title.lower().split():
        if len(word) > 3:
            core_words.add(word.lower())
    if authors:
        for a in authors.split(","):
            core_words.add(a.strip().split()[-1].lower())
    if journal:
        core_words.add(journal.lower())

    filtered = {}
    for title, article in articles.items():
        title_lower = title.lower()
        hits = sum(1 for w in core_words if w in title_lower)
        score = hits / max(len(core_words), 1)
        if score >= min_relevance:
            filtered[title] = {**article, "relevance_score": round(score, 2)}

    return filtered


def main():
    parser = argparse.ArgumentParser(description="搜索微信公众号文章")
    parser.add_argument("--paper-title", required=True, help="论文英文标题")
    parser.add_argument("--paper-authors", default="", help="作者列表（逗号分隔）")
    parser.add_argument("--paper-journal", default="", help="期刊名")
    parser.add_argument("--paper-year", default="", help="发表年份")
    parser.add_argument("--chinese-field", default="", help="中文学科领域（如'蛋白质从头设计'）")
    parser.add_argument("--paper-type", default="论文", help="论文类型（论文/综述/临床试验）")
    parser.add_argument("--output", default="search_results.json", help="输出文件路径")
    parser.add_argument("--max-results", type=int, default=10, help="每页最大结果数")
    args = parser.parse_args()

    # 构造搜索关键词
    queries = build_search_queries(
        args.paper_title, args.paper_authors, args.paper_journal,
        args.paper_year, args.chinese_field, args.paper_type
    )
    print(f"生成 {len(queries)} 组搜索关键词:")
    for i, q in enumerate(queries, 1):
        print(f"  {i}. {q}")

    # 搜索
    print("\n开始搜索...")
    articles = search_sogou(queries, page=1)

    # 过滤
    if articles:
        print("\n相关性过滤...")
        relevant = filter_relevant(articles, args.paper_title, args.paper_authors, args.paper_journal)
        print(f"  过滤后: {len(relevant)} 篇（共 {len(articles)} 篇原始）")
    else:
        relevant = {}
        print("  无搜索结果")

    # 保存
    output = {
        "paper": {
            "title": args.paper_title,
            "authors": args.paper_authors,
            "journal": args.paper_journal,
            "year": args.paper_year,
            "chinese_field": args.chinese_field,
            "type": args.paper_type,
        },
        "search_queries": queries,
        "total_raw": len(articles),
        "total_filtered": len(relevant),
        "articles": list(relevant.values()),
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存到 {args.output}")
    print("\n=== 推荐文章标题 ===")
    for i, (title, art) in enumerate(relevant.items(), 1):
        print(f"  {i}. [{art.get('relevance_score', '?')}] {title}")


if __name__ == "__main__":
    main()
