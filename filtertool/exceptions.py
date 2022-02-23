
class ConditionError(Exception):
    """To be raised when a parameter for a filter do not comply with its preconditions"""
    def __init__(self, condition, param, message='Error!\nCondition not fulfilled by parameter.'):
        message += f"\n\t Parameter: {param}"
        message += f"\n\t Condition: {condition}"
        super().__init__(message)
