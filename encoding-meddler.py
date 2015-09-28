#!/usr/bin/env python

from config import *
import base64, string

change_block_len = 3

changeable = string.lowercase + string.uppercase

variables = variants.keys()

assignments = [0] * len(variables)

all_solutions = []

if __name__ == "__main__":
    while True:
        assigned = dict( (k, variants[k][assignments[i]]) for i, k in enumerate(variables) )
        
        target_assigned = unicode(target % assigned)
        
        change_pos = 0
        min_target_assigned = target_assigned
        min_encoded = base64.b64encode(min_target_assigned.encode("utf-16le"))
        min_count = sum( e in forbidden for e in min_encoded )
        
        while change_pos < len(target_assigned):
            for change_bits in range(2**change_block_len):
                tmp = list(min_target_assigned)
                
                for pos in range(change_block_len):
                    if not tmp[change_pos + pos] in changeable: continue
                    tmp[change_pos + pos] = chr(ord(tmp[change_pos + pos]) ^ (0x20 if (change_bits & 1<<pos) else 0x00))
                
                target_assigned = u"".join(tmp)
                
                encoded = base64.b64encode(target_assigned.encode("utf-16le"))
                count = sum( e in forbidden for e in encoded )
                
                if count < min_count:
                    min_target_assigned = target_assigned
                    min_encoded = encoded
                    min_count = count
                
                if count == 0 and all_solutions is not None:
                    all_solutions.append( (target_assigned, encoded) )
            
            if min_count == 0 and all_solutions is None:
                break
            
            change_pos = change_pos + change_block_len
        
        if min_count == 0 and all_solutions is None:
            break
        
        overflow = 1
        for i in range(len(assignments)):
            assignments[i] = assignments[i] + overflow
            overflow, assignments[i] = divmod(assignments[i], len(variants[variables[i]]))
        
        if overflow: break

    print "Forbidden count: %s" % min_count
    print "Resultant string: %s" % min_target_assigned
    print "Resultant encoding: %s" % min_encoded
    
    if all_solutions:
        print
        for target_assigned, encoded in all_solutions:
            print repr(target_assigned)
            print "=> %s" % encoded
    
