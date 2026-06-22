PID_FILE := .mdserve.pid

# Tools that receive note-* skills/commands (opencode is the source of truth)
NOTE_TOOLS := .cursor .codebuddy .qoder

# Sync note-* skills/commands from .opencode (source) to cursor/codebuddy/qoder.
# Only note-* prefixed files/dirs are touched; non-note files are left intact.
note-sync:
	@for tool in $(NOTE_TOOLS); do \
		echo "==> Syncing note-* to $$tool/"; \
		mkdir -p "$$tool/skills" "$$tool/commands"; \
		for d in .opencode/skills/note-*/; do \
			[ -d "$$d" ] || continue; \
			name=$$(basename "$$d"); \
			rm -rf "$$tool/skills/$$name"; \
			cp -R "$$d" "$$tool/skills/$$name"; \
			echo "   skills : $$tool/skills/$$name"; \
		done; \
		for f in .opencode/commands/note-*.md; do \
			[ -f "$$f" ] || continue; \
			cp "$$f" "$$tool/commands/"; \
			echo "   command: $$tool/commands/$$(basename $$f)"; \
		done; \
	done
	@echo "==> note-* synced to: $(NOTE_TOOLS)"

# Git commit with timestamp and changed files
commit:
	@timestamp=$$(date '+%Y-%m-%d %H:%M:%S'); \
	files=$$(git status --short | awk '{print $$2}' | tr '\n' ', ' | sed 's/,$$//'); \
	count=$$(git status --short | wc -l); \
	if [ "$${count}" -eq 0 ]; then \
		echo "No changes to commit"; \
	else \
		echo "Files: $${files}"; \
		git add -A; \
		git commit -m "docs: update $${count} file(s) - $${timestamp}"; \
	fi

push: commit
	@for remote in $$(git remote); do \
		echo "==> Pushing to $$remote..."; \
		git push $$remote HEAD; \
	done
	@echo "==> All remotes pushed."

serve:
	@mdserve serve

served:
	@nohup mdserve serve > /dev/null 2>&1 & echo $$! > $(PID_FILE) && echo "mdserve started (PID: $$(cat $(PID_FILE)))"

kill:
	@if [ -f $(PID_FILE) ]; then \
		kill $$(cat $(PID_FILE)) 2>/dev/null && echo "mdserve stopped (PID: $$(cat $(PID_FILE)))" || echo "Process not found"; \
		rm -f $(PID_FILE); \
	else \
		echo "PID file not found, mdserve may not be running"; \
	fi

restart: kill served

status:
	@if [ -f $(PID_FILE) ]; then \
		if kill -0 $$(cat $(PID_FILE)) 2>/dev/null; then \
			echo "mdserve is running (PID: $$(cat $(PID_FILE)))"; \
		else \
			echo "mdserve is not running (stale PID file)"; \
			rm -f $(PID_FILE); \
		fi \
	else \
		echo "mdserve is not running"; \
	fi
