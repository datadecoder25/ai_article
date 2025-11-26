# ML Article Generator

A powerful tool that automatically generates SQL INSERT queries for machine learning articles by searching the internet and using AI to create comprehensive, high-quality content.

## 🎯 Features

- **AI-Powered Content Generation**: Uses Claude Sonnet 4 via Intuit Genos API to create comprehensive, well-structured articles
- **Complete SQL Generation**: Generates production-ready SQL INSERT statements
- **Batch Processing**: Process multiple topics in one run
- **Flexible Configuration**: Customize tags, premium status, view counts, and more
- **Custom LLM Integration**: Uses your existing `call_llm.py` function for LLM calls

## 📋 Generated Content

For each topic, the tool generates:

1. **Title**: SEO-friendly, engaging title (50-60 characters)
2. **Content**: Comprehensive article (1500-2500 words) with HTML formatting
3. **Excerpt**: Short preview text (100-150 characters)
4. **Summary**: 100-word AI concept explanation
5. **Summary Title**: Short concept title (2-5 words)
6. **Featured Image**: High-quality image URL
7. **Reading Time**: Estimated reading time in minutes
8. **Tags**: Relevant topic tags
9. **Premium Flag**: Free or premium content designation
10. **View Count**: Initial view counter

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download this repository
cd ai_article

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration (Optional)

The tool uses your custom LLM function from `call_llm.py` (Intuit Genos API with Claude Sonnet 4).

You can optionally configure the following environment variables:

```bash
# Set creator UUID (Optional)
export CREATED_BY_UUID='your-uuid-here'

# Set LLM model name (Optional, default: anthropic.claude-sonnet-4-20250514-v1-0)
export LLM_MODEL_NAME='anthropic.claude-sonnet-4-20250514-v1-0'
```

**Note:** The LLM calls are made through `call_llm.py` which handles authentication with Intuit's Genos API.

### 3. Create Your Topics File

Create or edit `topics.json` with your desired topics:

```json
{
  "topics": [
    {
      "name": "Understanding Transformers in Deep Learning",
      "tags": ["Transformers", "NLP", "Deep Learning", "Architecture"],
      "is_premium": false,
      "views": 15420
    },
    {
      "name": "Fine-tuning Large Language Models with LoRA",
      "tags": ["LLM", "Fine-tuning", "LoRA", "Training"],
      "is_premium": true,
      "views": 8950
    }
  ]
}
```

**Field Descriptions:**
- `name` (required): The topic/title of the article
- `tags` (required): Array of relevant tags for categorization
- `is_premium` (optional): Set to `true` for premium content, default is `false`
- `views` (optional): Initial view count, default is `0`

### 4. Generate SQL

```bash
# Using default topics.json
python article_generator.py

# Using a custom topics file
python article_generator.py my_custom_topics.json
```

### 5. Output

The tool will generate a timestamped SQL file:
```
articles_insert_20251125_143022.sql
```

You can then run this SQL file against your database:
```bash
psql -U your_user -d your_database -f articles_insert_20251125_143022.sql
```

## 📝 Input Format

The `topics.json` file should contain an array of topic objects:

```json
{
  "topics": [
    {
      "name": "Topic Name",
      "tags": ["Tag1", "Tag2", "Tag3"],
      "is_premium": false,
      "views": 1000
    }
  ]
}
```

## 🗄️ Database Schema

The generated SQL statements match this schema:

```sql
CREATE TABLE articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  excerpt TEXT,
  summary TEXT,
  summary_title TEXT,
  featured_image TEXT,
  reading_time INTEGER,
  tags TEXT[] DEFAULT '{}',
  is_premium BOOLEAN DEFAULT false,
  views INTEGER DEFAULT 0,
  created_by UUID REFERENCES profiles(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `SERPER_API_KEY` (optional): Your Serper API key for web search
- `CREATED_BY_UUID` (optional): UUID of the article creator (default: 'c41b5bc1-d819-4b8a-ab04-cf1ae4692304')

### Customization

You can modify the `article_generator.py` file to:
- Change the OpenAI model (default: `gpt-4o`)
- Adjust content length and style
- Customize image sources
- Modify the prompt template

## 💡 Example Usage

### Basic Example

```bash
# Run with default topics
python article_generator.py
```

### Advanced Example

```bash
# Set environment variables
export CREATED_BY_UUID='your-user-uuid'
export LLM_MODEL_NAME='anthropic.claude-sonnet-4-20250514-v1-0'

# Run with custom topics file
python article_generator.py custom_ml_topics.json
```

## 📊 Sample Topics Included

The repository includes a `topics.json` with 10 sample ML topics:

1. Understanding Transformers in Deep Learning
2. Fine-tuning Large Language Models with LoRA
3. Convolutional Neural Networks for Computer Vision
4. Retrieval Augmented Generation (RAG) Systems
5. Introduction to Reinforcement Learning
6. Optimizing Neural Networks: A Practical Guide
7. Building Recommendation Systems with Deep Learning
8. Understanding Diffusion Models for Image Generation
9. Graph Neural Networks: Theory and Practice
10. MLOps: Deploying Machine Learning Models at Scale

## ⚠️ Important Notes

1. **LLM Integration**: The tool uses your custom `call_llm.py` function which calls Intuit's Genos API with Claude Sonnet 4. Ensure the credentials in `call_llm.py` are valid.

2. **Rate Limits**: Be aware of API rate limits. The tool processes topics sequentially to avoid issues.

3. **Content Review**: Always review generated content before publishing. While AI-generated content is high quality, human review ensures accuracy and brand consistency.

4. **UUID**: Make sure the `created_by` UUID exists in your `profiles` table before running the SQL.

## 🛠️ Troubleshooting

### LLM API errors
Make sure the credentials in `call_llm.py` are valid and the Intuit Genos API is accessible. Check the `ENV`, `APP_ID`, `APP_SECRET`, `EXPERIENCE_ID`, and `OFFLINE_JOB_ID` values.

### "Input file not found"
Make sure your topics file exists:
```bash
ls topics.json
```

### Content quality issues
- The tool uses Claude Sonnet 4 by default which provides excellent quality
- Adjust the prompt template in the code if needed
- Try different model versions by setting `LLM_MODEL_NAME`

## 📄 License

This tool is provided as-is for generating content for your ML website.

## 🤝 Contributing

Feel free to modify and extend this tool for your specific needs. Some ideas:
- Integrate with Pexels API for better image selection
- Switch between different LLM models in the Genos API
- Generate images using DALL-E or Stable Diffusion
- Add multi-language support
- Add custom prompt templates for different article styles

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the generated SQL for errors
3. Verify your API keys are correct
4. Ensure your topics.json is valid JSON

---

**Happy article generating! 🚀**

