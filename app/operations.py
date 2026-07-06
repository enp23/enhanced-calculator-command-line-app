########################
# Operation Classes    #
########################

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import ValidationError

#-------------------------------
# Decorator
#-------------------------------
def register_operation(description: str):
    """
    Decorator to register an operation class with a description.

    This decorator adds a 'description' attribute to the decorated operation class,
    allowing for easy identification and documentation of the operation's purpose.

    Args:
        description (str): A brief description of the operation.
    """
    def decorator(cls):
        cls.description = description
        return cls
    return decorator


#-------------------------------
# Base class
#------------------------------

class Operation(ABC):
    """
    Abstract base class for calculator operations.

    Defines the interface for all arithmetic operations. Each operation must
    implement the execute method and can optionally override operand validation.
    """

    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Execute the operation.

        Performs the arithmetic operation on the provided operands.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Result of the operation.

        Raises:
            OperationError: If the operation fails.
        """
        pass  # pragma: no cover

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands before execution.

        Can be overridden by subclasses to enforce specific validation rules
        for different operations.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Raises:
            ValidationError: If operands are invalid.
        """
        pass

    def __str__(self) -> str:
        """
        Return operation name for display.

        Provides a string representation of the operation, typically the class name.

        Returns:
            str: Name of the operation.
        """
        return self.__class__.__name__

#-------------------------------
# Concrete operation classes
#-------------------------------

@register_operation("Add two numbers")
class Addition(Operation):
    """
    Addition operation implementation.

    Performs the addition of two numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Add two numbers.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Sum of the two operands.
        """
        self.validate_operands(a, b)
        return a + b


@register_operation("Subtract two numbers")
class Subtraction(Operation):
    """
    Subtraction operation implementation.

    Performs the subtraction of one number from another.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Subtract one number from another.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Difference between the two operands.
        """
        self.validate_operands(a, b)
        return a - b


@register_operation("Multiply two numbers")
class Multiplication(Operation):
    """
    Multiplication operation implementation.

    Performs the multiplication of two numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Multiply two numbers.

        Args:
            a (Decimal): First operand.
            b (Decimal): Second operand.

        Returns:
            Decimal: Product of the two operands.
        """
        self.validate_operands(a, b)
        return a * b


@register_operation("Divide two numbers")
class Division(Operation):
    """
    Division operation implementation.

    Performs the division of one number by another.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands, checking for division by zero.

        Overrides the base class method to ensure that the divisor is not zero.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Raises:
            ValidationError: If the divisor is zero.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Divide one number by another.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Returns:
            Decimal: Quotient of the division.
        """
        self.validate_operands(a, b)
        return a / b


@register_operation("Raise to power")
class Power(Operation):
    """
    Power (exponentiation) operation implementation.

    Raises one number to the power of another.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for power operation.

        Overrides the base class method to ensure that the exponent is not negative.

        Args:
            a (Decimal): Base number.
            b (Decimal): Exponent.

        Raises:
            ValidationError: If the exponent is negative.
        """
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents not supported")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate one number raised to the power of another.

        Args:
            a (Decimal): Base number.
            b (Decimal): Exponent.

        Returns:
            Decimal: Result of the exponentiation.
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b)))


@register_operation("Calculate nth root")
class Root(Operation):
    """
    Root operation implementation.

    Calculates the nth root of a number.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for root operation.

        Overrides the base class method to ensure that the number is non-negative
        and the root degree is not zero.

        Args:
            a (Decimal): Number from which the root is taken.
            b (Decimal): Degree of the root.

        Raises:
            ValidationError: If the number is negative or the root degree is zero.
        """
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the nth root of a number.

        Args:
            a (Decimal): Number from which the root is taken.
            b (Decimal): Degree of the root.

        Returns:
            Decimal: Result of the root calculation.
        """
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1 / float(b)))

@register_operation("Calculate modulus")
class Modulus(Operation):
    """
    Modulus operation implementation.

    Calculates the remainder of the division of one number by another.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for modulus operation.

        Overrides the base class method to ensure that the divisor is not zero.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Raises:
            ValidationError: If the divisor is zero.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the modulus of one number by another.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Returns:
            Decimal: Remainder of the division.
        """
        self.validate_operands(a, b)
        return a % b

@register_operation("Perform integer division")
class IntegerDivision(Operation):
    """
    Integer Division operation implementation.

    Performs integer division of one number by another.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for integer division operation.

        Overrides the base class method to ensure that the divisor is not zero.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Raises:
            ValidationError: If the divisor is zero.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Divisor cannot be zero")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Perform integer division of one number by another.

        Args:
            a (Decimal): Dividend.
            b (Decimal): Divisor.

        Returns:
            Decimal: Result of the integer division.
        """
        self.validate_operands(a, b)
        return Decimal(int(a / b))

@register_operation("Calculate percentage")
class Percentage(Operation):
    """
    Percentage operation implementation.

    Calculates the percentage of one number relative to another.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for percentage operation.

        Overrides the base class method to ensure that the total is not zero.

        Args:
            a (Decimal): Part value.
            b (Decimal): Total value.

        Raises:
            ValidationError: If the total is zero.
        """
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Total value cannot be zero")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the percentage of one number relative to another.

        Args:
            a (Decimal): Part value.
            b (Decimal): Total value.

        Returns:
            Decimal: Percentage value.
        """
        self.validate_operands(a, b)
        return (a / b) * Decimal(100)
        
@register_operation("Calculate absolute difference")
class AbsoluteDifference(Operation):
    """
    Absolute Difference operation implementation.

    Calculates the absolute difference between two numbers.
    """

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the absolute difference between two numbers.

        Args:
            a (Decimal): First number.
            b (Decimal): Second number.

        Returns:
            Decimal: Absolute difference between the two numbers.
        """
        self.validate_operands(a, b)
        return abs(a - b)   
    

class OperationFactory:
    """
    Factory class for creating operation instances.

    Implements the Factory pattern by providing a method to instantiate
    different operation classes based on a given operation type. This promotes
    scalability and decouples the creation logic from the Calculator class.
    """

    # Dictionary mapping operation identifiers to their corresponding classes
    _operations: Dict[str, type] = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root,
        'modulus': Modulus,
        'int_div': IntegerDivision,
        'percentage': Percentage,
        'abs_diff': AbsoluteDifference,
    }

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """
        Register a new operation type.

        Allows dynamic addition of new operations to the factory.

        Args:
            name (str): Operation identifier (e.g., 'modulus').
            operation_class (type): The class implementing the new operation.

        Raises:
            TypeError: If the operation_class does not inherit from Operation.
        """
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls._operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """
        Create an operation instance based on the operation type.

        This method retrieves the appropriate operation class from the
        _operations dictionary and instantiates it.

        Args:
            operation_type (str): The type of operation to create (e.g., 'add').

        Returns:
            Operation: An instance of the specified operation class.

        Raises:
            ValueError: If the operation type is unknown.
        """
        operation_class = cls._operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class()
