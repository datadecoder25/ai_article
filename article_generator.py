#!/usr/bin/env python3
"""
Article Generator for ML Website
Generates SQL INSERT queries for articles by searching the internet and using AI to create content.
"""

import json
import os
import sys
import re
from typing import List, Dict, Optional
from datetime import datetime
import requests
from call_llm import get_llm_output


class ArticleGenerator:
    """Generate SQL INSERT queries for ML articles."""
    
    def __init__(self, model_name: str = "anthropic.claude-sonnet-4-20250514-v1-0"):
        """
        Initialize the article generator.
        
        Args:
            model_name: LLM model name to use (default: Claude Sonnet 4)
        """
        self.model_name = model_name
        
    def generate_article_content(self, topic: str, tags: List[str]) -> Dict:
        """
        Generate article content using LLM based on topic.
        
        Args:
            topic: Article topic
            tags: List of tags
            
        Returns:
            Dictionary with all article fields
        """
        # Generate the article using LLM
        prompt = f"""You are an expert technical writer specializing in Machine Learning and AI.

Generate a comprehensive article about: "{topic}"

Tags: {', '.join(tags)}

Please provide a JSON response with the following fields:

1. "title": An engaging, SEO-friendly title (50-60 characters)
2. "content": Comprehensive article which will describe the concept in very easy language along with mathematical equations to explain everything. This should be a technical document.
The content should be around (1500-2500 words) formatted in HTML with:
   - Multiple sections with <h2> and <h3> headings
   - Paragraphs in <p> tags
   - Code examples in <pre><code> blocks if relevant
   - Lists using <ul>/<ol> and <li> tags
   - Strong emphasis with <strong> tags for key concepts
   - Make it technical but accessible
   - Write mathematical equations properly which can be rendered properly in the article.
   - add main main items. Don't make it a very big article. Make it concise and to the point.
   
3. "excerpt": A compelling 100-150 character preview that makes readers want to click

4. "summary": Exactly ~100 words explaining the core concept. Should be:
   - Self-contained and comprehensive
   - Not too technical but should be able to explain the concept in a way that is easy to understand
   - Cover key points and applications
   - Standalone explanation that doesn't require reading the full article
   - The intent of this summary is to make user understand the concept in a very short and concise way and very quickly.

5. "summary_title": A short 2-5 word title for the concept (different from main title)

6. "reading_time": Estimated reading time in minutes (based on content length)

Make the content authoritative, well-researched, and valuable for ML practitioners.

Return ONLY valid JSON, no other text."""

        try:
            # Call the custom LLM function
            response_content = get_llm_output(prompt, model_name=self.model_name)
            
            # Try to extract JSON if wrapped in markdown code blocks
            if response_content.startswith("```"):
                response_content = re.sub(r'^```json?\s*\n?', '', response_content)
                response_content = re.sub(r'\n?```\s*$', '', response_content)
            
            article_data = json.loads(response_content)
            
            # Validate required fields
            required_fields = ['title', 'content', 'excerpt', 'summary', 'summary_title', 'reading_time']
            for field in required_fields:
                if field not in article_data:
                    raise ValueError(f"Missing required field: {field}")
            
            return article_data
            
        except Exception as e:
            print(f"❌ Error generating content for '{topic}': {str(e)}")
            # Return fallback content
            return {
                'title': f"Understanding {topic}: A Comprehensive Guide",
                'content': f"<p>This is a comprehensive guide about {topic}.</p>",
                'excerpt': f"Learn about {topic} in machine learning.",
                'summary': f"{topic} is an important concept in machine learning. " * 10,
                'summary_title': topic[:30],
                'reading_time': 10
            }
    
    def get_featured_image(self, topic: str) -> str:
        """
        Get a featured image URL for the article.
        Uses Pexels as a default placeholder (you can enhance this with Pexels API).
        
        Args:
            topic: Article topic
            
        Returns:
            Image URL
        """
        # Default ML/AI related images from Pexels
        default_images = [
            'https://images.pexels.com/photos/8439093/pexels-photo-8439093.jpeg',
            'https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg',
            'https://images.pexels.com/photos/8386434/pexels-photo-8386434.jpeg',
            'https://images.pexels.com/photos/8438918/pexels-photo-8438918.jpeg',
            'https://images.pexels.com/photos/7516366/pexels-photo-7516366.jpeg'
        ]
        
        # Simple hash to consistently assign images
        return default_images[hash(topic) % len(default_images)]
    
    def escape_sql_string(self, text: str) -> str:
        """
        Escape single quotes in SQL strings.
        
        Args:
            text: Text to escape
            
        Returns:
            Escaped text
        """
        return text.replace("'", "''")
    
    def generate_sql_insert(
        self,
        topic: str,
        tags: List[str],
        is_premium: bool = False,
        views: int = 0,
        created_by: str = 'c41b5bc1-d819-4b8a-ab04-cf1ae4692304'
    ) -> str:
        """
        Generate a SQL INSERT statement for an article.
        
        Args:
            topic: Article topic
            tags: List of tags
            is_premium: Whether article is premium
            views: Initial view count
            created_by: UUID of the creator
            
        Returns:
            SQL INSERT statement
        """
        print(f"\n📝 Generating article for: {topic}")
        print(f"   Tags: {', '.join(tags)}")
        
        # Generate content
        print("   🤖 Generating content with AI...")
        article_data = self.generate_article_content(topic, tags)
        
        # Get featured image
        featured_image = self.get_featured_image(topic)
        
        # Escape all text fields
        title = self.escape_sql_string(article_data['title'])
        content = self.escape_sql_string(article_data['content'])
        excerpt = self.escape_sql_string(article_data.get('excerpt', ''))
        summary = self.escape_sql_string(article_data.get('summary', ''))
        summary_title = self.escape_sql_string(article_data.get('summary_title', ''))
        
        # Format tags as PostgreSQL array
        tags_str = ", ".join([f"'{tag}'" for tag in tags])
        
        # Build SQL INSERT statement
        sql = f"""  (
    '{title}',
    '{content}',
    '{excerpt}',
    '{summary}',
    '{summary_title}',
    '{featured_image}',
    {article_data.get('reading_time', 10)},
    ARRAY[{tags_str}],
    {str(is_premium).lower()},
    {views},
    '{created_by}'
  )"""
        
        print(f"   ✅ Generated: {article_data['title']}")
        
        return sql
    
    def generate_batch_sql(
        self,
        topics: List[Dict],
        created_by: str = 'c41b5bc1-d819-4b8a-ab04-cf1ae4692304'
    ) -> str:
        """
        Generate SQL INSERT statements for multiple articles.
        
        Args:
            topics: List of topic dictionaries with 'name', 'tags', 'is_premium', 'views'
            created_by: UUID of the creator
            
        Returns:
            Complete SQL INSERT statement
        """
        print(f"\n🚀 Starting batch generation for {len(topics)} articles...\n")
        
        sql_header = """INSERT INTO articles (title, content, excerpt, summary, summary_title, featured_image, reading_time, tags, is_premium, views, created_by)
VALUES
"""
        
        inserts = []
        for i, topic_data in enumerate(topics, 1):
            print(f"\n[{i}/{len(topics)}] Processing: {topic_data['name']}")
            
            insert = self.generate_sql_insert(
                topic=topic_data['name'],
                tags=topic_data.get('tags', []),
                is_premium=topic_data.get('is_premium', False),
                views=topic_data.get('views', 0),
                created_by=created_by
            )
            inserts.append(insert)
        
        # Join all inserts with commas
        sql_values = ",\n".join(inserts)
        
        # Complete SQL statement
        complete_sql = sql_header + sql_values + ";"
        
        print(f"\n\n✨ Successfully generated SQL for {len(topics)} articles!\n")
        
        return complete_sql


def load_topics_from_file(filepath: str) -> List[Dict]:
    """
    Load topics from a JSON file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        List of topic dictionaries
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return data.get('topics', [])


def main():
    """Main function to run the article generator."""
    print("=" * 80)
    print("ML Article Generator - SQL Insert Query Builder")
    print("=" * 80)
    
    # Load configuration from environment
    created_by_uuid = os.getenv('CREATED_BY_UUID', 'c41b5bc1-d819-4b8a-ab04-cf1ae4692304')
    model_name = os.getenv('LLM_MODEL_NAME', 'anthropic.claude-sonnet-4-20250514-v1-0')
    
    print(f"\n🤖 Using LLM Model: {model_name}")
    
    # Check for input file
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'topics.json'
    
    if not os.path.exists(input_file):
        print(f"\n❌ Error: Input file '{input_file}' not found!")
        print(f"Usage: python article_generator.py [topics_file.json]")
        print(f"Using default: topics.json")
        sys.exit(1)
    
    # Load topics
    print(f"\n📖 Loading topics from: {input_file}")
    topics = load_topics_from_file(input_file)
    print(f"   Found {len(topics)} topics to process")
    
    # Initialize generator
    generator = ArticleGenerator(model_name=model_name)
    
    # Generate SQL
    sql_output = generator.generate_batch_sql(topics, created_by=created_by_uuid)
    
    # Save to file
    output_file = f"articles_insert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    with open(output_file, 'w') as f:
        f.write(sql_output)
    
    print(f"\n📄 SQL output saved to: {output_file}")
    print(f"\n{'=' * 80}")
    print("Done! You can now run this SQL file against your database.")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()

