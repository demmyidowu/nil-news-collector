"""
NIL News Monitor - Main Workflow
Run this script weekly to generate NIL news summaries
"""

import os
import sys
from datetime import datetime
import logging

# Add src directory to path
sys.path.append('src')

from collector import NILNewsCollector
from summarizer import NILNewsSummarizer

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = ['data', 'outputs', 'logs', 'config', 'src']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def setup_logging():
    """Setup logging configuration"""
    try:
        log_filename = f"logs/nil_news_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    except Exception as e:
        # Fallback to console-only logging if file creation fails
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        logger = logging.getLogger(__name__)
        logger.warning(f"Could not create log file, using console only: {e}")
        return logger

def main():
    """Main workflow"""
    setup_directories()  # Create directories BEFORE logging
    logger = setup_logging()
    
    try:
        logger.info("Starting NIL News collection and summarization...")
        
        # Step 1: Collect articles
        collector = NILNewsCollector()
        articles = collector.collect_rss_feeds(days_back=7)
        
        if not articles:
            logger.warning("No articles collected. Exiting.")
            return
        
        # Step 2: Filter relevant articles
        relevant_articles = collector.filter_relevant_articles(articles)
        
        if not relevant_articles:
            logger.warning("No relevant NIL articles found. Exiting.")
            return
        
        # Step 3: Save raw data
        data_file = collector.save_articles(relevant_articles)
        
        # Step 4: Generate summary with custom names
        summarizer = NILNewsSummarizer()
        
        # Create text summary
        text_summary = summarizer.create_text_summary(relevant_articles)
        text_output = f"outputs/NIL_Weekly_Summary_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(text_output, 'w', encoding='utf-8') as f:
            f.write(text_summary)
        logger.info(f"Text summary saved to {text_output}")
        
        # Create Word document with custom name
        doc_output = summarizer.create_word_document(
            relevant_articles, 
            custom_name="NIL_Weekly_Report"
        )
        
        # Step 5: Generate NotebookLM Assets
        try:
            sys.path.append('.')  # Add current directory to path
            from notebooklm_generator import create_notebooklm_assets
            
            logger.info("📝 Creating NotebookLM-optimized script and summary...")
            script_path, summary_path = create_notebooklm_assets(relevant_articles)
            
            logger.info(f"✅ NotebookLM Script: {script_path}")
            logger.info(f"✅ NotebookLM Summary: {summary_path}")
            logger.info("🎙️ Ready for NotebookLM podcast generation!")
                
        except ImportError:
            logger.info("💡 To enable NotebookLM generation, save the NotebookLM generator code as 'notebooklm_generator.py'")
        except Exception as e:
            logger.warning(f"NotebookLM generation error: {e}")
        
        # Print summary statistics
        logger.info("=" * 50)
        logger.info("NIL News summary generation completed successfully!")
        logger.info(f"Text summary: {text_output}")
        logger.info(f"Word document: {doc_output}")
        if 'script_path' in locals() and script_path:
            logger.info(f"📝 NotebookLM Script: {script_path}")
            logger.info(f"📄 NotebookLM Summary: {summary_path}")
        logger.info(f"Total articles processed: {len(relevant_articles)}")
        
        # Print top stories
        logger.info("\n🔥 Top NIL Stories This Week:")
        sorted_articles = sorted(relevant_articles, 
                               key=lambda x: x.get('relevance_score', 0), 
                               reverse=True)
        for i, article in enumerate(sorted_articles[:5], 1):
            logger.info(f"{i}. {article['title']} (Score: {article.get('relevance_score', 0)})")
        
    except Exception as e:
        logger.error(f"Error in main workflow: {e}")
        raise

if __name__ == "__main__":
    main()