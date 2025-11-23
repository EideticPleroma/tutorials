# IDE Configuration Guide

This guide explains how to configure AI behavior for each supported IDE in this tutorial.

---

## Overview

Different IDEs have different ways of configuring AI assistant behavior. This project includes configuration files for each major IDE:

| IDE                             | Configuration File       | Auto-Read `.cursorrules`? |
| ------------------------------- | ------------------------ | ------------------------- |
| **Cursor**                      | `.cursorrules`           | ✅ Yes                     |
| **Continue** (VS Code)          | `.cursorrules`           | ✅ Yes                     |
| **Cline/Claude Code** (VS Code) | `.cursorrules`           | ✅ Yes                     |
| **GitHub Copilot**              | `.vscode/settings.json`  | ❌ No (manual setup)       |
| **Manual/Other**                | `README.md` + this guide | ⚠️ Reference manually      |

---

## Cursor Configuration

**Status**: ✅ Fully Configured

Cursor automatically reads the `.cursorrules` file at the project root.

### What's Configured
- Project context and goals
- Coding standards (PEP 8, type hints, docstrings)
- Agentic development rules
- Testing methodology (O.V.E.)
- Lab development guidelines (mentor mode)
- Git workflow

### How to Verify
1. Open this project in Cursor
2. Start a new chat (Cmd/Ctrl+L)
3. Ask: "What are the coding standards for this project?"
4. Cursor should reference the rules from `.cursorrules`

### Customization
Edit `.cursorrules` directly. Changes take effect immediately in new chat sessions.

---

## Continue (VS Code Extension) Configuration

**Status**: ✅ Fully Configured

Continue automatically reads `.cursorrules` (same file as Cursor!) and respects `.vscode/settings.json`.

### What's Configured
- **`.cursorrules`**: Project-specific AI behavior (same as Cursor)
- **`.vscode/settings.json`**: Continue-specific settings
  - Telemetry disabled
  - Tab autocomplete enabled
  - Python testing configuration

### How to Verify
1. Install Continue extension in VS Code
2. Open Continue sidebar (Cmd/Ctrl+L)
3. Ask: "What testing methodology should I use?"
4. Continue should reference O.V.E. from `.cursorrules`

### Customization
- **AI Behavior**: Edit `.cursorrules`
- **Extension Settings**: Edit `.vscode/settings.json`
- **Model Selection**: Continue → Settings → Choose model (Ollama/Claude/GPT)

### Recommended Settings
Already configured in `.vscode/settings.json`:
```json
{
  "continue.telemetryEnabled": false,
  "continue.enableTabAutocomplete": true
}
```

---

## Cline (Claude Code for VS Code) Configuration

**Status**: ✅ Fully Configured

Cline (formerly Claude Dev) automatically reads `.cursorrules` and provides agentic AI capabilities.

### What's Configured
- **`.cursorrules`**: Project-specific AI behavior (same as Cursor/Continue)
- **`.vscode/settings.json`**: Python and editor configuration
- **Agentic Mode**: Can autonomously execute multi-step tasks

### What is Cline?
Cline is an autonomous AI assistant that can:
- Execute terminal commands
- Edit multiple files simultaneously
- Create entire features from descriptions
- Review its own changes before applying
- Use local models (Ollama) or Claude API

### How to Verify
1. Install Cline extension in VS Code
2. Open Cline sidebar
3. Ask: "What are the project coding standards?"
4. Cline should reference `.cursorrules` automatically

### Configuration Options

**Option A: Use Claude API (Recommended for best quality)**
1. Get API key from [console.anthropic.com](https://console.anthropic.com)
2. In Cline settings, add your API key
3. Select Claude 3.5 Sonnet as the model

**Option B: Use Local Ollama (Free)**
1. Ensure Ollama is running (`ollama serve`)
2. In Cline settings, select "Ollama" as provider
3. Select `llama3.1:8b` as the model
4. Note: Less capable than Claude API but free and private

### Pro Tips
- **Agentic Mode**: Let Cline implement entire features autonomously
- **Approval Workflow**: Cline asks permission before executing commands or making changes
- **Context**: Cline automatically includes relevant files in context
- **`.cursorrules`**: Cline follows project guidelines automatically

### Use Cases for This Tutorial
- Implementing tools (Exercise 2)
- Refactoring prompts (Exercise 3)
- Writing comprehensive tests (Exercise 4)
- Complex multi-file changes

### Limitations
- Claude API requires paid subscription ($20/month)
- Ollama mode is less capable than Claude
- Can be more autonomous than needed for learning exercises

---

## GitHub Copilot (VS Code) Configuration

**Status**: ⚠️ Partial (Manual Setup Required)

Copilot does NOT automatically read `.cursorrules`. You must configure behavior manually.

### What's Configured
- **`.vscode/settings.json`**: Copilot enablement for file types
- **Project README**: Reference for AI consultations

### Manual Setup Required

**Option 1: Use `.cursorrules` as a Chat Prompt** (Recommended)

1. Open `.cursorrules` in VS Code
2. Copy the entire contents
3. Open Copilot Chat (Cmd/Ctrl+I)
4. Paste this prompt:
   ```
   I'm working on a project with these guidelines:
   
   [PASTE .cursorrules HERE]
   
   Please follow these rules in all our conversations.
   ```
5. Copilot will remember this for the current session

**Option 2: Create a Workspace Prompt File**

1. Create `.github/copilot-instructions.md`:
   ```markdown
   # GitHub Copilot Instructions
   
   Please follow these project guidelines:
   - [Copy key rules from .cursorrules]
   ```
2. Reference this file at the start of each Copilot chat session

**Option 3: Add Inline Comments**

Add comments to your code files:
```python
# Project uses O.V.E. testing methodology
# Tools must return human-readable strings, not exceptions
# See .cursorrules for full guidelines
```

### Limitations
- No automatic rules loading
- Must re-establish context for each chat session
- Inline suggestions don't consider project rules

### Recommended Workflow
1. Keep `.cursorrules` open in a tab
2. Reference it when asking Copilot questions
3. Paste relevant sections into chat when needed

---

## Other IDEs (Manual Consultation)

**Status**: 📖 Reference Documentation

For IDEs without AI integration (vim, Emacs, Sublime, etc.), use these files as reference when consulting external AI:

### Reference Files
1. **`.cursorrules`**: Complete project guidelines
2. **`README.md`**: Project overview and structure
3. **This guide**: IDE-specific advice

### Recommended Workflow

**When asking AI tools (ChatGPT, Claude, etc.):**

1. **Provide Context** (first message):
   ```
   I'm working on an agentic AI tutorial project. Here are the guidelines:
   
   [Paste relevant sections from .cursorrules]
   
   Current task: [describe what you're working on]
   ```

2. **Include Code Context**:
   ```
   Here's the current code I'm working on:
   
   [Paste code snippet]
   
   How should I implement [feature] following the project guidelines?
   ```

3. **Reference Specific Rules**:
   ```
   The project uses O.V.E. testing methodology. How do I write a test for this tool?
   ```

### Key Guidelines to Remember

Copy these to keep handy:

**Coding Standards:**
- Python: PEP 8, mandatory type hints, Google-style docstrings
- Tools must return human-readable strings, not exceptions
- Docstrings are critical (agents read them!)

**Testing:**
- Use O.V.E. methodology (Observe, Validate, Evaluate)
- Every tool needs unit tests + E2E tests
- Check for test flakiness (5 runs)

**Agent Development:**
- System prompts are critical
- Temperature 0.1-0.2 for deterministic behavior
- Test with multiple queries

---

## Configuration Files Summary

### `.cursorrules`
**For**: Cursor, Continue  
**Auto-loaded**: Yes  
**Content**: Complete project guidelines

### `.vscode/settings.json`
**For**: VS Code (Continue, Copilot, Python)  
**Auto-loaded**: Yes (by VS Code)  
**Content**: Editor settings, extension config, file exclusions

### `.vscode/extensions.json`
**For**: VS Code  
**Purpose**: Recommended extensions list  
**Auto-loaded**: VS Code prompts to install

### `.github/copilot-instructions.md` (Optional)
**For**: GitHub Copilot  
**Auto-loaded**: No (manual reference)  
**Content**: Simplified guidelines for Copilot

---

## Troubleshooting

### "AI isn't following the project rules"

**Cursor/Continue:**
- Verify `.cursorrules` exists at project root
- Start a new chat (clear context)
- Ask: "What are the project guidelines?" to verify rules are loaded

**Copilot:**
- Copilot doesn't auto-load rules
- Paste rules at start of each session
- Use inline comments as reminders

### "AI is too slow/verbose"

**All IDEs:**
- Check how many files are open (close unused files)
- Start new chat sessions regularly
- Be specific in questions ("explain X in file Y" vs. "fix my code")

### "Rules file changed but AI doesn't see it"

**Cursor/Continue:**
- Changes take effect in NEW chat sessions only
- Close and reopen chat, or start new conversation

**Copilot:**
- Must manually re-paste updated rules

---

## Best Practices

### 1. Keep Configuration in Sync
If you modify `.cursorrules`:
- Cursor/Continue: Automatically picks up changes
- Copilot: Update your saved prompt template
- Manual: Update your reference notes

### 2. Start Fresh When Switching Tasks
- Clear context between major tasks
- New chat = new context = better focus

### 3. Reference Explicitly
Instead of: "How do I test this?"  
Say: "How do I test this following O.V.E. methodology?"

### 4. Use Multiple Tools
- Cursor/Continue for implementation
- Copilot for inline suggestions
- External AI (ChatGPT/Claude) for architecture discussions

---

## Next Steps

1. ✅ Verify your IDE can read the configuration
2. ✅ Test by asking about project guidelines
3. ✅ Start Lab 1 with proper AI assistance
4. ✅ Reference this guide when AI behavior seems off

**Need help?** See [Troubleshooting Guide](./troubleshooting.md)

