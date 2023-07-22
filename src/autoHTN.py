import pyhop
import json


def check_enough(state, ID, item, num):
    if getattr(state, item)[ID] >= num:
        return []
    return False


def produce_enough(state, ID, item, num):
    return [("produce", ID, item), ("have_enough", ID, item, num)]


pyhop.declare_methods("have_enough", check_enough, produce_enough)


def produce(state, ID, item):
    return [("produce_{}".format(item), ID)]


pyhop.declare_methods("produce", produce)


def make_method(name, rule):
    def method(state, ID):
        new_checks = []
        for names in rule["Recipes"][name]:
            if names == "Requires":
                nextitem = next(iter(rule["Recipes"][name][names]))
                new_checks.append("have_enough", ID, nextitem, rule["Recipes"][name][names][nextitem])
            if names == "Consumes":
                for item in rule["Recipes"][name][names]:
                    new_checks.append(("have_enough", ID, item, rule["Recipes"][name][names][item]))
            new_checks.append(("op_"+name, ID))
        return new_checks               
    return method


def declare_methods(data):
    Produces_list = {}
    for Produce in data["Recipes"]:
        temp = data["Recipes"][Produce]["Produces"].items()
        for key, value in temp:
            if key not in list(Produces_list.keys()):
                Produces_list[key] = [Produce]
            else:
                Produces_list[key].append(produce)
                Produces_list.sort(key=lambda p:data["Recipes"][p])
                

    # temp = {}
    # for produce in Produces_list:
    #     temp[str("produce_" + produce)] = []

    print(temp)
    pass


def make_operator(rule):
    def operator(state, ID):
        # your code here
        pass

    return operator


def declare_operators(data):
    # your code here
    # hint: call make_operator, then declare the operator to pyhop using pyhop.declare_operators(o1, o2, ..., ok)
	
    pass


def add_heuristic(data, ID):
    # prune search branch if heuristic() returns True
    # do not change parameters to heuristic(), but can add more heuristic functions with the same parameters:
    # e.g. def heuristic2(...); pyhop.add_check(heuristic2)
    def heuristic(state, curr_task, tasks, plan, depth, calling_stack):
        # your code here
        return False  # if True, prune this branch

    pyhop.add_check(heuristic)


def set_up_state(data, ID, time=0):
    state = pyhop.State("state")
    state.time = {ID: time}

    for item in data["Items"]:
        setattr(state, item, {ID: 0})

        # state.wood[ID] = 0

    for item in data["Tools"]:
        setattr(state, item, {ID: 0})

    for item, num in data["Initial"].items():
        setattr(state, item, {ID: num})

    return state


def set_up_goals(data, ID):
    goals = []
    for item, num in data["Goal"].items():
        goals.append(("have_enough", ID, item, num))

    return goals


if __name__ == "__main__":
    rules_filename = "crafting.json"

    with open(rules_filename) as f:
        data = json.load(f)

    state = set_up_state(data, "agent", time=239)  # allot time here
    goals = set_up_goals(data, "agent")

    declare_operators(data)
    declare_methods(data)
    add_heuristic(data, "agent")

    # data["axe"]

    # pyhop.print_operators()
    # pyhop.print_methods()

    # Hint: verbose output can take a long time even if the solution is correct;
    # try verbose=1 if it is taking too long
    pyhop.pyhop(state, goals, verbose=3)
    # pyhop.pyhop(state, [('have_enough', 'agent', 'cart', 1),('have_enough', 'agent', 'rail', 20)], verbose=3)
