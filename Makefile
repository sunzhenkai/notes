PID_FILE := .mdserve.pid

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
	@git push

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
