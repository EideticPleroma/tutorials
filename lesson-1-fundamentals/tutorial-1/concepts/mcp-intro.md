# Model Context Protocol (MCP)

**Page 5 of 16** | [← Previous: Tool Calling Architecture](./tool-calling-architecture.md) | [Next: Testing Agents →](./testing-agents.md) | [↑ Reading Guide](../READING_GUIDE.md) | [📋 Tech Stack Reference](./tech-stack-decisions.md)

The Model Context Protocol (MCP) is an open standard that standardizes how AI agents interact with data and tools.

## The Problem

Before MCP, every AI tool needed a custom integration. This created an $N \times M$ mess:

```mermaid
graph TD
    subgraph "The N x M Mess"
        C1[Claude] --> G[GitHub]
        C1 --> D[Drive]
        C1 --> S[Slack]
        C2[ChatGPT] --> G
        C2 --> D
        C2 --> S
        C3[Cursor] --> G
        C3 --> D
        C3 --> S
    end
```

*   Connecting to GitHub required a specific GitHub API wrapper.
*   Connecting to PostgreSQL required a specific SQL wrapper.
*   Connecting to Google Drive required a specific Drive wrapper.

## The MCP Solution

MCP works like a USB-C port for AI applications.

```mermaid
graph TD
    subgraph "The MCP Standard"
        C1[Claude] --> P((MCP Protocol))
        C2[ChatGPT] --> P
        C3[Cursor] --> P
        P --> G[GitHub Server]
        P --> D[Drive Server]
        P --> S[Slack Server]
    end
```

*   **MCP Servers**: Expose resources (data) and tools (functions) via a standard protocol.
*   **MCP Clients**: AI applications (like Cursor, Claude Desktop, or your custom agent) that can connect to any MCP server.

## How We Use It

In this tutorial, we will use MCP to give our agent superpowers without writing complex integration code.

1.  **Consumption**: Our agent will act as an MCP Client.
2.  **Integration**: We will connect to existing MCP servers (like a Filesystem server) to instantly give our agent ability to read/write files safely.
3.  **Future**: In later tutorials, we will build custom MCP servers to expose your own data to any AI.

## Architecture in Tutorial 1

```mermaid
flowchart LR
    A["Python Agent"] -->|JSON-RPC| B["MCP Client (TypeScript)"]
    B -->|Stdio| C["Filesystem MCP Server"]
    C --> D["Local Disk"]
```

We use a TypeScript bridge because the MCP ecosystem is currently strongest in TypeScript, allowing us to leverage the official SDKs easily.

