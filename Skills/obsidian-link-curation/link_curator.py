#!/usr/bin/env python3
"""
Obsidian Link Curation Script
Intelligent wikilink management that respects Forever Notes system
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from collections import defaultdict

# Paths
VAULT_ROOT = "/Users/julianwest/Obsidian/Main_Notes"

# Protected areas (NEVER modify)
PROTECTED_ZONES = [
    "✱ MAIN",
    "Daily-Journal-Notes"
]

# Focus areas for curation
FOCUS_AREAS = [
    "1-inbox",
    "2-agentworkfolder",
    "Resources",
    "Areas",
    "Blog-Draft-Pipeline",
    "Blog-Hugo-CMS",
    "Blog-Posts"
]

class LinkCurator:
    def __init__(self):
        self.vault_root = VAULT_ROOT
        self.all_notes = []
        self.focus_notes = []
        self.protected_notes = []
        self.broken_links = []
        self.orphaned_notes = []
        self.potential_connections = []

    def scan_vault(self):
        """Scan vault for link health and connection opportunities"""
        print("🔗 OBSIDIAN LINK CURATION SCAN")
        print("=" * 50)
        print("🛡️  Respecting Forever Notes system and protected areas")
        print()

        # Discover all notes
        self._discover_notes()

        # Analyze link health
        self._analyze_link_health()

        # Find connection opportunities
        self._find_connection_opportunities()

        # Display results
        self._display_scan_results()

    def _discover_notes(self):
        """Discover all notes and categorize by protection level"""
        print("📂 Discovering notes...")

        # Find all .md files
        result = subprocess.run(['rg', '--files', '-g', '*.md', self.vault_root],
                              capture_output=True, text=True)

        if result.returncode != 0:
            print("❌ No markdown files found")
            return

        all_files = result.stdout.strip().split('\n')
        all_files = [f for f in all_files if f.strip()]

        # Categorize notes
        for file_path in all_files:
            relative_path = os.path.relpath(file_path, self.vault_root)

            # Check if in protected zone
            is_protected = any(protected in relative_path for protected in PROTECTED_ZONES)

            # Check if in focus area
            is_focus = any(focus in relative_path for focus in FOCUS_AREAS)

            note_info = {
                'path': file_path,
                'relative_path': relative_path,
                'name': os.path.basename(file_path),
                'is_protected': is_protected,
                'is_focus': is_focus
            }

            self.all_notes.append(note_info)

            if is_protected:
                self.protected_notes.append(note_info)
            elif is_focus:
                self.focus_notes.append(note_info)

        print(f"   📄 Total notes: {len(self.all_notes)}")
        print(f"   🛡️  Protected notes: {len(self.protected_notes)}")
        print(f"   🎯 Focus area notes: {len(self.focus_notes)}")

    def _analyze_link_health(self):
        """Analyze link health in focus areas"""
        print("\n🔍 Analyzing link health...")

        broken_count = 0
        orphan_count = 0

        # Check links in focus area notes only
        for note_info in self.focus_notes:
            try:
                with open(note_info['path'], 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find all wikilinks
                links = re.findall(r'\[\[([^\]]+)\]\]', content)

                # Check for broken links
                broken_in_file = []
                for link in links:
                    # Simple broken link detection
                    # Extract just the note name (before | or #)
                    link_target = link.split('|')[0].split('#')[0]

                    # Check if target exists
                    target_exists = any(
                        link_target.lower() in note['name'].lower() or
                        link_target.lower() in note['relative_path'].lower()
                        for note in self.all_notes
                    )

                    if not target_exists:
                        broken_in_file.append(link)

                if broken_in_file:
                    self.broken_links.append({
                        'note': note_info,
                        'broken_links': broken_in_file
                    })
                    broken_count += len(broken_in_file)

                # Check for orphaned notes (no incoming or outgoing links)
                if not links:  # No outgoing links
                    # TODO: Check if no incoming links (would need to scan all notes)
                    # For now, mark as potentially orphaned
                    if len(content.strip()) > 100:  # Only meaningful content
                        self.orphaned_notes.append(note_info)
                        orphan_count += 1

            except Exception as e:
                print(f"⚠️  Error reading {note_info['path']}: {e}")

        print(f"   💔 Broken links found: {broken_count}")
        print(f"   🏝️  Potentially orphaned notes: {orphan_count}")

    def _find_connection_opportunities(self):
        """Find opportunities to connect content to Forever Notes"""
        print("\n🎯 Finding connection opportunities...")

        # Look for content that could connect to Forever Notes
        forever_notes = [note for note in self.protected_notes if "✱ MAIN" in note['relative_path']]

        connection_count = 0

        # Simple keyword-based connection suggestions
        for focus_note in self.focus_notes[:10]:  # Limit for demo
            try:
                with open(focus_note['path'], 'r', encoding='utf-8') as f:
                    content = f.read().lower()

                # Look for keywords that suggest connections to Forever Notes
                career_keywords = ['sccm', 'azure', 'powershell', 'tech', 'it', 'career', 'certification']
                business_keywords = ['consulting', 'client', 'business', 'revenue', 'project']

                suggested_connections = []

                if any(keyword in content for keyword in career_keywords):
                    suggested_connections.append("✱ Career 👨🏻‍💻")

                if any(keyword in content for keyword in business_keywords):
                    suggested_connections.append("✱ Business ventures")

                if suggested_connections:
                    self.potential_connections.append({
                        'note': focus_note,
                        'suggested_targets': suggested_connections,
                        'reasoning': 'Content keywords suggest thematic connection'
                    })
                    connection_count += 1

            except Exception as e:
                continue

        print(f"   🔗 Connection opportunities found: {connection_count}")

    def _display_scan_results(self):
        """Display organized scan results"""
        print("\n" + "="*60)
        print("📊 LINK CURATION SCAN RESULTS")
        print("="*60)

        # Vault overview
        print(f"📁 Vault Overview:")
        print(f"   Total notes: {len(self.all_notes)}")
        print(f"   Protected (Forever Notes): {len(self.protected_notes)}")
        print(f"   Focus areas: {len(self.focus_notes)}")
        print()

        # Link health summary
        broken_count = sum(len(item['broken_links']) for item in self.broken_links)
        print(f"🏥 Link Health:")
        print(f"   💔 Broken links: {broken_count}")
        print(f"   🏝️  Orphaned notes: {len(self.orphaned_notes)}")
        print(f"   🎯 Connection opportunities: {len(self.potential_connections)}")
        print()

        # Show some examples
        if self.broken_links:
            print("💔 BROKEN LINKS (sample):")
            for item in self.broken_links[:3]:
                note_name = item['note']['name'][:50] + "..." if len(item['note']['name']) > 50 else item['note']['name']
                print(f"   📄 {note_name}")
                for link in item['broken_links'][:2]:
                    print(f"      💔 [[{link}]]")
                print()

        if self.potential_connections:
            print("🔗 CONNECTION OPPORTUNITIES (sample):")
            for item in self.potential_connections[:3]:
                note_name = item['note']['name'][:50] + "..." if len(item['note']['name']) > 50 else item['note']['name']
                print(f"   📄 {note_name}")
                print(f"      → Suggest linking to: {', '.join(item['suggested_targets'])}")
                print(f"      💡 {item['reasoning']}")
                print()

        if self.orphaned_notes:
            print("🏝️  ORPHANED NOTES (sample):")
            for note in self.orphaned_notes[:3]:
                note_name = note['name'][:50] + "..." if len(note['name']) > 50 else note['name']
                print(f"   📄 {note_name}")
                print(f"      📁 {note['relative_path']}")
            print()

        # Suggested next actions
        self._suggest_next_actions()

    def _suggest_next_actions(self):
        """Suggest next curation actions"""
        print("💡 SUGGESTED NEXT ACTIONS:")
        print("-" * 30)

        if self.broken_links:
            print("1. 🔧 Fix broken links in focus areas")
            print("   Command: obsidian-link-curation fix-broken --dry-run")

        if self.potential_connections:
            print("2. 🎯 Review connection opportunities")
            print("   Command: obsidian-link-curation suggest-connections")

        if self.orphaned_notes:
            print("3. 🏝️  Integrate orphaned content")
            print("   Command: obsidian-link-curation orphan-check")

        print("\n📋 Or analyze specific areas:")
        print("   obsidian-link-curation analyze inbox")
        print("   obsidian-link-curation analyze resources")
        print("   obsidian-link-curation analyze areas")
        print()

        print("🛡️  PROTECTED AREAS RESPECTED:")
        print("   ✱ MAIN/* - Forever Notes (read-only)")
        print("   Daily-Journal-Notes/* - Journal system (read-only)")
        print("   All suggestions will connect TO these systems, never modify them")

def main():
    if len(sys.argv) < 2:
        print("Usage: python link_curator.py <command> [args]")
        print("Commands: scan, analyze, fix-broken, suggest-connections, orphan-check")
        sys.exit(1)

    command = sys.argv[1]
    curator = LinkCurator()

    if command == 'scan':
        curator.scan_vault()
    else:
        print(f"Command '{command}' not yet implemented")

if __name__ == '__main__':
    main()