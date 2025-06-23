import json
from datetime import datetime
import logging
import re

class NotebookLMScriptGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_notebooklm_script(self, articles, output_path=None):
        """Create a comprehensive script optimized for NotebookLM podcast generation about NIL news"""
        
        if output_path is None:
            date_str = datetime.now().strftime('%Y%m%d')
            output_path = f"outputs/NIL_NotebookLM_Script_{date_str}.md"
        
        # Categorize articles
        categories = self._categorize_articles(articles)
        
        # Build comprehensive script
        script = self._build_comprehensive_script(categories, articles)
        
        # Save script
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script)
        
        self.logger.info(f"✅ NotebookLM script saved to: {output_path}")
        
        # Also create a summary document for context
        summary_path = output_path.replace('Script', 'Summary').replace('.md', '.txt')
        self._create_summary_document(articles, summary_path)
        
        return output_path, summary_path
    
    def _categorize_articles(self, articles):
        """Enhanced categorization for NIL content"""
        categories = {
            'breaking': [],      # Major announcements & breaking news
            'mega_deals': [],    # High-value NIL deals
            'athlete_stories': [], # Individual athlete deals and stories
            'collectives': [],   # NIL collective developments
            'policy': [],        # NCAA and state policy changes
            'legal': [],         # Legal developments and lawsuits
            'platforms': [],     # NIL platforms and technology
            'education': [],     # Guidance and educational content
            'trends': []         # Market analysis and trends
        }
        
        for article in articles:
            text = (article['title'] + ' ' + article.get('summary', '')).lower()
            priority = article.get('priority_level', 'Medium')
            
            # Categorize based on content and priority
            if priority == 'Critical' or any(kw in text for kw in ['breaking', 'exclusive', 'announces', 'just']):
                categories['breaking'].append(article)
            elif any(kw in text for kw in ['million', 'six-figure', 'record deal', 'largest', 'mega']):
                categories['mega_deals'].append(article)
            elif any(kw in text for kw in ['student', 'player', 'quarterback', 'star', 'recruit']) and any(kw in text for kw in ['deal', 'partnership', 'endorsement']):
                categories['athlete_stories'].append(article)
            elif any(kw in text for kw in ['collective', 'booster', 'fund', 'donor']):
                categories['collectives'].append(article)
            elif any(kw in text for kw in ['ncaa', 'policy', 'rule', 'regulation', 'compliance', 'enforcement']):
                categories['policy'].append(article)
            elif any(kw in text for kw in ['lawsuit', 'court', 'legal', 'litigation', 'case']):
                categories['legal'].append(article)
            elif any(kw in text for kw in ['platform', 'marketplace', 'app', 'technology', 'opendorse']):
                categories['platforms'].append(article)
            elif any(kw in text for kw in ['guide', 'how to', 'tips', 'education', 'workshop']):
                categories['education'].append(article)
            else:
                categories['trends'].append(article)
        
        return categories
    
    def _build_comprehensive_script(self, categories, all_articles):
        """Build a rich, conversational script for NotebookLM focused on NIL"""
        
        date_str = datetime.now().strftime('%B %d, %Y')
        total_articles = len(all_articles)
        
        script = f"""# NIL Industry Weekly Podcast Script
**Date:** {date_str}
**Total Stories Covered:** {total_articles}

## Podcast Overview
This week's NIL (Name, Image, and Likeness) update covers major developments in college athlete compensation, from groundbreaking deals to policy changes that are reshaping collegiate athletics. We'll explore mega-deals, collective activities, legal developments, and emerging trends in the rapidly evolving NIL landscape.

---

## Executive Summary

### Key Themes This Week:
"""
        
        # Add thematic overview
        for category, articles in categories.items():
            if articles:
                count = len(articles)
                category_names = {
                    'breaking': 'Breaking News',
                    'mega_deals': 'Major NIL Deals',
                    'athlete_stories': 'Athlete Success Stories',
                    'collectives': 'NIL Collectives',
                    'policy': 'Policy & Regulation',
                    'legal': 'Legal Developments',
                    'platforms': 'Technology & Platforms',
                    'education': 'Education & Resources',
                    'trends': 'Market Trends'
                }
                script += f"- **{category_names.get(category, category.title())}**: {count} significant development{'s' if count > 1 else ''}\n"
        
        script += f"\n### Market Context\n"
        script += f"The NIL landscape continues its rapid transformation with {total_articles} noteworthy developments this week. "
        
        # Add high-level insights
        mega_deals_count = len(categories.get('mega_deals', []))
        policy_count = len(categories.get('policy', []))
        
        if mega_deals_count > 0:
            script += f"We saw {mega_deals_count} major NIL deal{'s' if mega_deals_count != 1 else ''} announced, signaling continued growth in athlete valuations. "
        
        if policy_count > 0:
            script += f"Additionally, {policy_count} policy development{'s' if policy_count != 1 else ''} emerged that could impact how NIL operates going forward. "
        
        script += "Let's dive into the details.\n\n---\n\n"
        
        # Add detailed sections
        section_order = ['breaking', 'mega_deals', 'athlete_stories', 'collectives', 'policy', 'legal', 'platforms', 'education', 'trends']
        section_titles = {
            'breaking': '🚨 Breaking News & Major Announcements',
            'mega_deals': '💰 Mega Deals & High-Value Partnerships',
            'athlete_stories': '⭐ Athlete Success Stories',
            'collectives': '🏆 NIL Collectives & Booster Activities',
            'policy': '📋 Policy, Compliance & NCAA Updates',
            'legal': '⚖️ Legal Developments & Court Cases',
            'platforms': '📱 Technology, Platforms & Marketplaces',
            'education': '📚 Education & Best Practices',
            'trends': '📈 Market Trends & Analysis'
        }
        
        for category in section_order:
            articles = categories.get(category, [])
            if not articles:
                continue
                
            script += f"## {section_titles[category]}\n\n"
            
            # Add section context
            script += self._get_section_context(category, len(articles))
            script += "\n\n"
            
            # Add articles with rich context
            for i, article in enumerate(articles[:8], 1):  # Limit to top 8 per section
                script += self._format_article_for_script(article, i, category)
                script += "\n"
            
            script += "---\n\n"
        
        # Add conclusion and analysis
        script += self._build_conclusion_section(categories, all_articles)
        
        return script
    
    def _get_section_context(self, category, count):
        """Get contextual introduction for each section"""
        contexts = {
            'breaking': f"This week brought {count} major announcement{'s' if count != 1 else ''} that are reshaping the NIL landscape. These developments represent pivotal moments in the evolution of college athlete compensation.",
            
            'mega_deals': f"The market saw {count} significant NIL deal{'s' if count != 1 else ''} this week, demonstrating the growing financial opportunities available to college athletes and the increasing sophistication of NIL valuations.",
            
            'athlete_stories': f"Individual athletes made headlines with {count} notable development{'s' if count != 1 else ''} this week, showcasing the diverse ways student-athletes are leveraging their name, image, and likeness.",
            
            'collectives': f"NIL collectives showed significant activity with {count} important development{'s' if count != 1 else ''}, highlighting the evolving role of organized support systems in college athletics.",
            
            'policy': f"The regulatory landscape saw {count} key development{'s' if count != 1 else ''} this week, as stakeholders work to establish clearer guidelines for NIL activities.",
            
            'legal': f"The legal arena featured {count} significant case{'s' if count != 1 else ''} or development{'s' if count != 1 else ''} that could shape the future of NIL rights and regulations.",
            
            'platforms': f"Technology and platforms advanced with {count} notable update{'s' if count != 1 else ''}, making NIL opportunities more accessible and manageable for athletes.",
            
            'education': f"Educational initiatives produced {count} resource{'s' if count != 1 else ''} to help athletes, schools, and other stakeholders navigate the NIL landscape effectively.",
            
            'trends': f"Market analysis revealed {count} significant trend{'s' if count != 1 else ''} that provide insights into the direction of the NIL ecosystem."
        }
        
        return contexts.get(category, f"This section covers {count} important development{'s' if count != 1 else ''} in {category}.")
    
    def _format_article_for_script(self, article, index, category):
        """Format individual articles with rich context for engaging discussion"""
        
        title = article.get('title', 'Untitled Article')
        source = article.get('source', 'Unknown Source')
        summary = article.get('summary', '')
        priority = article.get('priority_level', 'Medium')
        published = article.get('published', '')
        
        # Clean title
        clean_title = re.sub(r'^\d+\.\s*', '', title)  # Remove numbering
        clean_title = re.sub(r'[🔥⭐💰]', '', clean_title)  # Remove emojis
        
        script_section = f"### {index}. {clean_title}\n\n"
        
        # Add priority indicator and context
        priority_context = {
            'Critical': '**🚨 CRITICAL DEVELOPMENT**',
            'High': '**⭐ HIGH IMPACT**',
            'Medium': '**📢 NOTABLE**',
            'Low': '**📋 UPDATE**'
        }
        
        if priority in priority_context:
            script_section += f"{priority_context[priority]}\n\n"
        
        # Add metadata
        script_section += f"**Source:** {source}\n"
        if published:
            try:
                pub_date = datetime.fromisoformat(published).strftime('%B %d, %Y')
                script_section += f"**Date:** {pub_date}\n"
            except:
                pass
        script_section += "\n"
        
        # Add rich summary and discussion points
        if summary:
            # Clean summary
            clean_summary = summary.replace('Summary:', '').strip()
            if clean_summary:
                script_section += f"**Key Details:** {clean_summary}\n\n"
        
        # Add discussion prompts based on category
        discussion_prompts = self._get_discussion_prompts(category, clean_title, summary)
        if discussion_prompts:
            script_section += f"**Discussion Points:**\n{discussion_prompts}\n\n"
        
        # Add NIL-specific implications
        implications = self._get_nil_implications(category, clean_title, priority)
        if implications:
            script_section += f"**NIL Market Implications:** {implications}\n\n"
        
        return script_section
    
    def _get_discussion_prompts(self, category, title, summary):
        """Generate relevant discussion prompts for NotebookLM hosts"""
        
        title_lower = title.lower()
        summary_lower = (summary or '').lower()
        
        prompts = {
            'breaking': [
                "- What makes this announcement particularly significant for college athletics?",
                "- How might this impact recruiting and athlete decisions?",
                "- What precedent does this set for future NIL activities?"
            ],
            'mega_deals': [
                "- How does this deal compare to other recent NIL agreements?",
                "- What factors likely contributed to this valuation?",
                "- What does this mean for athlete market values going forward?"
            ],
            'athlete_stories': [
                "- What can other athletes learn from this success story?",
                "- How does this demonstrate the evolving NIL opportunities?",
                "- What unique approach did this athlete take?"
            ],
            'collectives': [
                "- How are collectives changing the recruiting landscape?",
                "- What role do boosters play in this new ecosystem?",
                "- How sustainable is the collective model long-term?"
            ],
            'policy': [
                "- How will this policy change affect current NIL practices?",
                "- What compliance challenges might schools face?",
                "- How does this align with or diverge from state laws?"
            ],
            'legal': [
                "- What legal precedents might this case establish?",
                "- How could this impact future NIL regulations?",
                "- What are the broader implications for college sports?"
            ]
        }
        
        base_prompts = prompts.get(category, [
            "- What are the key takeaways from this development?",
            "- How might this impact the broader NIL ecosystem?",
            "- What should stakeholders watch for next?"
        ])
        
        return '\n'.join(base_prompts)
    
    def _get_nil_implications(self, category, title, priority):
        """Generate NIL-specific market implications"""
        
        implications = {
            'mega_deals': "This deal sets new benchmarks for athlete valuations and may trigger increased competition among collectives and brands seeking top talent.",
            'policy': "Policy changes like this directly impact how athletes, schools, and businesses structure their NIL relationships and compliance strategies.",
            'collectives': "Collective activities shape the competitive balance in college sports and influence how schools approach recruiting and athlete support.",
            'legal': "Legal developments create important precedents that will guide future NIL activities and regulatory frameworks.",
            'Critical': "This development has the potential to fundamentally reshape aspects of the NIL landscape and how stakeholders operate.",
            'High': "This represents a significant shift that NIL participants should monitor closely for strategic implications."
        }
        
        return implications.get(category, implications.get(priority, "This development contributes to the ongoing evolution of the NIL marketplace."))
    
    def _build_conclusion_section(self, categories, all_articles):
        """Build comprehensive conclusion with NIL-specific analysis"""
        
        conclusion = "## Weekly Analysis & Looking Ahead\n\n"
        
        conclusion += "### Key Takeaways\n\n"
        
        # Synthesize major themes
        if categories.get('mega_deals'):
            conclusion += "**Deal Flow:** This week's high-value NIL agreements demonstrate the continued maturation of athlete valuations and the increasing sophistication of deal structures. Brands and collectives are becoming more strategic in their partnerships.\n\n"
        
        if categories.get('policy'):
            conclusion += "**Regulatory Evolution:** Policy developments this week show the ongoing effort to balance athlete rights with competitive equity and institutional concerns. The regulatory framework continues to evolve rapidly.\n\n"
        
        if categories.get('collectives'):
            conclusion += "**Collective Impact:** NIL collective activities are increasingly shaping recruiting dynamics and competitive balance across conferences. Their role continues to expand beyond initial expectations.\n\n"
        
        if categories.get('legal'):
            conclusion += "**Legal Landscape:** Legal challenges and developments indicate that many fundamental questions about NIL rights and restrictions remain unsettled, suggesting continued evolution ahead.\n\n"
        
        conclusion += "### Industry Implications\n\n"
        conclusion += "The developments covered this week reflect several important trends:\n\n"
        conclusion += "- **Market Maturation:** The NIL market is showing signs of increased sophistication in deal structures and valuations\n"
        conclusion += "- **Competitive Dynamics:** Schools and conferences are adapting strategies to compete effectively in the NIL era\n"
        conclusion += "- **Athlete Empowerment:** Student-athletes continue to find creative ways to monetize their brands\n"
        conclusion += "- **Regulatory Clarity:** Stakeholders seek clearer guidelines while navigating a patchwork of state laws and NCAA rules\n\n"
        
        conclusion += "### What to Watch Next Week\n\n"
        conclusion += "Based on this week's developments, here are key areas to monitor:\n\n"
        conclusion += "- Additional major NIL deal announcements as signing periods approach\n"
        conclusion += "- NCAA responses to recent policy challenges and state law variations\n"
        conclusion += "- Collective fundraising efforts and new program launches\n"
        conclusion += "- Legal proceedings that could set important precedents\n"
        conclusion += "- Platform innovations making NIL more accessible to all athletes\n\n"
        
        conclusion += "### Conclusion\n\n"
        conclusion += f"This week's {len(all_articles)} developments underscore the dynamic nature of the NIL landscape. "
        conclusion += "From record-breaking deals to evolving policies, the pace of change continues to accelerate. "
        conclusion += "As the NIL ecosystem matures, we're seeing increased sophistication in how athletes, "
        conclusion += "institutions, and businesses approach these opportunities.\n\n"
        conclusion += "The NIL era represents a fundamental shift in college athletics, with each week bringing "
        conclusion += "new developments that shape the future of amateur sports and athlete compensation.\n\n"
        
        return conclusion
    
    def _create_summary_document(self, articles, output_path):
        """Create a concise summary document for NotebookLM context"""
        
        date_str = datetime.now().strftime('%B %d, %Y')
        
        summary = f"""NIL Weekly Summary - {date_str}

OVERVIEW
========
This document summarizes {len(articles)} key developments in Name, Image, and Likeness (NIL) from the past week.

MAJOR DEVELOPMENTS
==================
"""
        
        # Sort by priority and add top stories
        sorted_articles = sorted(articles, 
                               key=lambda x: (x.get('relevance_score', 0), x.get('published', '')), 
                               reverse=True)
        
        for i, article in enumerate(sorted_articles[:15], 1):  # Top 15 stories
            summary += f"\n{i}. {article.get('title', 'Untitled')}\n"
            summary += f"   Source: {article.get('source', 'Unknown')}\n"
            summary += f"   Category: {article.get('content_type', 'general').title()}\n"
            if article.get('summary'):
                clean_summary = article['summary'].replace('Summary:', '').strip()
                if len(clean_summary) > 150:
                    clean_summary = clean_summary[:147] + '...'
                summary += f"   Details: {clean_summary}\n"
            if article.get('priority_level'):
                summary += f"   Priority: {article['priority_level']}\n"
        
        # Add category breakdown
        categories = self._categorize_articles(articles)
        summary += f"\n\nCATEGORY BREAKDOWN\n==================\n"
        
        category_names = {
            'breaking': 'Breaking News',
            'mega_deals': 'Major Deals',
            'athlete_stories': 'Athlete Stories',
            'collectives': 'Collectives',
            'policy': 'Policy & Regulation',
            'legal': 'Legal',
            'platforms': 'Technology',
            'education': 'Education',
            'trends': 'Market Trends'
        }
        
        for category, cat_articles in categories.items():
            if cat_articles:
                summary += f"{category_names.get(category, category.title())}: {len(cat_articles)} stories\n"
        
        # Save summary
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        self.logger.info(f"✅ NotebookLM summary document saved to: {output_path}")

# Integration function
def create_notebooklm_assets(articles_data):
    """Create both script and summary for NotebookLM"""
    
    generator = NotebookLMScriptGenerator()
    
    print("📝 Creating NotebookLM-optimized assets for NIL news...")
    
    script_path, summary_path = generator.create_notebooklm_script(articles_data)
    
    print(f"✅ NotebookLM Script: {script_path}")
    print(f"✅ Summary Document: {summary_path}")
    print("\n🎙️ Next steps:")
    print("1. Upload both files to NotebookLM")
    print("2. Click 'Generate Podcast' in NotebookLM")
    print("3. Enjoy your NIL-focused conversational podcast!")
    
    return script_path, summary_path

if __name__ == "__main__":
    # Test with existing data
    import json
    from datetime import datetime
    
    date_str = datetime.now().strftime('%Y%m%d')
    data_file = f"data/nil_articles_{date_str}.json"
    
    try:
        with open(data_file, 'r') as f:
            articles = json.load(f)
        create_notebooklm_assets(articles)
    except FileNotFoundError:
        print(f"No articles file found at {data_file}")
        print("Run your NIL news collector first: python main.py")