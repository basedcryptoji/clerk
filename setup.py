from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent
LONG_DESCRIPTION = (ROOT / "README.md").read_text(encoding="utf-8")

setup(
    name="clerk-api",
    version="0.1.1",
    description="AI-native legal data layer for the agentic economy. 500M+ US federal court records via x402 on Base.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Solvr Labs",
    author_email="hello@solvrbot.com",
    url="https://clerk.solvrlabs.ai",
    project_urls={
        "Source": "https://github.com/basedcryptoji/clerk",
        "Documentation": "https://clerk.solvrlabs.ai/docs",
        "Issues": "https://github.com/basedcryptoji/clerk/issues",
    },
    packages=find_packages(exclude=["examples", "examples.*", "tests", "tests.*"]),
    python_requires=">=3.10",
    install_requires=["httpx>=0.24.0"],
    extras_require={
        "examples": ["requests>=2.28.0", "eth-account>=0.10.0"],
    },
    keywords=["clerk", "court records", "x402", "solvr", "legal research", "agents", "federal courts"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
