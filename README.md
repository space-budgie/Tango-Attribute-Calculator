# Attribute Calculator

Attribute Calculator is a Tango device that allows the user to input mathematical formulas, where the variables are external Tango attributes. This formula is then stored as an attribute in this device, and the result is calculated whenever the attribute is read. The new attribute can also be plotted with Taurustrend, used for other Tango devices, etc.

## Usage

### Creating a Device
To get started, you can create your own instance of the Attribute Calculator by using the Calculator Creator device. This Calculator Creator device can be found under **attributecalculator/calculators/CalculatorCreator**.
Select the **AddNewDevice** command and type the name of your new Attribute Calculator device in the input box. The device will now be created under **attributecalculator/calculators/\<your entered name\>**.

### Adding a Formula
To add a formula to your device, you can execute the **AddNewExpression** command. The input is a string, which follows the format:

`"attribute_name = math_expression"`

This will create an attribute on the device with the specified attribute name. Every time the attribute is read, the math expression is evaluated. The math expression has the following limitations:

- Operators and operands need to be seperated by a whitespace.
- Supported operators are:
    - Addition (+) and subtraction (-)
    - Multiplication (*) and division (/)
    - Exponent (^)
- Supported operands are:
    - Integers and floats, both positive and negative
    - External Tango attributes in the form of **domain/family/device/attribute**
- The standard order of operations is used (exponent - multiplication/division - addition/subtraction). Priority can be given using parentheses ().

Note that in contrast to numbers, Tango attributes cannot be signed. That is to say, `-5` is a valid expression, but `-domain/family/device/attribute` is not. If you want a Tango attribute to be the negative equivalent of its value, you can for example write:

`(0 - domain/family/device/attribute)`

Please note that when entering a new expression via the 'Test Device' interface in Jive, **the expression must be surrounded in quotation marks ""**. The interface also gives a warning for this above the text input box.

#### Example
Let's say we want to compare the vertical emmitance of the 1.5 GeV storage ring with the current flowing through the ring. The vertical emittance of the ring can be read from **r1/dia/bemon-01/verticalemittance**, and the current in the ring can be read from **r1-101s/dia/dcct-01/current**. We can pass in the following input to the **AddNewExpression** command:

`"example = r1/dia/bemon-01/verticalemittance / r1-101s/dia/dcct-01/current"`

This will add an attribute called 'example' to the device that the **AddNewExpression** command is executed on. Everytime this attribute is read, the present values of the vertical emittance and current are retrieved, and the division operation is performed between these two values. 

Note that the operands (the emittance and current) and the operator (the division symbol) are seperated by a white space. This is required to properly parse the expression.

### Troubleshooting
If something is wrong with the inputted expression, the attribute will not be added and an error message is returned, stating what went wrong. In general, remember two things when troubleshooting inputting expression:
- Make sure all operators and operands are seperated by a white space.
- Wrap the input in quotation marks if it is entered via the Jive 'Test Device' interface.

If an already added attribute cannot be updated/read for any reason, the quality of the attribute will be set to `INVALID`. In order to determine what went wrong, you can look at the logging stream of the Tango device. To do this, open the Logviewer application (for example, by executing the 'logviewer' command in the terminal). Inside the Logviewer, locate your device in the left-hand panel. Right-click on your device, and select 'Add'. Right-click on your device again, and under 'Set Logging Level', select 'DEBUG' to see all messages entering the stream. Try to read the attribute again, and see what errors are shown in the Logviewer.

## Roadmap

Some ideas for future versions:
- Support for common math formulas (sin, cos, exp, etc.)
- Improved error handling with more clarity for the user on what went wrong.

## Contact

Feel free to contact me about issues, feature suggestions, etc.

rutger_arend.nieuwenhuis@maxiv.lu.se
