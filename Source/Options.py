#! /bin/python3

import argparse
import sys

from Source.Keys import *
from Source.Settings import *
from Source.Commands import *

Designation = "HexaPA"
License = "License: BSD 3-Clause License"
Copyright = "Copyright (c) 2023, Tibor Áser Veres All rights reserved."
BSD3CL_Details = '''
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    
    - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    
    - Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
    
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
OptionDescription = Designation + " v" + str (Settings.SoftwareVersion) + " - " + Copyright

Parser = argparse.ArgumentParser (description = OptionDescription)
Parser.add_argument ('--version', action = 'store_true', help = 'Print version and licensing.')
Parser.add_argument ('-u', '--user', type = str, help = 'Enter username. (Only for scripting... Changing username still not implemented, it will cause crash, since your API key is encrytped with the old username and password.)')
Parser.add_argument ('-p', '--password', type = str, help = 'Enter password. (Not recommended! It\'s only for scripting...)')
Parser.add_argument ('--openai-key', type = str, help='Specify OpenAI API Key.')
Parser.add_argument ('--import-chat', type = str, help = 'Import conversation from JSON. (Takes path/file.json file as argument.)')
Parser.add_argument ('--renew-data', action = 'store_true', help = 'Converts all blocks in the chain to new data version when loading existing conversation, rather then continuing old chain with new version data. (It is slow, and re-writes old AND new data since different blocks may contain different version data in the same chain. Use this once for each existing conversation if you see a warning messages after update...')
Parser.add_argument ('-v', '--verbose', action = 'store_true', help = 'Verbose output.')
Parser.add_argument ('--debug', action = 'store_true', help = argparse.SUPPRESS) # Not shown just in case I forget something I shouldn't in the code... ;)

Args = Parser.parse_args ()
