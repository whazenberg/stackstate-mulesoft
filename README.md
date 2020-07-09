# Mulesoft for StackState

Stub.

Developed against StackState 4.0.2 and StackState Agent v2.

## Installation

### Agent
Copy mulesoft.py in /etc/stackstate-agent/checks.d/
Copy mulesoft.yaml in /etc/stackstate-agent/conf.d/

Change ownership of file to `stackstate-agent:stackstate-agent`

Test:

```
stackstate-agent check mulesoft
```


## StackPack

1. zip contents of `stackpack/`:

  *Note*: rename zip to use sts extension.
  
  Example:
  
  ```
  zip -r mulesoft-0.0.1.sts stackpack.conf provisioning resources
  ```
  
  ```
  .
  ├── provisioning
  ├── resources
  └── stackpack.conf
  ```
  
1. upload with the StackState CLI

  ```
  sts stackpack upload <path to sts file>
  ```
  
1. Install in StackState

  Main menu -> StackPacks -> MuleSoft StackPack.
  
  Organization ID should match what is defined in `mulesoft.yaml`.
