## University of Delaware CISC-481/681 Knowledge Base Project
This project contains our team's implementation of three inference algorithms and infrastructure for applying them to a knowledge base of *facts* and *rules* about poisonous mushrooms and the consequences of eating them. 

### Inference Algorithms
1. Resolution
2. Forward Chaining
3. Backward Chaining (recursive)
4. Backward Chaining (iterative)

### Dependencies
The SymPy module is required, and is dependent upon:

1. Python 2.6 or higher
2. Mpmath, a Python module for arbitrary-precision arithmetic

SymPy can be installed via pip, as can Mpmath, or via your Linux distribution's package manager. More detailed instructions can be found at:

1. http://docs.sympy.org/dev/install.html (If your version of SymPy is 0.7.7 or lower, mpmath is included.)
2. http://mpmath.org/

### Usage
To use the system, ensure that a properly formatted rules file exists and that KB.py is executable. (i.e. chmod +x KB.py)

To begin, run ./KB.py $PATH\_TO\_RULES\_FILE

You will be prompted to select a method (interactive or from file) to build the knowledge base. If you select interactive mode by answering 'yes' you will be prompted to answer questions about the properties of the poisonous mushroom and the symptoms the patient is exhibiting. If you answer 'no', you will be prompted to provide the location of a properly formatted facts file. 

Once the knowledge base is constructed, you will be prompted to select from one of several query types. There are built-in options to perform multiple related queries automatically--e.g. to perform all queries necessary to determine which possible genuses of mushroom you are dealing with. Alternatively, you can enter arbitrary queries in sequence. For any query, you will be prompted to select which inference algorithm to use to determine whether or not the knowledge base entails the query.
