from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'service'

executables = [
    Executable('main.py', base=base, target_name = 'DiscordBirthdayBot')
]

setup(name='DiscordBirthdayBot',
      version = '1.0',
      description = 'A discord bot for tracking birthdays.',
      options = {'build_exe': build_options},
      executables = executables)
