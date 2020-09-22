import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dash_access_manager",
    version="0.0.1",
    author="Evan",
    author_email="elehella@enssat.fr",
    description="Dash-Access-Manager provides user access management for Dash.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['bcrypt', 'mongoengine', 'flask_login',
                      'dash', 'dash_core_components',
                      'dash_html_components', 'dash_bootstrap_components'],
    url="https://github.com/evan-lh/dash-access-manager",
    packages=setuptools.find_packages(),
    license="MIT",
)
