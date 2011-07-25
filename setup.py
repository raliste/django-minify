from setuptools import setup, find_packages

setup(
    name='django_minify',
    version='0.1',
    description=('A Django app that will contact and minify JS and CSS.' +
                 'Based on Jingo Minify by James Socol.'),
    author='Rodrigo Aliste P.',
    author_email='raliste@gmail.com',
    url='http://github.com/raliste/django-minify',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intented Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
