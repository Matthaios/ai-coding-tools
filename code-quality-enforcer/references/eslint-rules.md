# Custom ESLint Rules Reference

Guide to writing custom ESLint rules for project-specific standards.

## Table of Contents
1. [AST Basics](#ast-basics)
2. [Rule Structure](#rule-structure)
3. [Common Node Types](#common-node-types)
4. [Auto-Fix Patterns](#auto-fix-patterns)
5. [Example Rules](#example-rules)

---

## AST Basics

ESLint parses code into an Abstract Syntax Tree (AST). Use [astexplorer.net](https://astexplorer.net) to explore.

### Example: Function Call

```javascript
// Code
console.log("hello")

// AST
{
  "type": "ExpressionStatement",
  "expression": {
    "type": "CallExpression",
    "callee": {
      "type": "MemberExpression",
      "object": {
        "type": "Identifier",
        "name": "console"
      },
      "property": {
        "type": "Identifier",
        "name": "log"
      }
    },
    "arguments": [
      {
        "type": "Literal",
        "value": "hello"
      }
    ]
  }
}
```

---

## Rule Structure

```javascript
module.exports = {
  meta: {
    type: 'problem',  // 'problem' | 'suggestion' | 'layout'
    docs: {
      description: 'Rule description',
      recommended: true,
    },
    fixable: 'code',  // 'code' | 'whitespace' | null
    schema: [
      // Rule options schema (JSON Schema)
      {
        type: 'object',
        properties: {
          allowInTests: { type: 'boolean' }
        }
      }
    ],
    messages: {
      unexpected: 'Unexpected {{name}}',
      prefer: 'Prefer {{preferred}} over {{actual}}',
    }
  },
  
  create(context) {
    // Get rule options
    const options = context.options[0] || {};
    
    // Get source code utilities
    const sourceCode = context.getSourceCode();
    
    // Return visitor object
    return {
      // Visit specific node types
      Identifier(node) {
        // Check conditions
        if (node.name === 'forbidden') {
          context.report({
            node,
            messageId: 'unexpected',
            data: { name: node.name },
            fix(fixer) {
              return fixer.replaceText(node, 'allowed');
            }
          });
        }
      }
    };
  }
};
```

---

## Common Node Types

### Identifiers

```javascript
// Code: myVariable
{
  type: 'Identifier',
  name: 'myVariable'
}

// Visitor
Identifier(node) {
  console.log(node.name);
}
```

### Function Calls

```javascript
// Code: myFunction(arg1, arg2)
{
  type: 'CallExpression',
  callee: { type: 'Identifier', name: 'myFunction' },
  arguments: [...]
}

// Visitor
CallExpression(node) {
  if (node.callee.name === 'myFunction') {
    // Do something
  }
}
```

### Member Expressions

```javascript
// Code: object.property
{
  type: 'MemberExpression',
  object: { type: 'Identifier', name: 'object' },
  property: { type: 'Identifier', name: 'property' }
}

// Code: object['property']
{
  type: 'MemberExpression',
  object: { type: 'Identifier', name: 'object' },
  property: { type: 'Literal', value: 'property' },
  computed: true
}
```

### Variable Declarations

```javascript
// Code: const x = 5
{
  type: 'VariableDeclaration',
  kind: 'const',
  declarations: [{
    type: 'VariableDeclarator',
    id: { type: 'Identifier', name: 'x' },
    init: { type: 'Literal', value: 5 }
  }]
}
```

### Import Declarations

```javascript
// Code: import { foo } from 'bar'
{
  type: 'ImportDeclaration',
  source: { type: 'Literal', value: 'bar' },
  specifiers: [{
    type: 'ImportSpecifier',
    imported: { type: 'Identifier', name: 'foo' },
    local: { type: 'Identifier', name: 'foo' }
  }]
}
```

---

## Auto-Fix Patterns

### Replace Text

```javascript
fix(fixer) {
  return fixer.replaceText(node, 'newCode');
}
```

### Replace Range

```javascript
fix(fixer) {
  return fixer.replaceTextRange([start, end], 'newCode');
}
```

### Insert Before/After

```javascript
fix(fixer) {
  return fixer.insertTextBefore(node, 'prefix');
}

fix(fixer) {
  return fixer.insertTextAfter(node, 'suffix');
}
```

### Remove Node

```javascript
fix(fixer) {
  return fixer.remove(node);
}
```

### Multiple Fixes

```javascript
fix(fixer) {
  return [
    fixer.insertTextBefore(node, '/* '),
    fixer.insertTextAfter(node, ' */')
  ];
}
```

---

## Example Rules

### No console.log

```javascript
module.exports = {
  meta: {
    type: 'problem',
    docs: { description: 'Disallow console.log' },
    fixable: 'code',
  },
  create(context) {
    return {
      CallExpression(node) {
        if (
          node.callee.type === 'MemberExpression' &&
          node.callee.object.name === 'console' &&
          node.callee.property.name === 'log'
        ) {
          context.report({
            node,
            message: 'Unexpected console.log',
            fix(fixer) {
              // Remove the entire statement
              const parent = node.parent;
              if (parent.type === 'ExpressionStatement') {
                return fixer.remove(parent);
              }
            }
          });
        }
      }
    };
  }
};
```

### Prefer Named Exports

```javascript
module.exports = {
  meta: {
    type: 'suggestion',
    docs: { description: 'Prefer named exports over default' },
  },
  create(context) {
    return {
      ExportDefaultDeclaration(node) {
        context.report({
          node,
          message: 'Prefer named exports over default exports',
        });
      }
    };
  }
};
```

### Enforce Import Order

```javascript
module.exports = {
  meta: {
    type: 'layout',
    docs: { description: 'External imports before internal' },
  },
  create(context) {
    let sawInternalImport = false;
    
    return {
      ImportDeclaration(node) {
        const isInternal = node.source.value.startsWith('.');
        
        if (isInternal) {
          sawInternalImport = true;
        } else if (sawInternalImport) {
          context.report({
            node,
            message: 'External imports should come before internal imports',
          });
        }
      }
    };
  }
};
```

### No Magic Numbers

```javascript
module.exports = {
  meta: {
    type: 'suggestion',
    docs: { description: 'Disallow magic numbers' },
    schema: [{
      type: 'object',
      properties: {
        ignore: { type: 'array', items: { type: 'number' } }
      }
    }]
  },
  create(context) {
    const ignore = new Set(context.options[0]?.ignore || [0, 1, -1]);
    
    return {
      Literal(node) {
        if (
          typeof node.value === 'number' &&
          !ignore.has(node.value) &&
          node.parent.type !== 'VariableDeclarator'
        ) {
          context.report({
            node,
            message: `Magic number ${node.value} should be a named constant`,
          });
        }
      }
    };
  }
};
```

---

## Testing Rules

```javascript
// tests/no-console-log.test.js
import { RuleTester } from 'eslint';
import rule from '../rules/no-console-log';

const ruleTester = new RuleTester();

ruleTester.run('no-console-log', rule, {
  valid: [
    'console.error("error")',
    'console.warn("warning")',
    'log("message")',
  ],
  invalid: [
    {
      code: 'console.log("test")',
      errors: [{ message: 'Unexpected console.log' }],
      output: '',  // Expected auto-fix output
    },
  ],
});
```

---

## Best Practices

1. **Use messageId** - Easier to maintain than inline strings
2. **Add schema** - Document and validate options
3. **Test thoroughly** - Cover valid and invalid cases
4. **Auto-fix when possible** - Reduce friction
5. **Keep rules focused** - One concern per rule
6. **Document with examples** - Show what triggers the rule
