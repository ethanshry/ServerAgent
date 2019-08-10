# ServerAgent

Multi-process deployment manager

## node_env.toml

The node_env.toml file is a confiiguration file designed to contain information about all the applications currently running on the agent.

Format is as follows:

```toml
# Entry 1
[PORT_NO]
name = "pm2_process_name"

# Entry 2
[PORT_NO]
name = "pm2_process_name"
```

We will be adding to this format as the project develops
