from setuptools import setup, find_packages

if __name__=="__main__":
  setup(
    name = "tangods-attributecalculator",
    version = "1.1.14",
    description = "Tango device that allows math expressions with external Tango attributes.",
    author = "Rutger Nieuwenhuis",
    author_email = "rutger_arend.nieuwenhuis@maxiv.lu.se",
    license = "MIT",
    url = "http://www.maxiv.lu.se",
    packages = find_packages(),
    install_requires = ['pyparsing>=3.0.9', 'pytango>=9.2.1'],
    entry_points={'console_scripts': ['AttributeCalculator = attribute_calculator.main:main']},
 )

