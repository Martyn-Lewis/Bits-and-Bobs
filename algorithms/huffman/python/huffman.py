import collections
from array import array
import math
import struct

# This code lacks a lot of comments, sorry in advance.
# As this is pure python (not even numpy) it is very slow.
# The method used is also not very performance-orientated either.

class Tree(object):
    def __init__(self):
        self.left_node = None
        self.right_node = None
        self.value = None
        self.frequency = 0
        
def is_tuple(x):
    return isinstance(x, tuple)

def frequency(of):
    if isinstance(of, tuple):
        return of[1]
    else:
        return of.frequency

def require_tree(of):
    if isinstance(of, tuple):
        result = Tree()
        result.value = of[0]
        result.frequency = of[1]
        return result
    return of

def sorted_replace(of, into):
    did_something = False
    for idx in range(len(into)):
        if frequency(of) > frequency(into[idx]):
            did_something = True
            into.insert(idx, of)
            break
    if not did_something:
        into.append(of)
        
def generate_tree(s_from):
    alphabet_density = collections.Counter(s_from)
    common_last = alphabet_density.most_common()
    common_last.reverse()
    # Pairs of (value, frequency).
    
    values = [x[0] for x in common_last]
    
    elements = len(common_last)
    
    
    head = None
    if elements > 0 and elements <= 2:
        head = Tree()
        left = require_tree(common_last[0])
        head.left_node = left
        if elements == 2:
            right = require_tree(common_last[1])
            head.right_node = right
    elif elements > 0:
        while len(common_last) > 1:
            left = require_tree(common_last[0])
            right = require_tree(common_last[1])
            del common_last[0:2]
            tree = Tree()
            tree.left_node = left
            tree.right_node = right
            sorted_replace(tree, common_last)
        head = common_last[0]
    else:
        raise ValueError("Empty input?")
    
    # This saves a lot of time.
    cache = {}
    for x in values:
        cache[x] = find_for_alpha(x, head)
    head.cache = cache
    
    return head

def find_for_alpha(alpha, encode_tree, pattern=0, depth=0):
    if encode_tree == None:
        return
    if encode_tree.value == alpha:
        return (encode_tree, pattern, depth)
    left = find_for_alpha(alpha, encode_tree.left_node, pattern << 1 | 0, depth + 1)
    if left:
        return left
    return find_for_alpha(alpha, encode_tree.right_node, pattern << 1 | 1, depth + 1)

def compress(s, encode_tree, debug=True):
    total_depth = 0
    for x in s:
        total_depth = total_depth + encode_tree.cache[x][2]
    if debug:
        print("Packing %d total bits." % (total_depth))
    counter = 0
    current = 0
    i = 0
    parts = [0] * math.ceil(total_depth / 8)
    for x in s:
        pattern = encode_tree.cache[x]
        rtree, pattern, depth = pattern
        current = (current << depth) | pattern
        counter = counter + depth
        if counter > 8:
            diff = (counter - 8)
            left = current >> diff
            current = current & (2 ** diff - 1)
            counter = counter - 8
            parts[i] = left
            i = i + 1
    if counter > 0:
        parts[i] = current << (8 - counter)
    return bytes(parts), total_depth

def tree2str(tree):
    # Format: header(left?right?)
    # Header:
    #       0b001 = has left
    #       0b010 = has_right
    #       0b011 = has_left and has_right
    #       0b100 = final token
    if not tree:
        return b''
    if not tree.value == None:
        return b'\x04' + bytes(tree.value, 'ascii')
    tree_header = 0
    if tree.left_node:
        tree_header = tree_header | 0x01
    if tree.right_node:
        tree_header = tree_header | 0x02
    return (tree_header).to_bytes(1, 'big') + tree2str(tree.left_node) + tree2str(tree.right_node)

def decompress_tree(s_from, idx_from=0):
    header = s_from[idx_from]
    has_left = header & 0b1
    has_right = header & 0b10
    is_final = header & 0b100
    if is_final:
        final_node = Tree()
        final_node.value = chr(s_from[idx_from + 1])
        return (final_node, 2)
    shifted_idx_from = idx_from + 1
    left = None
    right = None
    this_tree = Tree()
    this_tree.cache = [None, None] # Removes branching inside decompress.
    this_tree.value = 0
    if has_left:
            left = decompress_tree(s_from, shifted_idx_from)
            shifted_idx_from = shifted_idx_from + left[1]
            this_tree.left_node = left[0]
            this_tree.cache[0] = left[0]
    if has_right:
            right = decompress_tree(s_from, shifted_idx_from)
            shifted_idx_from = shifted_idx_from + right[1]
            this_tree.right_node = right[0]
            this_tree.cache[1] = right[0]
    this_tree.cache = (this_tree.cache[0], this_tree.cache[1],)
    return (this_tree, shifted_idx_from - idx_from)
    
def tree_possibilities(tree, result={}, pattern=1):
    if tree.left_node:
        tree_possibilities(tree.left_node, result, (pattern << 1))
    if tree.right_node:
        tree_possibilities(tree.right_node, result, (pattern << 1) | 1)
    if tree.value:
        result[tree.value] = pattern
    
    return result
    
def decompress(s, output_file, debug=True):
    def pretty_tree(x, depth=0):
        # Purely for debug reasons.
        if x == None:
            return ""
        left = pretty_tree(x.left_node, depth + 1)
        middle = "%s%s:%d\n" % ('\t' * depth, repr(x.value), x.frequency)
        right = pretty_tree(x.right_node, depth + 1)
        return "%s\n%s%s" % (left, middle, right)

    tree, idx = decompress_tree(s)

    if debug:
        f = open("output-decomp.txt", "w")
        f.write(pretty_tree(tree))
        f.close()
    
    content_length = s[idx:idx+4]
    content_length = struct.unpack('>L', content_length)[0]

    if debug:
        print("Unpacking %d total bits." % (content_length))
    
    current_next = tree
    src = s[idx+4:]
    peak = min(255, content_length)
    end = 0
    
    block = 0
    block_length = 0
    for x in src:
        if block_length < min(256, content_length):
            block_length = block_length + 8
            block = (block << 8) | x
        
        if block_length < min(256, content_length):
            continue
        
        if content_length < 255:
            if content_length <= 0:
                break
        offset = block_length
        while offset > 0:
            offset = offset - 1
            current_next = current_next.cache[(block >> offset) & 1]
            
            if current_next.value != 0:
                output_file.write(current_next.value)
                current_next = tree
        content_length = content_length - block_length
        block_length = 0
        block = 0
    return
