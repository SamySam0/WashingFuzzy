#!/usr/bin/env python3

import sys
from typing import List
from frules.rules import Rule as FuzzySet
from frules.expressions import Expression as MemFunction
from frules.expressions import ltrapezoid, trapezoid, rtrapezoid


# membership functions and corresponding fuzzy sets for how dirty (in tablespoons)
almost_clean_fn = MemFunction(ltrapezoid(0.25, 1.00), "almost_clean")
almost_clean_set = FuzzySet(value=almost_clean_fn)

dirty_fn = MemFunction(rtrapezoid(0.50, 1.0), "dirty")
dirty_set = FuzzySet(value=dirty_fn)

# membership functions and corresponding fuzzy sets for how delicate (in fabric weight)
very_delicate_fn = MemFunction(ltrapezoid(2.00, 4.00), "very_delicate")
very_delicate_set = FuzzySet(value=very_delicate_fn)

delicate_fn = MemFunction(trapezoid(3.00, 4.00, 6.00, 7.00), "delicate")
delicate_set = FuzzySet(value=delicate_fn)

not_delicate_fn = MemFunction(rtrapezoid(6.00, 7.00), "not_delicate")
not_delicate_set = FuzzySet(value=not_delicate_fn)

# dictionary with the output level for each of the rules; the key pertains to the rule number
rule_weights_dict = {1:10, 2:40, 3:60, 4:100}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Implement the function that computes the degree to which a crisp input belongs to a fuzzy set
def fuzzify(fuzzy_set: FuzzySet, val: float) -> float:
	return fuzzy_set.eval(value = val)

# Implement the function for computing the conjunction of a rule's antecedents
def get_conjunction(fuzzified_dirt: float, fuzzified_fabric_weight: float) -> float:
	return min(fuzzified_dirt, fuzzified_fabric_weight)

# Implement the function for computing the disjunction of a rule's antecedents
def get_disjunction(fuzzified_dirt: float, fuzzified_fabric_weight: float) -> float:
	return max(fuzzified_dirt, fuzzified_fabric_weight)



# Implement the function for computing the combined value of a rule antecedent
def get_rule_antecedent_value(ant1: FuzzySet, val1: float, ant2: FuzzySet, val2: float, operator: str) -> float:
	if operator == "AND":
		return get_conjunction(fuzzify(ant1, val1), fuzzify(ant2, val2))
	elif operator == "OR":
		return get_disjunction(fuzzify(ant1, val1), fuzzify(ant2, val2))
	else:
		if ant1 == None and ant2 == None:
			return 0
		elif ant1 == None:
			return fuzzify(ant2, val2)
		else:
			return fuzzify(ant1, val1)
			


# Implement function that returns the weighted output level of a rule
def get_rule_output_value(rule_number: int, rule_antecedent_value: float) -> float:
	return rule_weights_dict[rule_number] * rule_antecedent_value


# dirt_amount can range from 0 to 2.5 inclusive
# fabric_weight range from 1.0 to 11.00 inclusive
def configure_washing_machine(dirt_amount: float, fabric_weight: float) -> tuple:
	all_antecedents = [get_rule_antecedent_value(very_delicate_set, fabric_weight, None, 0.0, ""), get_rule_antecedent_value(delicate_set, fabric_weight, almost_clean_set, dirt_amount, "OR"), get_rule_antecedent_value(delicate_set, fabric_weight, dirty_set, dirt_amount, "AND"), get_rule_antecedent_value(not_delicate_set, fabric_weight, dirty_set, dirt_amount, "AND")] # this should be set to a List containing the antecedent values for all rules
	all_outputs = [get_rule_output_value(i+1, all_antecedents[i]) for i in range(len(all_antecedents))] # this should be set to a List containing the output values for all rules
	return (all_antecedents, all_outputs)


# Implement function that computes the weighted average over all rules
def get_weighted_average(all_antecedents: List, all_outputs: List) -> float:
	return sum(all_outputs)/sum(all_antecedents)


# Implement function for computing the actual temperature the machine should be set to
def get_temperature(all_antecedents: List, all_outputs: List) -> float:
	return 10 + 80*get_weighted_average(all_antecedents, all_outputs)/100

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Debug
if __name__ == '__main__':
	if len(sys.argv) > 2:
		cmd = "{}({})".format(sys.argv[1], ",".join(sys.argv[2:]))
		print("debug run:", cmd)
		ret = eval(cmd)
		print("ret value:", ret)
	else:
		sys.stderr.write("Usage: fuzzy_washing_machine.py FUNCTION ARG...")
		sys.exit(1)
