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
            cpp=StaticRule('clang++ -std=c++11 -c $< -o $@', debug='-O0 -g', release='-O2'),
            c=StaticRule('clang -std=c11 -c -O2 $< -o $@', debug='-O0 -g', release='-O2')
        )
    )


def depend(_: ctxt.BuildContext):
    return SuffixRule(
        cpp=StaticRule('clang++ -MMD -c $< -o $@'),
        c=StaticRule('clang -MMD -c $< -o $@')
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
