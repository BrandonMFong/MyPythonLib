"""
Utilities
================
"""

from .Logger import Logger
import math

log = Logger(noTime=True)

# Forward Declarations
class List(list):       pass
class Polynomial(List): pass
class Term():           pass 

def subtraction(a, b):
    return a - b 

def addition(a, b):
    return a + b 

def multiplication(a, b):
    return a * b

def division(a, b):
    if b == 0:
        raise ZeroDivisionError('Not a good thing')
    return a / b

def DoesContainOrderedTerm(polynomial: Polynomial, term: Term):
    """
    Returns true if the polynomial has a term with the same order as term 
    """
    result = False 
    okayToContinue = True 
    index = 0
    count = len(polynomial)
    tempTerm = Term()
    
    while okayToContinue and index < count and result == False:
        tempTerm = polynomial[index]
        if tempTerm is not None:
            if tempTerm.fExponent == term.fExponent:
                result = True
        else: 
            log.Fatal("Received a null term")
            okayToContinue = False
        index += 1

    return result

def InsertNullTerms(firstPolynomial: Polynomial, secondPolynomial: Polynomial):
    okayToContinue = True 
    index = 0
    count = 0
    tempTerm = Term()
    contains = False 

    if okayToContinue:
        index = 0 
        count = len(firstPolynomial)
        while index < count and okayToContinue: 
            if okayToContinue:
                tempTerm = firstPolynomial[index]
                if tempTerm is None:
                    okayToContinue = False 
                    log.Fatal("Null term")

            if okayToContinue:
                contains = False 
                contains = DoesContainOrderedTerm(
                    polynomial = secondPolynomial,
                    term = tempTerm
                )

                # If the polynomial does not contain it then 
                # insert a zeroed out term 
                if contains is False:
                    secondPolynomial.append(Term(
                        coefficient = 0,
                        exponent    = tempTerm.fExponent
                    ))
            index += 1 

    return firstPolynomial, secondPolynomial 

def MatchPolynomialLengths(firstPolynomial, secondPolynomial):
    okayToContinue = True 

    if okayToContinue:
        secondPolynomial, firstPolynomial = InsertNullTerms(secondPolynomial, firstPolynomial)
        if firstPolynomial is None:
            okayToContinue = False 
        elif secondPolynomial is None:
            okayToContinue = False 

    if okayToContinue:
        firstPolynomial, secondPolynomial = InsertNullTerms(firstPolynomial, secondPolynomial)
        if firstPolynomial is None:
            okayToContinue = False 
        elif secondPolynomial is None:
            okayToContinue = False 

    if okayToContinue is False:
        firstPolynomial = None 
        secondPolynomial = None
        log.Error("Error in inserting NULL terms")

    return firstPolynomial, secondPolynomial

class List(list):
    def Contains(self, value):
        return value in self 

    @staticmethod
    def ListWithRange(boundRange):
        order = 0
        success = True 

        if isinstance(boundRange, list) is False:
            success = False
        elif len(boundRange) != 2:
            success = False
        elif boundRange[0] == boundRange[1]:
            success = False 
        
        if success is False:
            raise Exception("The input must be a value like [start, end]")

        if success:
            if boundRange[0] < boundRange[1]:
                order = 1
            else:
                order = -1

        return List([*range(boundRange[0], boundRange[1]+order, order)])

    def __sub__(self,other):
        return self.OverloadingOperations(self, other, subtraction)

    def __mul__(self, other):
        """
        this is 1 dimensional linear multiplication 
        """
        return self.OverloadingOperations(self, other, multiplication)

    def PolynomialMultiplication(self, other):
        pass 

    def OverloadingOperations(self, other, callback):
        result = List()
        index = 0
        count = 0
        ourLength = len(self)
        theirLength = len(other)
        a = 0
        b = 0

        if ourLength < theirLength:
            count = theirLength
        else:
            count = ourLength

        while index < count:
            if (index < ourLength):
                a = self[index]
            else:
                a = 0

            if (index < theirLength):
                b = other[index]
            else:
                b = 0
        
            result.append(callback(a, b))

            index += 1

        return result

class Wave():
    """ 
    Wave 
    ===============
    Digital Signal Wave

    Discussion 
    --------------------
    Since this is a digital signal wave, the start and end indices has to be integers
    """ 
    # Init arguments
    # Use these in your sub classes
    kAngularFrequencyArgument   = "freq"
    kPhaseArgument              = "phase"
    kCallbackSinusoidalArgument = "function"
    kStartArgument              = "start"
    kEndArgument                = "end"

    def __init__(self, *args, **kwargs) -> None:
        success                 = True 
        okayToContinue          = True 
        keysList                = List()
        self.fAngularFrequency  = 1 # Frequency is always 1 for any wave 
        self.fPhase             = 0 # Always zero phase initially
        self.fFunction          = None
        self.fStart             = -math.pi
        self.fEnd               = -self.fStart
        self.fData              = List()
        self.fIndices           = List()

        if success and okayToContinue:
            keysList = List(kwargs.keys())
            if len(keysList) == 0:
                okayToContinue = False 
        
        # Scope for arguments
        if success and okayToContinue:
            # Get Frequency
            if keysList.Contains(self.kAngularFrequencyArgument):
                self.fAngularFrequency = kwargs[self.kAngularFrequencyArgument]
                if isinstance(self.fAngularFrequency, float) is False:
                    success = okayToContinue = False
                    log.Fatal("Angular frequency argument has to be a float")

            # Get Phase
            if keysList.Contains(self.kPhaseArgument):
                self.fPhase = kwargs[self.kPhaseArgument]
                if isinstance(self.fPhase, float) is False:
                    success = okayToContinue = False
                    log.Fatal("Phase argument has to be a float")

            # Get start index 
            if keysList.Contains(self.kStartArgument):
                self.fStart = kwargs[self.kStartArgument]
                if isinstance(self.fStart, int) is False:
                    success = okayToContinue = False
                    log.Fatal("Start index argument has to be a int")

            # Get End index 
            if keysList.Contains(self.kEndArgument):
                self.fEnd = kwargs[self.kEndArgument]
                if isinstance(self.fEnd, int) is False:
                    success = okayToContinue = False
                    log.Fatal("End index argument has to be a int")

            # Get callback function for the sinusoidal wave 
            if keysList.Contains(self.kCallbackSinusoidalArgument):
                self.fFunction = kwargs[self.kCallbackSinusoidalArgument]
            else:
                okayToContinue = False 

        if success and okayToContinue:
            success = self.Execute()

        if success is False:
            self = None
            raise Exception("Error in Wave init method")

    def Execute(self):
        success     = True 
        index       = self.fStart
        count       = self.fEnd
        tempValue   = float()

        if success:
            if len(self.fData) != 0 or len(self.fIndices):
                log.Error("The data and indices must not have data in it already")
                success = False 

        if success:
            while index < count: 
                tempValue = self.fFunction((self.fAngularFrequency * index) + self.fPhase)
                self.fData.append(tempValue)
                self.fIndices.append(index)
                index +=1 

            if len(self.fData) == 0 and len(self.fIndices) == 0:
                success = False 
                log.Error("Signal generation failed")

        return success 

    def __len__(self):
        return len(self.fData)

    def __getitem__(self, index: int):
        result = None 
        if isinstance(index, int):
            result = self.fData[index]
        return result 

class Sine(Wave):
    def __init__(self, freq=1.0, phase=0.0, start=-math.pi, end=math.pi) -> None:
        super().__init__(
            freq        = freq,
            phase       = phase,
            function    = math.sin,
            start       = start,
            end         = end 
        )

    def __copy__(self):
        return Sine(
            freq        = self.fAngularFrequency,
            phase       = self.fPhase,
            start       = self.fStart,
            end         = self.fEnd
        )

class Term():
    """
    Term
    """
    def __init__(self, coefficient=1.0, exponent=1.0) -> None:
        success = True 
        self.fCoefficient = coefficient
        self.fExponent = exponent

        if success is False:
            raise Exception("Error")

    def __getitem__(self,variable):
        return math.pow(self.fCoefficient * variable, self.fExponent)

    def __truediv__(self, otherTerm):
        result = None 
        okayToContinue = True 

        if okayToContinue:
            if otherTerm.fCoefficient == 0:
                okayToContinue = False 
                log.Fatal("Cannot do 0 division")

        if okayToContinue:
            result = Term(
                coefficient = self.fCoefficient / otherTerm.fCoefficient, 
                exponent    = self.fExponent - otherTerm.fExponent
            )
            
        return result 
    
    def __mul__(self, otherTerm):
        return Term(
            coefficient = self.fCoefficient * otherTerm.fCoefficient, 
            exponent    = self.fExponent + otherTerm.fExponent
        )

    def __sub__(self, otherTerm):
        result = None 

        if self.fExponent == otherTerm.fExponent:
            result = Term(
                coefficient = self.fCoefficient - otherTerm.fCoefficient,
                exponent    = self.fExponent
            )

        return result 
    
class Polynomial(List):

    def __init__(self, coefficients=None, bounds=None) -> None:
        """
        bounds: range from start exponent to end exponent
        """
        success = True 
        okayToContinue = True 
        result = List()
        errMessage = "Init error"
        exponents = List()
        index = 0
        count = 0
        tempTerm = None

        # Doing a blank initialization 
        if success and okayToContinue:
            if coefficients is None or bounds is None:
                okayToContinue = False 

        if success and okayToContinue:
            if len(bounds) != 2:
                success = False
                errMessage = "bounds must be length two"

        if success and okayToContinue:
            exponents = List.ListWithRange(bounds)
            if exponents[0] != bounds[0]:
                success = False
            elif exponents[len(exponents) - 1] != bounds[1]:
                success = False 

            if success is False:
                errMessage = "bounds construction error"

        if success and okayToContinue:
            if len(coefficients) != len(exponents):
                success = False 
                errMessage = "The bounds you provided does not match the number of coefficients for this polynomial"
        
        if success and okayToContinue:
            index = 0
            count = len(coefficients)
            while index < count and success:
                if success:
                    tempTerm = Term(
                        coefficient = coefficients[index],
                        exponent = exponents[index]
                    )
                    if tempTerm is None:
                        success = False 
                        errMessage = "could not generate term"
                if success:
                    result.append(tempTerm)

                index += 1

        if success:
            super().__init__(result)
        else:
            raise Exception(errMessage)

    @staticmethod
    def MatchLength(firstPolynomial, secondPolynomial):
        """
        Based on the exponents of each term, matches length 
        """

        firstPolynomial, secondPolynomial = MatchPolynomialLengths(
            firstPolynomial, secondPolynomial
        ) 

        if len(firstPolynomial) != len(secondPolynomial):
            log.Fatal("Lengths do not match")

        return firstPolynomial, secondPolynomial 
    
    def __truediv__(self, otherPolynomial):
        return self.__DoDivision(self, otherPolynomial)

    def __DoDivision(self, numerator, denominator):
        result = Polynomial()
        okayToContinue = True 
        tempTerm = Term()
        newTerm = Term()

        if okayToContinue:
            newTerm = numerator[0] / denominator[0]
            if newTerm is None:
                okayToContinue = False
                log.Fatal("Null term")
            else:
                result.append(newTerm)

        if okayToContinue:
            index = 0
            count = len(denominator)
            while index < count and okayToContinue:
                if okayToContinue:
                    tempTerm = denominator[index]
                    if tempTerm is None: 
                        okayToContinue = False 
                        log.Fatal("Null term")

                if okayToContinue:
                    tempTerm = tempTerm * newTerm
                    if tempTerm is None: 
                        okayToContinue = False 
                        log.Fatal("Null term")
                
                if okayToContinue:
                    denominator[index] = tempTerm

                index += 1
        
        if okayToContinue:
            numerator, denominator = Polynomial.MatchLength(numerator, denominator)
            if numerator is None:
                okayToContinue = False 
            elif denominator is None:
                okayToContinue = False 
            
            if okayToContinue is False:
                log.Fatal("Received null numerator or denominator")
        
        if okayToContinue:
            if len(numerator) != len(denominator):
                okayToContinue = False 

        # subtract polynomials 
        if okayToContinue:
            result = numerator - denominator

        return result 

    def __sub__(self, otherPolynomial):
        result = Polynomial()

        result = self.__DoSubtraction(self, otherPolynomial)

        return result

    def __DoSubtraction(self, first, second):
        result = Polynomial()
        tempTerm = None 
        error = False

        for firstTerm in first:
            for secondTerm in second:
                if firstTerm.fExponent == secondTerm.fExponent:
                    tempTerm = firstTerm - secondTerm
                    if tempTerm is None:
                        log.Fatal("Null term")
                        error = True 
                        break 
                    else:
                        result.append(firstTerm - secondTerm)
                        break 
            
            if error:
                log.Error("Error occured, received null term")
                result = None 
                break 

        return result 
