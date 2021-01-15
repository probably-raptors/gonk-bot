import setuptools

setuptools.setup(
    name='squirrel-sweeper-bot',
    version="0",
    url='',
    maintainer='m odonnell, b altman',
    maintainer_email='mike@devferret.com',
    packages=[
        'bot',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'discord.py',
        'python-dotenv'
    ],
    entry_points={'console_scripts':[
        'bot=bot.bot:main',
    ]},
)
