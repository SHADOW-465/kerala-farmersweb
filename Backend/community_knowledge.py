"""
Community Knowledge Sharing Module
AI-powered platform for farmers to share knowledge, ask questions, and learn from each other
"""

import json
import sqlite3
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import re
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class User:
    """User profile for community platform"""
    user_id: str
    username: str
    full_name: str
    location: Dict[str, str]  # state, district, village
    farming_experience: int  # years
    crops_grown: List[str]
    expertise_areas: List[str]
    reputation_score: float
    join_date: datetime
    is_verified: bool
    profile_picture: str
    bio: str

@dataclass
class Question:
    """Question posted by farmers"""
    question_id: str
    user_id: str
    title: str
    content: str
    category: str
    tags: List[str]
    location: Dict[str, str]
    crop_related: List[str]
    urgency: str  # low, medium, high
    status: str  # open, answered, closed
    views: int
    upvotes: int
    created_at: datetime
    updated_at: datetime

@dataclass
class Answer:
    """Answer to a question"""
    answer_id: str
    question_id: str
    user_id: str
    content: str
    is_accepted: bool
    upvotes: int
    downvotes: int
    created_at: datetime
    updated_at: datetime

@dataclass
class Article:
    """Knowledge article or best practice"""
    article_id: str
    user_id: str
    title: str
    content: str
    category: str
    tags: List[str]
    crop_related: List[str]
    difficulty_level: str  # beginner, intermediate, advanced
    views: int
    likes: int
    shares: int
    is_featured: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class Discussion:
    """Discussion thread"""
    discussion_id: str
    user_id: str
    title: str
    content: str
    category: str
    tags: List[str]
    replies_count: int
    views: int
    likes: int
    is_pinned: bool
    created_at: datetime
    updated_at: datetime

class CommunityKnowledgePlatform:
    """
    AI-powered community knowledge sharing platform for farmers
    """
    
    def __init__(self, db_path: str = "community.db"):
        """
        Initialize community knowledge platform
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.init_database()
        self.load_knowledge_base()
    
    def init_database(self):
        """Initialize database for community platform"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        full_name TEXT NOT NULL,
                        state TEXT NOT NULL,
                        district TEXT NOT NULL,
                        village TEXT NOT NULL,
                        farming_experience INTEGER NOT NULL,
                        crops_grown TEXT NOT NULL,
                        expertise_areas TEXT NOT NULL,
                        reputation_score REAL DEFAULT 0,
                        join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_verified BOOLEAN DEFAULT 0,
                        profile_picture TEXT,
                        bio TEXT
                    )
                ''')
                
                # Questions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS questions (
                        question_id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        category TEXT NOT NULL,
                        tags TEXT NOT NULL,
                        state TEXT NOT NULL,
                        district TEXT NOT NULL,
                        village TEXT NOT NULL,
                        crop_related TEXT NOT NULL,
                        urgency TEXT DEFAULT 'medium',
                        status TEXT DEFAULT 'open',
                        views INTEGER DEFAULT 0,
                        upvotes INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')
                
                # Answers table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS answers (
                        answer_id TEXT PRIMARY KEY,
                        question_id TEXT NOT NULL,
                        user_id TEXT NOT NULL,
                        content TEXT NOT NULL,
                        is_accepted BOOLEAN DEFAULT 0,
                        upvotes INTEGER DEFAULT 0,
                        downvotes INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (question_id) REFERENCES questions (question_id),
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')
                
                # Articles table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS articles (
                        article_id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        category TEXT NOT NULL,
                        tags TEXT NOT NULL,
                        crop_related TEXT NOT NULL,
                        difficulty_level TEXT DEFAULT 'intermediate',
                        views INTEGER DEFAULT 0,
                        likes INTEGER DEFAULT 0,
                        shares INTEGER DEFAULT 0,
                        is_featured BOOLEAN DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')
                
                # Discussions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS discussions (
                        discussion_id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        category TEXT NOT NULL,
                        tags TEXT NOT NULL,
                        replies_count INTEGER DEFAULT 0,
                        views INTEGER DEFAULT 0,
                        likes INTEGER DEFAULT 0,
                        is_pinned BOOLEAN DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')
                
                # Replies table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS replies (
                        reply_id TEXT PRIMARY KEY,
                        discussion_id TEXT NOT NULL,
                        user_id TEXT NOT NULL,
                        content TEXT NOT NULL,
                        upvotes INTEGER DEFAULT 0,
                        downvotes INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (discussion_id) REFERENCES discussions (discussion_id),
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')
                
                # Knowledge base table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS knowledge_base (
                        kb_id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        category TEXT NOT NULL,
                        tags TEXT NOT NULL,
                        crop_related TEXT NOT NULL,
                        source TEXT NOT NULL,
                        reliability_score REAL DEFAULT 0.5,
                        views INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                logger.info("Community database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def load_knowledge_base(self):
        """Load knowledge base with farming information"""
        try:
            # Check if knowledge base is empty
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM knowledge_base')
                count = cursor.fetchone()[0]
                
                if count == 0:
                    self._populate_knowledge_base()
                
                logger.info("Knowledge base loaded successfully")
                
        except Exception as e:
            logger.error(f"Error loading knowledge base: {str(e)}")
    
    def _populate_knowledge_base(self):
        """Populate knowledge base with farming information"""
        knowledge_entries = [
            {
                'title': 'Rice Cultivation Best Practices',
                'content': 'Rice cultivation requires proper water management, soil preparation, and pest control. Key practices include: 1) Use certified seeds, 2) Maintain proper water level (2-3 inches), 3) Apply fertilizers in split doses, 4) Control weeds regularly, 5) Monitor for diseases like blast and bacterial blight.',
                'category': 'Crop Cultivation',
                'tags': ['rice', 'cultivation', 'water management', 'fertilizer'],
                'crop_related': ['Rice'],
                'source': 'Agricultural Extension',
                'reliability_score': 0.9
            },
            {
                'title': 'Organic Pest Control Methods',
                'content': 'Organic pest control methods include: 1) Neem oil spray for aphids and whiteflies, 2) Garlic and chili spray for various pests, 3) Companion planting with marigold, 4) Use of beneficial insects like ladybugs, 5) Crop rotation to break pest cycles.',
                'category': 'Pest Management',
                'tags': ['organic', 'pest control', 'natural methods', 'sustainable'],
                'crop_related': ['All'],
                'source': 'Organic Farming Research',
                'reliability_score': 0.85
            },
            {
                'title': 'Soil Health Improvement Techniques',
                'content': 'Improve soil health by: 1) Adding organic matter through compost, 2) Using green manure crops, 3) Practicing crop rotation, 4) Maintaining proper pH levels, 5) Avoiding over-tillage, 6) Using cover crops to prevent erosion.',
                'category': 'Soil Management',
                'tags': ['soil health', 'organic matter', 'compost', 'crop rotation'],
                'crop_related': ['All'],
                'source': 'Soil Science Research',
                'reliability_score': 0.9
            },
            {
                'title': 'Coconut Tree Care and Maintenance',
                'content': 'Coconut tree care includes: 1) Regular watering during dry periods, 2) Application of organic manure twice a year, 3) Pruning of old fronds, 4) Control of rhinoceros beetle, 5) Harvesting at proper maturity, 6) Protection from strong winds.',
                'category': 'Tree Care',
                'tags': ['coconut', 'tree care', 'maintenance', 'pest control'],
                'crop_related': ['Coconut'],
                'source': 'Horticulture Department',
                'reliability_score': 0.88
            },
            {
                'title': 'Weather-Based Farming Decisions',
                'content': 'Make farming decisions based on weather: 1) Check weather forecasts regularly, 2) Avoid planting during heavy rain, 3) Water crops before expected dry spells, 4) Harvest before storms, 5) Use weather data for pest and disease management.',
                'category': 'Weather Management',
                'tags': ['weather', 'farming decisions', 'forecasting', 'climate'],
                'crop_related': ['All'],
                'source': 'Meteorological Department',
                'reliability_score': 0.8
            }
        ]
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for entry in knowledge_entries:
                    kb_id = f"kb_{hashlib.md5(entry['title'].encode()).hexdigest()[:8]}"
                    
                    cursor.execute('''
                        INSERT INTO knowledge_base (
                            kb_id, title, content, category, tags, crop_related, source, reliability_score
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        kb_id,
                        entry['title'],
                        entry['content'],
                        entry['category'],
                        json.dumps(entry['tags']),
                        json.dumps(entry['crop_related']),
                        entry['source'],
                        entry['reliability_score']
                    ))
                
                conn.commit()
                logger.info("Knowledge base populated successfully")
                
        except Exception as e:
            logger.error(f"Error populating knowledge base: {str(e)}")
    
    def register_user(self, user_data: Dict[str, Any]) -> str:
        """
        Register a new user
        
        Args:
            user_data: Dictionary containing user data
            
        Returns:
            User ID of the created user
        """
        try:
            user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_data.get('username', 'unknown')}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO users (
                        user_id, username, full_name, state, district, village,
                        farming_experience, crops_grown, expertise_areas, reputation_score,
                        is_verified, profile_picture, bio
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    user_data['username'],
                    user_data['full_name'],
                    user_data['location']['state'],
                    user_data['location']['district'],
                    user_data['location']['village'],
                    user_data['farming_experience'],
                    json.dumps(user_data['crops_grown']),
                    json.dumps(user_data['expertise_areas']),
                    user_data.get('reputation_score', 0),
                    user_data.get('is_verified', False),
                    user_data.get('profile_picture', ''),
                    user_data.get('bio', '')
                ))
                
                conn.commit()
                logger.info(f"User registered: {user_id}")
                return user_id
                
        except Exception as e:
            logger.error(f"Error registering user: {str(e)}")
            raise
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
                row = cursor.fetchone()
                
                if row:
                    return User(
                        user_id=row[0],
                        username=row[1],
                        full_name=row[2],
                        location={
                            'state': row[3],
                            'district': row[4],
                            'village': row[5]
                        },
                        farming_experience=row[6],
                        crops_grown=json.loads(row[7]),
                        expertise_areas=json.loads(row[8]),
                        reputation_score=row[9],
                        join_date=datetime.fromisoformat(row[10]),
                        is_verified=bool(row[11]),
                        profile_picture=row[12] or '',
                        bio=row[13] or ''
                    )
                return None
                
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None
    
    def post_question(self, user_id: str, question_data: Dict[str, Any]) -> str:
        """
        Post a new question
        
        Args:
            user_id: User ID
            question_data: Dictionary containing question data
            
        Returns:
            Question ID
        """
        try:
            question_id = f"q_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO questions (
                        question_id, user_id, title, content, category, tags,
                        state, district, village, crop_related, urgency, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    question_id,
                    user_id,
                    question_data['title'],
                    question_data['content'],
                    question_data['category'],
                    json.dumps(question_data['tags']),
                    question_data['location']['state'],
                    question_data['location']['district'],
                    question_data['location']['village'],
                    json.dumps(question_data['crop_related']),
                    question_data.get('urgency', 'medium'),
                    'open'
                ))
                
                conn.commit()
                logger.info(f"Question posted: {question_id}")
                return question_id
                
        except Exception as e:
            logger.error(f"Error posting question: {str(e)}")
            raise
    
    def answer_question(self, user_id: str, question_id: str, answer_content: str) -> str:
        """
        Answer a question
        
        Args:
            user_id: User ID
            question_id: Question ID
            answer_content: Answer content
            
        Returns:
            Answer ID
        """
        try:
            answer_id = f"a_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO answers (
                        answer_id, question_id, user_id, content
                    ) VALUES (?, ?, ?, ?)
                ''', (answer_id, question_id, user_id, answer_content))
                
                # Update question status if it was open
                cursor.execute('''
                    UPDATE questions 
                    SET status = 'answered', updated_at = CURRENT_TIMESTAMP 
                    WHERE question_id = ? AND status = 'open'
                ''', (question_id,))
                
                conn.commit()
                logger.info(f"Answer posted: {answer_id}")
                return answer_id
                
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise
    
    def search_questions(self, query: str, category: str = None, limit: int = 10) -> List[Question]:
        """
        Search for questions based on query
        
        Args:
            query: Search query
            category: Optional category filter
            limit: Maximum number of results
            
        Returns:
            List of matching questions
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build search query
                search_query = '''
                    SELECT * FROM questions 
                    WHERE (title LIKE ? OR content LIKE ?)
                '''
                params = [f'%{query}%', f'%{query}%']
                
                if category:
                    search_query += ' AND category = ?'
                    params.append(category)
                
                search_query += ' ORDER BY created_at DESC LIMIT ?'
                params.append(limit)
                
                cursor.execute(search_query, params)
                rows = cursor.fetchall()
                
                questions = []
                for row in rows:
                    questions.append(Question(
                        question_id=row[0],
                        user_id=row[1],
                        title=row[2],
                        content=row[3],
                        category=row[4],
                        tags=json.loads(row[5]),
                        location={
                            'state': row[6],
                            'district': row[7],
                            'village': row[8]
                        },
                        crop_related=json.loads(row[9]),
                        urgency=row[10],
                        status=row[11],
                        views=row[12],
                        upvotes=row[13],
                        created_at=datetime.fromisoformat(row[14]),
                        updated_at=datetime.fromisoformat(row[15])
                    ))
                
                return questions
                
        except Exception as e:
            logger.error(f"Error searching questions: {str(e)}")
            return []
    
    def get_question_answers(self, question_id: str) -> List[Answer]:
        """Get answers for a question"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM answers 
                    WHERE question_id = ? 
                    ORDER BY upvotes DESC, created_at ASC
                ''', (question_id,))
                
                rows = cursor.fetchall()
                answers = []
                
                for row in rows:
                    answers.append(Answer(
                        answer_id=row[0],
                        question_id=row[1],
                        user_id=row[2],
                        content=row[3],
                        is_accepted=bool(row[4]),
                        upvotes=row[5],
                        downvotes=row[6],
                        created_at=datetime.fromisoformat(row[7]),
                        updated_at=datetime.fromisoformat(row[8])
                    ))
                
                return answers
                
        except Exception as e:
            logger.error(f"Error getting question answers: {str(e)}")
            return []
    
    def get_ai_suggestions(self, question_id: str) -> List[Dict[str, Any]]:
        """
        Get AI-powered suggestions for a question
        
        Args:
            question_id: Question ID
            
        Returns:
            List of AI suggestions
        """
        try:
            # Get question details
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM questions WHERE question_id = ?', (question_id,))
                row = cursor.fetchone()
                
                if not row:
                    return []
                
                question_title = row[2]
                question_content = row[3]
                question_category = row[4]
                crop_related = json.loads(row[9])
                
                # Search knowledge base for relevant information
                suggestions = []
                
                # Search by category
                cursor.execute('''
                    SELECT * FROM knowledge_base 
                    WHERE category = ? 
                    ORDER BY reliability_score DESC 
                    LIMIT 3
                ''', (question_category,))
                
                for kb_row in cursor.fetchall():
                    suggestions.append({
                        'type': 'knowledge_base',
                        'title': kb_row[1],
                        'content': kb_row[2],
                        'source': kb_row[6],
                        'reliability': kb_row[7]
                    })
                
                # Search by crop-related content
                if crop_related:
                    for crop in crop_related:
                        cursor.execute('''
                            SELECT * FROM knowledge_base 
                            WHERE crop_related LIKE ? 
                            ORDER BY reliability_score DESC 
                            LIMIT 2
                        ''', (f'%{crop}%',))
                        
                        for kb_row in cursor.fetchall():
                            suggestions.append({
                                'type': 'crop_specific',
                                'title': kb_row[1],
                                'content': kb_row[2],
                                'source': kb_row[6],
                                'reliability': kb_row[7]
                            })
                
                # Search for similar questions
                cursor.execute('''
                    SELECT * FROM questions 
                    WHERE category = ? AND question_id != ? 
                    ORDER BY created_at DESC 
                    LIMIT 3
                ''', (question_category, question_id))
                
                for q_row in cursor.fetchall():
                    suggestions.append({
                        'type': 'similar_question',
                        'title': q_row[2],
                        'content': q_row[3],
                        'question_id': q_row[0],
                        'views': q_row[12]
                    })
                
                return suggestions[:5]  # Return top 5 suggestions
                
        except Exception as e:
            logger.error(f"Error getting AI suggestions: {str(e)}")
            return []
    
    def upvote_content(self, content_type: str, content_id: str, user_id: str) -> bool:
        """
        Upvote content (question, answer, article)
        
        Args:
            content_type: Type of content (question, answer, article)
            content_id: Content ID
            user_id: User ID
            
        Returns:
            True if successful
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if content_type == 'question':
                    cursor.execute('''
                        UPDATE questions 
                        SET upvotes = upvotes + 1 
                        WHERE question_id = ?
                    ''', (content_id,))
                elif content_type == 'answer':
                    cursor.execute('''
                        UPDATE answers 
                        SET upvotes = upvotes + 1 
                        WHERE answer_id = ?
                    ''', (content_id,))
                elif content_type == 'article':
                    cursor.execute('''
                        UPDATE articles 
                        SET likes = likes + 1 
                        WHERE article_id = ?
                    ''', (content_id,))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error upvoting content: {str(e)}")
            return False
    
    def get_trending_topics(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get trending topics based on recent activity"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get trending questions
                cursor.execute('''
                    SELECT category, COUNT(*) as count 
                    FROM questions 
                    WHERE created_at >= date('now', '-7 days') 
                    GROUP BY category 
                    ORDER BY count DESC 
                    LIMIT ?
                ''', (limit,))
                
                trending = []
                for row in cursor.fetchall():
                    trending.append({
                        'topic': row[0],
                        'type': 'question_category',
                        'activity_count': row[1]
                    })
                
                # Get trending tags
                cursor.execute('''
                    SELECT tags 
                    FROM questions 
                    WHERE created_at >= date('now', '-7 days')
                ''')
                
                tag_counts = {}
                for row in cursor.fetchall():
                    tags = json.loads(row[0])
                    for tag in tags:
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
                
                # Sort tags by count
                sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
                
                for tag, count in sorted_tags[:5]:
                    trending.append({
                        'topic': tag,
                        'type': 'tag',
                        'activity_count': count
                    })
                
                return trending[:limit]
                
        except Exception as e:
            logger.error(f"Error getting trending topics: {str(e)}")
            return []
    
    def get_user_reputation(self, user_id: str) -> float:
        """Calculate user reputation score"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get user's contributions
                cursor.execute('''
                    SELECT 
                        (SELECT COUNT(*) FROM questions WHERE user_id = ?) as questions_count,
                        (SELECT COUNT(*) FROM answers WHERE user_id = ?) as answers_count,
                        (SELECT SUM(upvotes) FROM questions WHERE user_id = ?) as question_upvotes,
                        (SELECT SUM(upvotes) FROM answers WHERE user_id = ?) as answer_upvotes
                ''', (user_id, user_id, user_id, user_id))
                
                row = cursor.fetchone()
                if not row:
                    return 0.0
                
                questions_count = row[0] or 0
                answers_count = row[1] or 0
                question_upvotes = row[2] or 0
                answer_upvotes = row[3] or 0
                
                # Calculate reputation score
                reputation = (questions_count * 2 + answers_count * 5 + 
                            question_upvotes * 1 + answer_upvotes * 3)
                
                return min(1000, reputation)  # Cap at 1000
                
        except Exception as e:
            logger.error(f"Error calculating user reputation: {str(e)}")
            return 0.0
    
    def get_community_stats(self) -> Dict[str, Any]:
        """Get community statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total users
                cursor.execute('SELECT COUNT(*) FROM users')
                total_users = cursor.fetchone()[0]
                
                # Total questions
                cursor.execute('SELECT COUNT(*) FROM questions')
                total_questions = cursor.fetchone()[0]
                
                # Total answers
                cursor.execute('SELECT COUNT(*) FROM answers')
                total_answers = cursor.fetchone()[0]
                
                # Active users (last 30 days)
                cursor.execute('''
                    SELECT COUNT(DISTINCT user_id) 
                    FROM questions 
                    WHERE created_at >= date('now', '-30 days')
                ''')
                active_users = cursor.fetchone()[0]
                
                # Questions by category
                cursor.execute('''
                    SELECT category, COUNT(*) as count 
                    FROM questions 
                    GROUP BY category 
                    ORDER BY count DESC
                ''')
                questions_by_category = dict(cursor.fetchall())
                
                return {
                    'total_users': total_users,
                    'total_questions': total_questions,
                    'total_answers': total_answers,
                    'active_users': active_users,
                    'questions_by_category': questions_by_category
                }
                
        except Exception as e:
            logger.error(f"Error getting community stats: {str(e)}")
            return {}
    
    def create_article(self, user_id: str, article_data: Dict[str, Any]) -> str:
        """
        Create a new knowledge article
        
        Args:
            user_id: User ID
            article_data: Dictionary containing article data
            
        Returns:
            Article ID
        """
        try:
            article_id = f"art_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO articles (
                        article_id, user_id, title, content, category, tags,
                        crop_related, difficulty_level, is_featured
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    article_id,
                    user_id,
                    article_data['title'],
                    article_data['content'],
                    article_data['category'],
                    json.dumps(article_data['tags']),
                    json.dumps(article_data['crop_related']),
                    article_data.get('difficulty_level', 'intermediate'),
                    article_data.get('is_featured', False)
                ))
                
                conn.commit()
                logger.info(f"Article created: {article_id}")
                return article_id
                
        except Exception as e:
            logger.error(f"Error creating article: {str(e)}")
            raise

# Example usage and testing
if __name__ == "__main__":
    # Initialize community knowledge platform
    community = CommunityKnowledgePlatform()
    
    # Register a sample user
    sample_user_data = {
        'username': 'farmer_rajesh',
        'full_name': 'Rajesh Kumar',
        'location': {
            'state': 'Kerala',
            'district': 'Thiruvananthapuram',
            'village': 'Vattiyoorkavu'
        },
        'farming_experience': 15,
        'crops_grown': ['Rice', 'Coconut', 'Banana'],
        'expertise_areas': ['Organic Farming', 'Pest Management', 'Soil Health'],
        'bio': 'Experienced farmer with 15 years of organic farming experience'
    }
    
    user_id = community.register_user(sample_user_data)
    print(f"Registered user: {user_id}")
    
    # Post a sample question
    sample_question_data = {
        'title': 'How to control aphids on my rice plants?',
        'content': 'I have noticed aphids on my rice plants. What are the best organic methods to control them?',
        'category': 'Pest Management',
        'tags': ['aphids', 'rice', 'organic', 'pest control'],
        'location': {
            'state': 'Kerala',
            'district': 'Thiruvananthapuram',
            'village': 'Vattiyoorkavu'
        },
        'crop_related': ['Rice'],
        'urgency': 'high'
    }
    
    question_id = community.post_question(user_id, sample_question_data)
    print(f"Posted question: {question_id}")
    
    # Get AI suggestions for the question
    print("\nCommunity Knowledge Platform - Test Results")
    print("=" * 50)
    
    suggestions = community.get_ai_suggestions(question_id)
    print(f"AI Suggestions for Question:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion['title']}")
        print(f"   Type: {suggestion['type']}")
        print(f"   Content: {suggestion['content'][:100]}...")
        if 'reliability' in suggestion:
            print(f"   Reliability: {suggestion['reliability']}")
        print()
    
    # Search for questions
    search_results = community.search_questions('pest control', 'Pest Management', 5)
    print(f"Search Results for 'pest control':")
    for i, question in enumerate(search_results, 1):
        print(f"{i}. {question.title}")
        print(f"   Category: {question.category}")
        print(f"   Views: {question.views}")
        print()
    
    # Get trending topics
    trending = community.get_trending_topics(5)
    print("Trending Topics:")
    for topic in trending:
        print(f"- {topic['topic']} ({topic['type']}): {topic['activity_count']} activities")
    
    # Get community statistics
    stats = community.get_community_stats()
    print(f"\nCommunity Statistics:")
    print(f"Total Users: {stats['total_users']}")
    print(f"Total Questions: {stats['total_questions']}")
    print(f"Total Answers: {stats['total_answers']}")
    print(f"Active Users (30 days): {stats['active_users']}")
    
    print("\nQuestions by Category:")
    for category, count in stats['questions_by_category'].items():
        print(f"  {category}: {count}")
