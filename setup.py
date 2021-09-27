from setuptools import setup

if __name__ == "__main__":
    setup(
        name="ikea_api_wrapped",
        install_requires=[
            "ikea-api==0.6.2",
            "python-box==5.3.0",
        ],
        extras_require={
            "dev": [
                "black==21.9b0",
                "pre-commit==2.15.0",
            ]
        },
    )
