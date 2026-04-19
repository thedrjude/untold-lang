class Environment:
    """Holds variables for a scope. Scopes can be nested (functions, blocks)."""

    def __init__(self, parent=None):
        self.vars   = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"[Untold] Variable '{name}' is not defined")

    def set(self, name, value):
        """Set in current scope."""
        self.vars[name] = value

    def assign(self, name, value):
        """Assign to existing variable (walks up scope chain)."""
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NameError(f"[Untold] Cannot assign to undefined variable '{name}'")

    def set_constant(self, name, value):
        self.vars[f"__lock__{name}"] = True
        self.vars[name] = value

    def is_constant(self, name):
        return self.vars.get(f"__lock__{name}", False)
