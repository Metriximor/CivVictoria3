def create_state_dicts(strings):
    state_dicts = []
    for i, string in enumerate(strings):
        state_dict = {
            "id": i + 1
        }
        state_dicts.append(state_dict)
    return state_dicts

with open("src/input/states.txt", "r") as f:
    strings = f.read().strip().split("\n")

state_dicts = create_state_dicts(strings)

with open("src/output/00_states.txt", "w", encoding="utf-8-sig") as f:
    for i, state_dict in enumerate(state_dicts):
        f.write(f"STATE_{strings[i].upper()} = {{\n")
        for key, value in state_dict.items():
            f.write(f"    {key} = {value}\n")
        f.write("}\n\n")
