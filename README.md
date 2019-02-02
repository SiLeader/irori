# irori - build tool

Copyright 2019 SiLeader.

## features
+ configuration file is Python script
+ suffix rule
+ concurrent execution

## how to use
```bash
pip install irori
```

write configuration script (`makefile.py`).

```python
from irori.rules import SuffixRule, StaticRule, LinkRule
from irori import context as ctxt, runner
from irori.depend import Dependencies

import glob


target = 'hello.elf'


def build(_: ctxt.BuildContext):
    return LinkRule(
        command='clang++ -fPIC -o $@ $^',
        debug='-O0 -g',
        release='-O2',
        rules=SuffixRule(
            cpp=StaticRule('g++ -std=c++11 -c $< -o $@', debug='-O0 -g', release='-O2'),
            c=StaticRule('gcc -std=c11 -c -O2 $< -o $@', debug='-O0 -g', release='-O2')
        )
    )


def depend(_: ctxt.BuildContext):
    return SuffixRule(
        cpp=StaticRule('g++ -MMD -c $< -o $@'),
        c=StaticRule('gcc -MMD -c $< -o $@')
    )


def recipes():
    return {
        'build': build,
        'depend': depend
    }


def arguments(parser):
    pass


def find_files(_: ctxt.BuildContext):
    return glob.glob('*.c') + glob.glob('*.cpp')


runner.start(
    target,
    recipes=recipes, finder=find_files,
    arguments=arguments, dependencies=Dependencies(files=glob.glob('obj/*.d'))
)

```

run in `makefile.py`'s directory.
```bash
irori build
```

## license
GNU GPL version 3.0
