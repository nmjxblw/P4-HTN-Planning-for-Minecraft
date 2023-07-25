import pyhop
import json
import time
import os


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

        # print(f"produce:{name}")
        # get consumes to the list
        for key in Consumes.keys():
            newCheck = ("have_enough", ID, key, Consumes[key])
            # print(f"consumes:{key} {Consumes[key]}")
            list.append(newCheck)

        # get Requires to the list
        for key in Requires.keys():
            list = [("have_enough", ID, key, Requires[key])] + list
            # print(f"requires:{key} {Requires[key]}")

        # get the name and the id
        list.append((name, ID))

        # os.system("PAUSE")
        return list

    return method


def declare_methods(data):
    Produces_list = {}
    for Produce in data["Recipes"].keys():
        temp = data["Recipes"][Produce]["Produces"].items()
        # print(f"{list(data['Recipes'][Produce]['Produces'].keys())}")
        # print(Produce)
        # os.system("PAUSE")
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
                "op_" + Produce,
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
        requires = rule[0]
        consumes = rule[1]
        produces = rule[2]
        time = rule[3]

        # may need to check all reuqires are met
        for require in requires.keys():
            if requires[require] > getattr(state, require)[ID]:
                # Faile
                return False

        # same idea to check consumes
        for consume in consumes:
            if consumes[consume] > getattr(state, consume)[ID]:
                # Faile
                return False

        # also check time remain
        if time > state.time[ID]:
            return False

        # then we update the state info
        for key in consumes.keys():
            total = getattr(state, key)[ID]
            consumed = consumes[key]
            newTotal = total - consumed
            setattr(state, key, {ID: newTotal})

        for key in produces.keys():
            total = getattr(state, key)[ID]
            produced = produces[key]
            newTotal = total + produced
            setattr(state, key, {ID: newTotal})
        # update time
        state.time[ID] -= time

        return state

    return operator


def declare_operators(data):
    # your code here
    # hint: call make_operator, then declare the operator to pyhop using pyhop.declare_operators(o1, o2, ..., ok)
    for item in data["Recipes"].keys():
        requires = {}
        consumes = {}
        # to check if we need prerequire for making this item
        if "Requires" in data["Recipes"][item]:
            # hit:requiers is a dict
            requires = data["Recipes"][item]["Requires"]
        # also check the consumes
        if "Consumes" in data["Recipes"][item]:
            consumes = data["Recipes"][item]["Consumes"]
        # get result
        produces = data["Recipes"][item]["Produces"]
        # get time
        time = data["Recipes"][item]["Time"]

        rule = [requires, consumes, produces, time]

        operator = make_operator(rule)
        operator.__name__ = "op_" + item

        pyhop.declare_operators(operator)

    return


def add_heuristic(data, ID):
    def heuristic(state, curr_task, tasks, plan, depth, calling_stack):
        # print(f"curr_task:{curr_task}")
        # print(f"tasks:{tasks}")
        # print(f"plan:{plan}")
        # print(f"depth:{depth}")
        # print(f"calling_stack:{calling_stack}")

        if (
            curr_task[0] == "produce"
            and curr_task[2] in data["Tools"]
            and curr_task in calling_stack
        ):
            return True

        if curr_task[0] == "produce" and curr_task[2] == "iron_pickaxe":
            required = 0
            for task in tasks:
                if task[0] == "have_enough" and task[2] == "ingot":
                    required += task[3]
            # print(required)
            if required <= 11 and required > 0:
                return True

        if curr_task[0] == "produce" and curr_task[2] == "wooden_axe":
            required = 0
            for task in tasks:
                if task[0] == "have_enough" and task[2] == "wood":
                    required += task[3]
            # print(required)
            if required <= 9 and required > 0:
                return True

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
    start_time = time.time()
    rules_filename = "crafting.json"

    with open(rules_filename) as f:
        data = json.load(f)

    state = set_up_state(data, "agent", time=250)  # allot time here
    goals = set_up_goals(data, "agent")

    declare_operators(data)
    declare_methods(data)
    add_heuristic(data, "agent")

    # pyhop.print_operators()
    # pyhop.print_methods()

    # Hint: verbose output can take a long time even if the solution is correct;
    # try verbose=1 if it is taking too long
    # pyhop.pyhop(state, goals, verbose=1)
    pyhop.pyhop(
        state,
        [("have_enough", "agent", "cart", 1), ("have_enough", "agent", "rail", 20)],
        verbose=1,
    )
    end_time = time.time()

    excuted_time = end_time - start_time
    print(f"excuted:{excuted_time}")
