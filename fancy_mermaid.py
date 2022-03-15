import sys
import os
import random
from termcolor import colored


def script_path():
    '''set current path, to script path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def write_file(filename, text, mode='w'):
    '''write to file'''
    try:
        with open(filename, mode, encoding='utf-8') as f:
            f.write(text)
    except Exception as err:
        print('[x] failed to write to file: {}, err: {}'.format(filename, err))
    return None
    
    
class Fancy():
    """class for making fancy mermaid with use of node(s) objects"""
    def __init__(self, nodes):
        self.nodes = nodes
        self.enumerate_nodes()
        random.shuffle(self.nodes)
        self.connections = []
        
    def enumerate_nodes(self):
        """enumerate all nodes, by setting them indexes from 0-n"""
        for index, node in enumerate(self.nodes):
            node.index = index
        return
        
    def roll(self, quiet=False):
        """make connections between all nodes;
        for one the only inconvenience is that matching inputs is always first,
        it should be mixed between inputs and outputs matching
        """
        for node in self.nodes:
            if not quiet:
                print(colored(node.name, 'red'))
            available_outputs = self.list_possible(node, as_input=False)
            for x in range(node.inputs_left):
                if not available_outputs:
                    break
                choice = random.choice(available_outputs)
                node.make_input(choice)
                choice.make_output(node)
                available_outputs.remove(choice)
                if not quiet:
                    print(colored('    ({} -> {})'.format(choice.name, node.name), 'yellow'))
                self.connections.append((choice, node))
                
            available_inputs = self.list_possible(node, as_input=True)
            for x in range(node.outputs_left):
                if not available_inputs:
                    break
                choice = random.choice(available_inputs)
                node.make_output(choice)
                choice.make_input(node)
                available_inputs.remove(choice)
                if not quiet:
                    print(colored('    ({} -> {})'.format(node.name, choice.name), 'yellow'))
                self.connections.append((node, choice))
        return None
        
    def list_possible(self, node, as_input=True):
        local_nodes = self.nodes.copy()
        local_nodes.remove(node)
        if as_input:
            available_nodes = []
            for item in local_nodes:
                if item.full_inputs:
                    continue
                    
                if node in item.inputs:
                    continue
                    
                if not node.allow_reverse and (item in (node.outputs + node.inputs)):
                    continue
                    
                if not item.allow_reverse and (node in (item.outputs + item.inputs)):
                    continue
                    
                # finally append possible item
                available_nodes.append(item)
        else:
            # as output
            available_nodes = []
            for item in local_nodes:
                if item.full_outputs:
                    continue
                    
                if node in item.outputs:
                    continue
                    
                if not node.allow_reverse and (item in (node.outputs + node.inputs)):
                    continue
                    
                if not item.allow_reverse and (node in (item.outputs + item.inputs)):
                    continue
                    
                # finally append possible item
                available_nodes.append(item)
                
        return available_nodes
        
        
    def make_mermaid(self, brackets='round'):
        """make text mermaid, which can be used as graph in .md files"""
        blank_mermaid = """\
```mermaid
graph TD;
{}
```"""
        if brackets == 'round':
            br_start = '('
            br_stop = ')'
        elif brackets == 'curly':
            br_start = '{'
            br_stop = '}'
        elif brackets == 'square':
            br_start = '['
            br_stop = ']'
        else:
            br_start = '('
            br_stop = ')'
            
        connections_rows = []
        for (start, stop) in self.connections:
            pass
            row = '    {}{}{}{}-->{}{}{}{};'.format(
                                                start.index, br_start, start.name, br_stop,
                                                stop.index, br_start, stop.name, br_stop,
                                                )
            connections_rows.append(row)
        # connections_rows = ['    {}-->{};'.format(start, stop) for (start, stop) in self.connections]  # simple way
        connections_block = '\n'.join(connections_rows)
        mermaid = blank_mermaid.format(connections_block)
        return mermaid
        
        
class Node():
    def __init__(self, name, max_inputs=1, max_outputs=1, allow_reverse=True):
        self.name = name
        # if number of existing nodes is not enough
        # then max_inputs and max_outputs may be not reached
        self.max_inputs = max_inputs
        self.inputs_left = self.max_inputs
        
        self.max_outputs = max_outputs
        self.outputs_left = self.max_outputs
        
        # allow reverse connection between nodes
        # e.g. if 1 -> 2 then 2 -> 1 is prohobited if allow_reverse=False
        self.allow_reverse = allow_reverse
        
        self.inputs = []
        self.outputs = []
        if not self.max_inputs:
            self.full_inputs = True
        else:
            self.full_inputs = False
        if not self.max_outputs:
            self.full_outputs = True
        else:
            self.full_outputs = False
            
    def reset(self):
        """reset all connections"""
        self.inputs_left = self.max_inputs
        self.outputs_left = self.max_outputs
        self.inputs = []
        self.outputs = []
        if not self.max_inputs:
            self.full_inputs = True
        else:
            self.full_inputs = False
        if not self.max_outputs:
            self.full_outputs = True
        else:
            self.full_outputs = False
        return None
        
    def relations(self):
        left = tuple(sorted([item.name for item in self.inputs]))
        right = tuple(sorted([item.name for item in self.outputs]))
        center = self.name
        node_relations = '{} --> {} --> {}'.format(colored(left, 'cyan'), colored('(' + center + ')', 'yellow'), colored(right, 'cyan'))
        return node_relations
        
    def connect(self, node):
        """connect nodes in relation: executor -> node"""
        # ******** check if we can connect ********
        if not self.outputs_left:
            # print('[x] not enough outputs: {}'.format(self.name))
            return None
        if node in self.outputs:
            # connection already exists
            return None
        if not self.allow_reverse and (node in self.inputs):
            # reverse connection exists
            return None
            
        # ******** check if other node can be connected ********
        if not node.inputs_left:
            # print('[x] not enough outputs: {}'.format(self.name))
            return None
        if self in node.inputs:
            # connection already exists
            return None
        if not node.allow_reverse and (self in node.outputs):
            # reverse connection exists
            return None
            
        # ******** make connection for us ********
        self.outputs.append(node)
        self.outputs_left -= 1 # decrease outputs
        if len(self.outputs) >= self.max_outputs:
            self.full_outputs = True
            
        # ******** make connection for other node ********
        node.inputs.append(self)
        node.inputs_left -= 1  # decrease inputs
        if len(node.inputs) >= node.max_inputs:
            node.full_inputs = True
        return None
        
        
    def make_input(self, node):
        if not self.inputs_left:
            # print('[x] not enough inputs: {}'.format(self.name))
            return None
            
        if node in self.inputs:
            # connection already exists
            return None
            
        if not self.allow_reverse and (node in self.outputs):
            # reverse connection exists
            return None
            
        self.inputs.append(node)
        self.inputs_left -= 1  # decrease inputs
        if len(self.inputs) >= self.max_inputs:
            self.full_inputs = True
        return None
        
    def make_output(self, node):
        if not self.outputs_left:
            # print('[x] not enough outputs: {}'.format(self.name))
            return None
            
        if node in self.outputs:
            # connection already exists
            return None
            
        if not self.allow_reverse and (node in self.inputs):
            # reverse connection exists
            return None
            
        self.outputs.append(node)
        self.outputs_left -= 1 # decrease outputs
        if len(self.outputs) >= self.max_outputs:
            self.full_outputs = True
        return None
        
    def __str__(self):
        return self.name
        
        
if __name__ == "__main__":
    script_path()
    os.system('color')
    
    # ********* create nodes *********
    some = Node('some', max_inputs=1, max_outputs=1)
    thing = Node('thing', max_inputs=0, max_outputs=1)
    here = Node('here', max_inputs=2, max_outputs=0)
    they = Node('they', max_inputs=3, max_outputs=2)
    this = Node('this', max_inputs=1, max_outputs=3)
    meow = Node('meow', max_inputs=3, max_outputs=1)
    mandy = Node('mandy', max_inputs=1, max_outputs=1)
    candy = Node('candy', max_inputs=1, max_outputs=1)
    nodes = [some, thing, here, they, this, meow, mandy, candy]
    
    # ********* create fancy mermaid *********
    fancy = Fancy(nodes)
    fancy.roll(quiet=False)
    mermaid = fancy.make_mermaid(brackets='round')
    print(mermaid)
    write_file('mermaid.txt', mermaid)
    
    
    
"""
todo:
    -what if choice is in the list of inputs or outputs for a given node? then we don't lose shots, but we don't find any input/output. This needs to be fixed somehow by giving a while loop, or appropriate conditions that will filter out correctly available input and output nodes
    -allow_reverse - its fine for now
    -implement somy copy method for node?
        https://stackoverflow.com/questions/45051720/best-practice-to-implement-copy-method
    -what about the random order of pairing inputs and outputs? currently we iterate first all inputs and then all outputs, so the results are not fully random
    -I realize that node should keep it restrictions independ on Fancy class object (todo, make sure its ok)
    -relation between nodes should be make in one node, for both of them, to not be omitted
    -
    
"""
