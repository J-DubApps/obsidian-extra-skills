#!/usr/bin/env python3
"""
Obsidian Inbox Processing Script
Busy worker-friendly batch processing for inbox organization
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import subprocess

# Paths
VAULT_ROOT = "/Users/julianwest/Obsidian/Main_Notes"
INBOX_ROOT = os.path.join(VAULT_ROOT, "1-inbox")
TAG_INDEX = os.path.join(VAULT_ROOT, "~Frequent", "00-Core-Tag-Index.md")
FOLDER_INDEX = os.path.join(VAULT_ROOT, "~Frequent", "00-Core-Folder-Index.md")

class InboxProcessor:
    def __init__(self):
        self.inbox_files = []
        self.content_patterns = {
            'braindumps': [],
            'meetings': [],
            'tasks': [],
            'people': [],
            'blog_ideas': [],
            'research': [],
            'untagged': [],
            'needs_review': []
        }

    def scan_inbox(self):
        """Scan all .md files in inbox and categorize them"""
        print(f"📂 Scanning inbox: {INBOX_ROOT}")

        # Find all .md files
        result = subprocess.run(['rg', '--files', '-g', '*.md', INBOX_ROOT],
                              capture_output=True, text=True)

        if result.returncode != 0:
            print("❌ No markdown files found in inbox")
            return

        files = result.stdout.strip().split('\n')
        self.inbox_files = [f for f in files if f.strip()]

        print(f"📄 Found {len(self.inbox_files)} markdown files")

        # Analyze each file
        for file_path in self.inbox_files:
            self._analyze_file(file_path)

        self._display_scan_results()

    def _analyze_file(self, file_path):
        """Analyze a single file for content type and tagging"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract existing tags
            tag_pattern = r'#[\w\-]+'
            existing_tags = re.findall(tag_pattern, content)

            # Get file info
            stat = os.stat(file_path)
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            age_hours = (datetime.now() - modified_time).total_seconds() / 3600

            file_info = {
                'path': file_path,
                'relative_path': os.path.relpath(file_path, VAULT_ROOT),
                'name': os.path.basename(file_path),
                'content': content,
                'tags': existing_tags,
                'size': len(content),
                'age_hours': age_hours,
                'modified': modified_time
            }

            # Categorize based on location and content
            self._categorize_file(file_info)

        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")

    def _categorize_file(self, file_info):
        """Categorize file based on location, tags, and content"""
        path = file_info['path']
        tags = file_info['tags']
        content = file_info['content'].lower()

        # Braindumps (by location or tags)
        if '/braindumps/' in path or any(tag in ['#brainstorm-braindump', '#idea'] for tag in tags):
            self.content_patterns['braindumps'].append(file_info)

        # Meeting notes
        elif '#meeting' in tags or 'meeting' in content[:200]:
            self.content_patterns['meetings'].append(file_info)

        # Task notes
        elif '#task' in tags or any(word in content for word in ['todo', 'action item', 'follow up']):
            self.content_patterns['tasks'].append(file_info)

        # Blog ideas
        elif '#blog-idea' in tags or '#blog-draft' in tags:
            self.content_patterns['blog_ideas'].append(file_info)

        # Research content
        elif any(tag in ['#research', '#reference', '#clippings'] for tag in tags) or 'http' in content:
            self.content_patterns['research'].append(file_info)

        # People mentions (simple heuristic)
        elif any(word in content for word in ['contact', 'email:', '@', 'phone']):
            self.content_patterns['people'].append(file_info)

        # Untagged files
        elif not tags:
            self.content_patterns['untagged'].append(file_info)

        # Files with only #to-review
        elif tags == ['#to-review']:
            self.content_patterns['needs_review'].append(file_info)

        # Everything else goes to needs review
        else:
            self.content_patterns['needs_review'].append(file_info)

    def _display_scan_results(self):
        """Display organized scan results with friendly visual grouping"""
        print("\n" + "="*60)
        print("📊 INBOX SCAN RESULTS")
        print("="*60)

        total_files = len(self.inbox_files)
        if total_files == 0:
            print("✨ Inbox is empty! Nothing to process.")
            return

        print(f"📁 Total files scanned: {total_files}")

        # Priority indicators
        high_priority = len(self.content_patterns['untagged'])
        quick_wins = len(self.content_patterns['braindumps']) + len(self.content_patterns['meetings'])
        needs_attention = len(self.content_patterns['needs_review'])

        print(f"\n🎯 PRIORITY OVERVIEW:")
        print(f"🔥 High Priority (untagged):     {high_priority}")
        print(f"⚡ Quick Wins (clear category): {quick_wins}")
        print(f"🤔 Needs Attention (review):    {needs_attention}")

        # Category breakdown
        print(f"\n📂 CONTENT CATEGORIES:")
        for category, files in self.content_patterns.items():
            if not files:
                continue

            count = len(files)
            icon = self._get_category_icon(category)
            print(f"{icon} {category.replace('_', ' ').title()}: {count}")

            # Show first few file names for context
            if count > 0:
                for file_info in files[:3]:  # Show first 3
                    name = file_info['name'][:50] + "..." if len(file_info['name']) > 50 else file_info['name']
                    age = self._format_age(file_info['age_hours'])
                    print(f"   • {name} ({age})")
                if count > 3:
                    print(f"   ... and {count - 3} more")
                print()

        # Suggest next actions
        self._suggest_next_actions()

    def _get_category_icon(self, category):
        """Get emoji icon for category"""
        icons = {
            'braindumps': '🧠',
            'meetings': '🤝',
            'tasks': '✅',
            'people': '👥',
            'blog_ideas': '✍️',
            'research': '🔍',
            'untagged': '🏷️',
            'needs_review': '👀'
        }
        return icons.get(category, '📄')

    def _format_age(self, age_hours):
        """Format file age in human-readable format"""
        if age_hours < 1:
            return "< 1 hour"
        elif age_hours < 24:
            return f"{int(age_hours)}h"
        else:
            days = int(age_hours / 24)
            return f"{days}d"

    def _suggest_next_actions(self):
        """Suggest next processing actions based on scan results"""
        print("\n💡 SUGGESTED NEXT ACTIONS:")

        if self.content_patterns['untagged']:
            print("1. 🔥 Start with untagged files - add #to-review or proper tags")
            print("   Command: obsidian-inbox-processing analyze untagged")

        if self.content_patterns['braindumps']:
            print("2. 🧠 Process braindumps for blog ideas and projects")
            print("   Command: obsidian-inbox-processing analyze braindumps")

        if self.content_patterns['meetings']:
            print("3. 🤝 Format and move meeting notes")
            print("   Command: obsidian-inbox-processing analyze meetings")

        if self.content_patterns['tasks']:
            print("4. ✅ Review task notes and add Daily Note backlinks")
            print("   Command: obsidian-inbox-processing analyze tasks")

        print("\n📋 Or process in small batches:")
        print("   obsidian-inbox-processing suggest --batch-size 5")

def main():
    if len(sys.argv) < 2:
        print("Usage: python inbox_processor.py <command> [args]")
        print("Commands: scan, analyze, suggest")
        sys.exit(1)

    command = sys.argv[1]
    processor = InboxProcessor()

    if command == 'scan':
        processor.scan_inbox()
    elif command == 'analyze':
        if len(sys.argv) < 3:
            print("Usage: python inbox_processor.py analyze <category>")
            print("Categories: braindumps, meetings, tasks, people, research")
            sys.exit(1)

        category = sys.argv[2]
        if category == 'braindumps':
            # Import and run braindump analyzer
            from braindump_analyzer import BraindumpAnalyzer
            analyzer = BraindumpAnalyzer()
            analyzer.analyze_braindumps()
        else:
            print(f"Analysis for '{category}' not yet implemented")
    else:
        print(f"Command '{command}' not yet implemented")

if __name__ == '__main__':
    main()