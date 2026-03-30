---
name: obsidian-tag-curation
description: Maintain and clean up tags in Obsidian vaults - replace tags, find orphaned tags, detect duplicates, and standardize naming. Use this skill whenever users mention Obsidian tag cleanup, tag replacement, tag maintenance, fixing tag inconsistencies, finding unused tags, or any Obsidian tagging organization tasks.
---

# Obsidian Tag Curation

Comprehensive toolkit for maintaining clean, consistent tagging in Obsidian vaults. Handles tag replacement, orphan detection, duplicate consolidation, and hierarchy cleanup.

## Core Workflows

### 1. Advanced Tag Replacement

Replace one tag with another across specified folder paths or the entire vault, with smart handling of duplicate scenarios and multi-location tags.

**Smart Duplicate Detection Workflow:**

When replacing tags, always check for potential conflicts first:

1. **Cross-reference analysis**: Search for files with both old and new tags
2. **Strategy selection**:
   - Files with only old tag → **replacement** (`#old → #new`)
   - Files with both tags → **removal** (remove `#old`, keep `#new`)
3. **Multi-location scanning**: Check for tags beyond main tag lines

```bash
# 1. Identify overlap scenarios
obsidian search query="#old-tag" path="folder" > old_tag_files.txt
obsidian search query="#new-tag" path="folder" > new_tag_files.txt

# 2. Cross-reference to find files with both tags
# Files in both lists need removal, files only in old list need replacement

# 3. Process each scenario appropriately
```

**Multi-Location Tag Handling:**

Tags can appear in multiple places within files:

- **Tag lines** (top of note): `#tag1 #tag2 #tag3`
- **Content sections**: Scattered throughout note body
- **Footer references**: End-of-file tag collections

**Process:**

1. Use `obsidian-cli` to search for files with the old tag
2. **Cross-reference** with new tag search to identify overlap
3. **Choose processing strategy** based on batch vs. individual needs
4. **Comprehensive replacement**: Use global sed patterns (`s/#old/#new/g`) for multi-location tags
5. **Enhanced verification** with statistical validation
6. Report detailed changes with before/after analysis

**Example Usage:**

```bash
# Smart duplicate-aware replacement
obsidian search query="#MECM" path="Resources/tech-kb"
obsidian search query="#sccm-mecm" path="Resources/tech-kb"

# For files with only #MECM (replacement strategy)
sed -i '' 's/#MECM/#sccm-mecm/g' "file.md"

# For files with both tags (removal strategy)
sed -i '' 's/#MECM//g' "file-with-both-tags.md"

# Comprehensive verification
obsidian search query="#MECM" path="Resources/tech-kb"  # Should return "No matches"
obsidian search query="#sccm-mecm" path="Resources/tech-kb" | wc -l  # Count final distribution
```

**Batch Processing Decision Matrix:**

| Scenario             | File Count | Strategy     | Approach                                        |
| -------------------- | ---------- | ------------ | ----------------------------------------------- |
| Simple replacement   | 1-5 files  | Individual   | Process each file with dedicated sed command    |
| Complex names/chars  | Any count  | Individual   | Quote carefully, process one-by-one             |
| Clean bulk operation | 6-20 files | Batch        | Use for loops with proper quoting               |
| Large-scale changes  | 20+ files  | Staged batch | Process in smaller groups, verify incrementally |

### 2. Orphaned Tag Detection

Find tags that exist in vault files but are rarely used or potentially obsolete.

**Process:**

1. Get comprehensive tag list from vault
2. Count usage frequency for each tag
3. Identify low-usage tags (< 3 occurrences)
4. Present findings with usage context for user review

### 3. Duplicate/Similar Tag Detection

Find tags that may be redundant due to naming variations.

**Common Patterns to Detect:**

- Case variations: `#API` vs `#api`
- Separator variations: `#rest-api` vs `#rest_api` vs `#restapi`
- Singular/plural: `#note` vs `#notes`
- Abbreviations vs full forms: `#js` vs `#javascript`
- Spacing issues: `#tech-kb` vs `#techkb`

**Process:**

1. Extract all unique tags from vault
2. Group similar tags using pattern matching
3. Show grouped suggestions for consolidation
4. Allow user to choose preferred tag for each group

### 4. Tag Hierarchy Cleanup

Identify and standardize hierarchical tag relationships.

**Process:**

1. Find nested tag patterns (e.g., `#tech/api`, `#tech/database`)
2. Identify inconsistent hierarchy usage
3. Suggest standardization to consistent format
4. Handle parent-child tag relationships

## Safety Measures

**Folder Restrictions:**

- Always respect folder exclusions from CLAUDE.md
- Skip folders matching `*-primary-employer*` patterns
- Skip folders matching `ignore*` patterns
- Skip `_attachments` folder

**Backup Strategy:**

- For bulk operations (>10 files), offer to create backup
- Use git (if available) or filesystem backup before changes
- Never modify files without user confirmation for bulk operations

**Tag Type Handling:**

- **Primary focus:** Content tags (`#tagname`) in note body
- **Avoid by default:** YAML frontmatter tags unless specifically requested
- **Safe replacement:** Use sed with word boundaries to avoid partial matches

## Commands

### replace-tag

Replace one tag with another in specified scope.

**Usage:**

```
replace-tag --old "#old-tag" --new "#new-tag" [--path "folder/path"] [--confirm]
```

**Parameters:**

- `--old`: Tag to replace (include #)
- `--new`: Replacement tag (include #)
- `--path`: Limit to specific folder (optional, defaults to entire vault)
- `--confirm`: Skip confirmation prompt for automation

**Enhanced Process:**

1. **Duplicate analysis**: Search for files with both old and new tags
2. **Strategy determination**: Choose replacement vs. removal approach
3. **Preview generation**: Show files to be changed with strategy explanation
4. **User confirmation**: Get approval (unless --confirm flag used)
5. **Multi-location processing**: Handle tags throughout files, not just tag lines
6. **Batch optimization**: Use appropriate individual vs. batch processing
7. **Comprehensive verification**: Statistical validation and cross-referencing
8. **Detailed reporting**: Before/after analysis with file counts and strategy breakdown

### find-orphaned

Identify rarely used or orphaned tags.

**Usage:**

```
find-orphaned [--threshold 3] [--path "folder/path"]
```

**Parameters:**

- `--threshold`: Minimum usage count (default: 3)
- `--path`: Limit to specific folder (optional)

**Output:**

- List of tags below threshold with usage count
- Files where each orphaned tag appears
- Suggestions for consolidation or removal

### find-duplicates

Detect potentially duplicate or similar tags.

**Usage:**

```
find-duplicates [--similarity 0.8] [--include-case]
```

**Parameters:**

- `--similarity`: Similarity threshold (0.0-1.0, default: 0.8)
- `--include-case`: Include case-only variations

**Output:**

- Grouped similar tags with usage counts
- Suggested primary tag for each group
- Preview of consolidation impact

### audit-hierarchy

Review and standardize tag hierarchies.

**Usage:**

```
audit-hierarchy [--format "kebab-case|snake_case|camelCase"]
```

**Parameters:**

- `--format`: Preferred naming format for hierarchical tags

**Output:**

- Current hierarchy patterns found
- Inconsistencies and suggested standardizations
- Preview of hierarchy cleanup changes

## Integration Patterns

**With obsidian-cli:**

- Use for searching and reading vault content
- Leverage for tag counting and analysis
- Integrate with Obsidian's live tag system

**With existing tagging system:**

- Reference `00-Core-Tag-Index.md` for approved tag taxonomy
- Respect existing tag conventions and patterns
- Suggest additions to tag index for new standardized tags

**With filesystem tools:**

- Use sed for reliable tag replacement
- Use grep for pattern detection and analysis
- Use find for file discovery and filtering

## Output Formats

**Summary Report Template:**

```markdown
# Tag Curation Report - [Date]

## Changes Made

- Replaced `#old-tag` → `#new-tag` in [X] files
- [List of specific files changed]

## Orphaned Tags Found

- `#rarely-used-tag` (2 occurrences)
- `#obsolete-tag` (1 occurrence)

## Duplicate Groups Detected

### Group 1: API-related tags

- `#rest-api` (15 uses) ← suggested primary
- `#REST-API` (3 uses)
- `#rest_api` (2 uses)

## Recommendations

- Consider consolidating duplicate groups
- Review orphaned tags for removal
- Update tag index documentation
```

**Enhanced Verification Output:**

```
✅ Tag Consolidation Complete - [Date]

## Operation Summary
- **Strategy Applied**: [Replacement/Removal/Mixed]
- **Total files processed**: [X] files in [path]
- **Files with replacement** (#old → #new): [X] files
- **Files with removal** (had both, removed #old): [X] files

## Verification Results
- 🔍 **No remaining #old-tag instances** in target path
- 📊 **Final tag distribution**: [X] files now use #new-tag
- ✅ **Cross-reference validation**: All files properly tagged
- ⚙️  **Multi-location check**: Tags verified throughout file content

## Files Changed
[Detailed list of files with strategy used for each]

## Quality Assurance
- Zero duplicate tags created
- No orphaned or partial tag remnants
- All file modifications successful
- Statistical validation: [before count] → [after count]
```

## Enhanced Error Handling & Edge Cases

**Complex Real-World Scenarios:**

- **Multi-location tags**: Tags scattered throughout note content, not just tag lines
- **File naming complexity**: Spaces, special characters, long names requiring careful quoting
- **Overlapping tag scenarios**: Files with both old and new tags requiring different strategies
- **Batch vs. individual processing**: Knowing when to process files individually vs. in batches
- **Tags embedded in content**: References in code blocks, URLs, or other contexts
- **Permission errors**: Read-only files or locked notes
- **Partial matches**: Avoiding replacement of compound words containing tag text

**Advanced Recovery Strategies:**

- **Cross-reference validation**: Always verify tag overlap before processing
- **Staged processing**: Handle complex scenarios in smaller batches with incremental verification
- **Strategy-specific handling**: Use different replacement patterns for removal vs. substitution
- **Comprehensive verification**: Statistical validation and pattern checking beyond simple searches
- **Rollback procedures**: Backup strategies for bulk operations
- **Safe mode testing**: Test changes on single files before bulk operations
- **Detailed logging**: Track all changes with before/after states for each file

**Processing Decision Framework:**

When encountering complex scenarios:

1. **Analyze first**: Cross-reference old/new tag usage
2. **Choose strategy**: Replacement vs. removal based on overlap
3. **Select approach**: Individual vs. batch based on file complexity
4. **Verify incrementally**: Check progress at each step
5. **Validate comprehensively**: Use multiple verification methods

## Future Extensions

**Planned Enhancements:**

- Auto-tagging suggestions based on content analysis
- Tag template system for consistent new tags
- Integration with note templates
- Batch operations with progress tracking
- Tag usage analytics and trending

**Workflow Integration:**

- Hook into note creation workflows
- Integration with inbox processing
- Automated tag suggestions during note editing
- Scheduled tag maintenance routines
