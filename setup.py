from setuptools import setup

with open('Readme.md', 'r') as f:
    projects_details = f.read()

REPO_NAME = 'BookRecommendationApp'
AUTHOR = 'johnomage'
SRC_REPO = 'src'
REQUIREMENTS = open('requirements.txt', 'r')

setup(name=SRC_REPO,
      version='1.0.0',
      author=AUTHOR,
      description='A light books recommender app',
      long_description=projects_details,
      long_description_content_type='text/markdown',
      url=f'https://github.com/{AUTHOR}/{REPO_NAME}',
      packages=[SRC_REPO],
      license='MIT',
      install_requires=REQUIREMENTS)
