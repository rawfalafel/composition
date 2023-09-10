## The primary data structure is a JSON object stored in `<root>/composition.json`
`agents`: List of agents. Each name must be unique, and the unique name defines the file path at which the agent behavior is defined
`plan`: The entire plan so far, including what has been executed and what is planned to be executed
 - `agent`: Defines which agent will be used for the step
 - `log`: The conversation log for the step. Before the step has started, the log is empty
 - `result`: The resulting output of the conversation. It can have the following valid keys: `write`, `execute`, `next`
  - 