#!/usr/bin/env python3
"""
Braindump Analysis Module
Analyzes braindump content for blog ideas, projects, people mentions, and actionable items
"""

import os
import re
from datetime import datetime

class BraindumpAnalyzer:
    def __init__(self, vault_root="/Users/julianwest/Obsidian/Main_Notes"):
        self.vault_root = vault_root
        self.braindumps_folder = os.path.join(vault_root, "1-inbox", "braindumps")
        self.analysis_folder = os.path.join(self.braindumps_folder, "analysis")

    def analyze_braindumps(self):
        """Analyze all braindump files and suggest processing"""
        print("🧠 ANALYZING BRAINDUMP CONTENT")
        print("=" * 50)

        braindump_files = self._find_braindump_files()
        if not braindump_files:
            print("📭 No braindump files found.")
            return

        print(f"📄 Found {len(braindump_files)} braindump files")
        print()

        for file_path in braindump_files:
            self._analyze_single_braindump(file_path)

        self._suggest_analysis_creation(braindump_files)

    def _find_braindump_files(self):
        """Find all braindump .md files"""
        braindump_files = []
        try:
            for file in os.listdir(self.braindumps_folder):
                if file.endswith('.md'):
                    full_path = os.path.join(self.braindumps_folder, file)
                    if os.path.isfile(full_path):
                        braindump_files.append(full_path)
        except FileNotFoundError:
            print(f"⚠️  Braindumps folder not found: {self.braindumps_folder}")

        return sorted(braindump_files)

    def _analyze_single_braindump(self, file_path):
        """Analyze a single braindump file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            filename = os.path.basename(file_path)
            print(f"📝 **{filename}**")

            # Extract existing tags
            existing_tags = re.findall(r'#[\w\-]+', content)
            print(f"   🏷️  Current tags: {', '.join(existing_tags) if existing_tags else 'None'}")

            # Analyze content patterns
            analysis = self._extract_content_patterns(content)

            # Display analysis
            if analysis['blog_potential']:
                print("   ✍️  **Blog Potential**: High")
                for idea in analysis['blog_ideas'][:3]:
                    print(f"      • {idea}")

            if analysis['project_mentions']:
                print("   🎯 **Project Ideas**: Found")
                for project in analysis['project_mentions'][:2]:
                    print(f"      • {project}")

            if analysis['people_mentions']:
                print("   👥 **People Referenced**: Found")
                for person in analysis['people_mentions'][:2]:
                    print(f"      • {person}")

            if analysis['actionable_items']:
                print("   ✅ **Action Items**: Found")
                for action in analysis['actionable_items'][:2]:
                    print(f"      • {action}")

            # Suggest additional tags
            suggested_tags = self._suggest_tags(analysis, existing_tags)
            if suggested_tags:
                print(f"   🔧 **Suggested tags**: {', '.join(suggested_tags)}")

            # Suggest destination
            destination = self._suggest_destination(analysis)
            if destination:
                print(f"   📁 **Suggested destination**: {destination}")

            print()

        except Exception as e:
            print(f"⚠️  Error analyzing {file_path}: {e}")

    def _extract_content_patterns(self, content):
        """Extract patterns from braindump content"""
        content_lower = content.lower()
        lines = content.split('\n')

        analysis = {
            'blog_potential': False,
            'blog_ideas': [],
            'project_mentions': [],
            'people_mentions': [],
            'actionable_items': [],
            'tech_content': False,
            'business_content': False
        }

        # Blog potential indicators
        blog_indicators = ['blog', 'post', 'article', 'write about', 'content idea']
        if any(indicator in content_lower for indicator in blog_indicators):
            analysis['blog_potential'] = True

        # Extract bullet points and ideas as potential blog topics
        for line in lines:
            line = line.strip()
            if line.startswith(('- ', '• ', '* ')) and len(line) > 10:
                analysis['blog_ideas'].append(line[2:].strip()[:80])

        # Project mentions
        project_indicators = ['project', 'build', 'create', 'develop', 'implement']
        for line in lines:
            if any(indicator in line.lower() for indicator in project_indicators):
                if len(line.strip()) > 15:
                    analysis['project_mentions'].append(line.strip()[:80])

        # People mentions (simple detection)
        people_patterns = [r'@\w+', r'[A-Z][a-z]+ [A-Z][a-z]+']
        for pattern in people_patterns:
            matches = re.findall(pattern, content)
            analysis['people_mentions'].extend(matches[:5])

        # Actionable items
        action_patterns = [r'need to \w+', r'should \w+', r'todo:', r'action:', r'follow.?up']
        for pattern in action_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            analysis['actionable_items'].extend([m[:60] for m in matches])

        # Content type detection
        tech_keywords = ['obsidian', 'skill', 'claude', 'api', 'code', 'technical', 'development']
        business_keywords = ['business', 'consulting', 'client', 'revenue', 'marketing']

        if any(keyword in content_lower for keyword in tech_keywords):
            analysis['tech_content'] = True

        if any(keyword in content_lower for keyword in business_keywords):
            analysis['business_content'] = True

        return analysis

    def _suggest_tags(self, analysis, existing_tags):
        """Suggest additional tags based on content analysis"""
        suggestions = []
        existing_tags_lower = [tag.lower() for tag in existing_tags]

        if analysis['blog_potential'] and '#blog-idea' not in existing_tags_lower:
            suggestions.append('#blog-idea')

        if analysis['project_mentions'] and '#project' not in existing_tags_lower:
            suggestions.append('#project')

        if analysis['people_mentions'] and '#people' not in existing_tags_lower:
            suggestions.append('#people')

        if analysis['actionable_items'] and '#task' not in existing_tags_lower:
            suggestions.append('#task')

        if analysis['tech_content'] and '#tech-kb' not in existing_tags_lower:
            suggestions.append('#tech-kb')

        if analysis['business_content'] and '#business' not in existing_tags_lower:
            suggestions.append('#business')

        return suggestions

    def _suggest_destination(self, analysis):
        """Suggest processing destination based on content"""
        if analysis['blog_potential']:
            return "Blog-Draft-Pipeline/1_Raw/"
        elif analysis['project_mentions']:
            return "Projects/ (create project folder)"
        elif analysis['people_mentions']:
            return "References/People/ (extract contact info)"
        else:
            return "Create analysis note for review"

    def _suggest_analysis_creation(self, braindump_files):
        """Suggest creating analysis files"""
        print("💡 SUGGESTED NEXT ACTIONS:")
        print("-" * 30)

        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M")
        analysis_filename = f"braindump-analysis-{timestamp}.md"
        analysis_path = os.path.join(self.analysis_folder, analysis_filename)

        print(f"1. 📝 Create analysis file: `{analysis_filename}`")
        print(f"   Location: 1-inbox/braindumps/analysis/")
        print(f"   Consolidates insights from {len(braindump_files)} braindumps")
        print()

        print("2. 🔧 Apply suggested tags to braindump files")
        print("3. 📁 Move high-value content to suggested destinations")
        print("4. ✅ Extract action items to task notes")
        print()

        print("🎯 **Processing Priority:**")
        print("   • Blog ideas → Blog-Draft-Pipeline")
        print("   • Project concepts → Projects folder")
        print("   • People references → References/People")
        print("   • Action items → Task notes with Daily Note backlinks")

if __name__ == '__main__':
    analyzer = BraindumpAnalyzer()
    analyzer.analyze_braindumps()