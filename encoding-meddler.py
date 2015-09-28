#!/usr/bin/env python

import base64, string

def IPVariants(ip):
    def f():
        yield ip
        parts = map(int, ip.split("."))
        numeric = parts[0]*256**3 + parts[1]*256**2 + parts[2]*256 + parts[3]
        yield str(numeric)
        yield hex(numeric)
        yield "0{0:o}".format(numeric)
    return tuple(f())

def PowerShellEncode(s):
    return base64.b64encode(unicode(s).encode("utf-16le"))

def ForbiddenCharacters(forbidden):
    def judge(encoded):
        return sum( e in forbidden for e in encoded )
    return judge

execfile("config.py")

change_block_len = 3

changeable = string.lowercase + string.uppercase

all_solutions = []

DEBUG = False

def all_variants():
    global target
    
    if magic_spaces:
        count = 0
        while " " in target:
            pos = target.rfind(" ")
            target = target[:pos] + ("%%(__MSPACE%i)s" % count) + target[pos+1:]
            count = count + 1
        target = target + ("%%(__MSPACE%i)s" % count)
        count = count + 1
        
        for i in range(count):
            variants["__MSPACE%i" % i] = [" " * j for j in range(1, magic_spaces)]
    
    variables = variants.keys()

    assignments = [0] * len(variables)

    while True:
        assigned = dict( (k, variants[k][assignments[i]]) for i, k in enumerate(variables) )
        
        target_assigned = unicode(target % assigned)
        
        if DEBUG: print "Variant:", target_assigned
        yield target_assigned
        
        overflow = 1
        for i in range(len(assignments)):
            assignments[i] = assignments[i] + overflow
            overflow, assignments[i] = divmod(assignments[i], len(variants[variables[i]]))
        
        if overflow: break


def partial_solutions(base_string, base_count, change_pos):
    if change_pos >= len(base_string):
        if DEBUG: print "Abort:", base_string
        yield base_string
    else:
        for retval in partial_solutions(base_string, base_count, change_pos + change_block_len):
            if DEBUG: print "Pass:", retval
            yield retval
        
        for change_bits in range(1, 2**change_block_len):
            tmp = list(base_string)
            
            for pos in range(change_block_len):
                if change_pos + pos >= len(tmp): continue
                if not tmp[change_pos + pos] in changeable: continue
                tmp[change_pos + pos] = chr(ord(tmp[change_pos + pos]) ^ (0x20 if (change_bits & 1<<pos) else 0x00))
                
                modified_string = u"".join(tmp)
                encoded = encode(modified_string)
                count = judge(encoded)
                
                if count < base_count:
                    for retval in partial_solutions(modified_string, count, change_pos + change_block_len):
                        if DEBUG: print "Recurse", retval
                        yield retval
    

if __name__ == "__main__":
    min_count = None

    for target_assigned in all_variants():
        for partial_solution in partial_solutions(target_assigned, judge(encode(target_assigned)), 0):
            if partial_solution is None: continue
            encoded = encode(partial_solution)
            count = judge(encoded)
            
            if min_count is None or count < min_count:
                min_target_assigned = partial_solution
                min_encoded = encoded
                min_count = count
            
            if count == 0 and want_all_solutions:
                all_solutions.append( (partial_solution, encoded) )
            
            if min_count == 0 and not want_all_solutions:
                break
        
        if min_count == 0 and not want_all_solutions:
            break

    print "Forbidden count: %s" % min_count
    print "Resultant string: %s" % min_target_assigned
    print "Resultant encoding: %s" % min_encoded
    
    if all_solutions:
        print
        for target_assigned, encoded in all_solutions:
            print repr(target_assigned)
            print "=> %s" % encoded
    
