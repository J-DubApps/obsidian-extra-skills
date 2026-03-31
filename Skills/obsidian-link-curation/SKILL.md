---
name: obsidian-link-curation
description: Intelligent wikilink optimization that respects Forever Notes system. Focuses on connecting new content to established systems, fixing broken links in non-protected areas, consolidating duplicate references, and suggesting strategic backlinks without modifying protected zones.
argument-hint:
  [
    scan|analyze|suggest-connections|fix-broken|consolidate-duplicates|orphan-check,
  ]
allowed-tools: Bash(obsidian-cli:*), Bash(rg:*), Read, Write
---

# Obsidian Link Curation

Intelligent wikilink management that **respects your established Forever Notes system** while optimizing connections in areas that benefit from curation. Built with deep understanding of your vault's protected zones and established workflows.

## What It Does

### 🛡️ **Protected Zone Awareness**

- **Never modifies**: `✱ MAIN/*`, `/Daily-Journal-Notes/*`, notes with `#system` or `#established` tags
- **Respects READ-ONLY patterns** from CLAUDE.md
- **Suggests connections TO Forever Notes** without altering them
- **Preserves manual organizational choices** in established areas

### 🔍 **Smart Link Analysis**

- Scans focus areas: `/1-inbox/*`, `/2-agentworkfolder/*`, `/Resources/*`, `/Areas/*`, `/Blog-*` folders
- Identifies orphaned content that should connect to your established system
- Detects broken links from non-protected areas pointing to moved/renamed notes
- Finds duplicate references (e.g., `[[SCCM]]` and `[[Configuration Manager]]` for same concept)

### 🎯 **Strategic Connection Suggestions**

- **Inbound linking**: New content → Forever Notes connections
- **Cross-referencing**: Related content in Resources/Areas that should link together
- **Consolidation**: Duplicate references pointing to canonical notes
- **Integration**: Claude-generated content → established knowledge graph

## Core Operations

### `obsidian-link-curation scan`

Overview of linking health across focus areas - broken links, orphaned content, connection opportunities.

### `obsidian-link-curation analyze [AREA]`

Deep analysis of specific areas:

- `inbox` - New content needing integration into established systems
- `resources` - Reference material that could benefit from better cross-linking
- `areas` - Areas of responsibility content that should connect to Forever Notes
- `blog` - Content heading toward publication that needs strategic linking
- `agent-work` - Claude-generated content needing knowledge graph integration

### `obsidian-link-curation suggest-connections [--focus PATTERN]`

Generate strategic linking suggestions with optional focus patterns (e.g., `--focus "SCCM"` for infrastructure content).

### `obsidian-link-curation fix-broken [--dry-run]`

Find and suggest fixes for broken links from non-protected areas. Uses `--dry-run` to preview changes.

### `obsidian-link-curation consolidate-duplicates`

Identify and suggest consolidation of duplicate references pointing to the same concepts.

### `obsidian-link-curation orphan-check`

Find content that exists in isolation and should be connected to your established knowledge systems.

## Curation Focus Matrix

### New Content Integration (`/1-inbox/*`)

- **Goal**: Connect new notes to relevant Forever Notes and established systems
- **Method**: Content analysis → suggest backlinks to `✱ MAIN/*` notes
- **Safety**: Only suggest additions, never modify inbox organization
- **Priority**: High-value connections that strengthen knowledge graph

### Reference Material (`/Resources/*`)

- **Goal**: Improve cross-referencing between related technical/reference content
- **Method**: Detect similar topics, suggest bidirectional linking
- **Example**: Link SCCM notes to Azure notes when both mention endpoint management
- **Safety**: Respects existing folder organization, suggests link additions only

### Areas of Responsibility (`/Areas/*`)

- **Goal**: Connect ongoing work to relevant Forever Notes and Resources
- **Method**: Identify project/responsibility overlap with established knowledge
- **Integration**: Suggest connections to relevant `✱ MAIN/*` hub notes
- **Workflow**: Preserve existing project structure

### Blog Content (`/Blog-*` folders)

- **Goal**: Strategic linking for SEO and knowledge demonstration
- **Method**: Connect blog content to supporting Resources and established knowledge
- **Publication Ready**: Ensure proper internal linking before publication
- **Forever Notes**: Link blog topics back to personal knowledge hubs

### Agent Work Integration (`/2-agentworkfolder/*`)

- **Goal**: Connect Claude-generated content into established knowledge systems
- **Method**: Analyze content themes → suggest integration points
- **Examples**: Link skill documentation to relevant Forever Notes, connect analysis to source material
- **Workflow**: Bridge generated content with existing vault organization

## Protected Zone Respect

### Forever Notes System (`✱ MAIN/*`)

- **NEVER EDIT**: Hub notes, Collections, established links
- **DO SUGGEST**: New content that should link TO these notes
- **PRESERVE**: All existing link structures and manual curation choices
- **ENHANCE**: Strengthen the system by connecting relevant new content

### Daily Journal System (`/Daily-Journal-Notes/*`)

- **NEVER MODIFY**: Pre-created journal structure and existing entries
- **DO RESPECT**: Established daily/monthly/quarterly linking patterns
- **PRESERVE**: All manual journal entries and reflective content
- **SUPPORT**: Suggest relevant content connections only when explicitly beneficial

### Established Notes

- **DETECTION**: Notes with `#system`, `#established`, `#confidential` tags
- **READ-ONLY**: Content matching CLAUDE.md protection patterns
- **PRESERVATION**: All manual organizational decisions in these areas
- **RESPECT**: Existing linking patterns and established workflows

## Smart Link Operations

### Broken Link Detection & Repair

```bash
# Find broken links from non-protected areas
rg '\[\[([^\]]+)\]\]' --files-with-matches /non-protected-areas/
# Cross-reference against existing note names
# Suggest corrections for moved/renamed targets
```

### Duplicate Reference Consolidation

```bash
# Example: Multiple ways to reference same concept
[[SCCM]] → [[Configuration Manager SCCM]]
[[Config Manager]] → [[Configuration Manager SCCM]]
[[Microsoft SCCM]] → [[Configuration Manager SCCM]]
```

### Orphan Detection & Integration

- **Orphans**: Notes with no incoming links and minimal outgoing links
- **Integration**: Suggest connections to relevant Forever Notes or Resources
- **Contextualization**: Connect isolated content to broader knowledge themes

### Strategic Backlinking

- **Pattern**: New technical content → relevant `✱ MAIN/*` hub notes
- **Example**: New SCCM troubleshooting note → `[[✱ Career 👨🏻‍💻]]` or relevant tech hub
- **Bidirectional**: Suggest both directions when mutually beneficial

## Workflow Integration

### Leverages Existing Skills

- **obsidian-cli**: Discovery, validation, structural analysis
- **obsidian-tag-curation**: Tag-based linking suggestions
- **qmd**: Semantic similarity for connection recommendations

### Works With Your Systems

- **00-Core-Folder-Index.md**: Respects established folder purposes
- **00-Core-Tag-Index.md**: Uses tags to inform linking decisions
- **Forever Notes**: Strengthens hub-and-spoke architecture
- **Inbox Processing**: Coordinates with content organization workflow

## Advanced Features

### Semantic Connection Discovery

- **Content Analysis**: Similar topics across different folders
- **Theme Detection**: Related concepts that should be cross-linked
- **Knowledge Gaps**: Missing connections in established content areas
- **Relevance Scoring**: Prioritize high-value connection suggestions

### Link Health Monitoring

- **Broken Link Tracking**: Monitor link integrity over time
- **Connection Density**: Identify under-connected valuable content
- **Hub Analysis**: Understand how well Forever Notes serve as knowledge hubs
- **Orphan Alerts**: Flag valuable content that lacks integration

### Strategic Enhancement

- **Blog SEO**: Improve internal linking for published content
- **Knowledge Discoverability**: Make established knowledge more findable
- **Cross-Pollination**: Connect insights across different Areas/Projects
- **System Strengthening**: Reinforce Forever Notes as central knowledge hubs

## Safety & Validation

### Pre-Change Validation

- **Protected Zone Check**: Verify no modifications to restricted areas
- **Link Target Validation**: Confirm suggested targets exist and are accessible
- **Duplicate Prevention**: Check for existing links before suggesting additions
- **Context Preservation**: Maintain existing link context and meaning

### Change Tracking

- **Suggestion Logging**: Record all proposed link modifications
- **Rollback Support**: Provide undo guidance for implemented changes
- **Impact Assessment**: Preview how changes affect knowledge graph structure
- **User Confirmation**: Always suggest rather than auto-implement

### Error Handling

- **Graceful Degradation**: Handle missing files, permission issues
- **Context Awareness**: Understand when not to suggest links
- **Respect Boundaries**: Never breach protected zone limitations
- **Preserve Intent**: Maintain original content creator's organizational choices

## Usage Examples

```bash
# Quick link health overview
obsidian-link-curation scan

# Analyze inbox content for integration opportunities
obsidian-link-curation analyze inbox

# Find broken links and suggest fixes
obsidian-link-curation fix-broken --dry-run

# Discover orphaned content needing integration
obsidian-link-curation orphan-check

# Focus on specific content theme
obsidian-link-curation suggest-connections --focus "SCCM"

# Consolidate duplicate reference patterns
obsidian-link-curation consolidate-duplicates
```

---

_Built with deep respect for your Forever Notes system and established workflows. Enhances without disrupting._
