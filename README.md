# composition

**Composition** is a tool that allows humans to interactively build software with an LLM. Users interact with a web UI in which they can specify tasks in human language. Composition will interact with the user in order to answer clarifying questions, write specification files, write code, etc. Each step in this process is broken down into it’s own data object, and each data object is represented in the web UI such that users can edit each step, go back and retry a previous step in a different way, and furthermore record all of the interactions made with Composition during each session. 


# Starting Backend

```
$ poetry run uvicorn backend.main:app --reload
```