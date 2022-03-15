# fancy-mermaid
tool for making fancy mermaid graphs


## two nodes relations

![image](candy_and_mandy.png)

## example code

```python
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
```


## fancy graphs examples

```mermaid
graph TD;
    2(third)-->0(first);
    0(first)-->1(second);
    1(second)-->2(third);
```

---

```mermaid
graph TD;
    0(some)-->2(here);
    6(mandy)-->2(here);
    6(mandy)-->0(some);
    6(mandy)-->4(this);
    6(mandy)-->7(candy);
    6(mandy)-->5(meow);
    1(thing)-->7(candy);
    4(this)-->7(candy);
    7(candy)-->3(they);
    4(this)-->3(they);
    4(this)-->5(meow);
    3(they)-->5(meow);
    5(meow)-->3(they);
```

---

```mermaid
graph TD;
    22(some14)-->17(some9);
    17(some9)-->21(some13);
    17(some9)-->5(five);
    5(five)-->19(some11);
    21(some13)-->16(some8);
    16(some8)-->8(some0);
    16(some8)-->3(third);
    10(some2)-->20(some12);
    20(some12)-->6(six);
    20(some12)-->2(second);
    13(some5)-->10(some2);
    10(some2)-->4(fourth);
    8(some0)-->22(some14);
    8(some0)-->9(some1);
    19(some11)-->1(first2);
    11(some3)-->1(first2);
    22(some14)-->1(first2);
    12(some4)-->1(first2);
    4(fourth)-->1(first2);
    0(first)-->1(first2);
    15(some7)-->1(first2);
    13(some5)-->1(first2);
    18(some10)-->1(first2);
    21(some13)-->1(first2);
    6(six)-->1(first2);
    14(some6)-->1(first2);
    9(some1)-->1(first2);
    2(second)-->1(first2);
    7(seven)-->1(first2);
    18(some10)-->11(some3);
    11(some3)-->15(some7);
    15(some7)-->0(first);
    9(some1)-->12(some4);
    12(some4)-->13(some5);
    14(some6)-->0(first);
    19(some11)-->0(first);
    0(first)-->18(some10);
    0(first)-->7(seven);
```

## think of\todo

:black_square_button: what if choice is in the list of inputs or outputs for a given node? then we don't lose shots, but we don't find any input/output. This needs to be fixed somehow by giving a while loop, or appropriate conditions that will filter out correctly available input and output nodes

:white_check_mark:  `allow_reverse` - allow for reverse connections between nodes. In other case only one way connection is allowed. Its fine for now
    
:black_square_button: implement somy copy method for node? https://stackoverflow.com/questions/45051720/best-practice-to-implement-copy-method
        
:black_square_button: what about the random order of pairing inputs and outputs? currently we iterate first all inputs and then all outputs, so the results are not fully random
    
:black_square_button: I realize that node should keep it restrictions independ on Fancy class object (todo, make sure its ok)
    
:black_square_button: relation between nodes should be make in one node, for both of them, to not be omitted
    
:white_check_mark: remove `make_input` and `make_output` methods for Node class and implement fully `connect` method (also in Fancy class)
 
