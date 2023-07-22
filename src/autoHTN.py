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
        Requires = rule[0]
        Consumes = rule[1]
    
        list = []

        # get consumes to the list
        for key in Consumes.keys():
                newCheck = ("have_enough", ID, key, Consumes[key])
                list.append(newCheck)

        # get Requires to the list
        for key in Requires.keys():
            list = [("have_enough", ID, key, Requires[key])] + list

        # get the name and the id
        list.append((name, ID))

        return list

    return method


def declare_methods(data):
    Produces_list = {}
    for Produce in data["Recipes"]:
        temp = data["Recipes"][Produce]["Produces"].items()
        for key, value in temp:
            try:
                requires = data["Recipes"][Produce]["Requires"]
            except KeyError:
                requires = {}

            try:
                consumes = data["Recipes"][Produce]["Consumes"]
            except KeyError:
                consumes = {}

            new_method = make_method(
                Produce,
                [
                    requires,
                    consumes,
                ],
            )
            new_method.__name__ = Produce
            if key not in list(Produces_list.keys()):
                Produces_list[key] = [new_method]
            else:
                Produces_list[key].append(new_method)
                Produces_list[key].sort(
                    key=lambda p: data["Recipes"][p.__name__]["Time"]
                )

    for key in Produces_list.keys():
        pyhop.declare_methods(str("produce_" + key), *Produces_list[key])
    return


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
