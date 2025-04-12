from setuptools import setup

setup(
    name="NeutrOSINT",
    description="Determine if an email address exists on ProtonMail.",
    author="Kr0wZ",
    license="MIT",
    py_modules=["main", "neutrosint", "options"],
    install_requires=[
        "webdriver-manager",
        "selenium",
        "packaging",
        "argparse",
        "colorama",
        "requests",
        "dnspython",
    ],
    entry_points={
        "console_scripts": [
            "neutrosint = main:main",  # This tells setuptools to create a command 'neutrosint'
        ],
    },
)

