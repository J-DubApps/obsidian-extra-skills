---
name: obsidian-inbox-processing
description: Busy distracted person-friendly batch processing for inbox organization. Analyzes content patterns, suggests tagging and folder placement based on established taxonomy, respects Forever Notes system. Handles braindumps, meeting notes, tasks, people, and research content with visual grouping and smart recommendations.
argument-hint: [scan|analyze|process|suggest|move-batch|review-tags]
allowed-tools: Bash(obsidian-cli:*), Bash(rg:*), Bash(sed:*), Read, Write
---

# Obsidian Inbox Processing

Comprehensive Distracted-focus friendly toolkit for processing and organizing notes from the `/1-inbox/*` folder structure. Uses established taxonomy and respects the Forever Notes system while providing smart, batch-oriented suggestions.

## What It Does

### 🔍 **Content Analysis & Pattern Recognition**

- Scans all `.md` files in `/1-inbox/*` and subfolders
- Identifies content patterns: braindumps, meeting notes, people mentions, tasks, ideas, research
- Analyzes existing tags and suggests improvements based on `00-Core-Tag-Index.md`
- Detects missing tags and recommends appropriate folder placement

### 📊 **Friendly Visual Grouping**

- Groups similar content types for batch processing
- Provides visual summaries with counts and priorities
- Shows "quick wins" vs "needs attention" categories
- Presents actionable suggestions in digestible chunks

### 🏷️ **Smart Tagging Workflow**

- Cross-references content with established tag taxonomy
- Suggests tag additions/replacements for consistency
- Handles complex scenarios: multiple tags, tag hierarchies, duplicates
- Respects existing manual tagging choices

### 📁 **Folder Placement Intelligence**

- Uses `00-Core-Folder-Index.md` rules for destination suggestions
- Handles special cases: braindumps → analysis, meetings → ~Meetings, blog ideas → Blog-Draft-Pipeline
- Preserves inbox subfolders for ongoing workflow support
- Creates backlinks to Daily Notes for task creation tracking

## Core Operations

### `obsidian-inbox-processing scan`

Quick overview of current inbox state - counts, content types, and priority items.

### `obsidian-inbox-processing analyze [CATEGORY]`

Deep analysis of specific content categories:

- `braindumps` - Process braindump content for blog ideas, projects, people mentions
- `meetings` - Format and suggest placement for meeting notes
- `tasks` - Identify actionable items and kanban candidates
- `people` - Extract contact/people references for proper categorization
- `research` - Categorize research content and suggest reference placement

### `obsidian-inbox-processing suggest [--batch-size N]`

Generate organized suggestions for processing with configurable batch sizes (default: 10).

### `obsidian-inbox-processing process-batch [GROUP_ID]`

Execute suggested changes for a specific batch group after user confirmation.

### `obsidian-inbox-processing review-tags [FOLDER_PATH]`

Review and suggest tag improvements for notes that have already been moved from inbox.

## Content Processing Matrix

### Braindump Notes (`#brainstorm-braindump`, `#idea`)

- **Current Location**: Already in `/1-inbox/braindumps/`
- **Action**: Analyze content → suggest analysis file creation in `/1-inbox/braindumps/analysis/`
- **Tagging**: Add secondary tags based on content (`#blog-idea`, `#project`, `#research`)

### Meeting Notes (`#meeting` or contains "meeting" in title)

- **Target**: `/~Meetings/`
- **Naming**: `meeting-SUBJECT-MM-DD-YYYY.md`
- **Processing**: Extract attendees, action items, follow-ups

### Task Notes (`#task`, contains action words)

- **Target**: Stay in `/1-inbox/` with proper tags
- **Tagging**: Add `#task` + relevant domain tags
- **Backlinks**: Link to today's Daily Note for creation tracking
- **Kanban**: Suggest `#kanban-backlog-groom` if project-related

### People Notes (names, contact info, roles)

- **Target**: `/References/People/` or `/References/contacts/`
- **Tagging**: `#people` or `#contact` based on relationship level
- **Processing**: Extract role, relevance, connection context

### Blog Ideas (`#blog-idea`, creative content)

- **Target**: `/Blog-Draft-Pipeline/1_Raw/`
- **Tagging**: Preserve `#blog-idea`, add topic-specific tags

### Research Content (links, findings, analysis)

- **Target**: `/Research/` or `/Resources/` based on content type
- **Tagging**: Add `#research` + domain tags, consider `#reference` vs `#resource`

### General Notes (catch-all)

- **Default**: Add `#to-review` if untagged, suggest appropriate folders
- **Processing**: Content analysis for proper categorization

## Distracted Worker-Friendly Features

### Batch Processing Options

- **Small batches** (5-10 items): Quick wins, low cognitive load
- **Medium batches** (10-20 items): Focused processing sessions
- **Single-category batches**: Process only braindumps, or only meetings, etc.

### Visual Priority Indicators

- 🔥 **High Priority**: Untagged notes, old items, action-required content
- ⚡ **Quick Wins**: Clear categorization, obvious destinations
- 🤔 **Needs Attention**: Ambiguous content, complex decisions required
- ✅ **Ready to Move**: Properly tagged, clear destinations

### Gentle Guidance

- Suggests rather than auto-executes moves
- Preserves manual choices and existing organization
- Provides context for recommendations
- Allows selective acceptance of suggestions

## Protected Areas & Rules

### Never Modify

- `✱ MAIN/*` - Forever Notes hub system
- `Daily-Journal-Notes/*` - Pre-created journal structure
- Any note with `#confidential` tag

### Respect Existing Structure

- Don't move items between `/1-inbox/` subfolders without explicit instruction
- Preserve manual tagging choices unless obviously incorrect
- Maintain existing backlinks and references

### Smart Defaults

- Add `#to-review` to any note without tags that's been in inbox > 1 hour
- Create Daily Note backlinks for task notes
- Suggest blog pipeline for creative content
- Route technical content to appropriate Resources subfolders

## Integration Points

### Leverages Existing Skills

- **obsidian-cli**: Discovery, validation, obsidian:// URI operations
- **obsidian-tag-curation**: Advanced tagging operations when needed
- **qmd**: Semantic search for related content when processing

### Works With Your Systems

- **00-Core-Tag-Index.md**: Primary tagging authority
- **00-Core-Folder-Index.md**: Destination placement rules
- **Blog workflow**: Integrates with existing blog pipeline
- **Kanban workflow**: Suggests kanban integration for tasks
- **Forever Notes**: Respects hub/collection relationships

## Usage Examples

```bash
# Quick inbox overview
obsidian-inbox-processing scan

# Deep-dive into braindumps
obsidian-inbox-processing analyze braindumps

# Get organized suggestions for next 10 items
obsidian-inbox-processing suggest --batch-size 10

# Process a specific batch after review
obsidian-inbox-processing process-batch group-2

# Review tagging in moved content
obsidian-inbox-processing review-tags /References/People/
```

## Advanced Features

### Smart Duplicate Detection

- Identifies similar content across inbox and existing notes
- Suggests consolidation or cross-referencing
- Warns about potential duplicates before processing

### Content Enhancement

- Suggests missing metadata (creation dates, sources)
- Identifies opportunities for additional tags
- Recommends backlink creation for better knowledge graph

### Workflow Integration

- Tracks processing statistics for reflection
- Suggests optimal batch sizes based on processing patterns
- Integrates with weekly/daily review workflows

## Error Handling & Recovery

### Validation Checkpoints

- Confirms destination folders exist and are writable
- Validates tag syntax and taxonomy compliance
- Checks for existing files before moves

### Rollback Support

- Logs all changes made during processing
- Provides undo recommendations for recent changes
- Maintains processing history for learning

### Safe Processing

- Always suggests before executing
- Handles locked files and permission issues gracefully
- Preserves original content during tag/folder operations

---

_Built on the proven success of obsidian-tag-curation with real-world testing and useful design principles._
