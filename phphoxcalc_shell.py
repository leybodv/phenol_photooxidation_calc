#!/usr/bin/python3

import cmd

class PhPhOxCalcShell(cmd.Cmd):
    intro = 'Process data of phenol photooxidation experiment. Type help or ? to list commands.\n'
    prompt = '> '

    def do_helloworld(self, arg):
        """
        Prints "Hello world" and all arguments passed here
        """
        print(f'Hello world: {arg}')

    def do_quit(self, arg):
        """
        Quits program
        """
        print('bye')
        return True

if __name__ == '__main__':
    print(f'{dir() = }')
    PhPhOxCalcShell().cmdloop()
