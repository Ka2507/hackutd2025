"""
Context Store - Caches conversations and project memory.

SQLite-based storage for conversation history and agent context.
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import logger


class ContextStore:
    """Manages persistent storage of conversations and project context."""
    
    def __init__(self, db_path: str = "db/context.db"):
        """
        Initialize context store with SQLite database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema with all required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    agent_name TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    input_data TEXT,
                    output_data TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS context_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            """)
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    def create_project(self, name: str, description: str = "") -> int:
        """
        Create a new project.
        
        Args:
            name: Project name
            description: Project description
            
        Returns:
            Project ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO projects (name, description) VALUES (?, ?)",
                (name, description)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_project(self, project_id: int) -> Optional[Dict]:
        """
        Get project by ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project data dictionary or None
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM projects WHERE id = ?",
                (project_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def list_projects(self) -> List[Dict]:
        """
        List all projects.
        
        Returns:
            List of project dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM projects ORDER BY updated_at DESC"
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def add_conversation(
        self,
        project_id: int,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Add a conversation message.
        
        Args:
            project_id: Project ID
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata dictionary
            
        Returns:
            Message ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO conversations "
                "(project_id, role, content, metadata) "
                "VALUES (?, ?, ?, ?)",
                (
                    project_id,
                    role,
                    content,
                    json.dumps(metadata) if metadata else None
                )
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_conversation_history(
        self,
        project_id: int,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get conversation history for a project.
        
        Args:
            project_id: Project ID
            limit: Maximum number of messages to return
            
        Returns:
            List of conversation message dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM conversations "
                "WHERE project_id = ? "
                "ORDER BY created_at DESC "
                "LIMIT ?",
                (project_id, limit)
            )
            rows = cursor.fetchall()
            conversations = []
            for row in rows:
                conv = dict(row)
                if conv['metadata']:
                    conv['metadata'] = json.loads(conv['metadata'])
                conversations.append(conv)
            return list(reversed(conversations))
    
    def create_agent_task(
        self,
        project_id: int,
        agent_name: str,
        task_type: str,
        input_data: Dict
    ) -> int:
        """
        Create a new agent task.
        
        Args:
            project_id: Project ID
            agent_name: Name of the agent
            task_type: Type of task
            input_data: Task input data
            
        Returns:
            Task ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO agent_tasks "
                "(project_id, agent_name, task_type, "
                "input_data, status) "
                "VALUES (?, ?, ?, ?, 'pending')",
                (
                    project_id,
                    agent_name,
                    task_type,
                    json.dumps(input_data)
                )
            )
            conn.commit()
            return cursor.lastrowid
    
    def update_agent_task(
        self,
        task_id: int,
        status: str,
        output_data: Optional[Dict] = None
    ):
        """
        Update agent task status and output.
        
        Args:
            task_id: Task ID
            status: New status
            output_data: Optional output data
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if status == 'completed':
                cursor.execute(
                    "UPDATE agent_tasks "
                    "SET status = ?, output_data = ?, "
                    "completed_at = CURRENT_TIMESTAMP "
                    "WHERE id = ?",
                    (
                        status,
                        json.dumps(output_data) if output_data else None,
                        task_id
                    )
                )
            else:
                cursor.execute(
                    "UPDATE agent_tasks "
                    "SET status = ?, output_data = ? "
                    "WHERE id = ?",
                    (
                        status,
                        json.dumps(output_data) if output_data else None,
                        task_id
                    )
                )
            conn.commit()
    
    def get_agent_tasks(
        self,
        project_id: int,
        limit: int = 20
    ) -> List[Dict]:
        """
        Get agent tasks for a project.
        
        Args:
            project_id: Project ID
            limit: Maximum number of tasks to return
            
        Returns:
            List of task dictionaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM agent_tasks "
                "WHERE project_id = ? "
                "ORDER BY created_at DESC "
                "LIMIT ?",
                (project_id, limit)
            )
            rows = cursor.fetchall()
            tasks = []
            for row in rows:
                task = dict(row)
                if task['input_data']:
                    task['input_data'] = json.loads(task['input_data'])
                if task['output_data']:
                    task['output_data'] = json.loads(task['output_data'])
                tasks.append(task)
            return tasks
    
    def store_context(self, project_id: int, key: str, value: Any):
        """
        Store a context value.
        
        Args:
            project_id: Project ID
            key: Context key
            value: Context value (will be JSON serialized)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO context_memory "
                "(project_id, key, value) "
                "VALUES (?, ?, ?)",
                (project_id, key, json.dumps(value))
            )
            conn.commit()
    
    def get_context(self, project_id: int, key: str) -> Optional[Any]:
        """
        Get a context value.
        
        Args:
            project_id: Project ID
            key: Context key
            
        Returns:
            Context value or None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT value FROM context_memory "
                "WHERE project_id = ? AND key = ? "
                "ORDER BY created_at DESC "
                "LIMIT 1",
                (project_id, key)
            )
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None
    
    def get_all_context(self, project_id: int) -> Dict:
        """
        Get all context for a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            Dictionary of all context key-value pairs
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT key, value FROM context_memory "
                "WHERE project_id = ? "
                "ORDER BY created_at DESC",
                (project_id,)
            )
            rows = cursor.fetchall()
            context = {}
            for key, value in rows:
                if key not in context:
                    context[key] = json.loads(value)
            return context


context_store = ContextStore()
