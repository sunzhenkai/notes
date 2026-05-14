## ADDED Requirements

### Requirement: Change Detection
The system SHALL detect whether README.md has changed since the last synchronization by comparing the current file's SHA256 hash with the hash stored in `.cache/readme-sync-state.json`.

#### Scenario: First run with no cache
- **WHEN** the `/sync-index` command is executed and `.cache/readme-sync-state.json` does not exist
- **THEN** the system SHALL treat this as an initial synchronization, analyze the full README.md content, and establish the baseline mapping to index.html

#### Scenario: No changes since last sync
- **WHEN** the `/sync-index` command is executed and the SHA256 hash of README.md matches `last_sync_hash` in the cache
- **THEN** the system SHALL report that both files are in sync and exit without making changes

#### Scenario: Changes detected since last sync
- **WHEN** the `/sync-index` command is executed and the SHA256 hash of README.md differs from `last_sync_hash` in the cache
- **THEN** the system SHALL proceed to diff analysis and content update

### Requirement: Diff Analysis
The system SHALL analyze the diff between the current README.md and the cached version, identifying the semantic type of each change.

#### Scenario: Text modification detected
- **WHEN** a paragraph or sentence in README.md has been modified
- **THEN** the system SHALL classify the change as a "text update" and identify which sync:block it belongs to

#### Scenario: Link URL modification detected
- **WHEN** a hyperlink URL in README.md has been changed
- **THEN** the system SHALL classify the change as a "link update" and identify the corresponding sync:item anchor

#### Scenario: New content block added
- **WHEN** a new paragraph, link, or section has been added to README.md that does not map to any existing sync:block or sync:item
- **THEN** the system SHALL classify it as "new content", infer its semantic type based on context, and proceed to the human confirmation workflow

#### Scenario: Content removed
- **WHEN** a paragraph, link, or section has been removed from README.md
- **THEN** the system SHALL identify the corresponding sync:block or sync:item in index.html and flag it for potential removal

### Requirement: Anchor-Based Mapping
The system SHALL use HTML comments in index.html (`<!-- sync:block:xxx -->` and `<!-- sync:item:xxx -->`) as mapping anchors to locate the exact HTML elements to update.

#### Scenario: Block-level anchor found
- **WHEN** a change is mapped to a known sync:block (e.g., `sync:block:intro`)
- **THEN** the system SHALL locate the HTML content between the anchor comment and the next anchor comment as the update target

#### Scenario: Item-level anchor found
- **WHEN** a change is mapped to a known sync:item (e.g., `sync:item:link-github`)
- **THEN** the system SHALL locate the specific HTML element immediately associated with that anchor comment

#### Scenario: Anchor integrity check
- **WHEN** the system begins processing and loads index.html
- **THEN** the system SHALL verify that all expected sync:block and sync:item anchors are present, and SHALL warn the user if any are missing

### Requirement: Human Confirmation for New Content
The system SHALL present a diff preview and request user confirmation when new content needs to be added to index.html.

#### Scenario: New link added to README
- **WHEN** a new link is added to README.md in the links section and the system generates a corresponding new HTML element based on existing link-item patterns
- **THEN** the system SHALL display the proposed HTML addition as a diff and wait for user confirmation before applying

#### Scenario: User rejects proposed change
- **WHEN** the user rejects the proposed HTML addition
- **THEN** the system SHALL skip that specific change and proceed to the next change, if any

#### Scenario: User confirms proposed change
- **WHEN** the user confirms the proposed HTML addition
- **THEN** the system SHALL apply the change to index.html

### Requirement: State Persistence
The system SHALL update `.cache/readme-sync-state.json` after a successful synchronization.

#### Scenario: Successful sync completed
- **WHEN** all changes have been applied to index.html and confirmed
- **THEN** the system SHALL update the cache with the new SHA256 hash, current timestamp, and full README.md text

#### Scenario: Partial sync (user skipped some changes)
- **WHEN** some changes were applied and others were skipped by the user
- **THEN** the system SHALL update the cache with the current README.md state, treating the final state as the new baseline

### Requirement: ICP备案号保护
备案号 SHALL 永远不被同步操作修改，系统在更新 index.html 时必须无条件跳过备案号相关的 HTML 内容。

#### Scenario: 备案号在同步中被保留
- **WHEN** 系统对 index.html 进行任意内容更新
- **THEN** 备案号 `<a href="https://beian.miit.gov.cn/" ...>京ICP备2026013364号-2</a>` SHALL 保持不变，任何情况下不得更改或删除

#### Scenario: README 中新增备案相关内容
- **WHEN** README.md 中添加了新的备案相关信息
- **THEN** 系统 SHALL NOT 将该内容同步到 index.html 的 footer 区域，备案号以 index.html 中已有的为准

### Requirement: 双语内容处理
系统 SHALL 保留 README.md 中的中英文双语内容，并将英文部分自动翻译为中文，最终在 index.html 中优先展示中文。

#### Scenario: README 同时包含中英文描述
- **WHEN** README.md 中某段落同时包含中文和英文描述
- **THEN** 系统 SHALL 将英文部分翻译为中文，在 index.html 中以中文在前、英文可选在后的方式展示

#### Scenario: README 仅有英文内容
- **WHEN** README.md 中某段落仅有英文描述
- **THEN** 系统 SHALL 将其自动翻译为中文，index.html 中优先展示中文翻译，英文原文可保留作为辅助

#### Scenario: README 仅有中文内容
- **WHEN** README.md 中某段落仅有中文描述
- **THEN** 系统 SHALL 直接使用该中文内容，无需额外翻译

#### Scenario: 翻译保持语义一致性
- **WHEN** 系统对英文内容进行自动翻译
- **THEN** 翻译结果 SHALL 保持原文语义，符合技术文档的表达习惯

### Requirement: Style Consistency
The system SHALL maintain visual consistency with existing index.html styling when generating new HTML elements for added content.

#### Scenario: New link item generated
- **WHEN** the system generates a new link element for an added README link
- **THEN** the generated HTML SHALL use the same CSS classes (e.g., `link-item`, `label`, `sublabel`, `arrow`, `emoji`) and DOM structure as existing link items

#### Scenario: New site card generated
- **WHEN** the system generates a new site card for an added README site entry
- **THEN** the generated HTML SHALL use the same CSS classes (e.g., `site-card`, `site-name`, `site-desc`, `site-tech`) and DOM structure as existing site cards
